"""
SAML 2.0 Single Sign-On Integration
Enables enterprise SSO with Google Workspace, Microsoft 365, Okta, etc.
"""

import os
import base64
from pathlib import Path
from typing import Dict, Optional
from flask import Blueprint, request, redirect, session, url_for, jsonify
from urllib.parse import urlparse

# SAML library
try:
    from onelogin.saml2.auth import OneLogin_Saml2_Auth
    from onelogin.saml2.settings import OneLogin_Saml2_Settings
    from onelogin.saml2.utils import OneLogin_Saml2_Utils
    SAML_AVAILABLE = True
except ImportError:
    SAML_AVAILABLE = False
    print("⚠️  python3-saml not installed. Run: pip install python3-saml")


class SAMLConfig:
    """
    SAML configuration for Identity Provider (IdP)

    Supports:
    - Google Workspace
    - Microsoft 365 / Azure AD
    - Okta
    - Auth0
    - Custom SAML IdP
    """

    def __init__(self, config_dir: str = "config/saml"):
        """
        Initialize SAML configuration

        Args:
            config_dir: Directory containing SAML metadata and certificates
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_settings(self, idp_name: str = "default") -> Dict:
        """
        Get SAML settings for specific IdP

        Args:
            idp_name: Identity provider name (google, microsoft, okta, etc.)

        Returns:
            SAML settings dictionary
        """
        # Service Provider (your application) settings
        sp_entity_id = os.getenv('SAML_SP_ENTITY_ID', 'https://app.knowledgevault.com')
        sp_acs_url = os.getenv('SAML_SP_ACS_URL', f'{sp_entity_id}/saml/acs')
        sp_sls_url = os.getenv('SAML_SP_SLS_URL', f'{sp_entity_id}/saml/sls')

        # Load IdP metadata
        idp_entity_id = os.getenv(f'SAML_{idp_name.upper()}_ENTITY_ID', '')
        idp_sso_url = os.getenv(f'SAML_{idp_name.upper()}_SSO_URL', '')
        idp_slo_url = os.getenv(f'SAML_{idp_name.upper()}_SLO_URL', '')
        idp_cert = os.getenv(f'SAML_{idp_name.upper()}_CERT', '')

        # Load from file if not in env
        if not idp_cert:
            cert_file = self.config_dir / f"{idp_name}_idp_cert.pem"
            if cert_file.exists():
                idp_cert = cert_file.read_text()

        settings = {
            "strict": True,
            "debug": os.getenv('SAML_DEBUG', 'false').lower() == 'true',
            "sp": {
                "entityId": sp_entity_id,
                "assertionConsumerService": {
                    "url": sp_acs_url,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                },
                "singleLogoutService": {
                    "url": sp_sls_url,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
                "x509cert": "",  # Optional: SP certificate
                "privateKey": ""  # Optional: SP private key
            },
            "idp": {
                "entityId": idp_entity_id,
                "singleSignOnService": {
                    "url": idp_sso_url,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "singleLogoutService": {
                    "url": idp_slo_url,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "x509cert": idp_cert
            },
            "security": {
                "nameIdEncrypted": False,
                "authnRequestsSigned": False,
                "logoutRequestSigned": False,
                "logoutResponseSigned": False,
                "signMetadata": False,
                "wantMessagesSigned": False,
                "wantAssertionsSigned": False,
                "wantNameId": True,
                "wantNameIdEncrypted": False,
                "wantAssertionsEncrypted": False,
                "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                "digestAlgorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
            }
        }

        return settings

    def get_google_workspace_settings(self) -> Dict:
        """Get SAML settings for Google Workspace"""
        return self.get_settings('google')

    def get_microsoft_365_settings(self) -> Dict:
        """Get SAML settings for Microsoft 365 / Azure AD"""
        return self.get_settings('microsoft')

    def get_okta_settings(self) -> Dict:
        """Get SAML settings for Okta"""
        return self.get_settings('okta')


class SAMLHandler:
    """
    SAML SSO handler for Flask applications

    Usage:
        saml = SAMLHandler(app)

        # User clicks "Login with Google"
        # → Redirect to /saml/google/login

        # After authentication, IdP redirects to /saml/acs
        # → User is authenticated and session is created
    """

    def __init__(self, app=None, config_dir: str = "config/saml"):
        """
        Initialize SAML handler

        Args:
            app: Flask application (optional)
            config_dir: Directory for SAML configuration
        """
        if not SAML_AVAILABLE:
            raise ImportError("python3-saml not installed")

        self.config = SAMLConfig(config_dir=config_dir)
        self.app = app

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize SAML routes with Flask app"""
        self.app = app

        # Create SAML blueprint
        saml_bp = Blueprint('saml', __name__, url_prefix='/saml')

        # Register routes
        saml_bp.add_url_rule('/metadata', 'metadata', self.metadata, methods=['GET'])
        saml_bp.add_url_rule('/<idp>/login', 'login', self.login, methods=['GET'])
        saml_bp.add_url_rule('/acs', 'acs', self.acs, methods=['POST'])
        saml_bp.add_url_rule('/sls', 'sls', self.sls, methods=['GET', 'POST'])
        saml_bp.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])

        app.register_blueprint(saml_bp)

        print("✓ SAML SSO routes registered")

    def _prepare_request(self, request_data):
        """Prepare Flask request for SAML library"""
        url_data = urlparse(request_data.url)

        return {
            'https': 'on' if request_data.scheme == 'https' else 'off',
            'http_host': request_data.host,
            'server_port': url_data.port,
            'script_name': request_data.path,
            'get_data': request_data.args.copy(),
            'post_data': request_data.form.copy()
        }

    def metadata(self):
        """
        GET /saml/metadata
        Return SP metadata XML for IdP configuration
        """
        try:
            idp_name = request.args.get('idp', 'default')
            settings = self.config.get_settings(idp_name)

            auth = OneLogin_Saml2_Auth(
                self._prepare_request(request),
                settings
            )

            metadata = auth.get_settings().get_sp_metadata()
            errors = auth.get_settings().validate_metadata(metadata)

            if errors:
                return jsonify({
                    'error': 'Invalid metadata',
                    'details': errors
                }), 500

            return metadata, 200, {'Content-Type': 'application/xml'}

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def login(self, idp):
        """
        GET /saml/<idp>/login
        Initiate SAML login with specific IdP

        Args:
            idp: Identity provider (google, microsoft, okta, etc.)
        """
        try:
            settings = self.config.get_settings(idp)
            auth = OneLogin_Saml2_Auth(
                self._prepare_request(request),
                settings
            )

            # Store IdP in session for ACS callback
            session['saml_idp'] = idp

            # Redirect to IdP for authentication
            return redirect(auth.login())

        except Exception as e:
            return jsonify({
                'error': 'SAML login failed',
                'message': str(e)
            }), 500

    def acs(self):
        """
        POST /saml/acs
        Assertion Consumer Service - handles IdP response after authentication
        """
        try:
            idp = session.get('saml_idp', 'default')
            settings = self.config.get_settings(idp)

            auth = OneLogin_Saml2_Auth(
                self._prepare_request(request),
                settings
            )

            # Process SAML response
            auth.process_response()

            errors = auth.get_errors()
            if errors:
                return jsonify({
                    'error': 'SAML authentication failed',
                    'details': errors,
                    'reason': auth.get_last_error_reason()
                }), 401

            if not auth.is_authenticated():
                return jsonify({
                    'error': 'Authentication failed',
                    'message': 'User not authenticated by IdP'
                }), 401

            # Get user attributes from SAML response
            attributes = auth.get_attributes()
            nameid = auth.get_nameid()

            # Extract user info
            user_data = {
                'id': nameid,
                'email': attributes.get('email', [nameid])[0] if attributes.get('email') else nameid,
                'name': attributes.get('name', [nameid])[0] if attributes.get('name') else nameid,
                'first_name': attributes.get('first_name', [''])[0] if attributes.get('first_name') else '',
                'last_name': attributes.get('last_name', [''])[0] if attributes.get('last_name') else '',
                'organization': attributes.get('organization', [''])[0] if attributes.get('organization') else '',
                'roles': attributes.get('roles', []),
                'groups': attributes.get('groups', []),
            }

            # Store user in session
            session['saml_user'] = user_data
            session['saml_authenticated'] = True

            # Redirect to application
            relay_state = request.form.get('RelayState', '/')
            return redirect(relay_state)

        except Exception as e:
            return jsonify({
                'error': 'SAML processing failed',
                'message': str(e)
            }), 500

    def sls(self):
        """
        GET/POST /saml/sls
        Single Logout Service - handles logout
        """
        try:
            idp = session.get('saml_idp', 'default')
            settings = self.config.get_settings(idp)

            auth = OneLogin_Saml2_Auth(
                self._prepare_request(request),
                settings
            )

            # Process logout request/response
            url = auth.process_slo(delete_session_cb=lambda: session.clear())

            errors = auth.get_errors()
            if errors:
                return jsonify({
                    'error': 'Logout failed',
                    'details': errors
                }), 500

            if url:
                return redirect(url)
            else:
                return redirect('/')

        except Exception as e:
            return jsonify({
                'error': 'Logout processing failed',
                'message': str(e)
            }), 500

    def logout(self):
        """
        GET /saml/logout
        Initiate SAML logout
        """
        try:
            idp = session.get('saml_idp', 'default')
            settings = self.config.get_settings(idp)

            auth = OneLogin_Saml2_Auth(
                self._prepare_request(request),
                settings
            )

            # Clear local session
            session.clear()

            # Redirect to IdP for logout
            return redirect(auth.logout())

        except Exception as e:
            session.clear()
            return redirect('/')

    def is_authenticated(self) -> bool:
        """Check if user is authenticated via SAML"""
        return session.get('saml_authenticated', False)

    def get_user(self) -> Optional[Dict]:
        """Get authenticated SAML user from session"""
        if self.is_authenticated():
            return session.get('saml_user')
        return None


def requires_saml_auth(f):
    """Decorator: Require SAML authentication"""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('saml_authenticated'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'SAML authentication required'
            }), 401

        return f(*args, **kwargs)

    return decorated


# Example integration
def init_saml(app):
    """Initialize SAML SSO for Flask app"""
    try:
        saml = SAMLHandler(app)
        return saml
    except ImportError:
        print("⚠️  SAML not available (python3-saml not installed)")
        return None


if __name__ == "__main__":
    print("="*60)
    print("SAML SSO Configuration Guide")
    print("="*60)

    print("\n📋 SETUP STEPS:")
    print("\n1. Install python3-saml:")
    print("   pip install python3-saml")

    print("\n2. Configure Identity Provider (IdP):")
    print("   - Google Workspace: https://admin.google.com/saml")
    print("   - Microsoft 365: https://portal.azure.com")
    print("   - Okta: https://your-domain.okta.com/admin")

    print("\n3. Add to .env:")
    print("   SAML_SP_ENTITY_ID=https://app.knowledgevault.com")
    print("   SAML_SP_ACS_URL=https://app.knowledgevault.com/saml/acs")
    print("   SAML_GOOGLE_ENTITY_ID=https://accounts.google.com/o/saml2")
    print("   SAML_GOOGLE_SSO_URL=https://accounts.google.com/o/saml2/idp")
    print("   SAML_GOOGLE_CERT=<your_cert_here>")

    print("\n4. Get metadata:")
    print("   GET /saml/metadata?idp=google")
    print("   Upload to your IdP configuration")

    print("\n5. Test login:")
    print("   GET /saml/google/login")

    print("\n" + "="*60)
    print("✅ SAML SSO Ready!")
    print("="*60)
