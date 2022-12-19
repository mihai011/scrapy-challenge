# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ArtPiece(Item):
    url = Field()
    title = Field()
    media = Field()
    height_cm = Field()
    width_cm = Field()
    price_gbp = Field()
