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


@allure.feature("ADD PAGE")
@allure.story("Click on Add Page Button")
def test_click_add_menu_button(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Click on Add page button"):
            # Wait for the 'Add Menu' button to be clickable
            add_menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Add Page']"))
            )
            logger.info("'Add page' button is clickable")
            add_menu_button.click()
            take_screenshot(driver, screenshot_dir, "click_add_menu_button")
            logger.info("'Add page' button clicked successfully")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "add_page_button_error")
        logger.error(f"Error occurred while clicking the 'Add page' button: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


from selenium.webdriver.support.ui import Select


@allure.feature("Login and Form Submission")
@allure.story("Select all options in dropdown and then select the 2nd one")
def test_select_all_and_then_second_option_from_dropdown(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Iterate through all options and then select the 2nd option in the dropdown"):
        try:
            # Locate the dropdown element
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[@name='data_page_category_id']"))
            )

            # Create a Select object
            dropdown = Select(dropdown_element)

            # Open the dropdown to make all options visible
            dropdown_element.click()

            # Iterate through all options and log their text
            all_options = dropdown.options
            for index, option in enumerate(all_options):
                # Scroll to each option and click it to make it visible
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()  # Click the option to ensure it's selected and visible
                time.sleep(0.5)  # Add a brief pause to ensure visibility

                logger.info(f"Option {index + 1}: {option.text}")
                take_screenshot(driver, screenshot_dir, f"option_{index + 1}_dropdown")

            # Finally, select the 2nd option (index 1)
            dropdown.select_by_index(0)  # Index 1 corresponds to the second option

            logger.info("Selected the 2nd option ('Horizontal Tabs') from the dropdown.")
            take_screenshot(driver, screenshot_dir, "selected_second_option_dropdown")

        except Exception as e:
            logger.error(f"Error while selecting the 2nd option from the dropdown: {str(e)}")
            take_screenshot(driver, screenshot_dir, "dropdown_selection_error")
            raise


@allure.feature("Login and Form Submission")
@allure.story("Enter text in the 'Title' field and validate input")
def test_enter_text_in_title_field(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Enter text in the 'Title' field"):
        try:
            # Locate the input field by its name attribute
            title_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Title']"))
            )

            # Define the text to enter
            text_to_enter = "Automation text"

            # Enter text into the input field
            title_field.send_keys(text_to_enter)
            logger.info(f"Entered text '{text_to_enter}' in the 'Title' field.")

            # Validate the entered value
            entered_value = title_field.get_attribute('value')
            if entered_value.isdigit():
                raise ValueError("Entered value is a number, but only characters are allowed.")

            logger.info("Entered value is a valid string.")
            take_screenshot(driver, screenshot_dir, "entered_text_in_title_field")

        except ValueError as ve:
            logger.error(f"Validation Error: {str(ve)}")
            take_screenshot(driver, screenshot_dir, "title_field_validation_error")
            raise

        except Exception as e:
            logger.error(f"Error while entering text in the 'Title' field: {str(e)}")
            take_screenshot(driver, screenshot_dir, "title_field_error")
            raise


@allure.feature("Content Entry")
@allure.story("Enter content into TinyMCE editor")
def test_enter_content_into_tinymce_editor(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Switch to TinyMCE iframe"):
            # Switch to the TinyMCE iframe
            iframe = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))  # Adjust selector if needed
            )
            logger.info("Switched to TinyMCE iframe")

        with allure.step("Enter content into the TinyMCE editor"):
            # Locate the editable <p> tag inside the TinyMCE editor and enter content
            editor_body = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce p"))
            )
            editor_body.clear()
            editor_body.send_keys("This is some content entered into the TinyMCE editor.")
            take_screenshot(driver, screenshot_dir, "content_entered_into_tinymce")
            logger.info("Content entered into the TinyMCE editor")

        with allure.step("Switch back to the main content"):
            # Switch back to the main content from the iframe
            driver.switch_to.default_content()
            logger.info("Switched back to the main content")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "tinymce_content_entry_error")
        logger.error(f"Error occurred while entering content into TinyMCE editor: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Form Input")
@allure.story("Enter Kannada Title")
def test_enter_kannada_title(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Locate and click on the Kannada Title input field"):
            # Wait for the input field to be visible and then click it
            kannada_title_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Kannada Title']"))
            )
            kannada_title_input.click()
            logger.info("Clicked on the Kannada Title input field")

        with allure.step("Enter text into the Kannada Title field"):
            # Type example words into the input field
            kannada_title_input.send_keys("ಉದಾಹರಣೆಯ ಶೀರ್ಷಿಕೆ")
            take_screenshot(driver, screenshot_dir, "kannada_title_entered")
            logger.info("Entered example text 'ಉದಾಹರಣೆಯ ಶೀರ್ಷಿಕೆ' into the Kannada Title field")

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "kannada_title_entry_error")
        logger.error(f"Error occurred while entering Kannada title: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Content Entry")
@allure.story("Type content into TinyMCE editor")
def test_type_content_in_tinymce_editor(setup):
    driver, screenshot_dir, logger = setup

    try:
        with allure.step("Switch to TinyMCE iframe"):
            # Switch to the iframe that contains the TinyMCE editor
            tinymce_iframe = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='mce_']"))
            )
            logger.info("Switched to TinyMCE iframe")

        with allure.step("Type content into the editor"):
            # Locate the content body inside TinyMCE and type content
            content_body = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "body#tinymce.mce-content-body"))
            )
            content_body.click()
            content_body.send_keys("This is a test content for TinyMCE editor.")
            take_screenshot(driver, screenshot_dir, "typed_content_in_tinymce")
            logger.info("Content typed into TinyMCE editor")

        # Switch back to the main content
        driver.switch_to.default_content()

    except Exception as e:
        take_screenshot(driver, screenshot_dir, "tinymce_entry_error")
        logger.error(f"Error occurred while typing content in TinyMCE editor: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")


@allure.feature("Login and Form Submission")
@allure.story("Click on the 'Save' button")
def test_click_save_button(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Click on the 'Save' button"):
        try:
            # Locate the "Save" button by its class and name attributes
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='add_edit_page_button']"))
            )

            # Click the "Save" button
            save_button.click()
            logger.info("Clicked on the 'Save' button.")
            take_screenshot(driver, screenshot_dir, "clicked_save_button")

        except Exception as e:
            logger.error(f"Error while clicking on the 'Save' button: {str(e)}")
            take_screenshot(driver, screenshot_dir, "save_button_click_error")
            raise


@allure.feature("Login and Form Submission")
@allure.story("Verify Success Message After Saving the Form")
def test_verify_success_message(setup):
    driver, screenshot_dir, logger = setup

    with allure.step("Verify the success message after saving the form"):
        try:
            # Wait for the success message to become visible
            success_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//div[@id='content']//div[@class='alert alert-success'][normalize-space()='Data Saved successfully!']"))
            )

            # Extract the text from the success message
            success_message_text = success_message.text
            assert success_message_text == "Data Saved successfully!", \
                f"Expected 'Data Saved successfully!', but got '{success_message_text}'."

            logger.info("Success message 'Data Saved successfully!' was displayed.")
            take_screenshot(driver, screenshot_dir, "success_message_displayed")

        except Exception as e:
            logger.error(f"Error while verifying the success message: {str(e)}")
            take_screenshot(driver, screenshot_dir, "success_message_verification_error")
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




""""
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


"""