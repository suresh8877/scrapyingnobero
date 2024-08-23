from pathlib import Path
import scrapy
import json

jsondatahandaling=[]

jsondata={}

class NoberoSpider(scrapy.Spider):
    name = "quotes"

    starturl ="https://nobero.com/"
    def start_requests(self):
        yield scrapy.Request("https://nobero.com/pages/men", callback=self.parse)

    def parse(self, response):
        items=response.css(".custom-page-season-grid-item")
        for item in items:
            link=item.css(".custom-page-season-grid-item a::attr(href)").extract()
            jsondata.update({"category":link[0].split("/")[-1]})
            url = "https://nobero.com"+link[0].strip()
            yield scrapy.Request(url, callback=self.parse_item)
    
    def parse_item(self, response):
        items=response.css("#product-grid>section")
        for item in items:
            link=item.css("div a::attr(href)").get()
            try:
                url = "https://nobero.com"+link
                jsondata.update({"url":url})
                print(jsondata)
                yield scrapy.Request(url, callback=self.parse_card)
            except:
                pass

    def parse_card(self, response):
        data=response.css("div.w-full")
        title=data.css("h1::text").get().strip()
        price=data.css("#variant-price>spanclass::text").get()
        dicount=data.css("#variant-save-percentage::text").get()
        mrp=data.css("#variant-compare-at-price>spanclass::text").get()
        jsondata.update({"title":title,
                        "price":price[1:],
                        "discount":dicount,
                        "MRP":mrp[1:]})
        form=response.css("form")
        inputsform=form.css("input::attr(value)").getall()
        if len(inputsform[2]):
            jsondata.update({"color":inputsform[2]})
        size=[]
        
        for i in inputsform:
            if(len(i)<=4 and i!='✓'):
               size.append(i) 
        jsondata.update({"size":size})

        details=response.css("#product-metafields-container>div")
        for detail in details:
            jsondata.update({detail.css("h4::text").get():detail.css("p::text").get()})
        desc=response.css("#description_content::text").get()
        jsondatahandaling.append(jsondata)
        print(jsondata) #all data is showing here
        with open("jsonfile.json", 'w') as file:
            pass
        file.close()
        with open("jsonfile.json", 'w') as file:
            json.dump(jsondatahandaling, file, indent=4) 
        file.close()
        jsondata.clear()
         
