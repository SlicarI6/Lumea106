from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from vanzare_correcta import calculeaza_vinde_lem_correct
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from threading import Thread
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.firefox.options import Options
# Set up the service and options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
# Set up the service and options
# options.add_argument("-profile")
# options.add_argument("C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/8j3093g1.myUser")  # Use your profile path

# service = Service(executable_path='D:/TriburileProject/geckodriver.exe')  # Adjust path if necessary
# service = Service(executable_path='/usr/local/bin/geckodriver')
service = Service(executable_path='D:/Lumea106/geckodriver')

# Initialize the driver
driver = webdriver.Firefox(service=service, options=options)

# Step 1: Navigate to the main Triburile website
driver.get("https://www.triburile.ro/")

# Step 2: Wait for the "Lumea 104" button and click it
lumea_106_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[4]/div[10]/div[3]/div[2]/div[1]/a[2]/span'))
)
driver.execute_script("arguments[0].scrollIntoView();", lumea_106_button)
time.sleep(2) 
lumea_106_button.click()

# Step 3: Wait for the page to load, then navigate to the overview screen
WebDriverWait(driver, 20).until(
    EC.url_contains("ro106.triburile.ro")  # Wait for the URL to confirm you are on the correct page
)

# Add a brief wait for the page to load
time.sleep(3)  # Adjust as needed
click_assistenta_farmare = WebDriverWait(driver, 20).until(
EC.visibility_of_element_located((By.XPATH, '//*[@id="manager_icon_farm"]'))
)
print("Elementul manager_icon_farm a fost găsit.")
click_assistenta_farmare.click()

def click_protectie_bot(driver):
    # Verifică dacă butonul "Începeți verificarea protecției bot" este vizibil
    try:
        buton_verificare = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/a'))  # Modifică cu XPATH-ul corect
        )
        buton_verificare.click()
        print("Butonul 'Începeți verificarea protecției bot' a fost apăsat.")
        return True  # Indică că butonul a fost apăsat
    except NoSuchElementException:
        print("Butonul 'Începeți verificarea protecției bot' nu a fost găsit.")
        return False  # Indică că butonul nu a fost găsit

def click_checkbox_if_exists(driver):
    # Verifică checkbox-ul
    try:
        time.sleep(1)
        checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="anchor-tc"]'))
        )
        time.sleep(1)
        checkbox.click()
        print("Checkbox-ul a fost selectat.")
    except (NoSuchElementException, ElementClickInterceptedException):
        print("Checkbox-ul nu a fost găsit sau nu este clickabil.")




while True:
    try:
        # Refresh la începutul fiecărui ciclu
        driver.refresh()
        print("Pagina a fost reîmprospătată.")
        time.sleep(5)

        # Verificare număr cai disponibili
        try:
            cai_disponibili_in_asistenta_farm = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="light"]'))
            )
            cai_disponibili_in_asistenta_farm_text = cai_disponibili_in_asistenta_farm.text
            print("Text găsit pentru cai disponibili:", cai_disponibili_in_asistenta_farm_text)

            if cai_disponibili_in_asistenta_farm_text.isdigit():
                cai_disponibili_in_asistenta_farm_int = int(cai_disponibili_in_asistenta_farm_text)
                if cai_disponibili_in_asistenta_farm_int == 0:
                    print("Nu sunt trupe disponibile.")
                    time.sleep(400)  # Așteaptă 10 minute dacă nu sunt trupe disponibile
                    driver.refresh()
                    continue
            else:
                print("Valoarea pentru cai disponibili nu este numerică.")
                time.sleep(400)  # Așteaptă 10 minute dacă valoarea este invalidă
                driver.refresh()
                continue
        except (ValueError, NoSuchElementException):
            print("Eroare la găsirea sau conversia valorii pentru cai disponibili.")
            time.sleep(400)  # Așteaptă 10 minute în caz de eroare
            driver.refresh()
            continue

        # Găsire butoane de atac
        butoane_a = driver.find_elements(By.XPATH, '//a[contains(@class, "farm_village") or contains(@class, "farm_icon")]')
        print("Număr de butoane A găsite:", len(butoane_a))

        numar_atacuri = min(cai_disponibili_in_asistenta_farm_int, len(butoane_a))

        if numar_atacuri == 0:
            print("Nu sunt atacuri disponibile pentru execuție.")
            time.sleep(400)  # Așteaptă 10 minute dacă nu sunt atacuri disponibile
            driver.refresh()
            continue

        # Execută atacuri
        random.shuffle(butoane_a)
        for i, buton_a in enumerate(butoane_a[:numar_atacuri + 3]):
            try:
                # Confirmă că butonul este clickabil
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(buton_a))

                # Scroll la element
                driver.execute_script("arguments[0].scrollIntoView();", buton_a)

                # Click pe element
                driver.execute_script("arguments[0].click();", buton_a)

                print(f"S-a făcut click pe butonul A nr. {i + 1}.")
                time.sleep(1)
            except NoSuchElementException:
                print(f"Butonul A nr. {i + 1} nu a fost găsit.")
            except ElementClickInterceptedException:
                print(f"Butonul A nr. {i + 1} este obstrucționat de un alt element.")

        # Așteaptă 10 minute după atacuri
        print("Toate atacurile s-au terminat. Aștept 10 minute.")
        time.sleep(400)
        driver.refresh()
    except Exception as e:
        print(f"A apărut o eroare neașteptată: {e}")
        time.sleep(400)  # Așteaptă 10 minute și reia ciclul în caz de eroare
        driver.refresh()
