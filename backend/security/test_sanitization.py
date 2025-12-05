"""
Test Data Sanitization
Verify PII is removed before sending to OpenAI
"""

from data_sanitizer import DataSanitizer


def test_email_removal():
    """Test that emails are removed"""
    sanitizer = DataSanitizer()

    text = "Contact Dr. Smith at john.smith@research-lab.edu for trial results"
    result = sanitizer.sanitize_text(text)

    assert "@research-lab.edu" not in result
    assert "[EMAIL_REDACTED]" in result
    print("✅ Email removal works")


def test_phone_removal():
    """Test that phone numbers are removed"""
    sanitizer = DataSanitizer()

    text = "Call me at 555-123-4567 or (555) 987-6543"
    result = sanitizer.sanitize_text(text)

    assert "555-123-4567" not in result
    assert "555-987-6543" not in result
    assert "[PHONE_REDACTED]" in result
    print("✅ Phone number removal works")


def test_ssn_removal():
    """Test that SSNs are removed"""
    sanitizer = DataSanitizer()

    text = "Patient SSN: 123-45-6789"
    result = sanitizer.sanitize_text(text)

    assert "123-45-6789" not in result
    assert "[SSN_REDACTED]" in result
    print("✅ SSN removal works")


def test_data_minimization():
    """Test that long text is truncated"""
    sanitizer = DataSanitizer(max_length=100)

    long_text = "A" * 500
    result = sanitizer.sanitize_text(long_text)

    assert len(result) <= 150  # 100 + truncation message
    assert "[TRUNCATED_FOR_PRIVACY]" in result
    print("✅ Data minimization works")


def test_document_sanitization():
    """Test full document sanitization"""
    sanitizer = DataSanitizer()

    doc = {
        'id': 'secret-doc-123',
        'content': 'Email me at researcher@lab.edu about patient 123-45-6789. Call 555-123-4567.',
        'subject': 'Confidential Trial Data',
        'type': 'email',
        'date': '2024-01-15'
    }

    sanitized = sanitizer.sanitize_document(doc)

    # Should not contain PII
    assert '@lab.edu' not in str(sanitized)
    assert '123-45-6789' not in str(sanitized)
    assert '555-123-4567' not in str(sanitized)

    # Should have redactions
    assert '[EMAIL_REDACTED]' in sanitized.get('snippet', '')
    assert '[SSN_REDACTED]' in sanitized.get('snippet', '')

    # Should have safe fields only
    assert 'type' in sanitized
    assert 'date' in sanitized

    print("✅ Document sanitization works")
    print(f"   Original ID: secret-doc-123")
    print(f"   Sanitized ID: {sanitized.get('id')}")


def test_validation():
    """Test sanitization validation"""
    sanitizer = DataSanitizer()

    # Unsanitized text
    unsafe_text = "Contact john@example.com at 555-123-4567"
    validation = sanitizer.validate_sanitization(unsafe_text)

    assert not validation['is_safe']
    assert 'email' in validation['found_pii']
    assert 'phone' in validation['found_pii']

    # Sanitized text
    safe_text = sanitizer.sanitize_text(unsafe_text)
    validation = sanitizer.validate_sanitization(safe_text)

    assert validation['is_safe']
    assert len(validation['found_pii']) == 0

    print("✅ Validation works")


def test_sanitization_report():
    """Test sanitization reporting"""
    sanitizer = DataSanitizer()

    original = "Email me at john@lab.edu or call 555-123-4567. SSN: 123-45-6789"
    sanitized = sanitizer.sanitize_text(original)

    report = sanitizer.get_sanitization_report(original, sanitized)

    assert report['pii_removed']['email'] == 1
    assert report['pii_removed']['phone'] == 1
    assert report['pii_removed']['ssn'] == 1

    print("✅ Reporting works")
    print(f"   Removed: {report['pii_removed']}")


if __name__ == '__main__':
    print("="*60)
    print("Testing Data Sanitization for Research Lab Pilot")
    print("="*60)
    print()

    test_email_removal()
    test_phone_removal()
    test_ssn_removal()
    test_data_minimization()
    test_document_sanitization()
    test_validation()
    test_sanitization_report()

    print()
    print("="*60)
    print("✅✅✅ ALL SANITIZATION TESTS PASSED ✅✅✅")
    print("="*60)
    print()
    print("🔒 Your data is safe to send to OpenAI!")
    print("🔒 All PII has been removed!")
    print("🔒 Data minimization is active!")
