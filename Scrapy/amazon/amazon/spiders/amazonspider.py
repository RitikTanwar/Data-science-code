import scrapy
import os
import requests
import json


class AmazonspiderSpider(scrapy.Spider):
    name = 'amazonspider'
    base_dir = './amazon_data/'

    def start_requests(self):
        base_urls = 'https://www.amazon.in/s?k=/'
        items = ['watch', 'mobile', 'tv', 'bags', 'beds', 'chairs', 'books',
                 'laptops', 'sofa', 'microwave ovens', 'geysers', 'kitchen appliances']
        urls = []
        dir_names = []
        for item in items:
            query_string = '+'.join(item.split(' '))
            dir_name = '-'.join(item.split(' '))
            dir_names.append(dir_name)
            urls.append(base_urls+query_string)

            dir_path = self.base_dir+dir_name
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        for i in range(len(urls)):
            d = {
                "dir_name": dir_names[i]
            }
            resp = scrapy.Request(
                url=urls[i], callback=self.parse, dont_filter=True)
            resp.meta['dir_name'] = dir_names[i]
            yield resp

    def parse(self, response, **meta):
        product_urls = response.css(
            'a.a-link-normal.s-no-outline::attr(href)').getall()
        counter = 0
        for url in product_urls:
            url = 'https://www.amazon.in/'+url
            resp = scrapy.Request(
                url=url, callback=self.parse_item, dont_filter=True)
            resp.meta['dir_name'] = response.meta['dir_name']

            if counter == 10:
                break

            if resp is not None:
                counter += 1

            yield resp

    def parse_item(self, response, **meta):

        item_title = response.css('span#productTitle::text').get()
        item_title = item_title[8:]
        item_title = item_title[:-8]
        item_mrp = response.xpath(
            '//*[(@id = "price")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-text-strike", " " ))]/text()').getall()
        item_price = response.css('span#priceblock_ourprice::text').get()
        item_saving = response.css('span.priceBlockSavingsString::text').get()
        item_description = response.xpath(
            '//*[(@id = "feature-bullets")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-list-item", " " ))]/text()').getall()
        item_delivery = response.xpath(
            '//*[(@id = "ddmDeliveryMessage")]//b').getall()
        image_url_list = response.xpath(
            '//*[(@id = "altImages")]/ul/li/span/span/span/span/span/img/@src').extract()
        # image_url_list = image_list.css('img::attr(src)').getall()
        item_image = response.xpath(
            '//*[(@id = "imgTagWrapperId")]/img/@data-old-hires').get()
        # image_url_list.append(item_image)
        if(len(image_url_list) > 1):
            d = {
                'item_title': item_title,
                'item_mrp':item_mrp,
                'item_price': item_price,
                'item_description': item_description,
                'item_delivery':item_delivery,
                'item_saving': item_saving,
            }
            CATEGORY_NAME = response.meta['dir_name']
            ITEM_DIR_URL = os.path.join(
                self.base_dir, os.path.join(CATEGORY_NAME, item_title))
            if not os.path.exists(ITEM_DIR_URL):
                os.makedirs(ITEM_DIR_URL)
            with open(os.path.join(ITEM_DIR_URL, 'metadata.txt'), 'w') as f:
                json.dump(d, f)

            for i, image_url in enumerate(image_url_list):
                r = requests.get(image_url)
                with open(os.path.join(ITEM_DIR_URL, f"image_{i}.jpg"), 'wb') as f:
                    f.write(r.content)
            req = requests.get(item_image)
            with open(os.path.join(ITEM_DIR_URL, "Main_image.jpg"), 'wb') as f:
                f.write(req.content)
            print('Successfully saved \''+item_title +
                  '\'data at : '+ITEM_DIR_URL)
            yield d

        yield None
