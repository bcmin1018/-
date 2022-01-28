import pandas as pd
from library.db import *
from library.api_spreadsheet import *
from library.crwaling import *

if __name__ == "__main__":
    #DB접속
    ipo = MYSQL_CONNECT('ipo')

    #크롤링
    get_info = GET_ALL_INFO()

    #DB에 저장된 code 가져오기
    old_code = ipo.data_select('ipo_list', 'code')

    #웹에서 현재 code 가져오기
    url_list = get_info.get_url()
    new_code = []
    for url in url_list:
        html = get_info.parse_html(url)
        new_code.append(get_info.get_code(html))

    #update, insert 코드 분류
    insert_code = ipo.key_compare(old_code, new_code)[1]
    print('새로 생긴 코드 목록 : ', insert_code)
    update_code = ipo.key_compare(old_code, new_code)[0]
    print('기존 코드 목록 : ', update_code)

    #대상 정보 모두 크롤링
    all_info = []
    for url in url_list:
        info = get_info.all_crawl(url)
        all_info.append(info)

    #new_code insert
    for info in all_info:
        if info.get('code') in insert_code:
            ipo.data_insert('ipo_list', list(info.values()))

    #old_code update
    for info in all_info:
        code = info.get('code')
        if code in update_code:
            del info['code']
            ipo.data_update('ipo_list', code, list(info.values()))

    result = ipo.data_select('ipo_list', option='all')
    c_name = ['코드', '종목명', '업종', '공모청약일', '상장일', '확정 공모가', '자본금', '손익', '주간사', '청약한도', '시간']
    df = pd.DataFrame(result, columns=c_name)
    del_data = spreadsheet().clear_sheet('대시보드')
    data = spreadsheet().data_insert(df, '대시보드')
    print('업데이트를 완료하였습니다.')