from library.db import *
from library.get_info import *

ipo = MYSQL_CONNECT('ipo')
old_code = ipo.data_select("ipo_list", "code")
get_info = GET_ALL_INFO()
url_list = get_info.get_url()
code_list = []
for url in url_list:
    html = get_info.parse_html(url)
    code_list.append(get_info.get_code(html))
new_code = code_list
# print(old_code)
# print(new_code)
insert_code = ipo.key_compare(old_code,new_code)[1]
# print(insert_code)
all_info = []
for url in url_list:
    info = get_info.all_crawl(url)
    all_info.append(info)

# 새로 생성된 데이터 넣기
info_list = []
for info in all_info:
    if info.get('code') in insert_code:
        print(list(info.values()))
        ipo.data_insert('ipo_list', list(info.values()))
        info_list.append(info)
# print(info_list)
# ipo.data_insert('ipo_list', info_list)

#기존 데이터 업데이트
update_code = ipo.key_compare(old_code,new_code)[0]
update_list = []
for info in all_info:
    code = info.get('code')
    if code in update_code:
        del info['code']
        ipo.data_update('ipo_list', code, list(info.values()))



# print(ipo.key_compare(old_code, new_code))