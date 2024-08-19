import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
LINKEDIN_URL = "https://www.linkedin.com/search/results/people/?activelyHiringForJobTitles=%5B%22-100%22%5D&geoUrn=%5B%22103644278%22%5D&keywords=tech%20recruiter&network=%5B%22S%22%5D&origin=FACETED_SEARCH&page=55&searchId=f479b086-5308-4820-8857-44455a20d612&sid=qgl"

def set_up_webdriver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Firefox(options=options)

def log_in(driver, email, password):
    driver.get(LINKEDIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
    time.sleep(2)

def follow_element(html_element):
    try:
        html_element.click()
    except ElementClickInterceptedException:
        print("Elemento Follow não clicável. Pulando...")

def connect_element(driver, html_element):
    try:
        html_element.click()
        pop_up_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-button__text"))
        )
        for message in pop_up_elements:
            if message.text == "Send without a note":
                try:
                    message.click()
                except ElementClickInterceptedException:
                    print("Você não pode clicar em Send without a note. Pulando...")
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except ElementClickInterceptedException:
        print("Elemento Connect não clicável. Pulando...")

def process_buttons(driver):
    while True:
        webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        try:
            buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-button__text"))
            )

            for button in buttons:
                # if button.text == "Follow":
                #     follow_element(button)
                if button.text == "Connect":
                    connect_element(driver, button)
                elif button.text == "Next":
                    try:
                        button.click()
                    except ElementClickInterceptedException:
                        print("Elemento Next não clicável. Pulando...")

            # Pausar antes de recomeçar o loop para evitar sobrecarregar o servidor
            time.sleep(5)
        except TimeoutException:
            print("Não foi possível encontrar os elementos no tempo esperado. Encerrando o loop.")
            break

def main():
    driver = set_up_webdriver()
    try:
        log_in(driver, EMAIL, PASSWORD)
        process_buttons(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()