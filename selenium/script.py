import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=800,600")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.allocine.fr/vod/films/")

wait = WebDriverWait(driver, 10)
films = []
logs = []
def scrap_films(page=1):
  # Récupération des éléments des films
  filmsEl = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.mdl")))
  for i in range(0, len(filmsEl)):
    try:
      # Récupération des données du film
      filmEl = filmsEl[i]
      title = filmEl.find_element(By.CSS_SELECTOR, "a.meta-title-link").text
      if title.endswith("VOD"):
        titleClean = title[:-3].strip()
      else:
        titleClean = title.strip()      
      genresEl = filmEl.find_elements(By.CSS_SELECTOR, ".meta-body-info a")
      genres = [el.text for el in genresEl]
      producersEl = filmEl.find_elements(By.CSS_SELECTOR, ".meta-body-direction a")
      producers = [el.text for el in producersEl]
      try:
        pressRank = filmEl.find_element(By.CSS_SELECTOR, ".rating-holder .rating-item:nth-child(1) .stareval-note").text
      except:
        pressRank = "--"
      try:
        publicRank = filmEl.find_element(By.CSS_SELECTOR, ".rating-holder .rating-item:nth-child(2) .stareval-note").text
      except:
        publicRank = "--"
      # Ajout du film dans la liste
      films.append({
        "Titre": titleClean,
        "Genres": genres,
        "Réalisateurs": producers,
        "Note presse": pressRank, 
        "Note spéctateurs": publicRank
        })
    except Exception as e:
      # Enregistrement de l'erreur dans un fichier log
      print(f"error at index {i}, message: {e}")
      errorFilmTitle = titleClean or "missing title"
      logs.append(f"Page : {page} error at index {i}: {errorFilmTitle} , message: {e}")
  return

def navigatePages():
  # Le code suivant fonctionne mal car le html est mal est foutu et le click par parfois sur le bouton d'à coté
  # while True:
  #   try:
  #     page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".current-item"))).text
  #     print(page)
  #     scrap_films()
  #     button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination a.xXx.button.button-md.button-primary-full.button-right")))
  #     if button.is_displayed():
  #       button.click()
  #   except Exception as e:
  #     print(f"error for next page, message: {e}")
  #     return

  # Récupération du nombre de pages
  pageNb = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination-item-holder a:last-child"))).text
  for i in range(1, int(pageNb)+1):
    try:
      print(i)
      # on va sur la page séléctionnée
      driver.get(f"https://www.allocine.fr/vod/films/?page={i}")
      # Récupération du contenu de la page
      scrap_films(i)
    except Exception as e:
      print(f"error for page {i}, message: {e}")

def writeLogs():
  # Enregistrements des logs
  with open("logs.txt", "w", encoding="utf-8") as txtfile:
    for log in logs:
        txtfile.write(f"{log}\n")
def saveFilms():
  try:
    # Définition des colonnes
    columns = [
      "Titre",
      "Genres",
      "Réalisateurs",
      "Note presse",
      "Note spéctateurs"
    ]
    # Création du csv
    with open("films.csv.", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        # Écriture des combats dans le csv
        for film in films:
            writer.writerow(film)
  except Exception as e:
    print(f"error writing to csv, message: {e}")

def main():
  navigatePages()
  writeLogs()
  saveFilms()

main()