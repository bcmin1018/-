from library import cf
from sqlalchemy import create_engine
import pymysql
import datetime
pymysql.install_as_MySQLdb()

class mysql_connect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_conn = pymysql.connect(host=cf.db_ip,
                                       port=int(cf.db_port),
                                       user=cf.db_id,
                                       password=cf.db_passwd,
                                       charset='utf8')
        self.engine_setting()

    def engine_setting(self):
        self.db_engine = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/ipo",
            encoding='utf-8')

    def create_database(self):
        # if self.chk_database_exist() == False:
        sql = 'CREATE DATABASE %s'
        self.db_conn.cursor().execute(sql % (self.db_name))
        self.db_conn.commit()
        print("데이터베이스 생성 완료하였습니다.")
        # else:
        #     print("기존 데이터베이스가 존재합니다.")

    def drop_database(self):
        sql = 'DROP DATABASE %s'
        self.db_conn.cursor().execute(sql % (self.db_name))
        self.db_conn.commit()
        print('티이블 drop에 성공했습니다.')

    def chk_database_exist(self):
        sql = "SELECT 1 FROM Information_schema.SCHEMATA WHERE SCHEMA_NAME = '%s'"
        rows = self.db_engine.execute(sql % (self.db_name)).fetchall()
        print("rows : ", rows)
        if len(rows):
            return True
        else:
            return False

    def date_setting(self):
        self.today = datetime.datetime.today().strftime("%Y%m%d")
        self.today_detail = datetime.datetime.today().strftime("%Y%m%d%H%M")
        self.today_date_form = datetime.datetime.strptime(self.today, "%Y%m%d").date()

    def create_table(self, table_name):
        sql = '''create table %s.%s (
            code varchar(255) NOT NULL PRIMARY KEY, 
            item_name varchar(255),
            sector varchar(255), 
            ipo_days varchar(255),
            debut_days varchar(255),
            ipo_price varchar(255), 
            capital varchar(255), 
            profit varchar(255), 
            company varchar(255), 
            limit_ varchar(255)
            )'''
        self.db_conn.cursor().execute(sql % (self.db_name, table_name))
        self.db_conn.commit()
        print("테이블 생성 완료하였습니다.")

    def table_setting(self):
        print("self.simul_reset" + str(self.simul_reset))
        # 시뮬레이터를 초기화 하고 처음부터 구축하기 위한 로직
        if self.simul_reset:
            print("table reset setting !!! ")
            self.init_database()
        # 시뮬레이터를 초기화 하지 않고 마지막으로 끝난 시점 부터 구동하기 위한 로직
        else:
            # self.simul_reset 이 False이고, 시뮬레이터 데이터베이스와, all_item_db 테이블, jango_table이 존재하는 경우 이어서 시뮬레이터 시작
            if self.is_simul_database_exist() and self.is_simul_table_exist(self.db_name,
                                                                            "all_item_db") and self.is_simul_table_exist(
                self.db_name, "jango_data"):
                self.init_df_jango()
                self.init_df_all_item()
                # 마지막으로 구동했던 시뮬레이터의 날짜를 가져온다.
                self.last_simul_date = self.get_jango_data_last_date()
                print("self.last_simul_date: " + str(self.last_simul_date))
            #    초반에 reset 으로 돌다가 멈춰버린 경우 다시 init 해줘야함
            else:
                print("초반에 reset 으로 돌다가 멈춰버린 경우 다시 init 해줘야함 ! ")
                self.init_database()
                self.simul_reset = True


