def price_convert(price_str):
    # price_in_str = "3 triệu 800 nghìn" -> 3.8
    # price_in_str = "3 triệu" -> 3.0
    # price_in_str = "700.000 đ" -> 0.7
    price_split = price_str.split()

    if price_split[1] == "đ":
        millions, thousands = 0, float(price_split[0].replace('.', '')) / 1000
    else:
        try:
            millions, thousands = int(price_split[0]), int(price_split[2])
        except IndexError:
            millions, thousands = int(price_split[0]), 0

    return millions + thousands / 1000
