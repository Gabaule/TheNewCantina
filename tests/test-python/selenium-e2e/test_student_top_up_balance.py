# Fichier : tests/test-python/selenium-e2e/test_student_top_up_balance.py (Version Finale)

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestStudentBalance():

  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()

  def test_student_balance_top_up(self):
    driver = self.driver
    wait = WebDriverWait(driver, 10)

    # --- Connexion et Navigation ---
    driver.get("http://localhost:8081/login")
    driver.find_element(By.ID, "username").send_keys("student1@example.com")
    driver.find_element(By.ID, "password").send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.presence_of_element_located((By.ID, "header-balance")))
    header_balance_element = driver.find_element(By.ID, "header-balance")
    initial_balance_text = header_balance_element.text.replace('Balance: $', '')
    initial_balance = float(initial_balance_text)

    top_up_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Top Up Balance")))
    top_up_link.click()
    
    # --- Interaction finale et fiabilisée ---
    
    # 1. Attendre que le champ soit visible et cliquable. 
    #    Cela retourne un élément "frais" juste avant l'interaction.
    amount_input = wait.until(EC.element_to_be_clickable((By.ID, "amount")))
    amount_input.click() # Clic pour le focus
    
    # 2. Re-trouver l'élément juste avant d'écrire dedans, pour être 100% sûr.
    #    C'est redondant avec l'attente précédente, mais c'est une excellente protection contre les StaleElement.
    amount_input = driver.find_element(By.ID, "amount")
    amount_input.clear()
    amount_input.send_keys("10")
    
    # 3. Vérifier la valeur
    assert driver.find_element(By.ID, "amount").get_attribute("value") == "10", "La valeur n'a pas été saisie."
    
    # 4. Attendre que le bouton SOIT cliquable AVANT de cliquer.
    #    Ceci va gérer le cas où le DOM est modifié juste avant le clic.
    add_money_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Money to Account')]"))
    )
    add_money_button.click()
    
    # --- Vérifications finales ---
    expected_balance = initial_balance + 10.00
    
    # Attendre que le swap HTMX se termine sur l'en-tête
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "header-balance"), f"${expected_balance:.2f}")
    )
    
    # Attendre que le swap HTMX se termine sur le corps de la page
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "balance-content"), f"10.00 € ajouté avec succès.")
    )

    # --- Déconnexion ---
    logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    logout_link.click()
    wait.until(EC.url_contains("/login"))