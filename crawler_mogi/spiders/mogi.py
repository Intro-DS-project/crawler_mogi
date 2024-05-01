import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from hanoikovoidcdau import standardize

from crawler_mogi.items import RoomItem
from crawler_mogi.utils import price_convert
from crawler_mogi.gemini import extract_description, extract_location


class MogiSpider(scrapy.Spider):
    name = "mogi"
    stop = False

    def start_requests(self):
        i = 1
        while True:
            yield scrapy.Request(url=f"https://mogi.vn/ha-noi/thue-phong-tro-nha-tro?cp={i}", callback=self.parse)
            if self.stop:
                raise CloseSpider("Completed scraping the current day's item.")
            i += 1

    def parse(self, response):
        room_items = response.css(".props .link-overlay")
        for item in room_items:
            room_href = item.css("::attr(href)").get()
            yield response.follow(room_href, callback=self.parse_room_detail)

    def parse_room_detail(self, response):
        item = RoomItem()

        # Ngày đăng: 05/04/2024
        post_date_str = response.css("div.info-attr:nth-child(3) > span:nth-child(2)::text").get()
        post_date_datetime = datetime.strptime(post_date_str, "%d/%m/%Y").date()
        current_date = datetime.now().date()
        if (post_date_datetime < current_date):
            self.stop = True
            return
        item["post_date"] = post_date_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Giá
        price_str = response.css("div.price:nth-child(3)::text").get()
        item["price"] = price_convert(price_str)

        # Diện tích:  20 m2
        area_str = response.css("div.info-attr:nth-child(1) > span:nth-child(2)::text").get()
        item["area"] = float(area_str.split()[0])

        # Địa chỉ
        address = response.css(".address::text").get()
        (item["street"], item["ward"], item["district"], *_) = extract_location(address).split(',')
        item["street"] = standardize.standardize_street_name(item["street"])
        item["ward"] = standardize.standardize_ward_name(item["ward"])
        item["district"] = standardize.standardize_district_name(item["district"])

        # Dùng mô tả điền các trường còn lại
        desc_str = response.css(".info-content-body::text").getall()
        fields = extract_description(' '.join(desc_str)).split(',')
        fields_int = []
        for field in fields:
            try:
                fields_int.append(int(field))
            except ValueError:
                fields_int.append(field)
        (item["num_bedroom"], item["num_diningroom"], item["num_kitchen"], item["num_toilet"], item["num_floor"],
         item["current_floor"], item["direction"], item["street_width"], *_) = fields_int

        yield item
