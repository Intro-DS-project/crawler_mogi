import scrapy
from scrapy.exceptions import CloseSpider

from crawler_mogi.items import RoomItem
from crawler_mogi.utils import price_conversion, date_conversion


class MogiSpider(scrapy.Spider):
    name = "mogi"

    def start_requests(self):
        i = 1
        while True:
            yield scrapy.Request(url=f"https://mogi.vn/ha-noi/thue-phong-tro-nha-tro?cp={i}", callback=self.parse)
            i += 1

    def parse(self, response):
        room_items = response.css(".props .link-overlay")
        if not room_items:
            raise CloseSpider("No more room items to scrape")
        for item in room_items:
            room_href = item.css("::attr(href)").get()
            yield response.follow(room_href, callback=self.parse_room_detail)

    def parse_room_detail(self, response):
        item = RoomItem()

        # Địa chỉ: Võ Chí Công, Phường Nghĩa Đô, Quận Cầu Giấy, Hà Nội
        address = response.css(".address::text").get()
        address = address.split(",")
        item["street"] = address[0].strip()
        item["ward"] = address[1].strip()
        item["district"] = address[2].strip()

        # Giá: 3 triệu 800 nghìn
        price_str = response.css("div.price:nth-child(3)::text").get()
        item["price"] = price_conversion(price_str)

        # Diện tích:  20 m2
        area_str = response.css("div.info-attr:nth-child(1) > span:nth-child(2)::text").get()
        item["area"] = int(area_str.split()[0])

        # Ngày đăng: 05/04/2024
        post_date_str = response.css("div.info-attr:nth-child(3) > span:nth-child(2)::text").get()
        item["post_date"] = date_conversion(post_date_str)

        # Mô tả
        desc_str = response.css(".info-content-body::text").getall()
        item["description"] = ' '.join(desc_str)

        # Link
        item["url"] = response.url

        # Điền các trường còn thiếu
        item["num_bedroom"] = 0
        item["num_diningroom"] = 0
        item["num_kitchen"] = 0
        item["num_toilet"] = 0
        item["num_floor"] = 0
        item["current_floor"] = 0
        item["direction"] = ""
        item["street_width"] = 0

        yield item
