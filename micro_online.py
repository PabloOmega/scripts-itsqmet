from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time
from datetime import datetime, timedelta

client = OpenAI()
modulo = "Modulo 2"  # Cambiar según el módulo actual
automatico = True  # En verdadero guarda automáticamente la micro luego de dos minutos

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

def esperar_elemento_invisible(driver, xpath, type=By.XPATH, timeout=120):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((type, xpath))
        )
        return True
    except Exception as e:
        print(f"Error al esperar que el elemento sea invisible: {xpath}", e)
        return False

def obtener_fechas_semana():
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de la semana actual
    fechas = [inicio_semana + timedelta(days=i) for i in range(5)]
    return [fecha.strftime("%d-%m-%Y") for fecha in fechas]

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

driver.get("https://sisacad.itsqmet.edu.ec/ITSQMETPEAMicroplanificacion.aspx")

# time.sleep(5)

esperar_elemento(driver, "//select[@id='ContentPlaceHolder1_ddlModalidad']/option[@value='enlinea']")
option = driver.find_element(By.XPATH, "//select[@id='ContentPlaceHolder1_ddlModalidad']/option[@value='enlinea']")
option.click()

time.sleep(5)

esperar_elemento(driver, f"//select[@id='ContentPlaceHolder1_lstMaterias']/option[contains(text(), '{modulo}')]")

option = driver.find_element(By.XPATH, f"//select[@id='ContentPlaceHolder1_lstMaterias']/option[contains(text(), '{modulo}')]")
option.click()

fechas = obtener_fechas_semana()
print(fechas)
for fecha in fechas:
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

    cerrado = esperar_elemento_invisible(driver, "//*[@id='mdlMicro']")

    if automatico and not cerrado:
        print("Llenando automaticamente...")
        boton_guardar = driver.find_element(By.ID, "ContentPlaceHolder1_btnSave")
        driver.execute_script("arguments[0].click();", boton_guardar)
    elif not cerrado:
        print("Sigues ahí?")
        driver.quit()
        exit()
        break

time.sleep(60)

# driver.quit()
