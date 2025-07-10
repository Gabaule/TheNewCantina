# tests/test-python/selenium-e2e/test_admin_cafeteria_management.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAdminCafeteriaManagement():

  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()

  def test_admin_full_cafeteria_lifecycle(self):
    driver = self.driver
    
    driver.get("http://localhost:8081/login")
    driver.find_element(By.ID, "username").send_keys("admin@example.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Manage Cafeterias")))
    
    driver.find_element(By.LINK_TEXT, "Manage Cafeterias").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "add-cafeteria-row")))
    
    new_cafe_name = f"Café E2E {int(time.time())}"
    driver.find_element(By.ID, "new-name").send_keys(new_cafe_name)
    driver.find_element(By.XPATH, "//button[text()='Add']").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//td[contains(., '{new_cafe_name}')]"))
    )

    cafe_row = driver.find_element(By.XPATH, f"//td[contains(., '{new_cafe_name}')]/parent::tr")
    delete_button = cafe_row.find_element(By.CSS_SELECTOR, "button.button-danger")
    delete_button.click()
    
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, f"//td[contains(., '{new_cafe_name}')]"))
    )