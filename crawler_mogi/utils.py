from datetime import datetime

def address_conversion(address_str):

    def clean(str, pat):
        res = str
        for p in pat:
            if p in str:
                res = str.split(p)[-1]
                break
        return res.lstrip('0123456789/ ')

    address_parts = address_str.split(",")
    street = clean(address_parts[-4], ["Phố", "Đường", "phố", "đường", "Ngõ", "ngõ", "Ngách", "ngách"])
    ward = clean(address_parts[-3], ["Phường", "Xã", "phường", "xã",])
    district = clean(address_parts[-2], ["Quận", "Huyện", "quận", "huyện"])

    return street, ward, district


def price_conversion(price_str):
    # price_in_str = "3 triệu 800 nghìn" -> 3.8
    # price_in_str = "3 triệu" -> 3
    # price_in_str = "700.000 đ" -> 0.7
    price_split = price_str.split()
    millions = float(price_split[0].replace('.', ''))
    try:
        thousands = int(price_split[2])
    except IndexError:
        thousands = 0
    return millions + thousands / 1000


def date_conversion(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")
    converted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return converted_date
