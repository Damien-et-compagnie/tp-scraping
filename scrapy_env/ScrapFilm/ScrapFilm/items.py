# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapfilmItem(scrapy.Item):
    titre = scrapy.Field(type=str, default="Unknown")
    genres = scrapy.Field(type=list, default=[])
    realisateurs = scrapy.Field(type=list, default=[])
    note_presse = scrapy.Field(type=int, default="0")
    note_spectateurs = scrapy.Field(type=int, default="0")
    pass
