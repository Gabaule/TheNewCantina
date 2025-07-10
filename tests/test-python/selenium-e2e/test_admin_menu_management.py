# tests/test-python/selenium-e2e/test_admin_menu_management.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta

class TestAdminMenuManagement():

  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_admin_full_menu_lifecycle(self):
    driver = self.driver
    
    driver.get("http://localhost:8081/login")
    driver.find_element(By.ID, "username").send_keys("admin@example.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/dashboard"))

    future_date = date.today() + timedelta(days=30)
    future_date_str = future_date.strftime("%Y-%m-%d")
    driver.get(f"http://localhost:8081/admin/dashboard?date={future_date_str}")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Save Menu')]"))
    )

    combobox = driver.find_element(By.CSS_SELECTOR, "input[x-model='comboboxSearch']")
    combobox.send_keys("Pizza Prosciutto")
    pizza_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and text()='Pizza Prosciutto']"))
    )
    pizza_option.click()
    # Utiliser le nom visible pour trouver la checkbox (plus robuste que l'ID)
    driver.find_element(By.XPATH, "//th[text()='Nová Menza']/ancestor::thead/following-sibling::tbody/tr[1]//input[@type='checkbox']").click()
    driver.find_element(By.XPATH, "//tr[contains(., 'Search or add new')]//button[text()='Add']").click()

    new_dish_name = f"Plat Selenium {int(time.time())}"
    driver.find_element(By.CSS_SELECTOR, "input[x-model='comboboxSearch']").send_keys(new_dish_name)
    driver.find_element(By.CSS_SELECTOR, "input[x-model='newDish.description']").send_keys("Test E2E")
    driver.find_element(By.CSS_SELECTOR, "input[x-model='newDish.dine_in_price']").send_keys("5.55")
    Select(driver.find_element(By.CSS_SELECTOR, "select[x-model='newDish.dish_type']")).select_by_value("side_dish")
    driver.find_element(By.XPATH, "//th[text()='Stará Menza']/ancestor::thead/following-sibling::tbody/tr[1]//input[@type='checkbox']").click()
    driver.find_element(By.XPATH, "//tr[contains(., 'Search or add new')]//button[text()='Add']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//input[@value='{new_dish_name}']"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Pizza Prosciutto']"))
    )
    
    driver.find_element(By.XPATH, "//button[contains(., 'Save Menu')]").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'mis à jour')]"))
    )
    assert driver.find_element(By.XPATH, f"//input[@value='{new_dish_name}']")