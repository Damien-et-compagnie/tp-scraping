import scrapy
from ScrapFilm.items import ScrapfilmItem

class AllocineSpider(scrapy.Spider):
    name = "allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/vod/films/"]

    def parse(self, response):
        ## je récupère le nombre de page
        nb_page = response.css(".button.button-md.item:last-child::text").get()

        # J'itère dessus
        for i in range(int(nb_page)):
            ## Je recupere les films de la page
            films = response.css(".gd-col-middle ul li.mdl")
            #je crèe l'url
            url = "/vod/films/?page=" + str(i)

            # si i = 1, l'élèment n'existe pas donc je l'esquive et je suis déjà sur la page 1 
            if i != 1 :
                response.css("a[href='" + url + "']::attr(href)").get()
            
            # j'itère sur les films
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
