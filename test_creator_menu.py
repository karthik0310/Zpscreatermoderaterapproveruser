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
        username_field.send_keys("creator@site.com")
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
def test_click_active_ajax_link(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Click the active ajax link"):
            # Wait for the element to be visible and then click it
            ajax_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Main Menu']"))
            )
            logger.info("Active ajax link is visible")
            ajax_link.click()
            take_screenshot(driver, screenshot_dir, "click_main_menu")
            logger.info("Active Main menu clicked successfully")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "active_main_menu_error")
        logger.error(f"Error occurred while clicking the main menu: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Menu Management")
@allure.story("Click on Add Menu Button")
def test_click_add_menu_button(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Click on Add Menu button"):
            # Wait for the 'Add Menu' button to be clickable
            add_menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-sm btn-primary add_menu_button']"))
            )
            logger.info("'Add Menu' button is clickable")
            add_menu_button.click()
            take_screenshot(driver, screenshot_dir, "click_add_menu_button")
            logger.info("'Add Menu' button clicked successfully")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "add_menu_button_error")
        logger.error(f"Error occurred while clicking the 'Add Menu' button: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Login and Form Submission")
@allure.story("Fill in form fields")
def test_fill_in_form_fields(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Fill in form fields"):
        element_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@name="name"]'))  # //*[@name="name"]
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element_name)
        element_name.send_keys("Automation text")

        element_kn_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@name="kn_name"]'))  # //input[@name='kn_name']
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element_kn_name)
        element_kn_name.send_keys("Automation text")
        take_screenshot(driver, screenshot_dir, "form_filled")


@allure.feature("File Upload")
@allure.story("Upload a media file and verify successful upload")
def test_upload_media_file(setup):
    driver, screenshot_dir, logger = setup

    # Path to the file you want to upload
    file_path = os.path.join(os.path.dirname(__file__), r"C:\Users\GrDs_MyGovK\OneDrive\Pictures\Screenshots\2022-01-05 (2).png")

    with allure.step("Select the file to upload"):
        try:
            # Locate the file input element
            file_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@type='file' and @name='media_to_upload']"))
            )

            # Take a screenshot before selecting the file
            take_screenshot(driver, screenshot_dir, "file_input_visible")
            logger.info("File input element is visible")

            # Set the file path to the file input element
            file_input.send_keys(file_path)

            # Take a screenshot after selecting the file
            take_screenshot(driver, screenshot_dir, "file_selected")
            logger.info(f"File selected: {file_path}")

            # Wait for the upload process to complete (adjust as necessary for your application)
            #WebDriverWait(driver, 10).until(
            #    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.upload-success-message"))  # Adjust the selector
            #)

            # Take a screenshot after the file is uploaded
            take_screenshot(driver, screenshot_dir, "file_uploaded")
            logger.info("File uploaded successfully")

        except Exception as e:
            logger.error(f"Error during file upload process: {str(e)}")
            take_screenshot(driver, screenshot_dir, "file_upload_error")
            raise
def take_screenshot(driver, screenshot_dir, file_name):
    screenshot_path = os.path.join(screenshot_dir, f"{file_name}.png")
    driver.save_screenshot(screenshot_path)


@allure.feature("Dropdown Selection")
@allure.story("Select the first option from the dropdown")
def test_select_first_option_from_dropdown(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Navigate to the page and wait for dropdown to be visible"):
        try:
            # Wait for the dropdown to be visible
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "page"))
            )
            logger.info("Dropdown is visible.")

            # Select the first option (index 0)
            with allure.step("Select the first option from the dropdown"):
                select = Select(dropdown_element)
                select.select_by_index(1)
                logger.info("First option '# Link' selected from the dropdown.")

                # Take a screenshot after selection
                take_screenshot(driver, screenshot_dir, "dropdown_first_option_selected")

        except Exception as e:
            logger.error(f"Error selecting the first option from the dropdown: {str(e)}")
            take_screenshot(driver, screenshot_dir, "dropdown_selection_error")
            raise


@allure.feature("Dropdown Selection")
@allure.story("Select the second option 'Main Menu' from the menu_category dropdown")
def test_select_second_option_from_dropdown(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Navigate to the page and wait for the 'menu_category' dropdown to be visible"):
        try:
            # Wait for the dropdown to be visible
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "menu_category"))
            )
            logger.info("'menu_category' dropdown is visible.")

            # Select the second option (index 1 corresponds to 'Main Menu')
            with allure.step("Select the second option 'Main Menu' from the dropdown"):
                select = Select(dropdown_element)
                select.select_by_index(1)
                logger.info("Second option 'Main Menu' selected from the dropdown.")

                # Take a screenshot after selection
                take_screenshot(driver, screenshot_dir, "dropdown_second_option_selected")

        except Exception as e:
            logger.error(f"Error selecting the second option from the dropdown: {str(e)}")
            take_screenshot(driver, screenshot_dir, "dropdown_selection_error")
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


@allure.feature("Menu Save")
@allure.story("Verify that the menu is saved successfully and a success message is displayed")
def test_verify_menu_save_success(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Wait for the success message after saving the menu"):
        try:
            # Wait for the success message to appear
            success_message_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-success') and contains(text(), 'Menu Saved successfully!')]"))
            )
            logger.info("Success message 'Menu Saved successfully!' is displayed.")

            # Assert the message is displayed and contains the correct text
            assert "Menu Saved successfully!" in success_message_element.text, "Success message does not match."
            logger.info("Menu save success message verified successfully.")

            # Take a screenshot of the success message
            take_screenshot(driver, screenshot_dir, "menu_save_success_message")

        except Exception as e:
            logger.error(f"Error while verifying the success message: {str(e)}")
            take_screenshot(driver, screenshot_dir, "menu_save_error")
            raise



@allure.feature("Login and Form Submission")
@allure.story("Verify the form is saved successfully")
def test_verify_success_message(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Verify form submission and saved text in the table"):
        try:
            # Wait for the form table row where the saved text should be visible
            saved_text_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//td[contains(text(),'Automation text')]"))
            )

            # Get the full content of the cell
            saved_text = saved_text_element.get_attribute('innerHTML')
            logger.info(f"Saved text found in the table cell: {saved_text}")

            # Verify that both English and Kannada text are present in the cell
            assert "Automation text" in saved_text, "The English text 'Automation text' is not found."
            assert "ಉದಾಹರಣೆಯ ಶೀರ್ಷಿಕೆ" in saved_text, "The Kannada text 'ಉದಾಹರಣೆಯ ಶೀರ್ಷಿಕೆ' is not found."

            take_screenshot(driver, screenshot_dir, "form_submission_verified")
            logger.info("Form submission verified successfully with the correct text.")

        except Exception as e:
            logger.error(f"Error while verifying form submission and saved text: {str(e)}")
            take_screenshot(driver, screenshot_dir, "form_submission_verification_error")
            raise


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

'''
@allure.feature("Form Deletion")
@allure.story("Delete the form and verify deletion")
def test_delete_form_and_verify(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Locate and click on the 'Delete' button"):
        try:
            # Use a more generic XPath to locate the delete button (adjust if necessary)
            delete_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class, 'btn-danger')])[1]"))
            )

            # Take a screenshot before clicking the delete button
            take_screenshot(driver, screenshot_dir, "delete_button_visible")
            logger.info("Delete button located and visible.")

            # Click the delete button
            delete_button.click()
            logger.info("Clicked on the 'Delete' button.")
            take_screenshot(driver, screenshot_dir, "clicked_delete_button")

        except Exception as e:
            logger.error(f"Error while clicking the 'Delete' button: {str(e)}")
            take_screenshot(driver, screenshot_dir, "delete_button_click_error")
            raise



@allure.feature("Form Deletion verifying")
@allure.story("verify deletion")
def test_deleted_verify(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Verify that the form has been deleted"):
        try:
            # Wait for the form to disappear after deletion
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//div[@id='content']//div[@class='alert alert-success'][normalize-space()='Data Trashed successfully!']"))
            )

            logger.info("Verified that the form has been deleted successfully.")
            take_screenshot(driver, screenshot_dir, "form_deleted")

        except Exception as e:
            logger.error(f"Error while verifying form deletion: {str(e)}")
            take_screenshot(driver, screenshot_dir, "form_deletion_verification_error")
            raise


@allure.feature("Form Deletion")
@allure.story("Click on the 'View Trash' button after deletion")
def test_click_view_trash_button(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Click on the 'View Trash' button"):
        try:
            # Locate the "View Trash" button using the XPath
            view_trash_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='View Trash']"))
            )

            # Click the "View Trash" button
            view_trash_button.click()
            logger.info("Clicked on the 'View Trash' button.")
            take_screenshot(driver, screenshot_dir, "clicked_view_trash_button")

        except Exception as e:
            logger.error(f"Error while clicking the 'View Trash' button: {str(e)}")
            take_screenshot(driver, screenshot_dir, "view_trash_button_click_error")
            raise


@allure.feature("Form Deletion")
@allure.story("Verify the deleted form in 'Trash' view")
def test_verify_deleted_form_in_trash_view(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Verify the deleted form in 'Trash' view"):
        try:
            # Wait until the table with form data is loaded
            form_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "DataTables_Table_0"))
            )

            # Locate the row with the form title 'Automation text'
            deleted_form_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td[contains(text(), 'Automation text')]/..")
                )
            )

            # Check if the form row is displayed (this row should contain 'Automation text')
            assert deleted_form_row.is_displayed(), "The deleted form is not present in the trash view."
            logger.info("Verified the deleted form is present in the trash view.")
            take_screenshot(driver, screenshot_dir, "verified_deleted_form_in_trash_view")

        except Exception as e:
            logger.error(f"Error while verifying the deleted form in the trash view: {str(e)}")
            take_screenshot(driver, screenshot_dir, "verify_deleted_form_error")
            raise


@allure.feature("Form Restoration")
@allure.story("Restore the deleted form from 'Trash' view and validate removal")
def test_restore_form_and_validate_removal(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Restore the deleted form from 'Trash' view"):
        try:
            # Locate the "Restore" button (refresh icon) and click it
            restore_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@class='glyphicon glyphicon-refresh']"))
            )
            restore_button.click()
            logger.info("Clicked on the 'Restore' button.")
            take_screenshot(driver, screenshot_dir, "clicked_restore_button")

            # Wait for the form to be removed from the trash view
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='page_bx col-md-3 card mb-3 p-3'][@data-title='Automation text']"))
            )
            logger.info("Verified that the form has been removed from the trash view.")
            take_screenshot(driver, screenshot_dir, "form_removed_from_trash_view")

        except Exception as e:
            logger.error(f"Error while restoring the form or verifying removal from the trash view: {str(e)}")
            take_screenshot(driver, screenshot_dir, "restore_form_error")
            raise


@allure.feature("Form Restoration")
@allure.story("Verify that the form is restored and visible in live items")
def test_verify_form_restored_in_live_items(setup):
    driver, screenshot_dir, logger = setup
    restored_form_title = "Automation text"  # Update this based on the restored form title

    with allure.step("Verify that the form is restored and visible in live items"):
        try:
            # Navigate back to live items page
            go_back_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Go Back to Live Items']"))
            )
            go_back_button.click()

            # Wait for the table to load and locate the restored form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='DataTables_Table_0']"))
            )

            # Validate that the restored form is visible in the table
            restored_form_xpath = f"//table[@id='DataTables_Table_0']//td[contains(text(), '{restored_form_title}')]"
            restored_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, restored_form_xpath))
            )

            if restored_form.is_displayed():
                logger.info(f"Restored form '{restored_form_title}' is visible in live items.")
                take_screenshot(driver, screenshot_dir, "restored_form_visible")
            else:
                raise AssertionError(f"Restored form '{restored_form_title}' is not visible in live items.")

        except TimeoutException:
            logger.error("Timeout: Unable to find 'Go Back to Live Items' button or restored form.")
            take_screenshot(driver, screenshot_dir, "timeout_error")
        except NoSuchElementException as e:
            logger.error(f"Element not found: {str(e)}")
            take_screenshot(driver, screenshot_dir, "element_not_found_error")
        except Exception as e:
            logger.error(f"Error while verifying restored form: {str(e)}")
            take_screenshot(driver, screenshot_dir, "form_restoration_error")
'''