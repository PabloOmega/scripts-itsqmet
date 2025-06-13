from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time

client = OpenAI()
fecha = time.localtime()
# aria_label_curso = "MATEMATICAS DISCRETAS [Mod 2, ABR-SEP25 " + ("Mat" if time.strftime("%H") < "18" else "Ves. S-A")   # Nombre de la materia
aria_label_curso = "OFFICE ESSENTIALS [Mod 1, ABR-SEP25 " + ("Mat" if time.strftime("%H") < "18" else "Ves. S-A")   # Nombre de la materia

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

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/a/img"))
    )
except Exception as e:
    print("Error al esperar el botón de teams:", e)
    driver.quit()

button_teams = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/a/img")
button_teams.click()

tabs = driver.window_handles
driver.switch_to.window(tabs[-1])

time.sleep(5)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@aria-label, '{aria_label_curso}')]"))
    )
except Exception as e:
    print("Error al esperar el botón del equipo:", e)
    driver.quit()

equipo_teams = driver.find_element(By.XPATH, f"//div[contains(@aria-label, '{aria_label_curso}')]")
equipo_teams.click()

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c"))
    )
except Exception as e:
    print("Error al esperar el botón de archivos:", e)
    driver.quit()

boton_archivos = driver.find_element(By.ID, "3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c")
boton_archivos.click()

# time.sleep(20)
# time.sleep(60*2)    # Espera 7 minutos para que se cargue la grabación

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
)

iframes = driver.find_elements(By.TAG_NAME, "iframe")

for iframe in iframes:
    try:
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@title='Recordings']"))
        )
        print("Elemento encontrado en este iframe.")
        break
    except:
        driver.switch_to.default_content()

# print([element.text for element in driver.find_elements(By.TAG_NAME, "button")])
# iframe = driver.find_elements(By.TAG_NAME, "iframe")[1]
# iframe = driver.find_element(By.ID, "cacheable-iframe:3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c")
# driver.switch_to.frame(iframe)
# iframe = iframes[1]

time.sleep(1)
boton_recordings = driver.find_element(By.XPATH, "//*[@title='Recordings']")
boton_recordings.click()

aria_label = "20250520"
# aria_label = time.strftime("%Y%m%d")    # Si es que no se sube el video el mismo día, cambiar la fecha manualmente

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@aria-label, '{aria_label}')]"))
    )
except Exception as e:
    print("Error al esperar el contenedor de grabación:", e)
    driver.quit()

contenedor_grabacion = driver.find_elements(By.XPATH, f"//div[contains(@aria-label, '{aria_label}')]")[0]
contenedor_grabacion.click()

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Más']"))
    )
except Exception as e:
    print("Error al esperar el botón 'Más':", e)
    driver.quit()
time.sleep(1)
botones_mas = driver.find_elements(By.XPATH, "//button[@aria-label='Más']")
boton_mas = botones_mas[0]
boton_mas.click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@name='Copiar vínculo']"))
    )
except Exception as e:
    print("Error al esperar el botón 'Copiar vínculo':", e)
    driver.quit()

boton_copiar = driver.find_element(By.XPATH, "//button[@name='Copiar vínculo']")
boton_copiar.click()
# time.sleep(1)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Compartir']"))
    )
except Exception as e:
    print("Error al esperar el iframe de compartir:", e)
    driver.quit()

iframe = driver.find_element(By.XPATH, "//iframe[@title='Compartir']")
driver.switch_to.frame(iframe)
# time.sleep(1)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Vínculo creado']"))
    )
except Exception as e:
    print("Error al esperar el input de vínculo creado:", e)
    driver.quit()

input_copiar = driver.find_element(By.XPATH, "//input[@aria-label='Vínculo creado']")
link = input_copiar.get_attribute("value")
print(f"Link de la grabación: {link}")



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