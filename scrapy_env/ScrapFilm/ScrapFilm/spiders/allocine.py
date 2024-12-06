import scrapy
from ScrapFilm.items import ScrapfilmItem

class AllocineSpider(scrapy.Spider):
    name = "allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/vod/films/"]

    for i in range(1, 1572):
        start_urls.append("https://www.allocine.fr/vod/films/?page=" + str(i))
        

    def parse(self, response):
        films = response.css(".gd-col-middle ul li.mdl")
        
        for film in films:
            # J'intancie l'item
            item = ScrapfilmItem()
            # je récupère les données correspondantes
            try :
                item["titre"] = film.css(".meta-title-link::text").get()
                item["genres"] = ", ".join(film.css(".meta-body-info .dark-grey-link::text").getall())
                item["realisateurs"] = ", ".join(film.css(".meta-body-direction .dark-grey-link::text").getall())
                item["note_presse"] = film.css(".rating-item:nth-child(1) .stareval-note::text").get()
                item["note_spectateurs"] = film.css(".rating-item:nth-child(2) .stareval-note::text").get()

                yield item
            except :
                print("error page")

        pass
