from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv

# CONFIGURATION
CHROMEDRIVER_PATH = 'chromedriver.exe'
COOKIES_FILE = 'cookies.json'
TARGET_DOMAIN = 'resultat-bac.linternaute.com'

# Demande des informations utilisateur
nom_recherche = input("Entrez le prénom ou nom à rechercher : ").strip()
academie = input("Entrez l'académie (ex : academie-lyon) : ").strip()
annee = input("Entrez l'année de l'examen (ex : 2023) : ").strip()

URL_RÉSULTATS = f"https://{TARGET_DOMAIN}/{academie}/{annee}"

options = webdriver.ChromeOptions()
# options.add_argument('--headless')

print("[*] Lancement du navigateur...")
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(f"https://{TARGET_DOMAIN}")
    time.sleep(2)

    # Injection des cookies
    try:
        with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
            for cookie in cookies:
                cookie.pop('sameSite', None)
                cookie['domain'] = TARGET_DOMAIN
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
        print("[+] Cookies injectés avec succès.")
    except Exception as e:
        print(f"[!] Erreur injection cookies : {e}")

    driver.get(URL_RÉSULTATS)
    time.sleep(5)

    # Passage de la bannière
    print("[*] Recherche d'iframe(s)...")
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"[+] {len(iframes)} iframe(s) détectée(s).")

    bouton_trouve = False
    for idx, iframe in enumerate(iframes):
        try:
            print(f"[*] Analyse de l'iframe #{idx+1}")
            driver.switch_to.frame(iframe)
            time.sleep(1)
            boutons = driver.find_elements(By.TAG_NAME, "button")
            for btn in boutons:
                texte = btn.text.strip().lower()
                if "accepter" in texte or "tout accepter" in texte:
                    print(f"[+] Bouton détecté : '{btn.text.strip()}'")
                    try:
                        btn.click()
                    except:
                        driver.execute_script("arguments[0].click();", btn)
                    bouton_trouve = True
                    break
            driver.switch_to.default_content()
            if bouton_trouve:
                break
        except:
            driver.switch_to.default_content()

    if not bouton_trouve:
        print("[!] Aucun bouton 'accepter' trouvé dans les iframes.")

    # Formulaire JS
    print("[*] Saisie du formulaire de recherche...")
    try:
        champ_nom = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "candidate-label"))
        )
        champ_nom.clear()
        champ_nom.send_keys(nom_recherche)
        print("[+] Nom saisi.")

        select_academie = Select(driver.find_element(By.CLASS_NAME, "js-candidate-academia-uri"))
        select_academie.select_by_value(academie)
        print(f"[+] Académie sélectionnée : {academie.split('-')[-1].capitalize()}")

        select_annee = Select(driver.find_element(By.CLASS_NAME, "js-candidate-year"))
        select_annee.select_by_value(annee)
        print(f"[+] Année sélectionnée : {annee}")

        driver.execute_script("""
            const form = document.getElementById('form-examination');
            if (form) {
                form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
            }
        """)
        print("[+] Formulaire soumis via JavaScript.")
        time.sleep(7)
    except Exception as e:
        print(f"[!] Erreur formulaire : {e}")

    # Scraping
    print("[*] Extraction des résultats...")
    lignes = driver.find_elements(By.CSS_SELECTOR, 'table.odTableFlex tbody tr')
    print(f"[+] {len(lignes)} élèves trouvés.")

    nom_fichier = f"{nom_recherche.lower()}_{academie.split('-')[-1]}_{annee}.csv"
    with open(nom_fichier, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Nom complet', 'Type de Bac', 'Ville', 'Lien'])

        for i, ligne in enumerate(lignes):
            try:
                lien_element = ligne.find_element(By.CSS_SELECTOR, 'td:nth-child(1) a')
                nom_complet = lien_element.find_element(By.TAG_NAME, 'strong').text.strip()
                typedebac = lien_element.find_element(By.TAG_NAME, 'span').text.strip()
                ville = ligne.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text.strip()
                lien = lien_element.get_attribute('href')

                print(f"  [{i+1}] {nom_complet} - {typedebac} - {ville}")
                writer.writerow([nom_complet, typedebac, ville, lien])
            except Exception as ex:
                print(f"[!] Erreur ligne #{i+1} : {ex}")
finally:
    driver.quit()
