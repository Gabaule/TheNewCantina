#!/usr/bin/env python3
"""
Standalone Python script to convert a pytest JUnit XML report into a
detailed, human-readable Markdown test case report.

This script combines data from the JUnit XML (e.g., pass/fail status) with
pre-defined metadata (e.g., Test Steps, Prerequisites) to generate a
comprehensive report in the style of a traditional test case document.

---
HOW IT WORKS:
1. It parses the JUnit XML to get the execution results of each test function.
2. It looks up rich test case information from the `METADATA_REGISTRY`
   dictionary within this script, matching by the test function name.
3. It merges this data and generates a detailed Markdown file.
---

Usage:
    python3 report_generator.py <input_xml_file> <output_markdown_file>

Example:
    python3 report_generator_detailed.py tests_results.xml detailed_report.md
"""

import xml.etree.ElementTree as ET
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

# ==============================================================================
# 1. DATA MODELS - These classes represent the structure of your detailed report
# ==============================================================================

@dataclass
class TestStep:
    """A single step within a test case."""
    step_num: int
    details: str
    expected: str
    actual: str = "As Expected" # Default for passing tests
    status: str = "Pass"       # Default for passing tests

@dataclass
class TestCase:
    """Represents a full, detailed test case, combining XML results and metadata."""
    # Core execution data from XML
    name: str                   # The function name from pytest
    time: float
    status: str                 # 'Passed', 'Failed', 'Error', 'Skipped'
    failure_details: Optional[str] = None

    # Rich metadata (to be populated from METADATA_REGISTRY)
    test_id: str = "N/A"
    description: str = "N/A"
    created_by: str = "N/A"
    reviewed_by: str = "N/A"
    version: str = "1.0"
    qa_log: str = ""
    tester_name: str = "Automation"
    date_tested: str = ""
    prerequisites: List[str] = field(default_factory=list)
    test_data: List[str] = field(default_factory=list)
    test_scenario: str = ""
    test_steps: List[TestStep] = field(default_factory=list)


# ==============================================================================
# 2. METADATA REGISTRY - The "database" for your test cases
# ==============================================================================
# This is where you define the detailed information for each test case.
# The key MUST match the test function name from your pytest file.

METADATA_REGISTRY: Dict[str, Dict] = {
    "test_login_functionality": {
        "test_id": "BU_001",
        "description": "Test the Login Functionality in Banking",
        "created_by": "Mark",
        "reviewed_by": "Bill",
        "version": "2.1",
        "qa_log": "Review comments from Bill incorporate in version 2.1",
        "tester_name": "Mark",
        "prerequisites": ["Access to Chrome Browser"],
        "test_data": ["Userid = mg12345", "Pass = df12@434c"],
        "test_scenario": "Verify on entering valid userid and password, the customer can login",
        "test_steps": [
            TestStep(1, "Navigate to http://demo.guru99.com", "Site should open"),
            TestStep(2, "Enter Userid & Password", "Credential can be entered"),
            TestStep(3, "Click Submit", "Customer is logged in"),
        ],
    },
    "test_login_fails_with_invalid_password": {
        "test_id": "BU_002",
        "description": "Test that login fails with an invalid password",
        "created_by": "Jane",
        "reviewed_by": "Bill",
        "version": "1.0",
        "qa_log": "Test designed to fail to demonstrate failure reporting.",
        "tester_name": "Automation",
        "prerequisites": ["Valid username exists"],
        "test_data": ["Userid = mg12345", "Invalid Pass = wrongpassword"],
        "test_scenario": "Verify that the system shows an error message for incorrect credentials.",
        "test_steps": [
            TestStep(1, "Navigate to login page", "Login page is displayed"),
            TestStep(2, "Enter valid Userid and invalid Password", "Credentials are entered"),
            TestStep(3, "Click Submit", "An error message is displayed and user is not logged in"),
        ],
    },
    # --- Add more test case metadata here ---
    # "your_other_test_function_name": { ... }
}


# ==============================================================================
# 3. PARSING & DATA MERGING LOGIC
# ==============================================================================

def parse_and_merge_data(xml_file: str) -> List[TestCase]:
    """
    Parses the JUnit XML and merges its results with the METADATA_REGISTRY.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        suite_element = root.find('testsuite')
    except (ET.ParseError, FileNotFoundError, AttributeError):
        print(f"Error: Could not parse or find a valid <testsuite> in '{xml_file}'.")
        return []

    timestamp = suite_element.get('timestamp', datetime.now().isoformat())
    all_test_cases = []

    for case_element in suite_element.findall('testcase'):
        # Basic info from XML
        name = case_element.get('name', 'Unknown Test')
        time = float(case_element.get('time', '0'))
        status, failure_details = 'Passed', None

        if case_element.find('failure') is not None:
            status = 'Failed'
            failure_details = case_element.find('failure').text
        elif case_element.find('error') is not None:
            status = 'Error'
            failure_details = case_element.find('error').text
        elif case_element.find('skipped') is not None:
            status = 'Skipped'

        # Create the base TestCase object
        case = TestCase(name=name, time=time, status=status, failure_details=failure_details)

        # Enrich with metadata
        if name in METADATA_REGISTRY:
            metadata = METADATA_REGISTRY[name]
            for key, value in metadata.items():
                if hasattr(case, key):
                    setattr(case, key, value)

        case.date_tested = datetime.fromisoformat(timestamp).strftime('%d-%b-%Y')
        
        # Smartly update step statuses based on the overall result
        if case.status in ('Failed', 'Error') and case.test_steps:
            last_step = case.test_steps[-1]
            last_step.status = case.status
            last_step.actual = f"Execution failed. See details below."

        all_test_cases.append(case)

    return all_test_cases

# ==============================================================================
# 4. MARKDOWN GENERATION LOGIC
# ==============================================================================

def generate_summary(test_cases: List[TestCase]) -> str:
    """Creates the high-level summary section."""
    total = len(test_cases)
    passed = sum(1 for tc in test_cases if tc.status == 'Passed')
    failed = sum(1 for tc in test_cases if tc.status in ('Failed', 'Error'))
    skipped = sum(1 for tc in test_cases if tc.status == 'Skipped')
    
    return f"""# Test Execution Report

## 📊 Summary
| Metric          | Value |
|-----------------|-------|
| **Total Tests** | {total} |
| ✅ Passed       | {passed} |
| ❌ Failed/Error   | {failed} |
| ⏭️ Skipped       | {skipped} |

---
"""

def generate_detailed_case_markdown(case: TestCase) -> str:
    """Generates the detailed markdown for a single test case."""
    
    # Header table
    header = f"""### {case.test_id} - {case.description}
| | | | |
| :--- | :--- | :--- | :--- |
| **Test Case ID** | `{case.test_id}` | **Test Case Description** | {case.description} |
| **Created By** | {case.created_by} | **Reviewed By** | {case.reviewed_by} |
| **Version** | {case.version} | | |
| **QA Tester's Log** | <td colspan="3">{case.qa_log or "N/A"}</td> |
| **Tester's Name** | {case.tester_name} | **Date Tested** | {case.date_tested} |
| **Test Case (Pass/Fail)** | **{case.status}** | | |

"""
    
    # Prerequisites & Test Data
    prereqs = "\n".join([f"1. {p}" for p in case.prerequisites]) or "None"
    data = "\n".join([f"1. {d}" for d in case.test_data]) or "None"
    
    tables = f"""**Prerequisites:**
{prereqs}

**Test Data:**
{data}

**Test Scenario:**
{case.test_scenario or "N/A"}
"""

    # Test Steps
    steps_header = "| Step # | Step Details | Expected Results | Actual Results | Status |\n|:---:|:---|:---|:---|:---:|\n"
    steps_rows = "\n".join(
        [f"| {s.step_num} | {s.details} | {s.expected} | {s.actual} | **{s.status}** |" for s in case.test_steps]
    )
    steps = steps_header + steps_rows

    # Failure details
    failure_block = ""
    if case.failure_details:
        # This is the corrected, more compatible way to build the string
        details = case.failure_details.strip()
        failure_block = f"\n**Failure Details:**\n```\n{details}\n```\n"

    return f"{header}\n{tables}\n**Test Steps:**\n{steps}\n{failure_block}\n---\n"


# ==============================================================================
# 5. MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a JUnit XML file to a detailed Markdown test case report.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_xml", help="The path to the input JUnit XML file.")
    parser.add_argument("output_md", help="The path for the output Markdown file.")
    
    args = parser.parse_args()

    print(f"Parsing XML and merging with metadata: {args.input_xml}...")
    all_cases = parse_and_merge_data(args.input_xml)
    
    if not all_cases:
        print("No test cases found or parsed. Exiting.")
    else:
        print(f"Found {len(all_cases)} test cases. Generating Markdown report...")
        
        # Build the final report
        report_parts = [generate_summary(all_cases)]
        report_parts.append("## 📄 Detailed Test Case Results\n")
        
        # Sort cases to show failures first
        sorted_cases = sorted(all_cases, key=lambda c: (c.status != 'Passed', c.test_id))
        for case in sorted_cases:
            report_parts.append(generate_detailed_case_markdown(case))
            
        final_report = "\n".join(report_parts)
        
        try:
            with open(args.output_md, "w", encoding="utf-8") as f:
                f.write(final_report)
            print(f"✅ Successfully generated detailed report at: {args.output_md}")
        except IOError as e:
            print(f"Error: Could not write to output file '{args.output_md}'.\n{e}")