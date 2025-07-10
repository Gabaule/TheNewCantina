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
| **Execution Time** | `0.4330s` |
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
| **Execution Time** | `0.2960s` |
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
| **Execution Time** | `0.2890s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_get_all_menu_items_as_dicts` |

---

#### <a id="test-case-model-db-001"></a>MODEL_DB_001: Verify database uniqueness constraint for (cafeteria_id, menu_date) on update.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_DB_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2950s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_menu_uniqueness_constraint_on_update` |

---

#### <a id="test-case-model-menuitem-004"></a>MODEL_MENUITEM_004: Verify update_menu_item() with no arguments returns False.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_MENUITEM_004` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.2910s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_update_menu_item_with_no_data` |

---

### API Tests


#### <a id="test-case-api-sec-002"></a>API_SEC_002: Verify that unauthenticated API access is denied for all protected endpoints.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_002` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `9.8740s` |
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
| **Execution Time** | `3.9310s` |
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
| **Execution Time** | `12.4710s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_admin_full_menu_lifecycle` |

---

#### <a id="test-case-e2e-admin-user-001"></a>E2E_ADMIN_USER_001: E2E test for an admin creating, searching for, and deleting a user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_ADMIN_USER_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `4.1300s` |
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
| **Execution Time** | `2.6210s` |
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
| **Execution Time** | `2.1960s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_orderfoodinthepast` |

---

#### <a id="test-case-e2e-history-001"></a>E2E_HISTORY_001: E2E test for a student filtering their order history by month.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_HISTORY_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `2.6130s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_student_filter_order_history` |

---

### Scenario & Integration Tests


#### <a id="test-case-scen-int-001"></a>SCEN_INT_001: Test the full system integration by combining model and API tests in a realistic sequence.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `SCEN_INT_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.7800s` |
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
| **Execution Time** | `0.3480s` |
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
| **Execution Time** | `6.6300s` |
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
| **Execution Time** | `9.6760s` |
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
| **Execution Time** | `3.4880s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_api_user_access_is_forbidden (x10 params)` |

---

#### <a id="test-case-test-api-user-access-is-granted"></a>TEST_API_USER_ACCESS_IS_GRANTED: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_API_USER_ACCESS_IS_GRANTED` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `2.0820s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_api_user_access_is_granted (x6 params)` |

---

#### <a id="test-case-test-app-user-get-all-dicts"></a>TEST_APP_USER_GET_ALL_DICTS: No description provided.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `TEST_APP_USER_GET_ALL_DICTS` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.7840s` |
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
| **Execution Time** | `0.3380s` |
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
| **Execution Time** | `0.4680s` |
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
| **Execution Time** | `0.3780s` |
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
| **Execution Time** | `0.2910s` |
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
| **Execution Time** | `0.2940s` |
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
| **Execution Time** | `0.6870s` |
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
| **Execution Time** | `0.5820s` |
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
| **Execution Time** | `0.5780s` |
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
| **Execution Time** | `0.5820s` |
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
| **Execution Time** | `0.5850s` |
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
| **Execution Time** | `0.6730s` |
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
| **Execution Time** | `0.4670s` |
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
| **Execution Time** | `0.5800s` |
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
| **Execution Time** | `0.5800s` |
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
| **Execution Time** | `0.5810s` |
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
| **Execution Time** | `0.5830s` |
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
| **Execution Time** | `0.6820s` |
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
| **Execution Time** | `0.6680s` |
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
| **Execution Time** | `0.2950s` |
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
| **Execution Time** | `0.3950s` |
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
| **Execution Time** | `0.2890s` |
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
| **Execution Time** | `0.5830s` |
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
| **Execution Time** | `0.2890s` |
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
| **Execution Time** | `0.3360s` |
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
| **Execution Time** | `0.3360s` |
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
| **Execution Time** | `0.2880s` |
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
| **Execution Time** | `0.5540s` |
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
| **Execution Time** | `3.1100s` |
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
| **Execution Time** | `0.2900s` |
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
| **Execution Time** | `0.7780s` |
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
| **Execution Time** | `0.5900s` |
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
| **Execution Time** | `0.2890s` |
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
| **Execution Time** | `0.5880s` |
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
| **Execution Time** | `0.5940s` |
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
| **Execution Time** | `0.5840s` |
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
| **Execution Time** | `0.2880s` |
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
| **Execution Time** | `0.3350s` |
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
| **Execution Time** | `0.6900s` |
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
| **Execution Time** | `0.3320s` |
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
| **Execution Time** | `0.6960s` |
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
| **Execution Time** | `0.3430s` |
| **Date Tested** | `10-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_user_can_create_and_view_own_reservation` |

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