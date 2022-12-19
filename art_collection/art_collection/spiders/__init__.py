# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
from art_collection.items import ArtPiece


URL = "https://www.bearspace.co.uk/purchase?page=1000"
items = []



class ArtCrawler(scrapy.Spider):
    name = "artcrawler"
    start_urls = [URL]
    
    def parse(self, response):
        sels = response.xpath("//a[@class='oQUvqL x5qIv3']")
        for s in sels:
            url = s.attrib['href']
            yield scrapy.Request(url, callback = self.parse_item)
            
    def parse_item(self, response):
        art_piece = ArtPiece()
        
        art_piece["url"] = response.url
        art_piece["title"] = response.xpath("//h1[@data-hook='product-title']/text()").get()
        art_piece["price_gbp"] = response.xpath("//span[@data-hook='formatted-primary-price']/text()").get()
        contents = response.xpath("//pre[@data-hook='description']//text()").extract()
        dimensions = None
        media = []
        if contents:
            for content in contents:
                check_dim = re.findall(r"(\d+(\.|,)*\d*)", content)
                if check_dim and len(check_dim) >= 2 and not dimensions:
                    dimensions = check_dim
                elif not dimensions:
                    media.append(content)
            if dimensions:
                art_piece["height_cm"] = dimensions[0][0]
                art_piece["width_cm"] = dimensions[1][0]
            art_piece["media"] = " ".join(media)
        items.append(art_piece)
        yield art_piece