import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# URL and credentials for OrangeHRM
url = "http://orangehrm-url.com"  # Replace with actual OrangeHRM URL
admin_username = "Admin"
admin_password = "admin_password"

@pytest.fixture(scope="module")
def driver():
    # Setup: Initialize WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Teardown: Quit WebDriver
    driver.quit()

def login_as_admin(driver, username=admin_username, password=admin_password):
    """Helper function to log in as Admin."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtUsername")))
        
        driver.find_element(By.ID, "txtUsername").send_keys(username)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "btnLogin").click()
        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "welcome")))
    except TimeoutException:
        pytest.fail("Login fields not found or timed out.")

def test_forget_password(driver):
    """Test Case 1: Launch URL and Click Forgot Password."""
    driver.get(url)
    try:
        forgot_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot your password?"))
        )
        forgot_password.click()
        assert "resetPassword" in driver.current_url, "Forgot Password page did not load correctly."
    except TimeoutException:
        pytest.fail("Forgot Password link not found or timed out.")

def test_validate_admin_menus(driver):
    """Test Case 2: Validate Menu Options on Admin Page."""
    login_as_admin(driver)
    expected_menus = ["Admin", "PIM", "Leave", "Time", "Recruitment",
                      "My Info", "Performance", "Dashboard", "Directory",
                      "Maintenance", "Buzz"]
    try:
        menu_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='mainMenuFirstLevelUnorderedList']/li"))
        )
        displayed_menus = [menu.text for menu in menu_elements]
        
        for menu in expected_menus:
            assert menu in displayed_menus, f"{menu} menu option is missing!"
    except TimeoutException:
        pytest.fail("Main menu options not found or timed out.")

def test_validate_admin_submenus(driver):
    """Test Case 3: Validate Submenus Under Admin."""
    login_as_admin(driver)
    try:
        driver.find_element(By.ID, "menu_admin_viewAdminModule").click()
        
        expected_submenus = ["User Management", "Job", "Organization", "Qualifications",
                             "Nationalities", "Corporate Banking", "Configuration"]
        submenu_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='menu']/ul/li/a"))
        )
        displayed_submenus = [submenu.text for submenu in submenu_elements]
        
        for submenu in expected_submenus:
            assert submenu in displayed_submenus, f"{submenu} submenu option is missing!"
    except TimeoutException:
        pytest.fail("Admin submenu options not found or timed out.")
