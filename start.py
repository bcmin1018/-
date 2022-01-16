import pandas as pd
from library.get_info import *
from library.api_spreadsheet import *
from library.crwaling import *
from library.db import *

a = get_all_info()

def crawl(url):
    last_list=[]
    for i in url:
        parsed = a.parsing(i)
        code = a.get_code(parsed)
        name = a.get_name(parsed)
        sector = a.get_sector(parsed)
        days = a.get_days(parsed)
        debut = a.get_debut_days(parsed)
        price = a.get_ipo_price(parsed)
        capital = a.get_capital(parsed)
        profit = a.get_profit(parsed)
        company = a.get_ipo_company(parsed)
        limit = a.get_limit(parsed)
        # fixing
        # temp_list = (code, name, sector, days, debut, price, capital, profit, company, limit)
        temp_list = [name, sector, days, debut, price, capital, profit, company, limit, code]
        last_list.append(temp_list)
    return last_list

url = a.get_url()
last_list = crawl(url)
# print(last_list)

#fixing
# ipo_insert = mysql_connect('ipo')
# ipo_insert.data_insert('ipo_list', last_list)

c_name = ['종목명', '업종', '공모청약일','상장일', '확정 공모가', '자본금', '손익', '주간사', '청약한도', '코드']
df = pd.DataFrame(last_list, columns=c_name)

del_data = spreadsheet().clear_sheet('대시보드')
data = spreadsheet().data_insert(df, '대시보드')
print('업데이트를 완료하였습니다.')