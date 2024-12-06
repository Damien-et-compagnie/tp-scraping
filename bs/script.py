from bs4 import BeautifulSoup
import requests
import csv

url_base = "https://www.allocine.fr/vod/films/?page="

with open('films_allocine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Titre", "Genres", "Réalisateurs", "Note presse", "Note spectateurs"])

    def get_films(url):
        content = requests.get(url)
        soup = BeautifulSoup(content.text, "html.parser")
        films = soup.select("section.section div.gd-col-middle ul li.mdl")

        for film in films:
            title = film.select_one("h2.meta-title a").get_text(strip=True) if film.select_one("h2.meta-title a") else ""

            genres = [genre.get_text(strip=True) for genre in film.select(".meta-body-info .dark-grey-link")]
            if not genres:
                genres = [""]
            
            realisateurs = [realisateur.get_text(strip=True) for realisateur in film.select(".meta-body-direction .dark-grey-link")]
            if not realisateurs:
                realisateurs = [""]
            
            notes_items = film.select(".rating-holder .rating-item")
            note_presse = notes_items[0].select_one(".stareval .stareval-note").get_text(strip=True) if len(notes_items) > 0 else ""
            note_spectateurs = notes_items[1].select_one(".stareval .stareval-note").get_text(strip=True) if len(notes_items) > 1 else ""

            writer.writerow([title, genres, realisateurs, note_presse, note_spectateurs])

        return soup

    max_pages = 1572

    for page_num in range(1, max_pages + 1):
        url = f"{url_base}{page_num}"
        print(f"Récupération des films depuis : {url}")

        soup = get_films(url)
