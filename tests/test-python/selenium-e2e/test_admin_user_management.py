# tests/test-python/selenium-e2e/test_admin_user_management.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAdminUserManagement():
  
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_admin_full_user_lifecycle(self):
    driver = self.driver
    
    # 1. Login en tant qu'admin
    driver.get("http://localhost:8081/login")
    driver.find_element(By.ID, "username").send_keys("admin@example.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Attendre que le dashboard admin se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Manage Users"))
    )

    # 2. Naviguer vers la gestion des utilisateurs
    driver.find_element(By.LINK_TEXT, "Manage Users").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "users-table-body"))
    )

    # 3. Créer un nouvel utilisateur
    email_nouvel_utilisateur = f"test.selenium.{int(time.time())}@example.com"
    driver.find_element(By.ID, "new-first-name").send_keys("Selenium")
    driver.find_element(By.ID, "new-last-name").send_keys("User")
    driver.find_element(By.ID, "new-email").send_keys(email_nouvel_utilisateur)
    driver.find_element(By.ID, "new-password").send_keys("testpass123")
    driver.find_element(By.CSS_SELECTOR, "#add-user-row button").click()
    
    # Attendre que la table se mette à jour (on attend simplement que la recherche soit possible)
    time.sleep(1) 

    # 4. Rechercher et vérifier que l'utilisateur existe
    search_input = driver.find_element(By.ID, "search-input")
    search_input.send_keys(email_nouvel_utilisateur)
    
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "users-table-body"), email_nouvel_utilisateur)
    )
    
    # 5. Supprimer l'utilisateur
    user_row = driver.find_element(By.XPATH, f"//td[contains(., '{email_nouvel_utilisateur}')]/parent::tr")
    delete_button = user_row.find_element(By.CSS_SELECTOR, "button.button-danger")
    delete_button.click()
    
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    # 6. Vérifier que l'utilisateur n'existe plus
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, f"//td[contains(text(), '{email_nouvel_utilisateur}')]"))
    )