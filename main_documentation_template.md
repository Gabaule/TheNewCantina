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
    2.  [Automated Test Execution Results](#32-automated-test-execution-results)
    3.  [Manual Test Execution](#33-manual-test-execution)
4.  [Report and Conclusion](#4-report-and-conclusion)

***

## 1. Introduction

The primary objective of this project was to design and implement a robust testing strategy to validate the application's functionality, stability, and data integrity.

This report details the testing methodologies employed, the test cases executed (both automated and manual), and a summary of the overall test plan and results.

### 1.1. Team Members

The following students contributed to this semester project:
*   Ishan Baichoo
*   Gabriel Aumasson-Leduc
*   Clément De Simon

### 1.2. Description of Tested Functionality

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

## 2. Test Case Management Template

[PLACEHOLDER: A detailed description of the team's internal template for test case management, task distribution, and progress tracking will be presented here. This section is being prepared separately and will include a specific example of how a test case is recorded and managed within our workflow.]

***

## 3. Testing Methodology and Execution

### 3.1. Testing Methods & Tools

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
| **Custom Python Scripts** | A custom script (`report_converter.py`) was developed to parse the JUnit XML output from `pytest` and generate a professional, human-readable Markdown report, which is integrated directly into this document. |

#### **API Testing Strategy**
To ensure the reliability, security, and robustness of our "The New Cantina" application's API, we implemented a multi-layered testing strategy that combines manual/exploratory testing with a comprehensive suite of automated tests. This approach allows us to benefit from both rapid development and the confidence of preventing long-term regressions. Our strategy is built around two primary tools and three fundamental test scenarios:

**Manual and Exploratory Testing with Bruno**: The first layer of our strategy relies on the use of **Bruno**. It served as our manual and exploratory testing tool during development, enabling us to quickly validate endpoints, test edge cases, and easily debug API responses.

**Automated Testing with Pytest**: The backbone of our quality assurance is the suite of automated tests written with the **Pytest** framework. To achieve comprehensive coverage, we structured these tests around **three distinct use cases**:
1.  **Unauthenticated Access (Fundamental Security):** Verifies that all protected API endpoints correctly reject requests from unauthenticated clients.
2.  **Standard User Permissions (Access Control):** Validates that an authenticated standard user can access their own data but is blocked from administrative resources or another user's data.
3.  **Administrator Privileges (Core Functionality):** Ensures that a user with the "admin" role has the necessary privileges to perform full CRUD operations on all critical resources.

#### **Data Model and Unit Testing Strategy**
A significant portion of our automated testing effort was dedicated to the data models within the `app/models/` directory. This focus is deliberate, as the models represent the application's core business logic and data integrity rules. By ensuring this layer is exceptionally stable, we build a reliable foundation for all other components. Our model testing approach is justified by the following principles:

*   **Validating Business Logic:** Our models are more than just data containers; they encapsulate critical business logic. For instance, the `AppUser` model is responsible for hashing passwords. Test case `MODEL_USER_001` directly verifies that this security-critical logic is correctly executed during user creation.
*   **Enforcing Data Integrity:** We wrote specific tests to ensure the database enforces integrity rules defined by our models. `MODEL_DB_002` (testing email uniqueness) and `MODEL_DB_004` (verifying a dish in use cannot be deleted) are prime examples. These tests validate the crucial integration between our SQLAlchemy models and the database schema.
*   **Covering Edge Cases:** A thorough approach to model testing forces us to consider non-obvious code paths. Test case `MODEL_USER_004`, which confirms that calling an `update_user()` method with no arguments behaves predictably without causing an error, demonstrates this commitment to building resilient code.
*   **Creating a Stable Foundation:** By thoroughly testing the model layer, we create a verified and reliable foundation. This allows higher-level components, such as the API controllers, to trust the data and logic they are built upon, simplifying their own testing and reducing the chance of cascading failures.

In summary, our extensive model tests act as a fast, precise safety net that catches errors at their source and provides the confidence needed for future development and refactoring.

### 3.2. Automated Test Execution Results

All automated tests were executed via the `pytest` framework. The results were captured in a standard JUnit XML format. This XML file is then processed by our custom `report_converter.py` script to generate the detailed test case report below.

The report includes a high-level summary of the test run and detailed breakdowns for each executed test case, showing its status, execution time, and, where applicable, detailed test steps and failure logs.

---
%%AUTOMATED_TEST_RESULTS%%
---

### 3.3. Manual Test Execution

Manual testing was conducted to validate the application's usability and visual presentation. The following is an example of a manual test case executed by our team.

#### **Manual Test Case Example**

| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MANUAL-TC-001` |
| **Title** | Verify Visual Feedback and State on Balance Top-Up |
| **Description** | This test case verifies that when a user successfully adds funds to their account, the UI provides clear visual feedback, and all relevant balance indicators across the application are updated correctly without requiring a full page reload. |
| **Tester** | Clément De Simon |
| **Date Tested** | 08.07.2025 |

**Prerequisites:**
1.  The user is logged into the application as a standard user (e.g., `student1@example.com`).
2.  The application is running and accessible in a modern web browser (e.g., Chrome, Firefox).

**Test Steps:**

| Step # | Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Navigate to the "Top Up Balance" page from the sidebar menu. | The "Account Balance" page is displayed, showing the current balance and the form to add money. | As Expected | Pass |
| 2 | Enter `25.50` into the "Amount to Add" input field. | The value `25.50` is correctly displayed in the input field. | As Expected | Pass |
| 3 | Click the "Add Money to Account" button. | A success message (e.g., "25.50 € ajouté avec succès.") appears on the page. The "Current Balance" display on the page updates to reflect the new total. | As Expected | Pass |
| 4 | Observe the header of the application layout. | The user balance displayed in the top-right corner of the header should instantly update to the new total without a full page refresh. | As Expected | Pass |
| 5 | Navigate to the main "Dashboard" page. | The Dashboard loads. The balance in the header remains at the new, updated value. | As Expected | Pass |

**Final Result:** **PASS**

**Notes/Comments:**
The HTMX out-of-band swap for `#header-balance` works correctly, providing a seamless user experience. The visual feedback is clear and immediate.

***

## 4. Report and Conclusion

This document provides a high-level summary of the testing plan executed for "The New Cantina," a web application for university meal ordering. The primary objective was to validate the core functionality of the application, encompassing both the student-facing user interface and the administrative-level RESTful APIs. The goal was to ensure the system's stability, data integrity, and adherence to specified business rules before deployment.

A cornerstone of our strategy was a multi-layered approach to integration testing, which ensures that individual components work together correctly as a complete system. This went beyond simple unit tests by verifying interactions between the API controllers, the data models, and the database itself. Our tests were structured to validate vertical slices of functionality:
*   **Model & Database Integration:** We explicitly tested how different models interact through database constraints. For example, test case `MODEL_DB_004` verifies that a `Dish` cannot be deleted if it is referenced by a `DailyMenuItem`, confirming that foreign key relationships and cascade rules are correctly enforced.
*   **API & Service Integration:** Our API tests (`API_USER_001`, `API_MENU_001`, etc.) are inherently integration tests. They validate the full flow from an HTTP request hitting a controller, which then calls a model method, which in turn interacts with the database. This ensures the entire service layer for a given resource works as expected.
*   **Cross-Cutting Concerns Integration:** We validated the integration of our security module (`auth.py`) across all relevant endpoints. Tests like `API_SEC_001` and `API_SEC_002` confirm that our authentication and authorization decorators correctly protect resources based on user roles and session status.
*   **Scenario & Workflow Integration:** The highest level of integration was achieved through our scenario tests (`SCEN_INT_001`, `SCEN_ORDER_001`). These tests simulate complete, multi-step business workflows, such as an administrator setting up the system and a user subsequently placing an order, providing the highest degree of confidence in the application's overall stability.

A hybrid strategy combining automated and manual testing methodologies was employed to achieve broad and deep coverage. Critical API functionality, model-level data integrity, and repetitive UI workflows were automated to ensure consistent and repeatable verification. These automated scripts formed the core of our regression suite. Manual exploratory testing was used to supplement this, focusing on verifying visual layout, user experience edge cases, and scenarios not easily covered by automated scripts. This blended approach allowed for both efficient regression checking and flexible, human-driven validation.

To execute this strategy, a specific set of tools was chosen. The `pytest` framework served as the foundation for all Python-based testing due to its powerful fixture system and extensibility. For backend API and model-level tests, `pytest` was used with an in-memory SQLite database to ensure fast and isolated execution. End-to-end browser automation was accomplished using `Selenium IDE` for initial workflow recording, with the exported scripts managed and run via `pytest-selenium`. The entire application and its dependencies were orchestrated using `Docker` and `docker-compose`, which provided a consistent and reproducible testing environment across all stages.