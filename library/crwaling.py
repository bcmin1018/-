from library.get_info import *

def crawl(url):
    last_list=[]
    for i in url:
        parsed = a.parsing(i)
        name = a.get_name(parsed)
        sector = a.get_sector(parsed)
        days = a.get_days(parsed)
        debut = a.get_debut_days(parsed)
        price = a.get_ipo_price(parsed)
        capital = a.get_capital(parsed)
        profit = a.get_profit(parsed)
        company = a.get_ipo_company(parsed)
        limit = a.get_limit(parsed)
        temp_list = [name, sector, days, debut, price, capital, profit, company, limit]
        last_list.append(temp_list)
    return last_list