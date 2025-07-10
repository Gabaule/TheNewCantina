# tests/test-python/selenium-e2e/test_student_order_history.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestStudentOrderHistory():

  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()

  def test_student_filter_order_history(self):
    driver = self.driver
    
    driver.get("http://localhost:8081/login")
    driver.find_element(By.ID, "username").send_keys("jakub.novak@example.com")
    driver.find_element(By.ID, "password").send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Order History")))

    driver.find_element(By.LINK_TEXT, "Order History").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "orders-list-content")))

    initial_orders = driver.find_elements(By.XPATH, "//*[@id='orders-list-content']//h3[contains(text(), 'Order #')]")
    assert len(initial_orders) > 0

    june_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[text()='June 2025']"))
    )
    june_filter.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "orders-list-content"), "Viewing: June 2025")
    )
    
    filtered_orders_dates = driver.find_elements(By.XPATH, "//*[@id='orders-list-content']//div[contains(text(), 'Jun')]")
    assert len(filtered_orders_dates) > 0