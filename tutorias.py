from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time

client = OpenAI()

def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def esperar_elemento(driver, xpath, type=By.XPATH, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((type, xpath))
        )
    except Exception as e:
        print(f"Error al esperar el elemento: {xpath}", e)
        driver.quit()

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", False)
options.add_argument("--start-maximized")
driver = webdriver.Edge()

driver.get("https://campusvirtual.itsqmet.edu.ec/campusV/get/the/authorization/code")

# time.sleep(5)
esperar_elemento(driver, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/form/button")

boton_sisacad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/form/button")
boton_sisacad.click()

time.sleep(1)

tabs = driver.window_handles
driver.switch_to.window(tabs[-1])

driver.get("https://sisacad.itsqmet.edu.ec/ITSQMRegEstu0319.aspx#")    
time.sleep(10)    