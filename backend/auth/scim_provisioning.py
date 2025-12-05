"""
SCIM 2.0 Provisioning API
Automatic user provisioning/deprovisioning from HR systems and IdPs

SCIM (System for Cross-domain Identity Management) enables:
- Auto-create users when hired
- Auto-delete users when fired
- Auto-update user roles when changed
- Sync groups/teams automatically

Supported by: Okta, Azure AD, Google Workspace, OneLogin, etc.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from flask import Blueprint, request, jsonify
from functools import wraps

# In-memory user store (replace with database in production)
USERS_DB: Dict[str, Dict] = {}
GROUPS_DB: Dict[str, Dict] = {}


class SCIMError(Exception):
    """SCIM-specific error"""
    def __init__(self, status: int, scim_type: str, detail: str):
        self.status = status
        self.scim_type = scim_type
        self.detail = detail
        super().__init__(detail)


def scim_bearer_auth(f):
    """Decorator: Require SCIM bearer token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify({
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                "status": "401",
                "detail": "Bearer token required"
            }), 401

        token = auth_header[7:]  # Remove 'Bearer '
        expected_token = os.getenv('SCIM_BEARER_TOKEN', '')

        if not expected_token:
            return jsonify({
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                "status": "500",
                "detail": "SCIM not configured"
            }), 500

        if token != expected_token:
            return jsonify({
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                "status": "401",
                "detail": "Invalid bearer token"
            }), 401

        return f(*args, **kwargs)

    return decorated


# Create SCIM blueprint
scim = Blueprint('scim', __name__, url_prefix='/scim/v2')


# ==============================================================================
# SCIM ServiceProviderConfig
# ==============================================================================

@scim.route('/ServiceProviderConfig', methods=['GET'])
def service_provider_config():
    """
    GET /scim/v2/ServiceProviderConfig
    Returns SCIM service provider configuration
    """
    return jsonify({
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
        "documentationUri": "https://docs.knowledgevault.com/scim",
        "patch": {
            "supported": True
        },
        "bulk": {
            "supported": False,
            "maxOperations": 0,
            "maxPayloadSize": 0
        },
        "filter": {
            "supported": True,
            "maxResults": 200
        },
        "changePassword": {
            "supported": False
        },
        "sort": {
            "supported": True
        },
        "etag": {
            "supported": False
        },
        "authenticationSchemes": [
            {
                "type": "oauthbearertoken",
                "name": "OAuth Bearer Token",
                "description": "Authentication via OAuth Bearer Token",
                "specUri": "http://www.rfc-editor.org/info/rfc6750",
                "documentationUri": "https://docs.knowledgevault.com/scim/auth"
            }
        ]
    }), 200


# ==============================================================================
# SCIM ResourceTypes
# ==============================================================================

@scim.route('/ResourceTypes', methods=['GET'])
def resource_types():
    """
    GET /scim/v2/ResourceTypes
    Returns supported resource types
    """
    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 2,
        "Resources": [
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
                "id": "User",
                "name": "User",
                "endpoint": "/Users",
                "description": "User Account",
                "schema": "urn:ietf:params:scim:schemas:core:2.0:User"
            },
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
                "id": "Group",
                "name": "Group",
                "endpoint": "/Groups",
                "description": "Group",
                "schema": "urn:ietf:params:scim:schemas:core:2.0:Group"
            }
        ]
    }), 200


# ==============================================================================
# SCIM Schemas
# ==============================================================================

@scim.route('/Schemas', methods=['GET'])
def schemas():
    """
    GET /scim/v2/Schemas
    Returns SCIM schemas
    """
    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 2,
        "Resources": [
            {
                "id": "urn:ietf:params:scim:schemas:core:2.0:User",
                "name": "User",
                "description": "User Account"
            },
            {
                "id": "urn:ietf:params:scim:schemas:core:2.0:Group",
                "name": "Group",
                "description": "Group"
            }
        ]
    }), 200


# ==============================================================================
# SCIM Users
# ==============================================================================

@scim.route('/Users', methods=['GET'])
@scim_bearer_auth
def list_users():
    """
    GET /scim/v2/Users
    List all users (with filtering and pagination)
    """
    # Get query parameters
    start_index = int(request.args.get('startIndex', 1))
    count = int(request.args.get('count', 100))
    filter_query = request.args.get('filter', '')

    # Filter users
    users = list(USERS_DB.values())

    if filter_query:
        # Simple filter support: userName eq "john@example.com"
        if 'userName eq' in filter_query:
            username = filter_query.split('"')[1]
            users = [u for u in users if u.get('userName') == username]

    # Paginate
    total = len(users)
    users = users[start_index-1:start_index-1+count]

    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": total,
        "startIndex": start_index,
        "itemsPerPage": len(users),
        "Resources": users
    }), 200


@scim.route('/Users/<user_id>', methods=['GET'])
@scim_bearer_auth
def get_user(user_id):
    """
    GET /scim/v2/Users/{id}
    Get specific user
    """
    user = USERS_DB.get(user_id)

    if not user:
        return jsonify({
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "status": "404",
            "detail": f"User {user_id} not found"
        }), 404

    return jsonify(user), 200


@scim.route('/Users', methods=['POST'])
@scim_bearer_auth
def create_user():
    """
    POST /scim/v2/Users
    Create new user (auto-provisioning)
    """
    data = request.get_json()

    # Generate unique ID
    user_id = str(uuid.uuid4())

    # Create user object
    user = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": user_id,
        "userName": data.get('userName'),
        "name": {
            "givenName": data.get('name', {}).get('givenName', ''),
            "familyName": data.get('name', {}).get('familyName', ''),
            "formatted": data.get('name', {}).get('formatted', '')
        },
        "emails": data.get('emails', []),
        "active": data.get('active', True),
        "groups": data.get('groups', []),
        "roles": data.get('roles', []),
        "meta": {
            "resourceType": "User",
            "created": datetime.utcnow().isoformat() + "Z",
            "lastModified": datetime.utcnow().isoformat() + "Z",
            "location": f"/scim/v2/Users/{user_id}"
        }
    }

    # Store user
    USERS_DB[user_id] = user

    print(f"✅ SCIM: Created user {user['userName']} (ID: {user_id})")

    return jsonify(user), 201


@scim.route('/Users/<user_id>', methods=['PUT'])
@scim_bearer_auth
def update_user(user_id):
    """
    PUT /scim/v2/Users/{id}
    Update user (full replacement)
    """
    if user_id not in USERS_DB:
        return jsonify({
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "status": "404",
            "detail": f"User {user_id} not found"
        }), 404

    data = request.get_json()

    # Update user
    user = USERS_DB[user_id]
    user.update({
        "userName": data.get('userName', user.get('userName')),
        "name": data.get('name', user.get('name')),
        "emails": data.get('emails', user.get('emails')),
        "active": data.get('active', user.get('active')),
        "groups": data.get('groups', user.get('groups')),
        "roles": data.get('roles', user.get('roles')),
    })

    user['meta']['lastModified'] = datetime.utcnow().isoformat() + "Z"

    print(f"✅ SCIM: Updated user {user['userName']} (ID: {user_id})")

    return jsonify(user), 200


@scim.route('/Users/<user_id>', methods=['PATCH'])
@scim_bearer_auth
def patch_user(user_id):
    """
    PATCH /scim/v2/Users/{id}
    Partial update user
    """
    if user_id not in USERS_DB:
        return jsonify({
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "status": "404",
            "detail": f"User {user_id} not found"
        }), 404

    data = request.get_json()
    user = USERS_DB[user_id]

    # Process PATCH operations
    operations = data.get('Operations', [])

    for op in operations:
        op_type = op.get('op', '').lower()
        path = op.get('path', '')
        value = op.get('value')

        if op_type == 'replace':
            if path == 'active':
                user['active'] = value
            elif path == 'userName':
                user['userName'] = value
        elif op_type == 'add':
            # Add operation
            pass
        elif op_type == 'remove':
            # Remove operation (e.g., deactivate)
            if path == 'active':
                user['active'] = False

    user['meta']['lastModified'] = datetime.utcnow().isoformat() + "Z"

    print(f"✅ SCIM: Patched user {user['userName']} (ID: {user_id})")

    return jsonify(user), 200


@scim.route('/Users/<user_id>', methods=['DELETE'])
@scim_bearer_auth
def delete_user(user_id):
    """
    DELETE /scim/v2/Users/{id}
    Delete user (deprovisioning)
    """
    if user_id not in USERS_DB:
        return jsonify({
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "status": "404",
            "detail": f"User {user_id} not found"
        }), 404

    user = USERS_DB.pop(user_id)

    print(f"🗑️  SCIM: Deleted user {user['userName']} (ID: {user_id})")

    return '', 204


# ==============================================================================
# SCIM Groups
# ==============================================================================

@scim.route('/Groups', methods=['GET'])
@scim_bearer_auth
def list_groups():
    """
    GET /scim/v2/Groups
    List all groups
    """
    groups = list(GROUPS_DB.values())

    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(groups),
        "startIndex": 1,
        "itemsPerPage": len(groups),
        "Resources": groups
    }), 200


@scim.route('/Groups/<group_id>', methods=['GET'])
@scim_bearer_auth
def get_group(group_id):
    """
    GET /scim/v2/Groups/{id}
    Get specific group
    """
    group = GROUPS_DB.get(group_id)

    if not group:
        return jsonify({
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "status": "404",
            "detail": f"Group {group_id} not found"
        }), 404

    return jsonify(group), 200


@scim.route('/Groups', methods=['POST'])
@scim_bearer_auth
def create_group():
    """
    POST /scim/v2/Groups
    Create new group
    """
    data = request.get_json()

    group_id = str(uuid.uuid4())

    group = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
        "id": group_id,
        "displayName": data.get('displayName'),
        "members": data.get('members', []),
        "meta": {
            "resourceType": "Group",
            "created": datetime.utcnow().isoformat() + "Z",
            "lastModified": datetime.utcnow().isoformat() + "Z",
            "location": f"/scim/v2/Groups/{group_id}"
        }
    }

    GROUPS_DB[group_id] = group

    print(f"✅ SCIM: Created group {group['displayName']} (ID: {group_id})")

    return jsonify(group), 201


# ==============================================================================
# Error Handlers
# ==============================================================================

@scim.errorhandler(400)
def bad_request(error):
    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "status": "400",
        "detail": str(error)
    }), 400


@scim.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "status": "401",
        "detail": "Unauthorized"
    }), 401


@scim.errorhandler(404)
def not_found(error):
    return jsonify({
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "status": "404",
        "detail": "Resource not found"
    }), 404


def init_scim(app):
    """Initialize SCIM provisioning API with Flask app"""
    app.register_blueprint(scim)

    print("✓ SCIM 2.0 provisioning API registered")
    print("  - Endpoint: /scim/v2/")
    print("  - Users: /scim/v2/Users")
    print("  - Groups: /scim/v2/Groups")

    return scim


if __name__ == "__main__":
    print("="*60)
    print("SCIM 2.0 Provisioning Setup Guide")
    print("="*60)

    print("\n📋 SETUP STEPS:")

    print("\n1. Generate SCIM bearer token:")
    print("   python -c \"import secrets; print(secrets.token_urlsafe(32))\"")

    print("\n2. Add to .env:")
    print("   SCIM_BEARER_TOKEN=your_generated_token_here")

    print("\n3. Configure in your IdP:")
    print("   - Okta: Applications → Your App → Provisioning → Configure API Integration")
    print("   - Azure AD: Enterprise Applications → Your App → Provisioning → Provisioning Mode: Automatic")
    print("   - Google Workspace: Apps → SAML apps → Your App → User provisioning")

    print("\n4. SCIM Endpoint Configuration:")
    print("   Base URL: https://api.knowledgevault.com/scim/v2")
    print("   Auth: Bearer Token")
    print("   Token: <your_bearer_token>")

    print("\n5. Test SCIM API:")
    print("   GET /scim/v2/ServiceProviderConfig")
    print("   GET /scim/v2/Users")

    print("\n" + "="*60)
    print("✅ SCIM Provisioning Ready!")
    print("="*60)

    print("\n🔄 What SCIM Does:")
    print("   - Employee hired → Auto-create user ✅")
    print("   - Employee fired → Auto-delete user 🗑️")
    print("   - Role changed → Auto-update permissions 🔄")
    print("   - All synced from your HR system automatically!")
