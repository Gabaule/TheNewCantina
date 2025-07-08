#!/usr/bin/env python3
"""
Standalone Python script to convert a pytest JUnit XML report into a
clean, professional, and human-readable Markdown test case report.

This script generates a focused report, omitting unnecessary manual-process
fields like 'Created By', 'Reviewed By', and 'QA Log' for a concise output.
"""

import xml.etree.ElementTree as ET
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

# ==============================================================================
# 1. DATA MODELS (Streamlined for automation)
# ==============================================================================

@dataclass
class TestStep:
    """A single step within a test case."""
    step_num: int
    details: str
    expected: str
    actual: str = "As Expected"
    status: str = "Pass"

@dataclass
class TestCase:
    """Represents a full, detailed test case, combining XML results and metadata."""
    name: str
    time: float
    status: str
    failure_details: Optional[str] = None
    test_id: str = "N/A"
    description: str = "N/A"
    version: str = "1.0"
    tester_name: str = "Automation"
    date_tested: str = ""
    prerequisites: List[str] = field(default_factory=list)
    test_data: List[str] = field(default_factory=list)
    test_scenario: str = ""
    test_steps: List[TestStep] = field(default_factory=list)
    has_metadata: bool = False # Flag to track if metadata was found

# ==============================================================================
# 2. METADATA REGISTRY (Streamlined)
# ==============================================================================
METADATA_REGISTRY: Dict[str, Dict] = {
    # --- API: Admin CRUD Tests ---
    "test_user_crud": {
        "test_id": "API_001",
        "description": "Verify full CRUD (Create, Read, Update, Delete) for the User API endpoint.",
        "test_scenario": "An admin must be able to manage users through the API.",
        "prerequisites": ["An authenticated admin client."],
        "test_steps": [
            TestStep(1, "Send POST to `/api/v1/user/` to create a new user.", "Receives HTTP 201 and user data."),
            TestStep(2, "Send GET to `/api/v1/user/` to list all users.", "Receives HTTP 200 and the new user is in the list."),
            TestStep(3, "Send PUT to `/api/v1/user/{id}` to update the user.", "Receives HTTP 200 and updated data."),
            TestStep(4, "Send DELETE to `/api/v1/user/{id}` to delete the user.", "Receives HTTP 200."),
        ],
    },
    "test_cafeteria_crud": {
        "test_id": "API_002",
        "description": "Verify full CRUD for the Cafeteria API endpoint.",
        "prerequisites": ["An authenticated admin client."],
        "test_steps": [TestStep(1, "Perform Create, Read, Update, Delete operations on the Cafeteria API.", "All operations succeed with correct HTTP status codes.")]
    },
    "test_dish_crud": {
        "test_id": "API_003",
        "description": "Verify full CRUD for the Dish API endpoint.",
        "prerequisites": ["An authenticated admin client."],
        "test_steps": [TestStep(1, "Perform Create, Read, Update, Delete operations on the Dish API.", "All operations succeed with correct HTTP status codes.")]
    },
    "test_menu_and_item_crud": {
        "test_id": "API_004",
        "description": "Verify creation of Menus and linking Menu Items via API.",
        "prerequisites": ["Authenticated admin client.", "A Cafeteria and a Dish exist."],
        "test_steps": [
            TestStep(1, "Create a DailyMenu via POST request.", "Receives HTTP 201."),
            TestStep(2, "Create a DailyMenuItem linking the menu and a dish.", "Receives HTTP 201."),
        ],
    },
    
    # --- API: Auth Tests ---
    "test_user_api_permissions": {
        "test_id": "API_SEC_001",
        "description": "Verify API permissions for a standard authenticated user.",
        "test_scenario": "A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.",
        "test_steps": [
            TestStep(1, "Attempt to access admin-only endpoints (e.g., list all users).", "Access is denied with HTTP 401/403."),
            TestStep(2, "Attempt to access own user data.", "Access is allowed with HTTP 200."),
            TestStep(3, "Attempt to access another user's data (e.g., another user's reservation).", "Access is denied with HTTP 401/403/404."),
        ]
    },

    # --- E2E Tests ---
    "test_loginAdminLogOut": {
        "test_id": "E2E_001",
        "description": "Verify Admin Login and Logout functionality through the UI.",
        "prerequisites": ["Application is running.", "Default admin user exists."],
        "test_steps": [
            TestStep(1, "Navigate to login page.", "Page loads."),
            TestStep(2, "Enter admin credentials and submit.", "Redirected to admin dashboard."),
            TestStep(3, "Click the 'Logout' link.", "Redirected to login page."),
        ],
    },
    "test_orderfoodinthepast": {
        "test_id": "E2E_002",
        "description": "Verify a student can log in and attempt to order a meal.",
        "prerequisites": ["Application is running.", "Default student user exists."],
        "test_steps": [
            TestStep(1, "Navigate to login page and log in as a student.", "Redirected to user dashboard."),
            TestStep(2, "Select a cafeteria from the navigation.", "The menu for that cafeteria is displayed."),
            TestStep(3, "Add an item to the cart.", "The item appears in the cart summary."),
            TestStep(4, "Click 'Place Order'.", "The order is confirmed and user is redirected to order history."),
        ],
    },
    
    # --- Model Tests ---
    "test_menu_uniqueness_constraint_on_update": {
        "test_id": "MODEL_DB_001",
        "description": "Verify database uniqueness constraint for (cafeteria_id, menu_date) on update.",
        "test_scenario": "The system should prevent a menu from being updated to a date/cafeteria combination that already exists for another menu.",
        "test_steps": [
            TestStep(1, "Create Menu A for Cafeteria 1 on Date X.", "Menu is created."),
            TestStep(2, "Create Menu B for Cafeteria 2 on Date Y.", "Menu is created."),
            TestStep(3, "Attempt to update Menu B to Cafeteria 1 and Date X.", "The update operation must fail and return False due to the unique constraint violation."),
        ]
    },

    # --- Scenario Tests ---
    "test_complete_user_lifecycle": {
        "test_id": "SCEN_001",
        "description": "Test the full lifecycle of user management from creation to deletion at the model level.",
        "test_steps": [TestStep(1, "Execute create, update, and delete functions on the AppUser model.", "All model methods execute without error and reflect correct state changes in the database.")]
    },
}

# ==============================================================================
# 3. PARSING & DATA MERGING LOGIC
# ==============================================================================

def parse_and_merge_data(xml_file: str) -> List[TestCase]:
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

        case = TestCase(name=name, time=time, status=status, failure_details=failure_details)
        
        clean_name = name.split('[')[0]

        if clean_name in METADATA_REGISTRY:
            metadata = METADATA_REGISTRY[clean_name]
            case.has_metadata = True
            for key, value in metadata.items():
                if hasattr(case, key):
                    setattr(case, key, value)

        case.date_tested = datetime.fromisoformat(timestamp).strftime('%d-%b-%Y')
        
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
    # A much cleaner, key-value table for the header.
    header = f"""### {case.test_id}: {case.description}
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `{case.test_id}` |
| **Version** | `{case.version}` |
| **Tester** | `{case.tester_name}` |
| **Execution Time** | `{case.time:.4f}s` |
| **Date Tested** | `{case.date_tested}` |
| **Final Status** | **{case.status}** |
| **Test Function**| `{case.name}` |
"""
    
    prereqs = "\n".join([f"1. {p}" for p in case.prerequisites]) or "None"
    data = "\n".join([f"1. {d}" for d in case.test_data]) or "None"
    
    details_section = f"""
**Prerequisites:**
{prereqs}

**Test Scenario:**
{case.test_scenario or "N/A"}
"""

    steps_content = "*No detailed steps defined in metadata.*"
    if case.test_steps:
        steps_header = "| Step # | Step Details | Expected Results | Actual Results | Status |\n|:---:|:---|:---|:---|:---:|\n"
        steps_rows = "\n".join(
            [f"| {s.step_num} | {s.details} | {s.expected} | {s.actual} | **{s.status}** |" for s in case.test_steps]
        )
        steps_content = steps_header + steps_rows

    failure_block = ""
    if case.failure_details:
        details = case.failure_details.strip()
        failure_block = f"\n**Failure Details:**\n```\n{details}\n```\n"

    return f"{header}\n{details_section}\n**Test Steps:**\n{steps_content}\n{failure_block}\n---\n"


# ==============================================================================
# 5. MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JUnit XML to a clean Markdown test report.")
    parser.add_argument("input_xml", help="Path to the input JUnit XML file.")
    parser.add_argument("output_md", help="Path for the output Markdown file.")
    
    args = parser.parse_args()

    print(f"Parsing XML: {args.input_xml}...")
    all_cases = parse_and_merge_data(args.input_xml)
    
    if not all_cases:
        print("No test cases found. Exiting.")
    else:
        print(f"Found {len(all_cases)} test cases. Generating Markdown report...")
        
        # Filter for cases that have detailed metadata defined in the registry
        documented_cases = [case for case in all_cases if case.has_metadata]
        
        report_parts = [generate_summary(all_cases)]
        report_parts.append("## 📄 Detailed Test Case Results\n")
        
        if not documented_cases:
            report_parts.append("*No documented test cases with metadata were found.*")
        else:
            # Sort to show failures first, then by Test ID
            sorted_cases = sorted(documented_cases, key=lambda c: (c.status != 'Passed', c.test_id))
            for case in sorted_cases:
                report_parts.append(generate_detailed_case_markdown(case))
            
        final_report = "\n".join(report_parts)
        
        try:
            with open(args.output_md, "w", encoding="utf-8") as f:
                f.write(final_report)
            print(f"✅ Successfully generated clean report at: {args.output_md}")
        except IOError as e:
            print(f"Error: Could not write to output file '{args.output_md}'.\n{e}")