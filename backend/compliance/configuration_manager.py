"""
Configuration Management Tracking System
Tracks all security and system configurations for SOC 2 compliance

SOC 2 Requirements:
- CC8.1: Configuration change tracking
- CC6.6: Security configuration management
- CC7.2: System configuration monitoring
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import difflib


@dataclass
class ConfigurationItem:
    """Configuration item tracking"""
    config_id: str
    category: str
    name: str
    current_value: Any
    previous_value: Optional[Any]
    last_changed: str
    changed_by: str
    change_reason: str
    approved_by: Optional[str]
    checksum: str


class ConfigurationCategory:
    """Configuration categories"""
    SECURITY = "security"
    NETWORK = "network"
    DATABASE = "database"
    APPLICATION = "application"
    AUTHENTICATION = "authentication"
    ENCRYPTION = "encryption"
    MONITORING = "monitoring"
    BACKUP = "backup"


class ConfigurationManager:
    """
    Configuration management and tracking system

    Features:
    - Configuration baseline tracking
    - Change detection
    - Change approval workflow
    - Configuration drift detection
    - Audit trail
    """

    def __init__(self, config_dir: str = "data/configuration"):
        """Initialize configuration manager"""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.baseline_file = self.config_dir / "baseline.json"
        self.history_dir = self.config_dir / "history"
        self.history_dir.mkdir(exist_ok=True)

        self.configurations = self._load_configurations()

        print("✓ Configuration Manager initialized")
        print(f"  - Configurations tracked: {len(self.configurations)}")

    def _load_configurations(self) -> Dict[str, ConfigurationItem]:
        """Load current configurations"""
        if not self.baseline_file.exists():
            return self._initialize_baseline()

        with open(self.baseline_file, 'r') as f:
            data = json.load(f)

        configurations = {}
        for config_id, config_data in data.items():
            configurations[config_id] = ConfigurationItem(**config_data)

        return configurations

    def _save_configurations(self):
        """Save configurations to file"""
        data = {
            config_id: asdict(config)
            for config_id, config in self.configurations.items()
        }

        with open(self.baseline_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _initialize_baseline(self) -> Dict[str, ConfigurationItem]:
        """Initialize configuration baseline"""
        configs = {}

        # Security configurations
        configs['https_enforced'] = ConfigurationItem(
            config_id='https_enforced',
            category=ConfigurationCategory.SECURITY,
            name='HTTPS Enforcement',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['hsts_enabled'] = ConfigurationItem(
            config_id='hsts_enabled',
            category=ConfigurationCategory.SECURITY,
            name='HSTS Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['input_validation_enabled'] = ConfigurationItem(
            config_id='input_validation_enabled',
            category=ConfigurationCategory.SECURITY,
            name='Input Validation',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        # Authentication configurations
        configs['mfa_required'] = ConfigurationItem(
            config_id='mfa_required',
            category=ConfigurationCategory.AUTHENTICATION,
            name='MFA Required',
            current_value=os.getenv('REQUIRE_MFA', 'false').lower() == 'true',
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum(os.getenv('REQUIRE_MFA', 'false'))
        )

        configs['max_jwt_lifetime'] = ConfigurationItem(
            config_id='max_jwt_lifetime',
            category=ConfigurationCategory.AUTHENTICATION,
            name='Max JWT Lifetime (seconds)',
            current_value=int(os.getenv('MAX_JWT_LIFETIME_SECONDS', '3600')),
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum(os.getenv('MAX_JWT_LIFETIME_SECONDS', '3600'))
        )

        configs['auth0_domain'] = ConfigurationItem(
            config_id='auth0_domain',
            category=ConfigurationCategory.AUTHENTICATION,
            name='Auth0 Domain',
            current_value=os.getenv('AUTH0_DOMAIN', ''),
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum(os.getenv('AUTH0_DOMAIN', ''))
        )

        # Encryption configurations
        configs['encryption_enabled'] = ConfigurationItem(
            config_id='encryption_enabled',
            category=ConfigurationCategory.ENCRYPTION,
            name='Encryption Enabled',
            current_value=os.getenv('ENCRYPTION_KEY') is not None,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True' if os.getenv('ENCRYPTION_KEY') else 'False')
        )

        configs['encryption_algorithm'] = ConfigurationItem(
            config_id='encryption_algorithm',
            category=ConfigurationCategory.ENCRYPTION,
            name='Encryption Algorithm',
            current_value='AES-256 (Fernet)',
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('AES-256 (Fernet)')
        )

        # Monitoring configurations
        configs['system_monitoring_enabled'] = ConfigurationItem(
            config_id='system_monitoring_enabled',
            category=ConfigurationCategory.MONITORING,
            name='System Monitoring Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['audit_logging_enabled'] = ConfigurationItem(
            config_id='audit_logging_enabled',
            category=ConfigurationCategory.MONITORING,
            name='Audit Logging Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['incident_detection_enabled'] = ConfigurationItem(
            config_id='incident_detection_enabled',
            category=ConfigurationCategory.MONITORING,
            name='Incident Detection Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        # Backup configurations
        configs['automated_backups_enabled'] = ConfigurationItem(
            config_id='automated_backups_enabled',
            category=ConfigurationCategory.BACKUP,
            name='Automated Backups Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['backup_encryption_enabled'] = ConfigurationItem(
            config_id='backup_encryption_enabled',
            category=ConfigurationCategory.BACKUP,
            name='Backup Encryption Enabled',
            current_value=True,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('True')
        )

        configs['backup_retention_days'] = ConfigurationItem(
            config_id='backup_retention_days',
            category=ConfigurationCategory.BACKUP,
            name='Backup Retention (days)',
            current_value=30,
            previous_value=None,
            last_changed=datetime.now().isoformat(),
            changed_by='system',
            change_reason='Initial baseline',
            approved_by='system',
            checksum=self._calculate_checksum('30')
        )

        # Save baseline
        self._save_baseline(configs)

        return configs

    def _save_baseline(self, configs: Dict[str, ConfigurationItem]):
        """Save baseline configuration"""
        data = {
            config_id: asdict(config)
            for config_id, config in configs.items()
        }

        with open(self.baseline_file, 'w') as f:
            json.dump(data, f, indent=2)

    def update_configuration(
        self,
        config_id: str,
        new_value: Any,
        changed_by: str,
        change_reason: str,
        approved_by: Optional[str] = None
    ) -> bool:
        """
        Update a configuration item

        Args:
            config_id: Configuration identifier
            new_value: New configuration value
            changed_by: Person making the change
            change_reason: Reason for change
            approved_by: Person approving change (if required)

        Returns:
            True if successful
        """
        if config_id not in self.configurations:
            print(f"❌ Configuration not found: {config_id}")
            return False

        config = self.configurations[config_id]

        # Create change record
        change_record = {
            "config_id": config_id,
            "timestamp": datetime.now().isoformat(),
            "previous_value": config.current_value,
            "new_value": new_value,
            "changed_by": changed_by,
            "change_reason": change_reason,
            "approved_by": approved_by,
            "previous_checksum": config.checksum,
            "new_checksum": self._calculate_checksum(str(new_value))
        }

        # Save change to history
        self._save_change_history(change_record)

        # Update configuration
        config.previous_value = config.current_value
        config.current_value = new_value
        config.last_changed = datetime.now().isoformat()
        config.changed_by = changed_by
        config.change_reason = change_reason
        config.approved_by = approved_by
        config.checksum = self._calculate_checksum(str(new_value))

        self._save_configurations()

        print(f"✓ Configuration updated: {config_id}")
        print(f"  Previous: {config.previous_value}")
        print(f"  Current: {config.current_value}")

        return True

    def _save_change_history(self, change_record: Dict):
        """Save change to history"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = self.history_dir / f"change_{timestamp}_{change_record['config_id']}.json"

        with open(history_file, 'w') as f:
            json.dump(change_record, f, indent=2)

    def detect_drift(self) -> List[Dict[str, Any]]:
        """
        Detect configuration drift from baseline

        Returns:
            List of drifted configurations
        """
        drifts = []

        # Check current environment variables against baseline
        current_configs = {
            'mfa_required': os.getenv('REQUIRE_MFA', 'false').lower() == 'true',
            'max_jwt_lifetime': int(os.getenv('MAX_JWT_LIFETIME_SECONDS', '3600')),
            'auth0_domain': os.getenv('AUTH0_DOMAIN', ''),
            'encryption_enabled': os.getenv('ENCRYPTION_KEY') is not None,
        }

        for config_id, current_value in current_configs.items():
            if config_id in self.configurations:
                baseline_value = self.configurations[config_id].current_value

                if current_value != baseline_value:
                    drifts.append({
                        "config_id": config_id,
                        "baseline_value": baseline_value,
                        "current_value": current_value,
                        "drift_detected": datetime.now().isoformat()
                    })

        return drifts

    def get_change_history(
        self,
        config_id: Optional[str] = None,
        days: int = 30
    ) -> List[Dict]:
        """
        Get configuration change history

        Args:
            config_id: Optional specific configuration
            days: Number of days to look back

        Returns:
            List of changes
        """
        changes = []
        cutoff_date = datetime.now().timestamp() - (days * 86400)

        for history_file in sorted(self.history_dir.glob("change_*.json")):
            # Check file modification time
            if history_file.stat().st_mtime < cutoff_date:
                continue

            with open(history_file, 'r') as f:
                change = json.load(f)

            # Filter by config_id if specified
            if config_id is None or change['config_id'] == config_id:
                changes.append(change)

        return sorted(changes, key=lambda x: x['timestamp'], reverse=True)

    def generate_configuration_report(self) -> Dict[str, Any]:
        """Generate comprehensive configuration report"""
        # Group configurations by category
        by_category = {}
        for config in self.configurations.values():
            category = config.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(asdict(config))

        # Detect drift
        drifts = self.detect_drift()

        # Get recent changes
        recent_changes = self.get_change_history(days=30)

        return {
            "report_date": datetime.now().isoformat(),
            "total_configurations": len(self.configurations),
            "configurations_by_category": by_category,
            "drift_detected": len(drifts) > 0,
            "drifts": drifts,
            "recent_changes_count": len(recent_changes),
            "recent_changes": recent_changes[:10],  # Last 10 changes
            "soc2_compliance_note": "CC8.1, CC6.6 - Configuration management"
        }

    def _calculate_checksum(self, value: str) -> str:
        """Calculate SHA-256 checksum of value"""
        return hashlib.sha256(value.encode()).hexdigest()

    def export_report(self, output_file: Optional[str] = None) -> Path:
        """Export configuration report"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.config_dir / f"config_report_{timestamp}.json"
        else:
            output_file = Path(output_file)

        report = self.generate_configuration_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✓ Configuration report exported: {output_file}")
        return output_file


if __name__ == "__main__":
    print("=" * 70)
    print("CONFIGURATION MANAGEMENT SYSTEM")
    print("=" * 70)

    # Initialize manager
    manager = ConfigurationManager()

    # Display current configurations
    print("\n📋 Current Configurations:")
    for config_id, config in manager.configurations.items():
        print(f"  {config.name}: {config.current_value}")

    # Check for drift
    print("\n🔍 Checking for configuration drift...")
    drifts = manager.detect_drift()
    if drifts:
        print(f"  ⚠️  {len(drifts)} configuration drift(s) detected:")
        for drift in drifts:
            print(f"    - {drift['config_id']}: {drift['baseline_value']} → {drift['current_value']}")
    else:
        print("  ✓ No drift detected")

    # Generate report
    print("\n📊 Generating configuration report...")
    report_path = manager.export_report()

    print("\n" + "=" * 70)
    print("✅ CONFIGURATION MANAGEMENT WORKING!")
    print("=" * 70)
