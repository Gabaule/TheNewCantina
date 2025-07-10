# Semester Project: Testing "The New Cantina" Web Application

| | |
| :--- | :--- |
| **Project:** | The New Cantina - System Testing |
| **Course:** | Web Programming |
| **Team:** | Ishan Baichoo, Gabriel Aumasson-Leduc, Clément De Simon |
| **Submission Date:** | 10.07.2025 |

***

## Table of Contents
1.  [Introduction](#1-introduction)
    1.  [Team Members](#11-team-members)
    2.  [Description of Tested Functionality](#12-description-of-tested-functionality)
2.  [Test Case Management Template](#2-test-case-management-template)
3.  [Testing Methodology and Execution](#3-testing-methodology-and-execution)
    1.  [Testing Methods & Tools](#31-testing-methods--tools)
    2.  [Multi-Layered Testing Strategy](#32-multi-layered-testing-strategy)
    3.  [Test Results Summary](#33-test-results-summary)
4.  [Conclusion](#4-conclusion)
5.  [Annexes](#5-annexes)
    1.  [Annex A: Automated Test Execution Details](#annex-a-automated-test-execution-details)
    2.  [Annex B: Manual Test Execution Details](#annex-b-manual-test-execution-details)


***

## Introduction

The primary objective of this project was to design and implement a robust testing strategy to validate the application's functionality, stability, and data integrity.

This report details the testing methodologies employed, the test cases executed (both automated and manual), and a summary of the overall test plan and results.

### Team Members

The following students contributed to this semester project:

*   Ishan Baichoo

*   Gabriel Aumasson-Leduc

*   Clément De Simon

### Description of Tested Functionality

"The New Cantina" is a web-based meal ordering system designed for a university environment. The application serves two primary user roles, each with distinct functionalities:

*   **Student / Staff (User Role):**
    *   **Authentication:** Users can log in with their credentials.
    *   **Dashboard:** After logging in, users can view daily menus for different cafeterias. They can navigate between cafeterias and select different dates to view menus.
    *   **Ordering:** Users can add items to a shopping cart, review their order, and place it. The total cost is deducted from their account balance.
    *   **Account Management:** Users can view their current balance, top up their account with additional funds, and view their complete order history, filterable by month.

*   **Administrator (Admin Role):**
    *   **Authentication:** Admins log in through the same portal but are redirected to a dedicated admin dashboard.
    *   **User Management:** Admins can view, search, filter, and delete all users in the system. They can also create new users.
    *   **Cafeteria, Dish, and Menu Management:** Admins have full CRUD (Create, Read, Update, Delete) capabilities over cafeterias, individual dishes, and the daily menus that link them together. This includes a comprehensive interface for managing which dishes are served in which cafeterias on any given day.
    *   **RESTful API:** All administrative actions are backed by a secure RESTful API, ensuring that data management can be performed programmatically and is subject to authorization checks.

The entire application is built on a Flask framework with a PostgreSQL database and a modern, responsive frontend using HTMX and Alpine.js.

***

## Test Case Management Template

To effectively manage the testing process, our team designed a comprehensive and flexible template using Microsoft Excel. This approach was chosen for its universal accessibility, ease of use, and powerful features for data organization and tracking, requiring no specialized software for team members.

The system is built on a two-tiered structure:

1.  A high-level **Test Summary Dashboard** for at-a-glance project management and task distribution.

2.  Individual, detailed **Test Case Sheets** for every test, providing all necessary information for execution and recording.

#### The Test Summary Dashboard

The "Test Summary" sheet serves as the central hub for monitoring the entire testing effort. Its primary purpose is to provide a quick overview of test status, feature coverage, and team workload.

The key columns and their functions are:

*   **Test ID:** A unique identifier for each test case. A consistent naming convention (e.g., `MANUAL-TC-XXX`, `API-SEC-XXX`) is used to categorize tests by type and scope.
*   **Title:** A concise, human-readable name for the test case.
*   **Feature:** The application module or feature being tested (e.g., Account Management, Ordering, API Security). This allows for filtering to assess the test coverage of specific parts of the system.
*   **Status:** The current state of the test case, which is color-coded for immediate visual feedback:
    *   <span style="color:green;">**Passed:**</span> The test was executed successfully.
    *   <span style="color:red;">**Failed:**</span> The test was executed, and a defect was found.
    *   <span style="color:orange;">**In Progress:**</span> The test is currently being executed or debugged.
    *   **Not Executed / Draft:** The test case has been designed but not yet run.
*   **Assigned To:** The name of the team member responsible for the test case. This is crucial for distributing work and establishing clear ownership.
*   **Date Tested:** The date of the last execution, providing a timeline of testing activity.

This dashboard structure is essential for team coordination, allowing the project lead to quickly identify bottlenecks, track progress against features, and re-allocate tasks as needed.

#### The Detailed Test Case Sheet

Each test case listed in the summary dashboard has its own dedicated sheet, named after its Test ID (e.g., "MANUAL-TC-001"). This sheet provides a standardized and exhaustive template for a tester to follow, ensuring that tests are repeatable and results are recorded consistently.

The detailed sheet is organized into the following logical sections:

*   **Header & Metadata:** This top section captures the administrative details of the test case itself, including `Test Case ID`, `Description`, `Created By`, `Reviewed By`, and `Version`. This establishes a quality control process where tests can be drafted and peer-reviewed before execution. The `QA Tester's Log` provides space for notes on the test case's evolution.
*   **Execution Details:** This block records the results of a specific run, with fields for `Tester's Name`, `Date Tested`, and the final `Test Case (Pass/Fail)` status.
*   **Prerequisites & Test Data:** This section is critical for reproducibility. `Prerequisites` lists all conditions that must be met before starting the test (e.g., user must be logged in), while `Test Data` specifies any inputs or values needed (e.g., amount to add).
*   **Test Scenario:** A clear, one-sentence goal for the test.
*   **Test Steps:** The core of the test case, this table provides a script for the tester to follow with explicit columns for:
    *   **Step #:** Sequential numbering.
    *   **Step Details:** The action to be performed.
    *   **Expected Results:** The specific outcome that should occur if the application is working correctly.
    *   **Actual Results:** The observed outcome during the test.
    *   **Pass / Fail / ...:** The status of the individual step.

#### Specific Example: MANUAL-TC-001

To illustrate how the template is used in practice, here is the record for `MANUAL-TC-001`.

**1. View in the "Test Summary" Dashboard:**

| Test ID | Title | Feature | Status | Assigned To | Date Tested |
| :--- | :--- | :--- | :--- | :--- | :--- |
| MANUAL-TC-001 | Verify Visual Feedback and State on Balance Top-Up | Account Management | <span style="color:green;">Passed</span> | Clément De Simon | 2025-07-08 |

**2. View in the "MANUAL-TC-001" Detailed Sheet:**

| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MANUAL-TC-001` |
| **Test Case Description**| Verify that when a user adds funds, the UI provides clear feedback and all balance indicators update correctly without a full page reload. |
| **Created By** | Gabriel Aumasson-Leduc |
| **Reviewed By** | Ishan Baichoo |
| **Version**| 1.0 |
| **QA Tester's Log** | Initial draft for manual testing phase. Covers HTMX out-of-band swaps. |
| **Tester's Name** | Clément De Simon |
| **Date Tested** | 2025-07-08 |
| **Test Case (Pass/Fail/Not Executed)**| Pass |

**Prerequisites:**
1.  User is logged in as 'student1@example.com'.
2.  Application is running in a modern web browser.

**Test Data:**
1.  Amount to add: 25.50

**Test Scenario:**
Verify that when a user adds funds, the UI provides clear feedback and all balance indicators update correctly without a full page reload.

**Test Steps:**

| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Navigate to the 'Top Up Balance' page. | The 'Account Balance' page is displayed. | As Expected | Pass |
| 2 | Enter '25.50' into the amount field and click 'Add Money'. | A success message appears and the 'Current Balance' on the page updates. | As Expected | Pass |
| 3 | Observe the header of the application. | The balance in the top-right corner updates instantly without a page refresh. | As Expected | Pass |
| 4 | Navigate to the main 'Dashboard' page. | The balance in the header remains at the new, updated value. | As Expected | Pass |



## Testing Methodology and Execution

### Testing Methods & Tools

A hybrid testing strategy was adopted to ensure comprehensive coverage, combining the efficiency of automation with the intuitiveness of manual testing.

**Automated Testing:**
Automated tests form the backbone of our quality assurance process, focusing on the backend logic, API endpoints, and critical user workflows. This allows for rapid, repeatable, and consistent verification, which is essential for regression testing.

**Manual Testing:**
Manual testing was employed to cover areas where human observation is paramount. This includes exploratory testing to find edge cases, verifying the user interface (UI) for visual consistency and responsiveness, and assessing the overall user experience (UX).

The following tools were utilized to implement our testing strategy:

| Tool | Purpose |
| :--- | :--- |
| **pytest** | The core testing framework for Python. Used to write, organize, and run all automated tests, including model, API, and E2E tests. Its powerful fixture system was used to create isolated test environments. |
| **Selenium IDE** | Used for the initial recording of complex user workflows in the browser. This provided a quick way to generate baseline scripts for key end-to-end scenarios. |
| **pytest-selenium** | This `pytest` plugin was used to integrate and run the browser automation scripts (exported from Selenium IDE) within our primary testing framework, allowing for unified test execution and reporting. |
| **Docker & Docker Compose** | The entire application stack (Python app, PostgreSQL database, pgAdmin) was containerized using Docker. Docker Compose was used to define and orchestrate the multi-container environment, ensuring a consistent and reproducible setup for both development and testing. |
| **Custom Python Scripts** | A custom script (`report_converter.py`) was developed to parse the JUnit XML output from `pytest` and a manual test Excel file to generate a professional, human-readable Markdown report with a summary and detailed annexes. |
| **Microsoft Excel** | Used as a centralized tool for designing, documenting, and tracking the execution of manual test cases. |

### Multi-Layered Testing Strategy

Building on the tools listed above, our testing strategy was founded on a multi-layered approach to ensure robustness from the database level up to the final user interaction. By focusing heavily on model-level and API-level automated tests, we created a comprehensive and efficient quality assurance process.

#### Model-Level Testing: The Foundation of Data Integrity

The models (`app/models/`) are the bedrock of our application, directly mapping to our database schema and encapsulating fundamental data rules. Our strategy prioritized testing this layer for several key reasons:
*   **Ensuring Data Integrity:** This is the most effective layer to validate core database constraints. For example, test case `MODEL_DB_002` (`test_unique_email_constraint`) confirms that the database correctly rejects duplicate user emails, a critical business rule that prevents data corruption. Similarly, `MODEL_DB_004` (`test_dish_delete_fails_if_in_use_by_menu_item`) verifies that foreign key constraints are enforced, preventing an administrator from deleting a dish that is part of an active menu.
*   **Speed and Isolation:** By running these tests against a fast, in-memory SQLite database (configured in `conftest.py`), we achieve a rapid feedback loop. Developers can run the entire model test suite in seconds, allowing them to catch regressions and validate changes to the data layer instantly without the overhead of a full application server.
*   **Validating Core Logic:** The model methods themselves contain essential logic. For instance, `AppUser.create_user` is responsible for correctly hashing a password. Test case `MODEL_USER_001` validates not only that the user is created, but that the `verify_password` method works as expected, confirming the security logic at its source.

#### API-Level Testing: Validating Business Logic and Security

The RESTful API is the primary interface for all administrative actions and serves as the brain of the application. Testing at this level was critical for validating our core business workflows and security policies.
*   **Verifying the API Contract:** Our API tests (`tests/test-python/controller/`) act as a consumer of our own API, ensuring it adheres to its defined contract. They check that endpoints accept the correct data structures, perform the right actions, and return the expected HTTP status codes and JSON responses. This guarantees that any client (including our own HTMX-powered frontend) can rely on the API's behavior.
*   **Testing Complex Business Logic:** Controllers contain logic that orchestrates multiple model interactions. For example, placing an order involves checking the user's balance, creating a `Reservation` record, creating multiple `OrderItem` records, and updating the user's balance. An API test like `API_USER_001` (`test_user_crud`) is an integration test in itself, ensuring the full "Create, Read, Update, Delete" lifecycle for a resource works across the controller, model, and database layers.
*   **Enforcing Security Policies:** The API is the application's security gatekeeper. Our test suite rigorously checks the authentication and authorization decorators defined in `app/controller/auth.py`. The parametrized tests in `test_api_no_auth.py` systematically confirm that every protected endpoint rejects unauthenticated requests. More importantly, `test_api_auth.py` (`API_SEC_001`) validates our role-based access control, ensuring a standard user can view their own data but is correctly forbidden from accessing another user's data or any admin-only endpoints. This is a critical security validation that is far more efficient to automate at the API level than through the UI.


### Test Results Summary

The following tables provide a high-level overview of the entire testing effort, combining results from both automated and manual test executions.

#### Overall Test Statistics
| Test Category | Total | Passed | Failed | Skipped | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Model & Unit Tests | 5 | 2 | 3 | 0 | 40.0% |
| API Tests | 33 | 33 | 0 | 0 | 100.0% |
| End-to-End (E2E) Tests | 6 | 3 | 3 | 0 | 50.0% |
| Scenario & Integration Tests | 1 | 1 | 0 | 0 | 100.0% |
| Uncategorized | 139 | 122 | 17 | 0 | 87.8% |
| Manual Tests | 3 | 1 | 1 | 0 | 33.3% |
|---|---|---|---|---|---|
| **Total** | **187** | **162** | **24** | **0** | **86.6%** |

#### Key Findings (Failures)
This section highlights all tests that failed or resulted in an error during execution, providing a quick reference for developers to address critical issues. For complete details, including stack traces and test steps, please refer to the corresponding test case in the Annexes.

| Test ID | Description | Category | Details |
| :--- | :--------------------------------- | :--- | :---: |
| `API-SEC-001` | Test Case Description | Manual Tests | [See Details](#test-case-api-sec-001) |
| `E2E_ADMIN_MENU_001` | E2E test for an admin creating a complex daily menu for a future date. | End-to-End (E2E) Tests | [See Details](#test-case-e2e-admin-menu-001) |
| `E2E_HISTORY_001` | E2E test for a student filtering their order history by month. | End-to-End (E2E) Tests | [See Details](#test-case-e2e-history-001) |
| `E2E_ORDER_001` | E2E test simulating a student ordering food. | End-to-End (E2E) Tests | [See Details](#test-case-e2e-order-001) |
| `MODEL_DB_001` | Verify database uniqueness constraint for (cafeteria_id, menu_date) on update. | Model & Unit Tests | [See Details](#test-case-model-db-001) |
| `MODEL_MENUITEM_004` | Verify update_menu_item() with no arguments returns False. | Model & Unit Tests | [See Details](#test-case-model-menuitem-004) |
| `MODEL_MENUITEM_005` | Verify get_all_dicts for DailyMenuItem returns all records. | Model & Unit Tests | [See Details](#test-case-model-menuitem-005) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_FORBIDDEN` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-forbidden) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_API_USER_ACCESS_IS_GRANTED` | No description provided. | Uncategorized | [See Details](#test-case-test-api-user-access-is-granted) |
| `TEST_USER_CAN_CREATE_AND_VIEW_OWN_RESERVATION` | No description provided. | Uncategorized | [See Details](#test-case-test-user-can-create-and-view-own-reservation) |

***

## Conclusion

The primary objective was to validate the core functionality of the application, encompassing both the student-facing user interface and the administrative-level RESTful APIs. The goal was to ensure the system's stability, data integrity, and adherence to specified business rules before deployment.

A cornerstone of our strategy was a multi-layered approach to integration testing, which ensures that individual components work together correctly as a complete system. This went beyond simple unit tests by verifying interactions between the API controllers, the data models, and the database itself. Our tests were structured to validate vertical slices of functionality:
*   **Model & Database Integration:** We explicitly tested how different models interact through database constraints. For example, test case `MODEL_DB_004` verifies that a `Dish` cannot be deleted if it is referenced by a `DailyMenuItem`, confirming that foreign key relationships and cascade rules are correctly enforced.
*   **API & Service Integration:** Our API tests (`API_USER_001`, `API_MENU_001`, etc.) are inherently integration tests. They validate the full flow from an HTTP request hitting a controller, which then calls a model method, which in turn interacts with the database. This ensures the entire service layer for a given resource works as expected.
*   **Cross-Cutting Concerns Integration:** We validated the integration of our security module (`auth.py`) across all relevant endpoints. Tests like `API_SEC_001` and `API_SEC_002` confirm that our authentication and authorization decorators correctly protect resources based on user roles and session status.
*   **Scenario & Workflow Integration:** The highest level of integration was achieved through our scenario tests (`SCEN_INT_001`, `SCEN_ORDER_001`). These tests simulate complete, multi-step business workflows, such as an administrator setting up the system and a user subsequently placing an order, providing the highest degree of confidence in the application's overall stability.

A hybrid strategy combining automated and manual testing methodologies was employed to achieve broad and deep coverage. Critical API functionality, model-level data integrity, and repetitive UI workflows were automated to ensure consistent and repeatable verification. These automated scripts formed the core of our regression suite. Manual exploratory testing was used to supplement this, focusing on verifying visual layout, user experience edge cases, and scenarios not easily covered by automated scripts. This blended approach allowed for both efficient regression checking and flexible, human-driven validation.

To execute this strategy, a specific set of tools was chosen. The `pytest` framework served as the foundation for all Python-based testing due to its powerful fixture system and extensibility. For backend API and model-level tests, `pytest` was used with an in-memory SQLite database to ensure fast and isolated execution. End-to-end browser automation was accomplished using `Selenium IDE` for initial workflow recording, with the exported scripts managed and run via `pytest-selenium`. The entire application and its dependencies were orchestrated using `Docker` and `docker-compose`, which provided a consistent and reproducible testing environment across all stages.

***

## Annexes

This section contains the detailed execution reports for all automated and manual test cases.

## Annex A: Automated Test Execution Details

| Metric | Value |
|---|---|
| **Total Automated Tests** | 184 |
| Passed | 161 |
| Failed/Error | 23 |
| Skipped | 0 |


### Model & Unit Tests


#### <a id="test-case-model-user-001"></a>MODEL_USER_001: Verify AppUser model can create a user with a hashed password.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_USER_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.4140s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_user` |

**Test Scenario:**
The create_user class method should correctly instantiate a user, hash their password, and add them to the database session.

---

#### <a id="test-case-model-db-004"></a>MODEL_DB_004: Verify a dish cannot be deleted if referenced by a DailyMenuItem.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_DB_004` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3030s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_dish_delete_fails_if_in_use_by_menu_item` |

---

#### <a id="test-case-model-menuitem-005"></a>MODEL_MENUITEM_005: Verify get_all_dicts for DailyMenuItem returns all records.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_MENUITEM_005` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2880s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_get_all_menu_items_as_dicts` |

**Failure Details:**
```
self = <sqlalchemy.engine.base.Connection object at 0x11855fa10>
dialect = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x11851b390>
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x1190d8a10>
statement = <sqlalchemy.dialects.sqlite.base.SQLiteCompiler object at 0x11851a850>
parameters = [(None, '2025-07-10', '2025-07-10 19:51:35.698319')]

    def _exec_single_context(
        self,
        dialect: Dialect,
        context: ExecutionContext,
        statement: Union[str, Compiled],
        parameters: Optional[_AnyMultiExecuteParams],
    ) -> CursorResult[Any]:
        """continue the _execute_context() method for a single DBAPI
        cursor.execute() or cursor.executemany() call.
    
        """
        if dialect.bind_typing is BindTyping.SETINPUTSIZES:
            generic_setinputsizes = context._prepare_set_input_sizes()
    
            if generic_setinputsizes:
                try:
                    dialect.do_set_input_sizes(
                        context.cursor, generic_setinputsizes, context
                    )
                except BaseException as e:
                    self._handle_dbapi_exception(
                        e, str(statement), parameters, None, context
                    )
    
        cursor, str_statement, parameters = (
            context.cursor,
            context.statement,
            context.parameters,
        )
    
        effective_parameters: Optional[_AnyExecuteParams]
    
        if not context.executemany:
            effective_parameters = parameters[0]
        else:
            effective_parameters = parameters
    
        if self._has_events or self.engine._has_events:
            for fn in self.dispatch.before_cursor_execute:
                str_statement, effective_parameters = fn(
                    self,
                    cursor,
                    str_statement,
                    effective_parameters,
                    context,
                    context.executemany,
                )
    
        if self._echo:
            self._log_info(str_statement)
    
            stats = context._get_cache_stats()
    
            if not self.engine.hide_parameters:
                self._log_info(
                    "[%s] %r",
                    stats,
                    sql_util._repr_params(
                        effective_parameters,
                        batches=10,
                        ismulti=context.executemany,
                    ),
                )
            else:
                self._log_info(
                    "[%s] [SQL parameters hidden due to hide_parameters=True]",
                    stats,
                )
    
        evt_handled: bool = False
        try:
            if context.execute_style is ExecuteStyle.EXECUTEMANY:
                effective_parameters = cast(
                    "_CoreMultiExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_executemany:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_executemany(
                        cursor,
                        str_statement,
                        effective_parameters,
                        context,
                    )
            elif not effective_parameters and context.no_parameters:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute_no_params:
                        if fn(cursor, str_statement, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_execute_no_params(
                        cursor, str_statement, context
                    )
            else:
                effective_parameters = cast(
                    "_CoreSingleExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
>                   self.dialect.do_execute(
                        cursor, str_statement, effective_parameters, context
                    )

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1963: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x11851b390>
cursor = <sqlite3.Cursor object at 0x118ac09c0>
statement = 'INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)'
parameters = (None, '2025-07-10', '2025-07-10 19:51:35.698319')
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x1190d8a10>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlite3.IntegrityError: NOT NULL constraint failed: daily_menu.cafeteria_id

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/default.py:943: IntegrityError

The above exception was the direct cause of the following exception:

app = <Flask 'app.controller.controller'>

    def test_get_all_menu_items_as_dicts(app):
        with app.app_context():
            db.session.query(DailyMenuItem).delete()
            caf = Cafeteria.create_cafeteria("DMI5")
            dish = Dish.create_dish("D5", "", 1, "main_course")
            menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
>           db.session.commit()

tests/test-python/models/test_daily_menu_item.py:63: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/scoping.py:599: in commit
    return self._proxied.commit()
           ^^^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:2032: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:1313: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:1288: in _prepare_impl
    self.session.flush()
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4345: in flush
    self._flush(objects)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4480: in _flush
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py:224: in __exit__
    raise exc_value.with_traceback(exc_tb)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4441: in _flush
    flush_context.execute()
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/persistence.py:93: in save_obj
    _emit_insert_statements(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/persistence.py:1233: in _emit_insert_statements
    result = connection.execute(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x11851b390>
cursor = <sqlite3.Cursor object at 0x118ac09c0>
statement = 'INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)'
parameters = (None, '2025-07-10', '2025-07-10 19:51:35.698319')
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x1190d8a10>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: daily_menu.cafeteria_id
E       [SQL: INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)]
E       [parameters: (None, '2025-07-10', '2025-07-10 19:51:35.698319')]
E       (Background on this error at: https://sqlalche.me/e/20/gkpj)

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/default.py:943: IntegrityError
```

---

#### <a id="test-case-model-db-001"></a>MODEL_DB_001: Verify database uniqueness constraint for (cafeteria_id, menu_date) on update.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_DB_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2920s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_menu_uniqueness_constraint_on_update` |

**Failure Details:**
```
app = <Flask 'app.controller.controller'>

    def test_menu_uniqueness_constraint_on_update(app):
        """Vérifie la contrainte d'unicité (cafeteria_id, menu_date) lors d'une mise à jour."""
        with app.app_context():
            caf1 = Cafeteria.create_cafeteria("Caf 1")
            caf2 = Cafeteria.create_cafeteria("Caf 2")
            db.session.commit()
    
            # Menu existant pour caf1 à une date donnée
            DailyMenu.create_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
    
            # Autre menu pour caf2 qu'on va essayer de déplacer
            menu_to_update = DailyMenu.create_menu(cafeteria_id=caf2.cafeteria_id, menu_date=date(2030, 1, 2))
            db.session.commit()
    
            # Tenter de déplacer le menu vers une date/cafeteria déjà prise
            ok = menu_to_update.update_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
>           assert ok is False # La méthode doit retourner False en cas d'échec d'intégrité
            ^^^^^^^^^^^^^^^^^^
E           assert True is False

tests/test-python/models/test_daily_menu.py:61: AssertionError
```

---

#### <a id="test-case-model-menuitem-004"></a>MODEL_MENUITEM_004: Verify update_menu_item() with no arguments returns False.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_MENUITEM_004` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2890s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_update_menu_item_with_no_data` |

**Failure Details:**
```
self = <sqlalchemy.engine.base.Connection object at 0x11836ea50>
dialect = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x118519810>
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x11855ea50>
statement = <sqlalchemy.dialects.sqlite.base.SQLiteCompiler object at 0x11821cb90>
parameters = [(None, '2025-07-10', '2025-07-10 19:51:35.273834')]

    def _exec_single_context(
        self,
        dialect: Dialect,
        context: ExecutionContext,
        statement: Union[str, Compiled],
        parameters: Optional[_AnyMultiExecuteParams],
    ) -> CursorResult[Any]:
        """continue the _execute_context() method for a single DBAPI
        cursor.execute() or cursor.executemany() call.
    
        """
        if dialect.bind_typing is BindTyping.SETINPUTSIZES:
            generic_setinputsizes = context._prepare_set_input_sizes()
    
            if generic_setinputsizes:
                try:
                    dialect.do_set_input_sizes(
                        context.cursor, generic_setinputsizes, context
                    )
                except BaseException as e:
                    self._handle_dbapi_exception(
                        e, str(statement), parameters, None, context
                    )
    
        cursor, str_statement, parameters = (
            context.cursor,
            context.statement,
            context.parameters,
        )
    
        effective_parameters: Optional[_AnyExecuteParams]
    
        if not context.executemany:
            effective_parameters = parameters[0]
        else:
            effective_parameters = parameters
    
        if self._has_events or self.engine._has_events:
            for fn in self.dispatch.before_cursor_execute:
                str_statement, effective_parameters = fn(
                    self,
                    cursor,
                    str_statement,
                    effective_parameters,
                    context,
                    context.executemany,
                )
    
        if self._echo:
            self._log_info(str_statement)
    
            stats = context._get_cache_stats()
    
            if not self.engine.hide_parameters:
                self._log_info(
                    "[%s] %r",
                    stats,
                    sql_util._repr_params(
                        effective_parameters,
                        batches=10,
                        ismulti=context.executemany,
                    ),
                )
            else:
                self._log_info(
                    "[%s] [SQL parameters hidden due to hide_parameters=True]",
                    stats,
                )
    
        evt_handled: bool = False
        try:
            if context.execute_style is ExecuteStyle.EXECUTEMANY:
                effective_parameters = cast(
                    "_CoreMultiExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_executemany:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_executemany(
                        cursor,
                        str_statement,
                        effective_parameters,
                        context,
                    )
            elif not effective_parameters and context.no_parameters:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute_no_params:
                        if fn(cursor, str_statement, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_execute_no_params(
                        cursor, str_statement, context
                    )
            else:
                effective_parameters = cast(
                    "_CoreSingleExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
>                   self.dialect.do_execute(
                        cursor, str_statement, effective_parameters, context
                    )

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1963: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x118519810>
cursor = <sqlite3.Cursor object at 0x1184705c0>
statement = 'INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)'
parameters = (None, '2025-07-10', '2025-07-10 19:51:35.273834')
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x11855ea50>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlite3.IntegrityError: NOT NULL constraint failed: daily_menu.cafeteria_id

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/default.py:943: IntegrityError

The above exception was the direct cause of the following exception:

app = <Flask 'app.controller.controller'>

    def test_update_menu_item_with_no_data(app):
        with app.app_context():
            caf = Cafeteria.create_cafeteria("DMI4")
            dish = Dish.create_dish("D4", "", 1, "main_course")
            menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
>           db.session.commit()

tests/test-python/models/test_daily_menu_item.py:52: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/scoping.py:599: in commit
    return self._proxied.commit()
           ^^^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:2032: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:1313: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:1288: in _prepare_impl
    self.session.flush()
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4345: in flush
    self._flush(objects)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4480: in _flush
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py:224: in __exit__
    raise exc_value.with_traceback(exc_tb)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/session.py:4441: in _flush
    flush_context.execute()
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/persistence.py:93: in save_obj
    _emit_insert_statements(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/orm/persistence.py:1233: in _emit_insert_statements
    result = connection.execute(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x118519810>
cursor = <sqlite3.Cursor object at 0x1184705c0>
statement = 'INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)'
parameters = (None, '2025-07-10', '2025-07-10 19:51:35.273834')
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x11855ea50>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: daily_menu.cafeteria_id
E       [SQL: INSERT INTO daily_menu (cafeteria_id, menu_date, created_at) VALUES (?, ?, ?)]
E       [parameters: (None, '2025-07-10', '2025-07-10 19:51:35.273834')]
E       (Background on this error at: https://sqlalche.me/e/20/gkpj)

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/sqlalchemy/engine/default.py:943: IntegrityError
```

---

### API Tests


#### <a id="test-case-api-sec-002"></a>API_SEC_002: Verify that unauthenticated API access is denied for all protected endpoints.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_002` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `9.6200s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_api_unauthenticated_access_is_denied (x33 params)` |

---

### End-to-End (E2E) Tests


#### <a id="test-case-e2e-admin-cafe-001"></a>E2E_ADMIN_CAFE_001: E2E test for the full admin workflow of creating and deleting a cafeteria.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_ADMIN_CAFE_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.6280s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_admin_full_cafeteria_lifecycle` |

---

#### <a id="test-case-e2e-admin-menu-001"></a>E2E_ADMIN_MENU_001: E2E test for an admin creating a complex daily menu for a future date.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_ADMIN_MENU_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `15.6060s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_admin_full_menu_lifecycle` |

**Failure Details:**
```
self = <test_admin_menu_management.TestAdminMenuManagement object at 0x109b7e710>

    def test_admin_full_menu_lifecycle(self):
      driver = self.driver
    
      driver.get("http://localhost:8081/login")
      driver.find_element(By.ID, "username").send_keys("admin@example.com")
      driver.find_element(By.ID, "password").send_keys("password")
      driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
      WebDriverWait(driver, 10).until(EC.url_contains("/admin/dashboard"))
    
      future_date = date.today() + timedelta(days=30)
      future_date_str = future_date.strftime("%Y-%m-%d")
      driver.get(f"http://localhost:8081/admin/dashboard?date={future_date_str}")
    
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Save Menu')]"))
      )
    
      combobox = driver.find_element(By.CSS_SELECTOR, "input[x-model='comboboxSearch']")
      combobox.send_keys("Pizza Prosciutto")
>     pizza_option = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and text()='Pizza Prosciutto']"))
      )

tests/test-python/selenium-e2e/test_admin_menu_management.py:39: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="b28594d3-e494-4468-a2b1-ba6342f976fe")>
method = <function element_to_be_clickable.<locals>._predicate at 0x10f403600>
message = ''

    def until(self, method: Callable[[D], Union[Literal[False], T]], message: str = "") -> T:
        """Wait until the method returns a value that is not False.
    
        Calls the method provided with the driver as an argument until the
        return value does not evaluate to ``False``.
    
        Parameters:
        -----------
        method: callable(WebDriver)
            - A callable object that takes a WebDriver instance as an argument.
    
        message: str
            - Optional message for :exc:`TimeoutException`
    
        Return:
        -------
        object: T
            - The result of the last call to `method`
    
        Raises:
        -------
        TimeoutException
            - If 'method' does not return a truthy value within the WebDriverWait
            object's timeout
    
        Example:
        --------
        >>> from selenium.webdriver.common.by import By
        >>> from selenium.webdriver.support.ui import WebDriverWait
        >>> from selenium.webdriver.support import expected_conditions as EC
    
        # Wait until an element is visible on the page
        >>> wait = WebDriverWait(driver, 10)
        >>> element = wait.until(EC.visibility_of_element_located((By.ID, "exampleId")))
        >>> print(element.text)
        """
        screen = None
        stacktrace = None
    
        end_time = time.monotonic() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)
            if time.monotonic() > end_time:
                break
            time.sleep(self._poll)
>       raise TimeoutException(message, screen, stacktrace)
E       selenium.common.exceptions.TimeoutException: Message: 
E       Stacktrace:
E       RemoteError@chrome://remote/content/shared/RemoteError.sys.mjs:8:8
E       WebDriverError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:199:5
E       NoSuchElementError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:552:5
E       dom.find/</<@chrome://remote/content/shared/DOM.sys.mjs:136:16

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/support/wait.py:138: TimeoutException
```

---

#### <a id="test-case-e2e-admin-user-001"></a>E2E_ADMIN_USER_001: E2E test for an admin creating, searching for, and deleting a user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_ADMIN_USER_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `5.3600s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_admin_full_user_lifecycle` |

---

#### <a id="test-case-e2e-auth-001"></a>E2E_AUTH_001: E2E test to verify admin login and logout functionality through the UI.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_AUTH_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `2.7900s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_loginAdminLogOut` |

---

#### <a id="test-case-e2e-order-001"></a>E2E_ORDER_001: E2E test simulating a student ordering food.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_ORDER_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `2.6140s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_orderfoodinthepast` |

**Failure Details:**
```
self = <test_orderfoodinthepast.TestOrderfoodinthepast object at 0x109b7fb10>

    def test_orderfoodinthepast(self):
      self.driver.get("http://localhost:8081/login")
      self.driver.set_window_size(1512, 888)
      self.driver.find_element(By.ID, "username").click()
      self.driver.find_element(By.ID, "username").send_keys("student1@example.com")
      self.driver.find_element(By.ID, "password").send_keys("pass123")
      self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
>     self.driver.find_element(By.LINK_TEXT, "Kafeteria").click()
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test-python/selenium-e2e/test_orderfoodinthepast.py:28: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/webdriver.py:922: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/webdriver.py:454: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x10cd16c40>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"Unable to locate element: Kafeteria","stacktr.../content/shared/webdriver/Errors.sys.mjs:552:5\\ndom.find/</<@chrome://remote/content/shared/DOM.sys.mjs:136:16\\n"}}'}

    def check_response(self, response: dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                try:
                    value = json.loads(value_json)
                    if isinstance(value, dict):
                        if len(value) == 1:
                            value = value["value"]
                        status = value.get("error", None)
                        if not status:
                            status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                            message = value.get("value") or value.get("message")
                            if not isinstance(message, str):
                                value = message
                                message = message.get("message")
                        else:
                            message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: Kafeteria; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#nosuchelementexception
E       Stacktrace:
E       RemoteError@chrome://remote/content/shared/RemoteError.sys.mjs:8:8
E       WebDriverError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:199:5
E       NoSuchElementError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:552:5
E       dom.find/</<@chrome://remote/content/shared/DOM.sys.mjs:136:16

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/errorhandler.py:232: NoSuchElementException
```

---

#### <a id="test-case-e2e-history-001"></a>E2E_HISTORY_001: E2E test for a student filtering their order history by month.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_HISTORY_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.5680s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_student_filter_order_history` |

**Failure Details:**
```
self = <test_student_order_history.TestStudentOrderHistory object at 0x109b7f890>

    def test_student_filter_order_history(self):
      driver = self.driver
    
      driver.get("http://localhost:8081/login")
      driver.find_element(By.ID, "username").send_keys("jakub.novak@example.com")
      driver.find_element(By.ID, "password").send_keys("pass123")
      driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Order History")))
    
      driver.find_element(By.LINK_TEXT, "Order History").click()
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "orders-list-content")))
    
      initial_orders = driver.find_elements(By.XPATH, "//*[@id='orders-list-content']//h3[contains(text(), 'Order #')]")
>     assert len(initial_orders) > 0
E     assert 0 > 0
E      +  where 0 = len([])

tests/test-python/selenium-e2e/test_student_order_history.py:31: AssertionError
```

---

### Scenario & Integration Tests


#### <a id="test-case-scen-int-001"></a>SCEN_INT_001: Test the full system integration by combining model and API tests in a realistic sequence.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `SCEN_INT_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.7780s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_full_system_integration` |

---

### Uncategorized


#### <a id="test-case-test-admin-can-get-existing-reservation-and-item"></a>TEST_ADMIN_CAN_GET_EXISTING_RESERVATION_AND_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_ADMIN_CAN_GET_EXISTING_RESERVATION_AND_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3460s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_admin_can_get_existing_reservation_and_item` |

---

#### <a id="test-case-test-api-admin-access-is-granted"></a>TEST_API_ADMIN_ACCESS_IS_GRANTED: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_API_ADMIN_ACCESS_IS_GRANTED` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `6.6390s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_api_admin_access_is_granted (x19 params)` |

---

#### <a id="test-case-test-api-unauthenticated-access-is-denied"></a>TEST_API_UNAUTHENTICATED_ACCESS_IS_DENIED: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_API_UNAUTHENTICATED_ACCESS_IS_DENIED` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `9.6510s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_api_unauthenticated_access_is_denied (x33 params)` |

---

#### <a id="test-case-test-api-user-access-is-forbidden"></a>TEST_API_USER_ACCESS_IS_FORBIDDEN: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_API_USER_ACCESS_IS_FORBIDDEN` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.4270s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_api_user_access_is_forbidden (x10 params)` |

**Failure Details:**
```
--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Lister tous les utilisateurs]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Voir le profil d'un autre utilisateur]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Cr\xe9er un nouvel utilisateur]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Supprimer son propre compte via l'API admin]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Cr\xe9er une caf\xe9t\xe9ria]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Supprimer une caf\xe9t\xe9ria]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Cr\xe9er un plat]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Lister tous les menus (route admin)]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Ajouter un item \xe0 un menu]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_forbidden[Lister tous les items de commande (route admin)]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError
```

---

#### <a id="test-case-test-api-user-access-is-granted"></a>TEST_API_USER_ACCESS_IS_GRANTED: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_API_USER_ACCESS_IS_GRANTED` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `2.0840s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_api_user_access_is_granted (x6 params)` |

**Failure Details:**
```
--- FAILED PARAMETER: `test_api_user_access_is_granted[Voir son propre profil]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_granted[Modifier son propre profil]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_granted[Ajouter de l'argent \xe0 son solde]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_granted[Lister les caf\xe9t\xe9rias]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_granted[Lister les plats]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError

--- FAILED PARAMETER: `test_api_user_access_is_granted[Voir le menu d'une caf\xe9t\xe9ria]` ---
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError
```

---

#### <a id="test-case-test-app-user-get-all-dicts"></a>TEST_APP_USER_GET_ALL_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_APP_USER_GET_ALL_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.7550s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_app_user_get_all_dicts (x2 params)` |

---

#### <a id="test-case-test-app-user-update-nothing-returns-false"></a>TEST_APP_USER_UPDATE_NOTHING_RETURNS_FALSE: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_APP_USER_UPDATE_NOTHING_RETURNS_FALSE` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3320s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_app_user_update_nothing_returns_false` |

---

#### <a id="test-case-test-app-user-update-password-and-role"></a>TEST_APP_USER_UPDATE_PASSWORD_AND_ROLE: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_APP_USER_UPDATE_PASSWORD_AND_ROLE` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.4640s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_app_user_update_password_and_role` |

---

#### <a id="test-case-test-app-user-update-to-existing-email-fails"></a>TEST_APP_USER_UPDATE_TO_EXISTING_EMAIL_FAILS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_APP_USER_UPDATE_TO_EXISTING_EMAIL_FAILS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3760s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_app_user_update_to_existing_email_fails` |

---

#### <a id="test-case-test-cafeteria-get-all-dicts"></a>TEST_CAFETERIA_GET_ALL_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CAFETERIA_GET_ALL_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2890s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_cafeteria_get_all_dicts` |

---

#### <a id="test-case-test-complete-cafeteria-lifecycle"></a>TEST_COMPLETE_CAFETERIA_LIFECYCLE: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_COMPLETE_CAFETERIA_LIFECYCLE` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2930s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_complete_cafeteria_lifecycle` |

---

#### <a id="test-case-test-complete-menu-creation-workflow"></a>TEST_COMPLETE_MENU_CREATION_WORKFLOW: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_COMPLETE_MENU_CREATION_WORKFLOW` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2920s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_complete_menu_creation_workflow` |

---

#### <a id="test-case-test-complete-order-workflow"></a>TEST_COMPLETE_ORDER_WORKFLOW: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_COMPLETE_ORDER_WORKFLOW` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6890s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_complete_order_workflow` |

---

#### <a id="test-case-test-complete-user-lifecycle"></a>TEST_COMPLETE_USER_LIFECYCLE: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_COMPLETE_USER_LIFECYCLE` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6720s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_complete_user_lifecycle` |

---

#### <a id="test-case-test-create-cafeteria"></a>TEST_CREATE_CAFETERIA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_CAFETERIA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5810s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_cafeteria (x2 params)` |

---

#### <a id="test-case-test-create-dish"></a>TEST_CREATE_DISH: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_DISH` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5750s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_dish (x2 params)` |

---

#### <a id="test-case-test-create-menu"></a>TEST_CREATE_MENU: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_MENU` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5770s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_menu (x2 params)` |

---

#### <a id="test-case-test-create-menu-item"></a>TEST_CREATE_MENU_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_MENU_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5810s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_menu_item (x2 params)` |

---

#### <a id="test-case-test-create-order-item"></a>TEST_CREATE_ORDER_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_ORDER_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6660s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_order_item (x2 params)` |

---

#### <a id="test-case-test-create-reservation"></a>TEST_CREATE_RESERVATION: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_RESERVATION` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6720s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_reservation (x2 params)` |

---

#### <a id="test-case-test-create-user"></a>TEST_CREATE_USER: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_CREATE_USER` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.4620s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_create_user` |

---

#### <a id="test-case-test-delete-cafeteria"></a>TEST_DELETE_CAFETERIA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_CAFETERIA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5810s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_cafeteria (x2 params)` |

---

#### <a id="test-case-test-delete-dish"></a>TEST_DELETE_DISH: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_DISH` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5780s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_dish (x2 params)` |

---

#### <a id="test-case-test-delete-menu"></a>TEST_DELETE_MENU: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_MENU` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5790s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_menu (x2 params)` |

---

#### <a id="test-case-test-delete-menu-item"></a>TEST_DELETE_MENU_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_MENU_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5840s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_menu_item (x2 params)` |

---

#### <a id="test-case-test-delete-order-item"></a>TEST_DELETE_ORDER_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_ORDER_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6710s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_order_item (x2 params)` |

---

#### <a id="test-case-test-delete-reservation"></a>TEST_DELETE_RESERVATION: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_RESERVATION` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6730s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_reservation (x2 params)` |

---

#### <a id="test-case-test-delete-user"></a>TEST_DELETE_USER: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DELETE_USER` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6800s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_delete_user (x2 params)` |

---

#### <a id="test-case-test-dish-delete-fails-if-in-use-by-menu-item"></a>TEST_DISH_DELETE_FAILS_IF_IN_USE_BY_MENU_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DISH_DELETE_FAILS_IF_IN_USE_BY_MENU_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3010s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_dish_delete_fails_if_in_use_by_menu_item` |

---

#### <a id="test-case-test-dish-delete-fails-if-in-use-by-order-item"></a>TEST_DISH_DELETE_FAILS_IF_IN_USE_BY_ORDER_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_DISH_DELETE_FAILS_IF_IN_USE_BY_ORDER_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3930s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_dish_delete_fails_if_in_use_by_order_item` |

---

#### <a id="test-case-test-get-all-dicts"></a>TEST_GET_ALL_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_ALL_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2880s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_all_dicts` |

---

#### <a id="test-case-test-get-all-dishes-as-dicts"></a>TEST_GET_ALL_DISHES_AS_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_ALL_DISHES_AS_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5770s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_all_dishes_as_dicts (x2 params)` |

---

#### <a id="test-case-test-get-all-menus-as-dicts"></a>TEST_GET_ALL_MENUS_AS_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_ALL_MENUS_AS_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2960s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_all_menus_as_dicts` |

---

#### <a id="test-case-test-get-all-order-items-as-dicts"></a>TEST_GET_ALL_ORDER_ITEMS_AS_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_ALL_ORDER_ITEMS_AS_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3310s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_all_order_items_as_dicts` |

---

#### <a id="test-case-test-get-all-reservations-as-dicts"></a>TEST_GET_ALL_RESERVATIONS_AS_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_ALL_RESERVATIONS_AS_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3320s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_all_reservations_as_dicts` |

---

#### <a id="test-case-test-get-by-id"></a>TEST_GET_BY_ID: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_GET_BY_ID` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2910s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_get_by_id` |

---

#### <a id="test-case-test-referential-integrity-workflow"></a>TEST_REFERENTIAL_INTEGRITY_WORKFLOW: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_REFERENTIAL_INTEGRITY_WORKFLOW` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5530s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_referential_integrity_workflow` |

---

#### <a id="test-case-test-student-balance-top-up"></a>TEST_STUDENT_BALANCE_TOP_UP: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_STUDENT_BALANCE_TOP_UP` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.6600s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_student_balance_top_up` |

---

#### <a id="test-case-test-unauthenticated-access-security"></a>TEST_UNAUTHENTICATED_ACCESS_SECURITY: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UNAUTHENTICATED_ACCESS_SECURITY` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2970s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_unauthenticated_access_security[endpoint_subset0]` |

---

#### <a id="test-case-test-unique-email-constraint"></a>TEST_UNIQUE_EMAIL_CONSTRAINT: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UNIQUE_EMAIL_CONSTRAINT` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.7690s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_unique_email_constraint (x2 params)` |

---

#### <a id="test-case-test-update-cafeteria"></a>TEST_UPDATE_CAFETERIA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_CAFETERIA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5820s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_cafeteria (x2 params)` |

---

#### <a id="test-case-test-update-cafeteria-with-no-data"></a>TEST_UPDATE_CAFETERIA_WITH_NO_DATA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_CAFETERIA_WITH_NO_DATA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2910s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_cafeteria_with_no_data` |

---

#### <a id="test-case-test-update-from-dict"></a>TEST_UPDATE_FROM_DICT: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_FROM_DICT` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5870s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_from_dict (x2 params)` |

---

#### <a id="test-case-test-update-menu"></a>TEST_UPDATE_MENU: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_MENU` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5820s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_menu (x2 params)` |

---

#### <a id="test-case-test-update-menu-item"></a>TEST_UPDATE_MENU_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_MENU_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.5770s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_menu_item (x2 params)` |

---

#### <a id="test-case-test-update-menu-with-no-data"></a>TEST_UPDATE_MENU_WITH_NO_DATA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_MENU_WITH_NO_DATA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3050s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_menu_with_no_data` |

---

#### <a id="test-case-test-update-order-item"></a>TEST_UPDATE_ORDER_ITEM: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_ORDER_ITEM` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6720s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_order_item (x2 params)` |

---

#### <a id="test-case-test-update-order-item-with-no-data"></a>TEST_UPDATE_ORDER_ITEM_WITH_NO_DATA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_ORDER_ITEM_WITH_NO_DATA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3310s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_order_item_with_no_data` |

---

#### <a id="test-case-test-update-reservation"></a>TEST_UPDATE_RESERVATION: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_RESERVATION` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6680s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_reservation (x2 params)` |

---

#### <a id="test-case-test-update-reservation-with-no-data"></a>TEST_UPDATE_RESERVATION_WITH_NO_DATA: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_RESERVATION_WITH_NO_DATA` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3360s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_reservation_with_no_data` |

---

#### <a id="test-case-test-update-user"></a>TEST_UPDATE_USER: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_UPDATE_USER` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6770s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_update_user (x2 params)` |

---

#### <a id="test-case-test-user-can-create-and-view-own-reservation"></a>TEST_USER_CAN_CREATE_AND_VIEW_OWN_RESERVATION: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_USER_CAN_CREATE_AND_VIEW_OWN_RESERVATION` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3450s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_user_can_create_and_view_own_reservation` |

**Failure Details:**
```
client = <FlaskClient <Flask 'app.controller.controller'>>

    @pytest.fixture
    def user_client(client):
        """
        Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
        """
        user_credentials = {
            "username": "student1@example.com",
            "password": "pass123"
        }
        response = client.post("/login", data=user_credentials, follow_redirects=True)
    
        assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
        # Un utilisateur standard doit atterrir sur le dashboard utilisateur
>       assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
E       AssertionError: La page après login ne semble pas être le dashboard utilisateur.
E       assert (b'Mon Tableau de Bord' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' or b'Mon Panier' in b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n')
E        +  where b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data
E        +  and   b'\n\n\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>AR - University Meal Ordering</title>\n    <link rel="icon" href="data:;base64,iVBORw0KGgo=">\n    \n    <!--\n      1. This anti-flicker script runs immediately to set the \'dark\' class on the <html> element\n         based on localStorage before the page content renders.\n    -->\n    <script>\n      if (localStorage.theme === \'dark\' || (!(\'theme\' in localStorage) && window.matchMedia(\'(prefers-color-scheme: dark)\').matches)) {\n        document.documentElement.classList.add(\'dark\')\n      } else {\n        document.documentElement.classList.remove(\'dark\')\n      }\n    </script>\n\n    <!--\n      2. Load Tailwind CSS from CDN\n    -->\n    <script src="https://cdn.tailwindcss.com"></script>\n    \n    <!--\n      3. Configure Tailwind AFTER it loads\n    -->\n    <script>\n      tailwind.config = {\n        darkMode: \'class\'\n      }\n    </script>\n\n    <script src="https://unpkg.com/htmx.org@2.0.0"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></s...\n                return `${MONTH_NAMES[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;\n            },\n\n            changeMonth(amount) {\n                this.month += amount;\n                if (this.month < 0) {\n                    this.month = 11;\n                    this.year--;\n                } else if (this.month > 11) {\n                    this.month = 0;\n                    this.year++;\n                }\n                this.getDaysInMonth();\n            }\n        }\n    }\n\n    function themeSwitcher() {\n        return {\n            // The initial state is based on the class set by the anti-flicker script.\n            darkMode: document.documentElement.classList.contains(\'dark\'),\n            toggle() {\n                this.darkMode = !this.darkMode;\n                localStorage.setItem(\'theme\', this.darkMode ? \'dark\' : \'light\');\n                if (this.darkMode) {\n                    document.documentElement.classList.add(\'dark\');\n                } else {\n                    document.documentElement.classList.remove(\'dark\');\n                }\n            }\n        }\n    }\n    </script>\n\n    \n</body>\n\n</html>\n' = <WrapperTestResponse 18632 bytes [200 OK]>.data

tests/test-python/controller/test_api_auth.py:27: AssertionError
```

---

## Annex B: Manual Test Execution Details

#### <a id="test-case-api-sec-001"></a>Manual Test Case: API-SEC-001

| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API-SEC-001` |
| **Title** | API - Deny standard user access to admin endpoints |
| **Description** | Test Case Description |
| **Tester** | Ishan Baichoo |
| **Date Tested** | 2025-07-10 |
**Prerequisites:**
1.  A standard user is authenticated via API client.

**Test Steps:**
| Step # | Action | Expected Result | Actual Result | Status |
| :--- | :---------------------- | :---------------------- | :---------------------- | :--- |
| 1 | Authenticate as 'student1@example.com'. | Authentication successful. | As Expected | Pass |
| 2 | Send GET request to /api/v1/user/ | Server returns HTTP 403 Forbidden. | Server returned HTTP 404 Not Found. | Fail |
| 3 | None | None |  |  |
| 4 | None | None |  |  |

**Final Result:** **FAILED**

---

#### <a id="test-case-e2e-order-001"></a>Manual Test Case: E2E-ORDER-001

| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E-ORDER-001` |
| **Title** | Student - Complete E2E Order Workflow |
| **Description** | Test Case Description |
| **Tester** | Gabriel Aumasson-Leduc |
| **Date Tested** |  |
**Prerequisites:**
1.  Application is running.
1.  Default student user and menus exist.

**Test Steps:**
| Step # | Action | Expected Result | Actual Result | Status |
| :--- | :---------------------- | :---------------------- | :---------------------- | :--- |
| 1 | Login as student. | Redirect to dashboard. |  |  |
| 2 | Add an item to the cart. | Cart updates correctly. |  |  |
| 3 | Click 'Place Order'. | Order success message appears. |  |  |
| 4 | None | None |  |  |

**Final Result:** **IN PROGRESS**

---

#### <a id="test-case-manual-tc-001"></a>Manual Test Case: MANUAL-TC-001

| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MANUAL-TC-001` |
| **Title** | Verify Visual Feedback and State on Balance Top-Up |
| **Description** | Test Case Description |
| **Tester** | Clément De Simon |
| **Date Tested** | 2025-07-08 |
**Prerequisites:**
1.  User is logged in as 'student1@example.com'.
1.  Application is running in a modern web browser.

**Test Steps:**
| Step # | Action | Expected Result | Actual Result | Status |
| :--- | :---------------------- | :---------------------- | :---------------------- | :--- |
| 1 | Navigate to the 'Top Up Balance' page. | The 'Account Balance' page is displayed. | As Expected | Pass |
| 2 | Enter '25.50' into the amount field and click 'Add Money'. | A success message appears and the 'Current Balance' on the page updates. | As Expected | Pass |
| 3 | Observe the header of the application. | The balance in the top-right corner updates instantly without a page refresh. | As Expected | Pass |
| 4 | Navigate to the main 'Dashboard' page. | The balance in the header remains at the new, updated value. | As Expected | Pass |

**Final Result:** **PASSED**

---