import scrapy
from scrapy import Request
from scrapy import Spider


class SublimagixSpider(scrapy.Spider):
    name = "sublimagix"
    allowed_domains = ["sublimagix.cl"]
    start_urls = ["https://sublimagix.cl"]

    def parse(self, response):
        categories = response.xpath('//ul[@class="nav"]//a/@href').extract()
        for category in categories:
            yield Request(category, callback= self.parse_product)

    def parse_product(self, response):
        products =  response.xpath('//ul[@class="products columns-3"]/li/a/@href').extract()
        for product in products:
             if product:
                  yield Request(product, callback= self.parse_product_details)

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
             yield Request(next_page,callback = self.parse_product)

    def parse_product_details(self, response):
            url = response.url
            img_url = response.xpath('//div[@class="woocommerce-product-gallery__image"]/a/@href').get()
            name = response.xpath('//h1/text()').get()
            short_description = response.xpath('//div[@class="woocommerce-product-details__short-description"]//text()').extract()
            short_description = ''.join(short_description).strip()
            long_description =  response.xpath('//h2[text()="Description"]/following-sibling::p[1]/text()').extract()
            if long_description:
                 long_description = ''.join(long_description).strip()
            else:
                 long_description = response.xpath('//h2[text()="Description"]/following-sibling::table//p/text()').extract()
            price_text = response.xpath('//p[@class="price"]//text()').extract()
            price = ''.join(price_text)
            sku = response.xpath('//span[@class="sku"]/text()').get()
            if sku:
                sku = sku.strip()
            
            breadcrumbs = response.xpath('//nav[@class="woocommerce-breadcrumb"]//text()').extract()
            breadcrumb = ''.join(breadcrumbs).replace('\xa0/\xa0', ',').strip()
            
            voltage = response.xpath('//strong[text()="Voltaje:"]/following-sibling::text()').get()
            if voltage:
                 voltage = voltage.strip()
            Power = response.xpath('//strong[text()="Potencia:"]/following-sibling::text()').get()
            if Power:
                 Power = Power.strip() 
            Temperature_Range = response.xpath('//strong[text()="Rango de Temperatura:"]/following-sibling::text()').get()
            if Temperature_Range:
                 Temperature_Range = Temperature_Range.strip()
            Time_Control = response.xpath('//strong[text()="Control de Tiempo:"]/following-sibling::text()').get()
            if Time_Control:
                 Time_Control = Time_Control.strip()
            Machine_Size = response.xpath('//strong[text()="Medida de la Máquina:"]/following-sibling::text()').get()
            if Machine_Size:
                 Machine_Size = Machine_Size.strip()
            Weight = response.xpath('//strong[text()="Peso:"]/following-sibling::text()').get()
            if Weight:
                 Weight = Weight.strip()
            Select_measure = response.xpath('//th[text()="Selecciona medida"]/following-sibling::td/p/text()').get()
            if Select_measure:
                 Select_measure = Select_measure.strip()
            Categories = response.xpath('//span[@class="posted_in"]/a//text()').extract()
            if Categories:
                 Categories = ''.join(Categories).strip()
            stock = response.xpath('//p[@class="stock in-stock"]/text()').get()
            if stock:
                 stock = stock.strip()
          
            data = {
                'product-url' : url,
                'img_url' : img_url,
                'name' : name,
                'price': price,
                'short_description' : short_description,
                'long_description' : long_description,
                'sku' : sku,
                'breadcrumb' : breadcrumb,
                'voltage' : voltage,
                'Power' : Power,
                'Temperature_Range' : Temperature_Range,
                'Time_Control' : Time_Control,
                'Machine_Size' : Machine_Size,
                'Weight' : Weight,
                'Select_measure' : Select_measure,
                'Categories' : Categories,
                'stock' : stock }
            
            yield data
