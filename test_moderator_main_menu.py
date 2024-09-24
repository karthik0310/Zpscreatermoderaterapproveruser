import time
import pytest
import allure
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
from selenium.webdriver.support.ui import Select
import allure


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
@allure.story("Verify page title")
def test_verify_page_title(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Wait for page to load and verify title"):
        WebDriverWait(driver, 10).until(EC.title_contains("Zilla Panchayat Shivamogga"))
        page_title = driver.title
        assert page_title == "Zilla Panchayat Shivamogga", "Page title does not match after login button click"


@allure.feature("Login and Form Submission")
@allure.story("Fill in login credentials")
def test_fill_login_credentials(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Fill in login credentials"):
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
        )
        username_field.send_keys("moderator@site.com")
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
@allure.story("click on main menu")
def test_click_main_menu_link(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Click the main menu link"):
            # Wait for the element to be visible and then click it
            ajax_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Main Menu']"))
            )
            logger.info("main menu link is visible")
            ajax_link.click()
            take_screenshot(driver, screenshot_dir, "click_main_menu")
            logger.info("Main menu clicked successfully")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "main_menu_error")
        logger.error(f"Error occurred while clicking the main menu: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")

@allure.feature("Edit Button Functionality")
@allure.story("Click on the Edit button for a specific row")
def test_click_edit_button(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Locate and click on the 'Edit' button"):
        try:
            # Dynamically find the row where the Edit button exists
            # Replace the logic below with one that works for your case, e.g., finding by specific text or unique identifier in the row
            # Example: Find the row by matching text content
            row = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//tr[contains(@id, 'item-')]"))
            )
            item_id = row.get_attribute('id')  # Get the dynamic item id

            logger.info(f"Located row with dynamic item id: {item_id}")

            # Use the dynamic ID to locate the Edit button
            edit_button_xpath = f"//tr[@id='{item_id}']//i[@class='glyphicon glyphicon-pencil']"

            # Wait until the Edit button is clickable
            edit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, edit_button_xpath))
            )

            # Take a screenshot before clicking the Edit button
            take_screenshot(driver, screenshot_dir, "edit_button_visible")
            logger.info("Edit button located and visible.")

            # Click the Edit button
            time.sleep(1)
            edit_button.click()
            logger.info("Clicked on the 'Edit' button.")
            take_screenshot(driver, screenshot_dir, "clicked_edit_button")

        except Exception as e:
            logger.error(f"Error while clicking the 'Edit' button: {str(e)}")
            take_screenshot(driver, screenshot_dir, "edit_button_click_error")
            raise



@allure.feature("Login and Form Submission")
@allure.story("Save the form")
def test_submit_form(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Save the form"):
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='add_menu_submit_button']"))
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
            success_message_xpath = "//body/div[@class='ch-container']/div[@class='row']/div[@id='content']/div[1]"

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
