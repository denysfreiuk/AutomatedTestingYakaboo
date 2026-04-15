# Automated UI Testing for "Yakaboo"

This repository contains a professional automated UI testing framework for the [Yakaboo](https://www.yakaboo.ua/) online bookstore. The project demonstrates advanced skills in building test architectures, handling dynamic JavaScript content (Vue.js), and implementing custom solutions to bypass security protections and animations.

**[View Detailed HTML Test Report](  )**

---

## Technology Stack

* **Programming Language:** Python 3
* **Automation Tool:** Selenium WebDriver
* **Testing Framework:** Pytest
* **Driver Management:** webdriver-manager
* **Reporting:** pytest-html

---

## Project Architecture

The framework is built using the **Page Object Model (POM)** pattern, ensuring high maintainability and a clean separation between page interactions and test logic:

* **`pages/`** — Contains page classes (`HomePage`, `AuthModal`, `CheckoutPage`, `BasePage`). These house locators (XPath, CSS) and interaction methods (clicks, JS-based input, and animation handling).
* **`tests/`** — Contains isolated test scenarios with assertions. Each test is independent, with the browser lifecycle managed via Pytest fixtures (`setup_method` and `teardown_method`).
* **Technical Features:**
    * Advanced handling of Vue.js reactive components using `dispatchEvent` for stable data binding.
    * Stability-first approach using explicit waits and keyboard simulation (`Keys.TAB`) for reliable validation triggers.
    * Bypassing security layers using internal session redirects.

---

## Test Scenarios (Coverage)

The following core modules were automated to ensure critical user flows remain functional:

### 1. Authorization & Registration (`test_auth.py`)
* **Login Format Validation:** Verifying error messages for incorrect phone number formats.
* **Email Validation:** Testing the system's response to invalid email inputs.
* **Mandatory Field Checks:** Ensuring registration is blocked when required fields are left empty.
* **Password Complexity:** Boundary value testing to verify the minimum password length requirement (8 characters).

### 2. Shopping Cart (`test_cart.py`, `test_cart_clearance.py`)
* **State Persistence:** Confirming that cart contents remain saved and visible after a page refresh (F5).
* **Full Cart Clearance:** Testing the complete removal of items through the cart sidebar and the multi-step modal confirmation dialog.

### 3. Checkout Process (`test_checkout.py`)
* **Security Bypass:** Automated navigation to the checkout page using internal JavaScript redirects to bypass Cloudflare bot protection mechanisms.
* **Form Validation:** Verifying that mandatory fields are correctly flagged on the final checkout page.

---

## Solving Technical Challenges

During development, several complex front-end hurdles were overcome:

1.  **Cloudflare Protection:** Direct navigation via `driver.get()` to sensitive pages was frequently blocked. This was solved by utilizing internal JS-based redirection (`window.location.href`) within an active, authenticated session.
2.  **Vue.js "Flip" Animations:** To prevent `ElementClickInterceptedException` during form transition animations, a combination of explicit visibility waits and JS-injection clicks was implemented.
3.  **Data Binding Stability:** Standard Selenium `send_keys` occasionally failed to trigger the underlying reactive state in the JS framework. A "Spec Ops" method was created to manually trigger `input` and `change` events via JavaScript to ensure the website recognized the entered data.

---

## How to Run Tests Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/denysfreiuk/AutomatedTestingYakaboo.git
    cd AutomatedTestingYakaboo
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run tests with HTML report generation:**
    ```bash
    pytest --html=index.html --self-contained-html
    ```

---
