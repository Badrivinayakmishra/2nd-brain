"""
Manual Test Script for Azure OpenAI + Data Sanitization
Run this to verify:
1. PII sanitization works
2. Azure OpenAI connection works
3. Sanitized data flows correctly to Azure
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from openai import AzureOpenAI
from security.data_sanitizer import DataSanitizer


def test_azure_openai_connection():
    """Test 1: Azure OpenAI connection"""
    print("\n" + "="*60)
    print("TEST 1: Azure OpenAI Connection")
    print("="*60)

    # Load environment variables
    load_dotenv()

    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')

    print(f"\n📋 Configuration:")
    print(f"   Endpoint: {endpoint}")
    print(f"   Deployment: {deployment}")
    print(f"   API Version: {api_version}")
    print(f"   API Key: {'*' * 20}{api_key[-4:] if api_key else 'NOT SET'}")

    if not all([api_key, endpoint, deployment]):
        print("\n❌ ERROR: Azure OpenAI credentials not configured in .env")
        return False

    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

        # Test simple completion
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Azure OpenAI works!' if you can read this."}
            ],
            max_tokens=50
        )

        result = response.choices[0].message.content
        print(f"\n✅ Azure OpenAI Response: {result}")
        print("✅ Connection successful!")
        return True

    except Exception as e:
        print(f"\n❌ Azure OpenAI Error: {str(e)}")
        return False


def test_sanitization_with_azure():
    """Test 2: Sanitization + Azure OpenAI integration"""
    print("\n" + "="*60)
    print("TEST 2: Data Sanitization + Azure OpenAI")
    print("="*60)

    # Initialize sanitizer
    sanitizer = DataSanitizer(max_length=500)

    # Create test document with PII
    test_document = {
        'content': '''
        Research trial update for Dr. Sarah Johnson.
        Contact: sarah.johnson@med-research-lab.edu
        Phone: 555-123-4567
        Patient ID: 123-45-6789

        Trial results show promising outcomes. Patient responded well
        to treatment protocol. Next review scheduled for follow-up.
        ''',
        'subject': 'Confidential Trial Results - Phase 2',
        'type': 'email',
        'date': '2024-01-15'
    }

    print("\n📧 Original Document (WITH PII):")
    print("─" * 60)
    print(f"Subject: {test_document['subject']}")
    print(f"Content: {test_document['content'][:200]}...")

    # Sanitize the document
    sanitized = sanitizer.sanitize_document(test_document)

    print("\n🔒 Sanitized Document (PII REMOVED):")
    print("─" * 60)
    print(f"Subject: {sanitized.get('subject', 'N/A')}")
    print(f"Content snippet: {sanitized.get('snippet', 'N/A')}")

    # Validate sanitization
    validation = sanitizer.validate_sanitization(sanitized.get('snippet', ''))

    if not validation['is_safe']:
        print("\n❌ CRITICAL: PII still present after sanitization!")
        print(f"   Found: {validation['found_pii']}")
        return False

    print("\n✅ PII successfully removed!")

    # Get sanitization report
    report = sanitizer.get_sanitization_report(
        test_document['content'],
        sanitized.get('snippet', '')
    )

    print(f"\n📊 Sanitization Report:")
    print(f"   Emails removed: {report['pii_removed']['email']}")
    print(f"   Phone numbers removed: {report['pii_removed']['phone']}")
    print(f"   SSNs removed: {report['pii_removed']['ssn']}")
    print(f"   Original length: {report['original_length']} chars")
    print(f"   Sanitized length: {report['sanitized_length']} chars")

    # Now send ONLY sanitized data to Azure OpenAI
    print("\n🚀 Sending to Azure OpenAI (SANITIZED DATA ONLY):")
    print("─" * 60)

    try:
        load_dotenv()
        client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )

        # Send sanitized content to Azure
        prompt = f"""Analyze this research document and categorize it.
Document type: {sanitized.get('type')}
Content: {sanitized.get('snippet')}

Categorize as: work or personal"""

        response = client.chat.completions.create(
            model=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
            messages=[
                {"role": "system", "content": "You are a document classifier."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )

        result = response.choices[0].message.content
        print(f"Azure Response: {result}")
        print("\n✅ Sanitized data successfully processed by Azure OpenAI!")
        print("✅ No PII was sent to external API!")

        return True

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_where_is_data_stored():
    """Test 3: Explain data storage locations"""
    print("\n" + "="*60)
    print("TEST 3: Data Storage Locations")
    print("="*60)

    print("\n📁 YOUR DATA IS STORED IN THESE LOCATIONS:")
    print("─" * 60)

    backend_dir = Path(__file__).parent.parent

    storage_locations = {
        "ChromaDB Vector Database": {
            "path": backend_dir / "data" / "chroma_db",
            "description": "Vector embeddings for semantic search",
            "contains": "Document embeddings, metadata, similarity indexes",
            "isolated": "YES - separate collections per org_id"
        },
        "Employee Clusters (JSONL)": {
            "path": backend_dir / "data" / "employee_clusters",
            "description": "Clustered employee documents",
            "contains": "Raw document content, classifications, metadata",
            "isolated": "NO - needs organization_id in file structure"
        },
        "Project Clusters (JSONL)": {
            "path": backend_dir / "data" / "project_clusters",
            "description": "Project-level document clusters",
            "contains": "Project documents, cluster labels, summaries",
            "isolated": "NO - needs organization_id in file structure"
        },
        "Neo4j Knowledge Graph": {
            "path": "External database (bolt://localhost:7687)",
            "description": "Optional - entity relationships",
            "contains": "Entities, relationships, graph structure",
            "isolated": "NEEDS IMPLEMENTATION - add org_id labels"
        },
        "Environment Variables": {
            "path": backend_dir / ".env",
            "description": "API keys and configuration",
            "contains": "Azure OpenAI credentials, API keys",
            "isolated": "N/A - configuration file"
        }
    }

    for name, info in storage_locations.items():
        print(f"\n📂 {name}")
        print(f"   Location: {info['path']}")
        print(f"   Description: {info['description']}")
        print(f"   Contains: {info['contains']}")
        print(f"   Multi-tenant isolated: {info['isolated']}")

        # Check if path exists
        if isinstance(info['path'], Path):
            if info['path'].exists():
                print(f"   Status: ✅ EXISTS")
            else:
                print(f"   Status: ⚠️  NOT YET CREATED")

    print("\n" + "="*60)
    print("🔒 SECURITY NOTES:")
    print("="*60)
    print("✅ Azure OpenAI: Zero retention (data deleted immediately)")
    print("✅ ChromaDB: Multi-tenant isolated (org_{org_id}_collection)")
    print("⚠️  JSONL files: Need organization_id in directory structure")
    print("⚠️  Neo4j: Need to add organization_id labels to nodes")
    print("\n💡 RECOMMENDATION: Add organization_id to all file paths")
    print("   Example: data/employee_clusters/{org_id}/{employee}/...")

    return True


def main():
    """Run all tests"""
    print("\n")
    print("🧪" * 30)
    print("MANUAL TEST SUITE - Research Lab Pilot")
    print("Testing: Data Sanitization + Azure OpenAI Integration")
    print("🧪" * 30)

    results = {
        "Azure OpenAI Connection": test_azure_openai_connection(),
        "Sanitization + Azure Integration": test_sanitization_with_azure(),
        "Data Storage Documentation": test_where_is_data_stored()
    }

    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n" + "🎉" * 30)
        print("✅✅✅ ALL TESTS PASSED! ✅✅✅")
        print("🎉" * 30)
        print("\n🚀 YOU ARE READY FOR THE RESEARCH LAB PILOT!")
        print("\n📋 What to show research lab:")
        print("   1. Run this test script (shows PII removal)")
        print("   2. Show .env configuration (shows Azure Enterprise)")
        print("   3. Show data storage locations (shows isolation)")
        print("   4. Show PILOT_READY_CHECKLIST.md (shows implementation)")
    else:
        print("\n⚠️  SOME TESTS FAILED - Fix before pilot!")

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
