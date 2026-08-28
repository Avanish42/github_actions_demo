# tests/test_login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_login(driver, config):
    driver.get(config["base_url"])

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys(config["username"])

    driver.find_element(By.NAME, "password").send_keys(config["password"])
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    time.sleep(3)  # Wait for the page to load after login
    WebDriverWait(driver, 15).until(
        EC.url_contains("dashboard")
    )
    
    time.sleep(3)  # Wait for the page to load after login