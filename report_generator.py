#!/usr/bin/env python3
"""
The New Cantina - Ultimate Test Report Generator
=================================================

A standalone Python script that automates the entire test reporting process.

Features:
  - Runs pytest locally (default) or in Docker (--docker).
  - Streams real-time test output.
  - Parses automated (XML) and manual (Excel) test results.
  - Conditionally renders report sections for a cleaner look.
  - Generates professional Markdown and PDF reports.

Default Usage (Local):
  python report_generator.py

Docker Usage:
  python report_generator.py --docker
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
try:
    import openpyxl
    from openpyxl.utils.exceptions import InvalidFileException
except ImportError:
    print("Error: 'openpyxl' is not installed. Please run: pip install openpyxl", file=sys.stderr)
    sys.exit(1)
# ==============================================================================
# 1. DATA MODELS & CONFIGURATION
# ==============================================================================
@dataclass
class TestStep:
    step_num: int
    details: str
    expected: str
    actual: str
    status: str
@dataclass
class TestCase:
    name: str
    status: str
    category: str
    test_id: str
    description: str
    time: float = 0.0
    failure_details: Optional[str] = None
    tester_name: str = "Automation"
    date_tested: str = ""
    prerequisites: List[str] = field(default_factory=list)
    test_scenario: str = ""
    test_steps: List[TestStep] = field(default_factory=list)
    has_metadata: bool = False
CATEGORY_MAP = {
    "MODEL_": ("Model & Unit Tests", 1),
    "API_":   ("API Tests", 2),
    "E2E_":   ("End-to-End (E2E) Tests", 3),
    "SCEN_":  ("Scenario & Integration Tests", 4),
}
METADATA_REGISTRY: Dict[str, Dict] = {
    "tests.test-python.models.test_app_user.test_create_user": { "test_id": "MODEL_USER_001", "description": "Verify AppUser model can create a user with a hashed password.", "test_scenario": "The create_user class method should correctly instantiate a user, hash their password, and add them to the database session."},
    "tests.test-python.models.test_dish.test_dish_delete_fails_if_in_use_by_menu_item": { "test_id": "MODEL_DB_004", "description": "Verify a dish cannot be deleted if referenced by a DailyMenuItem." },
    "tests.test-python.controller.test_api_auth.test_user_api_permissions": { "test_id": "API_SEC_001", "description": "Verify API permissions for a standard authenticated (non-admin) user across multiple endpoints." },
    "tests.test-python.controller.test_api_no_auth.test_api_unauthenticated_access_is_denied": { "test_id": "API_SEC_002", "description": "Verify that unauthenticated API access is denied for all protected endpoints." },
    "tests.test-python.selenium-e2e.test_loginAdminLogOut.TestLoginAdminLogOut.test_loginAdminLogOut": { "test_id": "E2E_AUTH_001", "description": "E2E test to verify admin login and logout functionality through the UI." },
    "tests.test-python.selenium-e2e.test_orderfoodinthepast.TestOrderfoodinthepast.test_orderfoodinthepast": { "test_id": "E2E_ORDER_001", "description": "E2E test simulating a student ordering food." },
    "tests.test-python.selenium-e2e.test_combined_scenarios.TestSystemIntegrationScenario.test_full_system_integration": { "test_id": "SCEN_INT_001", "description": "Test the full system integration by combining model and API tests in a realistic sequence." },
    "tests.test-python.selenium-e2e.test_student_order_history.TestStudentOrderHistory.test_student_filter_order_history": {"test_id": "E2E_HISTORY_001", "description": "E2E test for a student filtering their order history by month."},
    "tests.test-python.selenium-e2e.test_student_top_up_balance.TestTopUpUserBalance.test_topUpUserBalance": {"test_id": "E2E_BALANCE_001", "description": "E2E test for a student topping up their account balance."},
    "tests.test-python.selenium-e2e.test_admin_cafeteria_management.TestAdminCafeteriaManagement.test_admin_full_cafeteria_lifecycle": { "test_id": "E2E_ADMIN_CAFE_001", "description": "E2E test for the full admin workflow of creating and deleting a cafeteria." },
    "tests.test-python.selenium-e2e.test_admin_menu_management.TestAdminMenuManagement.test_admin_full_menu_lifecycle": { "test_id": "E2E_ADMIN_MENU_001", "description": "E2E test for an admin creating a complex daily menu for a future date." },
    "tests.test-python.selenium-e2e.test_admin_user_management.TestAdminUserManagement.test_admin_full_user_lifecycle": { "test_id": "E2E_ADMIN_USER_001", "description": "E2E test for an admin creating, searching for, and deleting a user." },
    "tests.test-python.models.test_daily_menu.test_menu_uniqueness_constraint_on_update": { "test_id": "MODEL_DB_001", "description": "Verify database uniqueness constraint for (cafeteria_id, menu_date) on update." },
    # FIXED: Added missing metadata for failed tests from pytest_results.xml
    "tests.test-python.models.test_daily_menu_item.test_update_menu_item_with_no_data": { "test_id": "MODEL_MENUITEM_004", "description": "Verify update_menu_item() with no arguments returns False." },
    "tests.test-python.models.test_daily_menu_item.test_get_all_menu_items_as_dicts": { "test_id": "MODEL_MENUITEM_005", "description": "Verify get_all_dicts for DailyMenuItem returns all records." },
}
# ==============================================================================
# 2. CORE LOGIC
# ==============================================================================
def run_tests(use_docker: bool, xml_output_path: str) -> bool:
    if use_docker: return run_tests_in_docker(xml_output_path)
    return run_tests_locally(xml_output_path)
def _stream_process_output(process):
    print("-" * 60)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
    print("-" * 60)
    process.stdout.close()
    return process.wait()
def run_tests_locally(xml_output_path: str) -> bool:
    print("STEP 1: Running tests locally (with real-time output)...")
    if not shutil.which("pytest"):
        print("Error: 'pytest' not found. Please install it (`pip install pytest`).", file=sys.stderr)
        return False
    command = ["pytest", "-v", f"--junitxml={xml_output_path}"]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1)
        return_code = _stream_process_output(process)
        if return_code not in [0, 1]: print(f"Warning: Pytest exited with code {return_code}.", file=sys.stderr)
        print(f"✅ Tests completed. Results saved to '{xml_output_path}'.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred while running local tests: {e}", file=sys.stderr)
        return False
def run_tests_in_docker(xml_output_path: str) -> bool:
    print("STEP 1: Running tests inside Docker container (with real-time output)...")
    docker_compose_file = os.path.join("docker", "docker-compose.yml")
    if not os.path.exists(docker_compose_file):
        print(f"Error: Docker Compose file not found at '{docker_compose_file}'.", file=sys.stderr)
        return False
    command = ["docker", "compose", "-f", docker_compose_file, "exec", "-T", "python-app", "pytest", "-v", f"--junitxml={xml_output_path}"]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1)
        return_code = _stream_process_output(process)
        if return_code not in [0, 1]: print(f"Warning: Docker Pytest exited with code {return_code}.", file=sys.stderr)
        print(f"✅ Tests completed. Results saved to '{xml_output_path}'.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred while running Docker command: {e}", file=sys.stderr)
        return False
def parse_automated_tests(xml_file: str) -> List[TestCase]:
    print(f"STEP 2: Parsing automated tests from '{xml_file}'...")
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        suite_element = root.find('testsuite')
    except (ET.ParseError, FileNotFoundError, AttributeError) as e:
        print(f"Error: Could not parse '{xml_file}'.\nDetails: {e}", file=sys.stderr)
        sys.exit(1)
    auto_populate_registry(suite_element)
    timestamp_str = suite_element.get('timestamp', datetime.now().isoformat())
    date_tested = datetime.fromisoformat(timestamp_str).strftime('%d-%b-%Y')
    all_cases = []
    for case_element in suite_element.findall('testcase'):
        classname = case_element.get('classname', 'unknown.suite')
        name = case_element.get('name', 'Unknown Test')
        time = float(case_element.get('time', '0'))
        base_name = name.split('[')[0]
        registry_key = f"{classname}.{base_name}"
        status, failure_details = 'Passed', None
        if case_element.find('failure') is not None:
            status, failure_details = 'Failed', case_element.find('failure').text
        elif case_element.find('error') is not None:
            status, failure_details = 'Failed', case_element.find('error').text
        elif case_element.find('skipped') is not None:
            status = 'Skipped'
        metadata = METADATA_REGISTRY.get(registry_key, {})
        test_id = metadata.get("test_id", "") or re.sub(r'[^A-Z0-9_]', '', base_name.upper())
        case = TestCase(name=name, status=status, time=time, failure_details=failure_details, date_tested=date_tested, test_id=test_id, description=metadata.get("description", "No description provided."), test_scenario=metadata.get("test_scenario", ""), has_metadata=bool(metadata.get("test_id")), category="Uncategorized")
        for prefix, (category_name, _) in CATEGORY_MAP.items():
            if case.test_id.startswith(prefix):
                case.category = category_name
                break
        all_cases.append(case)
    print(f"✅ Parsed {len(all_cases)} automated test results.")
    return all_cases

def parse_manual_tests(excel_file: Optional[str]) -> List[TestCase]:
    if not excel_file: return []
    print(f"STEP 3: Parsing manual tests from '{excel_file}'...")
    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
    except FileNotFoundError:
        print(f"Info: Manual test file '{excel_file}' not found. Skipping manual tests.")
        return []
    except InvalidFileException as e:
        print(f"Warning: Could not open or parse '{excel_file}'. Skipping.\nDetails: {e}", file=sys.stderr)
        return []

    if "Test Summary" not in wb.sheetnames:
        print("Warning: 'Test Summary' sheet not found in the Excel file. Skipping manual tests.", file=sys.stderr)
        return []

    summary_ws, manual_cases = wb["Test Summary"], []
    header = [cell.value for cell in summary_ws[1] if cell.value]
    required_cols = ["Test ID", "Title", "Status", "Assigned To", "Date Tested"]
    if not all(col in header for col in required_cols):
        print(f"Warning: Excel 'Test Summary' sheet is missing required columns: {required_cols}. Skipping.", file=sys.stderr)
        return []

    col_map = {name: i for i, name in enumerate(header)}

    for row in summary_ws.iter_rows(min_row=2, values_only=True):
        test_id = row[col_map["Test ID"]]
        if not test_id or test_id not in wb.sheetnames:
            if test_id: print(f"Warning: Test ID '{test_id}' in summary has no matching sheet. Skipping.", file=sys.stderr)
            continue

        ws = wb[test_id]

        # Helper function to handle merged cells
        def get_cell_value(coord):
            try:
                cell = ws[coord]
                if isinstance(cell, openpyxl.cell.cell.MergedCell):
                    for mr in ws.merged_cells.ranges:
                        if cell.coordinate in mr: return ws.cell(row=mr.min_row, column=mr.min_col).value
                return cell.value
            except (KeyError, IndexError):
                return None

        # FIXED: Corrected cell coordinates to match create_test_template.py
        # Prioritize data from the detail sheet with fallbacks to the summary sheet
        dt_val = get_cell_value('F5') or row[col_map["Date Tested"]]
        date_tested = dt_val.strftime('%Y-%m-%d') if isinstance(dt_val, datetime) else str(dt_val or '')

        tester_name = get_cell_value('C5') or row[col_map["Assigned To"]]
        
        # In create_test_template.py, the description value is ultimately written to D1.
        # However, the original report suggests this may have failed.
        # We'll read from D1, but use a fallback to G1 for robustness, as G1 also holds the value.
        description = get_cell_value('D1') or get_cell_value('G1') or ""

        # Extract prerequisites from cells B8 to B12
        prerequisites = [p for r in range(8, 13) if (p := get_cell_value(f'B{r}'))]

        # Extract test steps from rows 16 to 25
        steps = []
        for i in range(16, 26):
            if get_cell_value(f'A{i}') or get_cell_value(f'B{i}'): # Process if step # or details exist
                steps.append(TestStep(
                    step_num=get_cell_value(f'A{i}'),
                    details=get_cell_value(f'B{i}'),
                    expected=get_cell_value(f'E{i}'),
                    actual=get_cell_value(f'G{i}'),
                    status=str(get_cell_value(f'J{i}') or "").title()
                ))

        manual_cases.append(TestCase(
            name=row[col_map["Title"]],  # Canonical title comes from the summary sheet
            status=str(row[col_map["Status"]] or "Draft").title(),
            category="Manual Tests",
            test_id=test_id,
            description=description,
            test_scenario=get_cell_value('C13') or "",
            tester_name=tester_name,
            date_tested=date_tested,
            prerequisites=prerequisites,
            test_steps=steps,
            has_metadata=True
        ))

    if manual_cases:
        print(f"✅ Parsed {len(manual_cases)} manual test cases.")
    return manual_cases

def generate_markdown_report(template_path: str, all_cases: List[TestCase], automated_cases: List[TestCase], manual_cases: List[TestCase]) -> str:
    print("STEP 4: Generating Markdown report content...")
    try:
        with open(template_path, "r", encoding="utf-8") as f: content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at '{template_path}'.", file=sys.stderr)
        sys.exit(1)
    summary_md, failed_summary_md = generate_global_summary_table(all_cases), generate_failed_tests_summary(all_cases)
    automated_annex_md, manual_annex_md = generate_automated_annex(automated_cases), generate_manual_annex(manual_cases)
    content = content.replace("%%TEST_SUMMARY%%", summary_md)
    content = content.replace("%%FAILED_TESTS_SUMMARY%%", failed_summary_md)
    content = content.replace("%%TEST_ANNEX%%", f"{automated_annex_md}\n\n{manual_annex_md}")
    print("✅ Markdown content generated.")
    return content
def export_to_pdf(md_input_path: str, pdf_output_path: str) -> bool:
    if not shutil.which("pandoc"):
        print("Error: 'pandoc' not found. Install from https://pandoc.org/installing.html", file=sys.stderr)
        return False
    if not shutil.which("pdflatex"):
        print("Warning: 'pdflatex' not found. PDF may fail. Install a LaTeX distribution.", file=sys.stderr)
    print(f"STEP 5: Exporting report to PDF at '{pdf_output_path}'...")
    command = ["pandoc", md_input_path, "-o", pdf_output_path, "--from=markdown", "--pdf-engine=pdflatex", "--toc", "--number-sections", "--number-offset=-1", "-V", "geometry:a4paper,margin=1in", "-V", "colorlinks", "-V", "urlcolor=blue"]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"✅ PDF report successfully created at '{pdf_output_path}'.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Pandoc failed. Exit Code: {e.returncode}\n--- Pandoc STDERR ---\n{e.stderr}", file=sys.stderr)
        return False
# ==============================================================================
# 3. HELPER & UTILITY FUNCTIONS
# ==============================================================================
def auto_populate_registry(suite_element: ET.Element):
    found_keys = {f"{case.get('classname', '')}.{case.get('name', '').split('[')[0]}" for case in suite_element.findall('testcase') if case.get('classname') and case.get('name')}
    missing_keys = found_keys - set(METADATA_REGISTRY.keys())
    if missing_keys:
        print(f"Info: Found {len(missing_keys)} undocumented tests. Adding them to the report.")
        for key in missing_keys: METADATA_REGISTRY[key] = {}
def create_anchor_id(test_id: str) -> str: return f"test-case-{re.sub(r'[^a-z0-9]+', '-', test_id.lower()).strip('-')}"
def generate_global_summary_table(all_cases: List[TestCase]) -> str:
    stats = defaultdict(lambda: defaultdict(int))
    for case in all_cases: stats[case.category]['total'] += 1; stats[case.category][case.status.lower()] += 1
    rows, total_stats = [], defaultdict(int)
    sorted_categories = sorted([cat for cat in stats.keys() if cat not in ["Manual Tests", "Uncategorized"]], key=lambda cat: next((c[1] for _, c in CATEGORY_MAP.items() if c[0] == cat), 99))
    if "Uncategorized" in stats: sorted_categories.append("Uncategorized")
    if "Manual Tests" in stats: sorted_categories.append("Manual Tests")
    for category in sorted_categories:
        s = stats[category]; total, passed, failed, skipped = s['total'], s.get('passed', 0), s.get('failed', 0), s.get('skipped', 0)
        total_stats['total'] += total; total_stats['passed'] += passed; total_stats['failed'] += failed; total_stats['skipped'] += skipped
        pass_rate = (passed / (total - skipped) * 100) if (total - skipped) > 0 else 0
        rows.append(f"| {category} | {total} | {passed} | {failed} | {skipped} | {pass_rate:.1f}% |")
    total_pass_rate = (total_stats['passed'] / (total_stats['total'] - total_stats['skipped']) * 100) if (total_stats['total'] - total_stats['skipped']) > 0 else 0
    total_row = f"| **Total** | **{total_stats['total']}** | **{total_stats['passed']}** | **{total_stats['failed']}** | **{total_stats['skipped']}** | **{total_pass_rate:.1f}%** |"
    return f"| Test Category | Total | Passed | Failed | Skipped | Pass Rate |\n| :--- | :---: | :---: | :---: | :---: | :---: |\n" + "\n".join(rows) + "\n|---|---|---|---|---|---|\n" + total_row
def generate_failed_tests_summary(all_cases: List[TestCase]) -> str:
    failed_cases = [c for c in all_cases if c.status.lower() in ('failed', 'error', 'fail')]
    if not failed_cases: return "Congratulations! All tests passed. No failures to report."
    rows = [f"| `{c.test_id}` | {c.description} | {c.category} | [See Details](#{create_anchor_id(c.test_id)}) |" for c in sorted(failed_cases, key=lambda c: c.test_id)]
    return f"| Test ID | Description | Category | Details |\n| :--- | :--------------------------------- | :--- | :---: |\n" + "\n".join(rows)
def generate_automated_annex(cases: List[TestCase]) -> str:
    if not cases: return "## Annex A: Automated Test Execution Details\n\nNo automated tests were run."
    total, passed, failed, skipped = len(cases), sum(1 for c in cases if c.status == 'Passed'), sum(1 for c in cases if c.status == 'Failed'), sum(1 for c in cases if c.status == 'Skipped')
    summary_table = f"\n| Metric | Value |\n|---|---|\n| **Total Automated Tests** | {total} |\n| Passed | {passed} |\n| Failed/Error | {failed} |\n| Skipped | {skipped} |\n"
    categorized_cases = defaultdict(list)
    for case in cases: categorized_cases[case.category].append(case)
    report_parts = ["## Annex A: Automated Test Execution Details", summary_table]
    sorted_categories = sorted(categorized_cases.keys(), key=lambda cat: next((c[1] for _, c in CATEGORY_MAP.items() if c[0] == cat), 99) if cat != "Uncategorized" else 100)
    for category_name in sorted_categories:
        report_parts.append(f"\n### {category_name}\n")
        grouped = defaultdict(list)
        for case in categorized_cases[category_name]: grouped[case.name.split('[')[0]].append(case)
        for key in sorted(grouped.keys()):
            runs = grouped[key]
            case = runs[0]
            if len(runs) > 1:
                final_status = 'Passed'
                failures = [f"--- FAILED PARAMETER: `{run.name}` ---\n{run.failure_details.strip()}" for run in runs if run.status == 'Failed' and run.failure_details]
                if failures: final_status = 'Failed'
                case.status, case.name, case.time, case.failure_details = final_status, f"{key} (x{len(runs)} params)", sum(r.time for r in runs), "\n\n".join(failures) if failures else None
            report_parts.append(generate_single_automated_case_md(case))
    return "\n".join(report_parts)
def generate_manual_annex(cases: List[TestCase]) -> str:
    if not cases: return "## Annex B: Manual Test Execution Details\n\nNo manual tests were provided."
    report_parts = ["## Annex B: Manual Test Execution Details"]
    for case in sorted(cases, key=lambda c: c.test_id):
        anchor_id = create_anchor_id(case.test_id)
        header = f"\n#### <a id=\"{anchor_id}\"></a>Manual Test Case: {case.test_id}\n\n| Attribute | Value |\n| :--- | :--- |\n| **Test Case ID** | `{case.test_id}` |\n| **Title** | {case.name} |\n| **Description** | {case.description} |\n| **Tester** | {case.tester_name} |\n| **Date Tested** | {case.date_tested} |"
        prereqs_section = f"\n**Prerequisites:**\n" + "\n".join([f"1.  {p}" for p in case.prerequisites]) if case.prerequisites else ""
        steps_section = f"\n\n**Test Steps:**\n| Step # | Action | Expected Result | Actual Result | Status |\n| :--- | :---------------------- | :---------------------- | :---------------------- | :--- |\n" + "\n".join([f"| {s.step_num} | {s.details} | {s.expected} | {s.actual or ''} | {s.status} |" for s in case.test_steps]) if case.test_steps else ""
        final_status = str(case.status).upper() if case.status and case.status.lower() not in ('none', '') else 'NOT EXECUTED'
        report_parts.append(f"{header}{prereqs_section}{steps_section}\n\n**Final Result:** **{final_status.upper()}**\n\n---")
    return "\n".join(report_parts)
def generate_single_automated_case_md(case: TestCase) -> str:
    """Formats a single automated TestCase, omitting empty sections."""
    anchor_id = create_anchor_id(case.test_id)
    header = f"\n#### <a id=\"{anchor_id}\"></a>{case.test_id}: {case.description}\n| Attribute | Value |\n| :--- | :--- |\n| **Test Case ID** | `{case.test_id}` |\n| **Version** | `1.0` |\n| **Tester** | `{case.tester_name}` |\n| **Execution Time** | `{case.time:.4f}s` |\n| **Date Tested** | `{case.date_tested}` |\n| **Final Status** | **{case.status}** |\n| **Test Function**| `{case.name}` |"
    # Conditional sections
    prereqs_section = f"\n\n**Prerequisites:**\n" + "\n".join([f"1. {p}" for p in case.prerequisites]) if case.prerequisites else ""
    scenario_section = f"\n\n**Test Scenario:**\n{case.test_scenario}" if case.test_scenario else ""

    # MODIFIED: Conditionally generate the entire steps section
    steps_section = ""
    if case.test_steps:
        steps_table = ("| Step # | Action | Expected Result | Actual Result | Status |\n|:---:|:---:|:---:|:---:|:---:|\n" +
                       "\n".join([f"| {s.step_num} | {s.details} | {s.expected} | {s.actual} | {s.status} |" for s in case.test_steps]))
        steps_section = f"\n\n**Test Steps:**\n{steps_table}"

    failure_block = f"\n\n**Failure Details:**\n```\n{case.failure_details.strip()}\n```" if case.failure_details else ""
    return f"{header}{prereqs_section}{scenario_section}{steps_section}{failure_block}\n\n---"
# ==============================================================================
# 5. MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The New Cantina - Ultimate Test Report Generator.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--docker", action="store_true", help="Run tests inside the Docker container instead of locally.")
    parser.add_argument("--no-run-tests", action="store_true", help="Skip running tests and use an existing XML file.")
    parser.add_argument("--xml-file", default="tests_results.xml", help="Path to the JUnit XML file (to use or to be created).")
    parser.add_argument("--manual-tests-excel", default="Comprehensive_Test_Report.xlsx", help="Optional path to an Excel file with manual test cases. Defaults to 'Comprehensive_Test_Report.xlsx'.")
    parser.add_argument("--template", default="main_documentation_template.md", help="Path to the Markdown template file.")
    parser.add_argument("--output-md", default="Complete_Testing_Report.md", help="Path for the final output Markdown file.")
    parser.add_argument("--output-pdf", help="Optional: Path to export the final report as a PDF.")
    args = parser.parse_args()
    if not args.no_run_tests:
        run_tests(use_docker=args.docker, xml_output_path=args.xml_file)
    automated_cases = parse_automated_tests(args.xml_file)
    manual_cases = parse_manual_tests(args.manual_tests_excel)
    all_cases = automated_cases + manual_cases
    final_markdown = generate_markdown_report(args.template, all_cases, automated_cases, manual_cases)
    try:
        with open(args.output_md, "w", encoding="utf-8") as f: f.write(final_markdown)
        print(f"✅ Successfully generated Markdown report at: {args.output_md}")
    except IOError as e:
        print(f"Error: Could not write to output file '{args.output_md}'.\n{e}", file=sys.stderr)
        sys.exit(1)
    if args.output_pdf:
        export_to_pdf(args.output_md, args.output_pdf)
    undocumented_count = sum(1 for k, v in METADATA_REGISTRY.items() if not v)
    if undocumented_count > 0:
        print(f"\n💡 FYI: {undocumented_count} automated tests ran but are not documented in the script's METADATA_REGISTRY.")
        print("   They will appear in the 'Uncategorized' section.")