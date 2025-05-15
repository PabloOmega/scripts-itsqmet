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

def obtener_objetivo(contenido):
    response = obtener_respuesta(f"""
                                 Genera máximo 4 objetivos de la clase para el siguiente contenido, 
                                 separa cada objetivo con un salto de línea y empieza 
                                 cada uno con un guion medio: {contenido}""")
    return response

def obtener_contenido_ejecutado(contenido):
    response = obtener_respuesta(f"""Genera un párrafo corto del contenido que se supone se ejecutó en la clase
                                 con base a los siguientes temas tratados: {contenido}""")
    return response

def esperar_elemento(driver, xpath, type=By.XPATH, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((type, xpath))
        )
    except Exception as e:
        print(f"Error al esperar el elemento: {xpath}", e)
        driver.quit()

option_materia = 12

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

# boton_docentes = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[1]/div[2]/ul/li[4]")
# boton_docentes = driver.find_element(By.XPATH, "//a[contains(text(), 'Docentes')]")
# boton_docentes.click()
# driver.execute_script("arguments[0].click();", boton_docentes)

driver.get("https://sisacad.itsqmet.edu.ec/ITSQMETPEAMicroplanificacion.aspx")

# time.sleep(5)

# boton_micro = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[1]/div[2]/ul/ul[4]/li[8]")
# boton_micro = driver.find_element(By.XPATH, "//a[contains(text(), 'PEA Micro')]")
# boton_micro.click()

# time.sleep(5)

esperar_elemento(driver, f"//select[@id='ContentPlaceHolder1_lstMaterias']/option[{option_materia}]")

option = driver.find_element(By.XPATH, f"//select[@id='ContentPlaceHolder1_lstMaterias']/option[{option_materia}]")
option.click()

time.sleep(5)

# fecha = "09-05-2025"
fecha = time.strftime("%d-%m-%Y", time.localtime())

esperar_elemento(driver, f"//table[@id='ContentPlaceHolder1_dtgDesarrolloCurso']//tr[td[text()='{fecha}']]")

time.sleep(5)

boton_agregar_micro = driver.find_element(By.XPATH, 
                                          f"//table[@id='ContentPlaceHolder1_dtgDesarrolloCurso']//tr[td[text()='{fecha}']]//input")
driver.execute_script("arguments[0].click();", boton_agregar_micro)

time.sleep(20)

esperar_elemento(driver, "//*[@id='ContentPlaceHolder1_txtSubtema']")
esperar_elemento(driver, "//*[@id='ContentPlaceHolder1_txtObjetivoClase']")
esperar_elemento(driver, "//*[@id='ContentPlaceHolder1_txtContenidoEjecutado']")
# esperar_elemento(driver, "//*[@id='ContentPlaceHolder1_rblAvance_0']")

contenido = driver.find_element(By.ID, "ContentPlaceHolder1_txtSubtema")
objetivo = driver.find_element(By.ID, "ContentPlaceHolder1_txtObjetivoClase")
contenido_ejecutado = driver.find_element(By.ID, "ContentPlaceHolder1_txtContenidoEjecutado")
opcion_100 = driver.find_element(By.ID, "ContentPlaceHolder1_rblAvance_0")
objetivo.send_keys(obtener_objetivo(contenido.text))
contenido_ejecutado.send_keys(obtener_contenido_ejecutado(contenido.text))
opcion_100.click()

time.sleep(60)

# driver.quit()
