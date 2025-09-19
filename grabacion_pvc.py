from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta, date

def obtener_numero_semana(fecha_inicio: str, formato='%Y-%m-%d') -> int:
    fecha_inicio_dt = datetime.strptime(fecha_inicio, formato)
    hoy = datetime.today()
    diferencia = hoy - fecha_inicio_dt
    return diferencia.days // 7

def obtener_fecha_jueves(fecha: date = None) -> date:
    if fecha is None:
        fecha = date.today()
    # lunes = 0, ..., domingo = 6
    dias_hasta_jueves = 3 - fecha.weekday()
    return fecha + timedelta(days=dias_hasta_jueves)

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

fecha_inicio_modulo = "2025-06-23"  # Fecha de inicio del módulo
numero_clase = 1
actividad = f"ENLACE DE LA CLASE {numero_clase} EN TEAMS" # Cambiar diariamente según el aula virtual
aria_label_curso = "MODULO 14 APLICACIONES MOVILES"   # Nombre de la materia
# link = "https://itsqmet.sharepoint.com/:v:/s/550613a01l1701102maabr2025sep2025vesenlineadesmod/EZv7lZL9K2BBjCYaT0ZyjYUBce3jlngyQsJmaSHlRwGILw?e=dcjaU5"
link = ""  # Si no se sube el video el mismo día, dejarlo vacío
aria_label = "20250423"
# aria_label = time.strftime("%Y%m%d")    # Si es que no se sube el video el mismo día, cambiar la fecha manualmente
# aria_label = obtener_fecha_jueves().strftime("%Y%m%d")  # Fecha del jueves de la semana actual

print(actividad)

driver.get("https://campusvirtual.itsqmet.edu.ec/campusV/get/the/authorization/code")

# time.sleep(5)

if not link:
    esperar_elemento(driver, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/a/img")

    button_teams = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/a/img")
    button_teams.click()

    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])

    time.sleep(5)

    esperar_elemento(driver, f"//div[contains(@aria-label, '{aria_label_curso}')]")

    equipo_teams = driver.find_element(By.XPATH, f"//div[contains(@aria-label, '{aria_label_curso}')]")
    equipo_teams.click()

    esperar_elemento(driver, "3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c", type=By.ID)

    boton_archivos = driver.find_element(By.ID, "3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c")
    boton_archivos.click()

    time.sleep(20)
    # time.sleep(60*2)    # Espera 7 minutos para que se cargue la grabación

    esperar_elemento(driver, "iframe", type=By.TAG_NAME, timeout=30)
    # WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    # )

    iframes = driver.find_elements(By.TAG_NAME, "iframe")

    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            esperar_elemento(driver, "//*[@title='Recordings']", timeout=20)
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@title='Recordings']"))
            # )
            print("Elemento encontrado en este iframe.")
            break
        except:
            driver.switch_to.default_content()

    time.sleep(5)
    boton_recordings = driver.find_element(By.XPATH, "//*[@title='Recordings']")
    boton_recordings.click()

    esperar_elemento(driver, f"//div[contains(@aria-label, '{aria_label}')]")

    contenedor_grabacion = driver.find_elements(By.XPATH, f"//div[contains(@aria-label, '{aria_label}')]")[1]
    contenedor_grabacion.click()

    esperar_elemento(driver, "//button[@aria-label='Más']", timeout=20)
    time.sleep(1)
    botones_mas = driver.find_elements(By.XPATH, "//button[@aria-label='Más']")
    boton_mas = botones_mas[0]
    boton_mas.click()

    esperar_elemento(driver, "//button[@name='Copiar vínculo']", timeout=10)

    boton_copiar = driver.find_element(By.XPATH, "//button[@name='Copiar vínculo']")
    boton_copiar.click()
    # time.sleep(1)

    esperar_elemento(driver, "//iframe[@title='Compartir']", timeout=20)

    iframe = driver.find_element(By.XPATH, "//iframe[@title='Compartir']")
    driver.switch_to.frame(iframe)
    # time.sleep(1)

    esperar_elemento(driver, "//input[@aria-label='Vínculo creado']", timeout=20)

    input_copiar = driver.find_element(By.XPATH, "//input[@aria-label='Vínculo creado']")
    link = input_copiar.get_attribute("value")
print(f"Link de la grabación: {link}")

tabs = driver.window_handles
driver.switch_to.new_window("tab")
driver.get("https://pvc.itsqmet.edu.ec/my/courses.php")
# driver.get("https://moodleonline.itsqmet.edu.ec/")
# time.sleep(5)

esperar_elemento(driver, f"//a[contains(text(), '{aria_label_curso}')]", timeout=30)

# link_aula = driver.find_element(By.XPATH, f"//a[span[contains(text(), '{aria_label_curso}')]]") # para pvc
link_aula = driver.find_element(By.XPATH, f"//a[contains(text(), '{aria_label_curso}')]")
# link_aula.click()
driver.execute_script("arguments[0].click();", link_aula)
driver.get(driver.current_url + f"&section=5") # para pvc

esperar_elemento(driver, "//button[@data-action='save' and text()='Sí']")
boton_si = driver.find_element(By.XPATH, "//button[@data-action='save' and text()='Sí']")
boton_si.click()

time.sleep(1)

esperar_elemento(driver, "//button[contains(text(), 'Activar edición')]", timeout=20)
boton_activar_edicion = driver.find_element(By.XPATH, "//button[contains(text(), 'Activar edición')]")
boton_activar_edicion.click()
# checkbox_activar_edicion = driver.find_element(By.XPATH, "//input[@id='680e56fa733fc680e56fa5bc4c5-editingswitch']")
# driver.execute_script("arguments[0].click();", checkbox_activar_edicion)  # para pvc

time.sleep(5)

esperar_elemento(driver, f"//li[@data-title='ENLACE DE LA CLASE {numero_clase}']//a[@aria-label='Editar' and contains(@class, 'dropdown-toggle')]", timeout=20)
dropdown_editar = driver.find_element(
    By.XPATH,
    f"//li[@data-title='ENLACE DE LA CLASE {numero_clase}']//a[@aria-label='Editar' and contains(@class, 'dropdown-toggle')]"
)
driver.execute_script("arguments[0].click();", dropdown_editar)

time.sleep(2)

esperar_elemento(driver, f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[.//span[normalize-space()='Mostrar']]", timeout=20)
boton_mostrar = driver.find_element(By.XPATH, f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[.//span[normalize-space()='Mostrar']]")
driver.execute_script("arguments[0].click();", boton_mostrar)

time.sleep(2)

esperar_elemento(driver, f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[@aria-label='Editar' and contains(@class, 'dropdown-toggle')]", timeout=20)
dropdown_editar = driver.find_element(
    By.XPATH,
    f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[@aria-label='Editar' and contains(@class, 'dropdown-toggle')]"
)
driver.execute_script("arguments[0].click();", dropdown_editar)

esperar_elemento(driver, f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[.//span[normalize-space()='Editar ajustes']]", timeout=20)
boton_editar = driver.find_element(By.XPATH, f"//li[@data-title='ENLACE CLASE {numero_clase}']//a[.//span[normalize-space()='Editar ajustes']]")

time.sleep(1)
driver.execute_script("arguments[0].click();", boton_editar)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "id_name"))
    )
except Exception as e:
    print("Error al esperar el input de nombre:", e)
    driver.quit()

input_nombre_grabacion = driver.find_element(By.ID, "id_name")
input_nombre_grabacion.clear()
input_nombre_grabacion.send_keys(f"{actividad}")

input_enlace = driver.find_element(By.ID, "id_externalurl")
input_enlace.clear()
input_enlace.send_keys(link)
time.sleep(1)

boton_guardar = driver.find_element(By.XPATH, "//input[@value='Guardar cambios y regresar al curso']")
driver.execute_script("arguments[0].click();", boton_guardar)

time.sleep(60)
# driver.quit()
