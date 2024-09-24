import time
import pytest
import allure
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging


@pytest.fixture(scope="module")
def setup():
    # Initialize the WebDriver and maximize the window
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Create screenshots directory if it doesn't exist
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    yield driver, screenshot_dir, logger

    # Cleanup
    driver.quit()
    logger.info("Closed the browser after test.")


def take_screenshot(driver, screenshot_dir, name):
    screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot taken: {screenshot_path}")
    # Attach screenshot to the Allure report
    allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)


@allure.feature("Login and Form Submission")
@allure.story("Open the application")
def test_open_application(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Open the application"):
        driver.get("https://demo.karnataka.gov.in/zpshivamogga.karnataka.gov.in/public/back/index")
        take_screenshot(driver, screenshot_dir, "open_application")


@allure.feature("Login and Form Submission")
@allure.story("Fill in login credentials")
def test_fill_login_credentials(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Fill in login credentials"):
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
        )
        username_field.send_keys("approver@site.com")
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(
            "01123")  # //input[@placeholder='Password']
        take_screenshot(driver, screenshot_dir, "fill_login_credentials")



@allure.feature("Login and Form Submission")
@allure.story("Submit login form")
def test_submit_login_form(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Submit login form"):
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='login_button']"))  # //input[@name='login_button']
        )
        submit_button.click()
        take_screenshot(driver, screenshot_dir, "submit_login_form")


@allure.feature("Navigation")
@allure.story("Click Pages link")
def test_click_pages_link(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Click the Pages"):
            # Wait for the element to be visible and then click it
            ajax_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Pages']"))
            )
            logger.info("pages link is visible")
            ajax_link.click()
            take_screenshot(driver, screenshot_dir, "click_pages_link")
            logger.info("Active page link clicked successfully")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "active_pages_error")
        logger.error(f"Error occurred while clicking the pages link: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Table Interaction")
@allure.story("Click Edit button for Automation text with Status Moderated")
def test_click_edit_button_for_moderated_row(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Locate and click on the 'Edit' button for the Moderated Automation text row"):
        try:
            # Define XPath for the row where Title contains 'Automation text' and Status is 'Moderated'
            row_xpath = "//tr[td[2][contains(text(),'Automation text')] and td[4][normalize-space()='Moderated']]"

            # Wait for the row to be present
            moderated_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, row_xpath))
            )

            # Take a screenshot of the table row
            take_screenshot(driver, screenshot_dir, "moderated_row_visible")
            logger.info("Row with 'Automation text' and 'Moderated' status located and visible.")

            # Locate and click the Edit button in that row
            edit_button_xpath = f"{row_xpath}//a[@class='btn btn-primary btn-sm']//i[@class='glyphicon glyphicon-eye-open']"
            edit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, edit_button_xpath))
            )

            # Take a screenshot before clicking the Edit button
            take_screenshot(driver, screenshot_dir, "edit_button_visible")
            logger.info("Edit button located in the Moderated row.")

            time.sleep(1)
            # Click the Edit button
            edit_button.click()
            logger.info("Clicked on the 'Edit' button.")
            take_screenshot(driver, screenshot_dir, "clicked_edit_button")

        except Exception as e:
            logger.error(f"Error while clicking the 'Edit' button: {str(e)}")
            take_screenshot(driver, screenshot_dir, "edit_button_click_error")
            raise


@allure.feature("Login and approve the request")
@allure.story("approve the request")
def test_approve_request(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("approve the request"):
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-sm btn-success']"))
        )
        save_button.click()
        take_screenshot(driver, screenshot_dir, "form_saved")


@allure.feature("Form Submission")
@allure.story("Verify success message after saving data")
def test_verify_success_message(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Submit the form and verify the success message"):
        try:
            # Submit the form (you might need to locate and click the submit button)
            # Example: driver.find_element(By.ID, 'submit_button_id').click()

            # Define XPath for the success alert message
            success_message_xpath = "//div[@id='content']//div[@class='alert alert-success'][normalize-space()='Data Approved successfully!']"

            # Wait for the success message to be visible
            success_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, success_message_xpath))
            )

            # Take a screenshot when the success message appears
            take_screenshot(driver, screenshot_dir, "success_message_visible")
            logger.info("Success message 'Data Saved successfully!' is visible.")

            # Additional verification, if needed
            assert success_message.is_displayed(), "Success message not displayed"

        except Exception as e:
            logger.error(f"Error while verifying the success message: {str(e)}")
            take_screenshot(driver, screenshot_dir, "success_message_error")
            raise

