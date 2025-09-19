from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

def numero_dia_clase(fecha_inicio_str: str, fecha_actual=None):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")

    if fecha_actual < fecha_inicio:
        print("El módulo aún no ha comenzado.")
        exit(0)
    
    dia_clase = 0
    fecha_iter = fecha_inicio

    while fecha_iter <= fecha_actual:
        if fecha_iter.weekday() < 5:
            dia_clase += 1
        fecha_iter += timedelta(days=1)

    if dia_clase > 20:
        print("El módulo ha terminado.")
        exit(0)
    else:
        return dia_clase
    
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
service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)
# driver = webdriver.Edge()

fecha_inicio_modulo = "2025-09-15"  # Fecha de inicio del módulo
aria_label = time.strftime("%Y%m%d")    # Si es que no se sube el video el mismo día, cambiar la fecha manualmente
# aria_label = "20250704"  # Cambiar manualmente según la fecha de la clase
numero_clase = numero_dia_clase(fecha_inicio_modulo, datetime.now())
# numero_clase = numero_dia_clase(fecha_inicio_modulo, datetime.strptime("2025-07-04", "%Y-%m-%d"))
actividad = f"ENLACE CLASE {numero_clase}" # Cambiar diariamente según el aula virtual
# aria_label_curso = "CALIDAD DE SOFTWARE SQA [Mod 5, ABR-SEP25 " + ("Mat" if time.strftime("%H") < "19" else "Ves. S-A")   # Nombre de la materia
aria_label_curso = "OFFICE ESSENTIALS [Mod 4, JUL-OCT25 Ves. S-A"
# aria_label_curso = "SISTEMAS CAD-CAM"  # Nombre del curso
# link = "https://itsqmet.sharepoint.com/:v:/s/matematicasdiscretasmod2abrsep25vessalmmiv18h0019h30/ETmoHwg3P0hPuWrXQRjSDY4BBwmsypdrQ2XER0COJ5s0Cw?e=fVIgMZ"
link = ""  # Si no se sube el video el mismo día, dejarlo vacío

print(actividad)

driver.get("https://campusvirtual.itsqmet.edu.ec/campusV/get/the/authorization/code")
driver.maximize_window()
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
        WebDriverWait(driver, 120).until(
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

    # print([element.text for element in driver.find_elements(By.TAG_NAME, "button")])
    # iframe = driver.find_elements(By.TAG_NAME, "iframe")[1]
    # iframe = driver.find_element(By.ID, "cacheable-iframe:3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c")
    # driver.switch_to.frame(iframe)
    # iframe = iframes[1]
    boton_recordings = driver.find_element(By.XPATH, "//*[contains(text(), 'Recordings')]")
    boton_recordings.click()

    print(f"Buscando grabación con aria-label: {aria_label}")

    time.sleep(5)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{aria_label}')]/../.."))
        )
    except Exception as e:
        print("Error al esperar el contenedor de grabación:", e)
        driver.quit()

    contenedor_grabacion = driver.find_element(By.XPATH, f"//span[contains(text(), '{aria_label}')]/../..")
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

    # time.sleep(5)
    # boton_recordings = driver.find_element(By.XPATH, "//*[@title='Recordings']")
    # boton_recordings.click()

    # # aria_label = "20250423"
    # aria_label = time.strftime("%Y%m%d")    # Si es que no se sube el video el mismo día, cambiar la fecha manualmente

    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.XPATH, f"//div[contains(@aria-label, '{aria_label}')]"))
    #     )
    # except Exception as e:
    #     print("Error al esperar el contenedor de grabación:", e)
    #     driver.quit()

    # contenedor_grabacion = driver.find_elements(By.XPATH, f"//div[contains(@aria-label, '{aria_label}')]")[1]
    # contenedor_grabacion.click()

    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Más']"))
    #     )
    # except Exception as e:
    #     print("Error al esperar el botón 'Más':", e)
    #     driver.quit()
    # time.sleep(1)
    # botones_mas = driver.find_elements(By.XPATH, "//button[@aria-label='Más']")
    # boton_mas = botones_mas[0]
    # boton_mas.click()

    # try:
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[@name='Copiar vínculo']"))
    #     )
    # except Exception as e:
    #     print("Error al esperar el botón 'Copiar vínculo':", e)
    #     driver.quit()

    # boton_copiar = driver.find_element(By.XPATH, "//button[@name='Copiar vínculo']")
    # boton_copiar.click()
    # # time.sleep(1)

    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.XPATH, "//iframe[@title='Compartir']"))
    #     )
    # except Exception as e:
    #     print("Error al esperar el iframe de compartir:", e)
    #     driver.quit()

    # iframe = driver.find_element(By.XPATH, "//iframe[@title='Compartir']")
    # driver.switch_to.frame(iframe)
    # # time.sleep(1)

    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Vínculo creado']"))
    #     )
    # except Exception as e:
    #     print("Error al esperar el input de vínculo creado:", e)
    #     driver.quit()

    # input_copiar = driver.find_element(By.XPATH, "//input[@aria-label='Vínculo creado']")
    # link = input_copiar.get_attribute("value")
print(f"Link de la grabación: {link}")

tabs = driver.window_handles
driver.switch_to.new_window("tab")
# driver.get("https://pvc.itsqmet.edu.ec/my/courses.php")
driver.get("https://virtual3.itsqmet.edu.ec:84/")
# time.sleep(5)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//a[.//*[contains(text(), '{aria_label_curso}')]]"))
    )
except Exception as e:
    print("Error al esperar el botón del curso:", e)
    driver.quit()

# link_aula = driver.find_element(By.XPATH, f"//a[span[contains(text(), '{aria_label_curso}')]]") # para pvc
link_aula = driver.find_element(By.XPATH, f"//a[.//*[contains(text(), '{aria_label_curso}')]]")
# link_aula.click()
driver.execute_script("arguments[0].click();", link_aula)

time.sleep(1)

driver.get(driver.current_url + "&section=7") # para pvc

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "editmode-switch-form"))
    )
except Exception as e:
    print("Error al esperar el botón 'Modo edición':", e)
    driver.quit()

# boton_activar_edicion = driver.find_element(By.XPATH, "//button[contains(text(), 'Activar edición')]")
# boton_activar_edicion.click()
# checkbox_activar_edicion = driver.find_element(By.XPATH, "//input[@id='680e56fa733fc680e56fa5bc4c5-editingswitch']")
# driver.execute_script("arguments[0].click();", checkbox_activar_edicion)  # para pvc
# label = driver.find_element(By.XPATH, "//form[@class='editmode-switch-form']")
form = driver.find_element(By.CLASS_NAME, "editmode-switch-form") 
# input_edicion = label.get_attribute("for") # Obtiene el valor del atributo 'for' (id del input)
input_edicion = form.find_element(By.XPATH, ".//input[@type='checkbox']") # Encuentra el input dentro del form
driver.execute_script("arguments[0].click();", input_edicion) # Activa el modo edición
time.sleep(10)

# actividad = "ENLACE DE LA CLASE 9 EN TEAMS"
# editar_icono = driver.find_element(
#     By.XPATH,
#     f"//div[@data-activityname='{actividad}']//a[.//img[@title='Editar']]"
# )

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//div[@data-activityname='{actividad}']/following-sibling::div[1]"))
    )
except Exception as e:
    print("Error al esperar el boton Editar:", e)
    driver.quit()

contenedor_editar = driver.find_element(
    By.XPATH,
    f"//div[@data-activityname='{actividad}']/following-sibling::div[1]"
)
editar_icono = contenedor_editar.find_element(By.XPATH, ".//a[.//img[@title='Editar']]")
print(editar_icono.get_attribute("outerHTML")) # Imprime el HTML del elemento encontrado
# editar_icono.click()
driver.execute_script("arguments[0].click();", editar_icono)
# time.sleep(1)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//a[.//span[contains(text(), 'Editar ajustes')]]"))
    )
except Exception as e:
    print("Error al esperar el boton Editar ajustes:", e)
    driver.quit()

boton_mostrar = editar_icono.find_element(By.XPATH, "following-sibling::div[1]//a[.//span[contains(text(), 'Mostrar')]]")
boton_editar = editar_icono.find_element(By.XPATH, "following-sibling::div[1]//a[.//span[contains(text(), 'Editar ajustes')]]")
driver.execute_script("arguments[0].click();", boton_mostrar)
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
input_nombre_grabacion.send_keys(f"{actividad} - {time.strftime('%d/%m/%Y')}")

input_enlace = driver.find_element(By.ID, "id_externalurl")
input_enlace.clear()
input_enlace.send_keys(link)
time.sleep(1)

boton_guardar = driver.find_element(By.XPATH, "//input[@value='Guardar cambios y regresar al curso']")
driver.execute_script("arguments[0].click();", boton_guardar)

time.sleep(60)
# driver.quit()
