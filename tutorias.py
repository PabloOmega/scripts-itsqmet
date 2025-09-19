from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import time
from datetime import datetime, timedelta

client = OpenAI()


def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def obtener_actividad_refuerzo(contenido):
    response = obtener_respuesta(f"""
                                 Dentro de la clase de {aria_label_curso} se trató el siguiente contenido
                                 en la semana: {contenido}. 
                                 En la tutoría di una corrección de la evaluación parcial 1.
                                 Tengo que elaborar un informe de la tutoría,
                                 por favor genera un párrafo corto que describa la actividad de refuerzo que se 
                                 realizó en la tutoría.
                                 """)
    return response

def obtener_resultados_evaluacion(contenido):
    response = obtener_respuesta(f"""
                                 Dentro de la clase de {aria_label_curso} se trató el siguiente contenido
                                 en la semana: {contenido}. 
                                 En la tutoría di una corrección de la evaluación parcial 1.
                                 Tengo que elaborar un informe de la tutoría,
                                 por favor genera un párrafo corto que describa los resultados obtenidos
                                 con los alumnos luego de realizar la corrección.
                                 """)
    return response

def obtener_conclusiones(contenido):
    response = obtener_respuesta(f"""
                                 Dentro de la clase de {aria_label_curso} se trató el siguiente contenido
                                 en la semana: {contenido}. 
                                 En la tutoría di una corrección de la evaluación parcial 1.
                                 Tengo que elaborar un informe de la tutoría,
                                 por favor genera un párrafo corto que describa las conclusiones que se pueden
                                 obtener luego de realizar la corrección.
                                 """)
    return response

def esperar_elemento(driver, xpath, type=By.XPATH, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((type, xpath))
        )
    except Exception as e:
        print(f"Error al esperar el elemento: {xpath}", e)
        driver.quit()

def obtener_lunes_actual():
    hoy = datetime.now()
    # weekday(): lunes = 0, domingo = 6
    lunes = hoy - timedelta(days=hoy.weekday())
    return lunes.strftime("%d/%m/%Y")     

# fecha = time.localtime()
fecha_grabacion = "20250908_07"
# fecha_tutoria = obtener_lunes_actual()
fecha_tutoria = "08/09/2025"
aria_label_curso = "CALIDAD DE SOFTWARE SQA [Mod 5, ABR-SEP25 " + ("Mat. S-A" if time.strftime("%H") < "18" else "Ves. S-A")   # Nombre de la materia
# aria_label_curso = "SISTEMAS CAD-CAM"    # Nombre de la materia
# link = "https://itsqmet.sharepoint.com/:v:/s/matematicasdiscretasmod2abrsep25matsalmmijv07h0008h30/EYMEjjobK41Brd2TE50R714B24xXW-m1_O5v2Eit0kkdkw?e=gETGBG"
link = ""  # Si no se sube el video el mismo día, dejarlo vacío   

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", False)
options.add_argument("--start-maximized")
service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)
# driver = webdriver.Edge()

driver.get("https://campusvirtual.itsqmet.edu.ec/campusV/get/the/authorization/code")

# time.sleep(5)

if not link:
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
        WebDriverWait(driver, 60).until(
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

    time.sleep(20)
    # time.sleep(60*5)    # Espera 7 minutos para que se cargue la grabación

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Total de iframes encontrados: {len(iframes)}")

    for iframe in iframes:
        try:
            # print(iframe)
            driver.switch_to.frame(iframe)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Recordings')]"))
            )
            print("Elemento encontrado en este iframe.")
            break
        except:
            driver.switch_to.default_content()

    boton_recordings = driver.find_element(By.XPATH, "//*[contains(text(), 'Recordings')]")
    boton_recordings.click()

    print(f"Buscando grabación con aria-label: {fecha_grabacion}")

    time.sleep(5)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{fecha_grabacion}')]/../.."))
        )
    except Exception as e:
        print("Error al esperar el contenedor de grabación:", e)
        driver.quit()

    contenedor_grabacion = driver.find_element(By.XPATH, f"//span[contains(text(), '{fecha_grabacion}')]/../..")
    # contenedor_grabacion.click()
    driver.execute_script("arguments[0].click();", contenedor_grabacion)

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
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Copiar vínculo')]/../.."))
        )
    except Exception as e:
        print("Error al esperar el botón 'Copiar vínculo':", e)
        driver.quit()

    boton_copiar = driver.find_element(By.XPATH, "//span[contains(text(), 'Copiar vínculo')]/../..")
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
time.sleep(5)    

esperar_elemento(driver, "//a[span[text()='ASISTENCIAS TUTORIAS']]")
boton_asistencia_tutorias = driver.find_element(By.XPATH, "//a[span[text()='ASISTENCIAS TUTORIAS']]")
boton_asistencia_tutorias.click()

esperar_elemento(driver, "//select[@id='ContentPlaceHolder1_tabCargaAcademica_TabPanel1_ddlAulasVirtuales']/option[contains(text(), 'CALIDAD DE SOFTWARE SQA MATUTINO')]")

option = driver.find_element(By.XPATH, f"//select[@id='ContentPlaceHolder1_tabCargaAcademica_TabPanel1_ddlAulasVirtuales']/option[contains(text(), 'CALIDAD DE SOFTWARE SQA MATUTINO')]")
option.click()

esperar_elemento(driver, f"//input[@value='{fecha_tutoria}']")

boton_tutoria = driver.find_element(By.XPATH, f"//input[@value='{fecha_tutoria}']")
driver.execute_script("arguments[0].click();", boton_tutoria)

time.sleep(10)

esperar_elemento(driver, f"//input[@value='Informe']")
boton_informe = driver.find_element(By.XPATH, f"//input[@value='Informe']")
driver.execute_script("arguments[0].click();", boton_informe)

time.sleep(5)

esperar_elemento(driver, f"//input[@value='Aprendizaje Basado En Problemas (ABP)']")
boton_abp = driver.find_element(By.XPATH, f"//input[@value='Aprendizaje Basado En Problemas (ABP)']")
driver.execute_script("arguments[0].click();", boton_abp)

esperar_elemento(driver, f"//input[@value='Método Expositivo o Lección Magistral']")
boton_metodo_expositivo = driver.find_element(By.XPATH, f"//input[@value='Método Expositivo o Lección Magistral']")
driver.execute_script("arguments[0].click();", boton_metodo_expositivo)

esperar_elemento(driver, f"//textarea[@id='ContentPlaceHolder1_txtContenidos']")
textarea_actividades = driver.find_element(By.XPATH, f"//textarea[@id='ContentPlaceHolder1_txtContenidos']")
contenido = "Patrones de Arquitectura. MVC (.NET), MVT (Django), Microservicios y sistemas basados en componentes"
textarea_actividades.send_keys(obtener_actividad_refuerzo(contenido))

esperar_elemento(driver, f"//textarea[@id='ContentPlaceHolder1_txtResultados']")
textarea_resultados = driver.find_element(By.XPATH, f"//textarea[@id='ContentPlaceHolder1_txtResultados']")
textarea_resultados.send_keys(obtener_resultados_evaluacion(contenido))

esperar_elemento(driver, f"//textarea[@id='ContentPlaceHolder1_txtConclusiones']")
textarea_conclusiones = driver.find_element(By.XPATH, f"//textarea[@id='ContentPlaceHolder1_txtConclusiones']")
textarea_conclusiones.send_keys(obtener_conclusiones(contenido))

esperar_elemento(driver, f"//textarea[@id='ContentPlaceHolder1_txtTeams']")
textarea_teams = driver.find_element(By.XPATH, f"//textarea[@id='ContentPlaceHolder1_txtTeams']")
textarea_teams.send_keys(link)

time.sleep(120)