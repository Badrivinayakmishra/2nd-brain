# Deployment Guide

**SOC 2 Compliant Automated Deployment**

## Quick Start

### 1. Development Deployment

```bash
# Deploy to development environment
python deployment/deploy.py --environment development --auto-approve

# Or with tests
python deployment/deploy.py --environment development
```

### 2. Staging Deployment

```bash
# Deploy to staging (recommended before production)
python deployment/deploy.py --environment staging

# Approve when prompted
```

### 3. Production Deployment

```bash
# Deploy to production (requires approval)
python deployment/deploy.py --environment production

# NEVER use --skip-tests in production!
# NEVER use --auto-approve in production!
```

---

## Pre-Deployment Checklist

### Required Environment Variables

Set these in your environment before deployment:

```bash
# Security
export ENCRYPTION_KEY="your-32-byte-key"  # Generate with: python -c "from security.encryption_manager import EncryptionManager; print(EncryptionManager.generate_key())"

# Auth0
export AUTH0_DOMAIN="your-domain.auth0.com"
export AUTH0_AUDIENCE="https://your-api.com"
export AUTH0_CLIENT_ID="your-client-id"
export AUTH0_CLIENT_SECRET="your-client-secret"

# Security Settings
export REQUIRE_MFA="true"
export MAX_JWT_LIFETIME_SECONDS="3600"  # 1 hour

# Alerts (optional but recommended)
export SENDGRID_API_KEY="your-sendgrid-key"
export ALERT_EMAIL_TO="security@yourcompany.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export TWILIO_ACCOUNT_SID="your-twilio-sid"
export TWILIO_AUTH_TOKEN="your-twilio-token"
export TWILIO_FROM_PHONE="+1234567890"
export TWILIO_TO_PHONE="+1234567890"
```

### Required Files

Ensure these files exist:
- `security/input_validator.py`
- `security/encryption_manager.py`
- `security/audit_logger.py`
- `security/incident_logger.py`
- `monitoring/uptime_monitor.py`
- `backup/backup_manager.py`
- `requirements.txt`

### Dependencies

```bash
pip install -r requirements.txt
```

---

## Deployment Process

The automated deployer follows these steps:

### 1. Pre-Deployment Validation ✅
- Checks environment variables
- Verifies required files exist
- Validates Python dependencies

### 2. Security Tests 🔒
- Runs comprehensive security test suite
- Tests all SOC 2 controls
- Validates 95%+ test coverage

### 3. Backup Creation 💾
- Creates encrypted backup of current state
- Enables rollback if deployment fails

### 4. Deployment Approval 👍
- Production requires manual approval
- Staging/dev can be auto-approved

### 5. Infrastructure Deployment 🏗️
- Creates required directories
- Sets up data storage
- Configures logging

### 6. Application Deployment 🚀
- Installs dependencies
- Deploys application code
- Updates configurations

### 7. Security Configuration 🛡️
- Enables HTTPS enforcement
- Configures encryption
- Sets up audit logging
- Enables incident detection

### 8. Health Checks ❤️
- CPU health
- Memory health
- Disk space
- Database connectivity

### 9. Monitoring Activation 📊
- Enables system monitoring
- Configures alerting
- Starts health tracking

### 10. Finalization 🎉
- Creates deployment marker
- Records deployment metadata
- Saves audit trail

---

## Rollback Procedure

If deployment fails, the system automatically:

1. Stops deployment
2. Restores from backup
3. Logs rollback event
4. Notifies administrators

### Manual Rollback

```bash
# If automatic rollback fails
python -c "from backup.backup_manager import BackupManager; \
           manager = BackupManager(); \
           manager.restore_backup('path/to/backup.tar.gz.encrypted', '.')"
```

---

## Post-Deployment Verification

### 1. Check Deployment Status

```bash
# View deployment log
cat logs/deployments/deploy_YYYYMMDD_HHMMSS.json
```

### 2. Verify Health

```bash
# Check system health
python -c "from monitoring.uptime_monitor import SystemHealthMonitor; \
           monitor = SystemHealthMonitor(); \
           print(monitor.get_overall_health())"
```

### 3. Test Security Controls

```bash
# Run security audit
python tests/comprehensive_security_test.py
```

### 4. Verify Monitoring

```bash
# Check monitoring is active
python -c "from monitoring.uptime_monitor import SystemHealthMonitor; \
           monitor = SystemHealthMonitor(); \
           monitor.check_all_systems()"
```

---

## Deployment Frequency

### SOC 2 Best Practices

- **Development**: Deploy as needed
- **Staging**: Weekly or before production
- **Production**:
  - Regular deployments: Bi-weekly
  - Security patches: Within 48 hours
  - Critical fixes: Immediately

---

## Deployment Evidence (SOC 2 CC8)

Each deployment automatically creates:

1. **Deployment Log**: `logs/deployments/deploy_*.json`
   - All deployment steps
   - Timestamps
   - Status
   - Errors (if any)

2. **Deployment Marker**: `data/deployments/deploy_*.json`
   - Deployment ID
   - Environment
   - Git commit hash
   - Timestamp

3. **Backup Archive**: `data/backups/pre_deploy_*.tar.gz.encrypted`
   - Pre-deployment state
   - Rollback capability

---

## Troubleshooting

### Deployment Fails at Validation

```bash
# Check environment variables
env | grep -E "(ENCRYPTION_KEY|AUTH0|REQUIRE_MFA)"

# Check required files
ls security/*.py monitoring/*.py backup/*.py
```

### Deployment Fails at Tests

```bash
# Run tests manually to see details
python tests/comprehensive_security_test.py

# Check specific test
python -m pytest tests/comprehensive_security_test.py::TestClassName -v
```

### Deployment Fails at Health Checks

```bash
# Check system resources
df -h  # Disk space
free -h  # Memory
top  # CPU

# Check logs
tail -f logs/monitoring/*.log
```

### Rollback Fails

```bash
# Manual restoration
cd data/backups
ls -lh pre_deploy_*.tar.gz.encrypted

# Restore manually
python -c "from backup.backup_manager import BackupManager; \
           manager = BackupManager(); \
           manager.restore_backup('pre_deploy_LATEST.tar.gz.encrypted', '.')"
```

---

## Security Notes

### Production Deployment Security

1. **NEVER skip tests** in production
2. **ALWAYS require approval** for production
3. **VERIFY backup exists** before deploying
4. **TEST rollback procedure** regularly
5. **MAINTAIN audit trail** of all deployments

### Change Management (SOC 2 CC8.1)

All deployments must:
- ✅ Be tested in staging first
- ✅ Have approval (production)
- ✅ Include rollback plan
- ✅ Be documented in deployment log
- ✅ Be verified with health checks

---

## Deployment Checklist

### Before Deployment

- [ ] All environment variables set
- [ ] Tests passing locally
- [ ] Staging deployment successful
- [ ] Backup verified
- [ ] Approval obtained (if production)
- [ ] Maintenance window scheduled (if production)

### During Deployment

- [ ] Monitor deployment log
- [ ] Watch for errors
- [ ] Verify each step completes
- [ ] Check health checks pass

### After Deployment

- [ ] Verify application is running
- [ ] Check health endpoint: `/health/detailed`
- [ ] Review deployment log
- [ ] Confirm monitoring active
- [ ] Test critical workflows
- [ ] Notify stakeholders

---

## Continuous Deployment (Future)

For CI/CD integration:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Staging
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          python deployment/deploy.py \
            --environment staging \
            --auto-approve
```

---

## Contact

For deployment issues:
- **Slack**: #deployments
- **Email**: devops@yourcompany.com
- **On-Call**: PagerDuty

---

**Last Updated**: December 5, 2024
**SOC 2 Control**: CC8.1 - Change Management
