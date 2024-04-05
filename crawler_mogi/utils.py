from datetime import datetime


def price_conversion(price_str):
    # price_in_str = "3 triệu 800 nghìn" -> 3.8
    # price_in_str = "3 triệu" -> 3
    price_split = price_str.split()
    millions = int(price_split[0])
    try:
        thousands = int(price_split[2])
    except IndexError:
        thousands = 0
    return millions + thousands / 1000


def date_conversion(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")
    converted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return converted_date


if __name__ == "__main__":
    print(date_conversion("15/12/2002"))
