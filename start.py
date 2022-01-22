import pandas as pd
from library.db import *
from library.api_spreadsheet import *
from library.crwaling import *

if __name__ == "__main__":
    info = GET_ALL_INFO()
    result = info.multi_process(info.crawl_info, info.get_url())
    # mysql = MYSQL_CONNECT('ipo')
    # mysql.create_table('ipo_list')
    # mysql.data_insert('ipo_list', result)
    c_name = ['코드', '종목명', '업종', '공모청약일', '상장일', '확정 공모가', '자본금', '손익', '주간사', '청약한도', '시간']
    df = pd.DataFrame(result, columns=c_name)
    del_data = spreadsheet().clear_sheet('대시보드')
    data = spreadsheet().data_insert(df, '대시보드')
    print('업데이트를 완료하였습니다.')