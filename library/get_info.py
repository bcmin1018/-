import requests
import time
import datetime
from multiprocessing import Pool
from bs4 import BeautifulSoup

class GET_ALL_INFO:
    def __init__(self):
        self.url_list = self.get_url()
        self.date_setting()

    # 종목 URL 가져오기
    def get_url(self):
        url = 'http://www.38.co.kr/html/fund/'
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        href = soup.find('table', {'summary': '공모주 청약일정'}).find_all('a', href=True)
        href_list = []
        for i in href:
            if 'index' not in i['href']:
                href_list.append('http://www.38.co.kr' + i['href'])
        return href_list

    def parse_html(self, url):
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        return soup

    def all_crawl(self, url):
        soup = self.parse_html(url)
        code = self.get_code(soup)
        name = self.get_name(soup)
        sector = self.get_sector(soup)
        days = self.get_days(soup)
        debut = self.get_debut_days(soup)
        price = self.get_ipo_price(soup)
        capital = self.get_capital(soup)
        profit = self.get_profit(soup)
        company = self.get_ipo_company(soup)
        limit = self.get_limit(soup)
        time = self.today_detail
        info_dict = {
            'code': code,
            'name': name,
            'sector': sector,
            'days': days,
            'debut': debut,
            'price': price,
            'capital': capital,
            'profit': profit,
            'company': company,
            'limit': limit,
            'time': time
        }
        # info = [code, name, sector, days, debut, price, capital, profit, company, limit, time]
        return info_dict

    def multi_process(self, func, list):
        start_time = time.time()
        pool = Pool(processes=4)
        info_list = pool.map(func, list)
        pool.close()
        pool.join()
        print("크롤링 종료")
        print("크롤링 소요 시간", time.time() - start_time)
        return info_list

    def date_setting(self):
        self.today = datetime.datetime.today().strftime("%Y%m%d")
        self.today_detail = datetime.datetime.today().strftime("%Y%m%d%H%M")
        self.today_date_form = datetime.datetime.strptime(self.today, "%Y%m%d").date()

    #종목코드 가져오기
    def get_code(self, soup):
        try:
            table = soup.find('table', {'summary': '기업개요'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 1:
                    tds = tr.find_all('td')
                    code = tds[3].text.strip()
            return code
        except AttributeError:
            pass

        # 종목명 가져오기
    def get_name(self, soup):
        try:
            table = soup.find('table', {'summary': '기업개요'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 0:
                    tds = tr.find_all('td')
                    #                 item_col = tds[0].text
                    item_name = tds[1].text.strip()

            return item_name
        except AttributeError:
            pass

    # 업종 가져오기
    def get_sector(self, soup):
        try:
            table = soup.find('table', {'summary': '기업개요'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 2:
                    tds = tr.find_all('td')
                    sector = tds[1].text.strip()

            return sector
        except AttributeError:
            pass

    # 자본금 가져오기
    def get_capital(self, soup):
        try:
            table = soup.find('table', {'summary': '기업개요'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 8:
                    tds = tr.find_all('td')
                    capital = tds[3].text.strip()
            return capital
        except AttributeError:
            pass

    # 순이익 가져오기
    def get_profit(self, soup):
        try:
            table = soup.find('table', {'summary': '기업개요'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 8:
                    tds = tr.find_all('td')
                    profit = tds[1].text.strip()
            return profit
        except AttributeError:
            pass

    # 공모청약일 가자오기
    def get_days(self, soup):
        try:
            table = soup.find('table', {'summary': '공모청약일정'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 1:
                    tds = tr.find_all("td")
                    #                 ipo_col = tds[0].text
                    ipo_days = tds[1].text.strip()
                    ipo_days = ipo_days.split('~')[1].strip()
                    # ipo_days = datetime.datetime.strptime(ipo_days, '%Y.%m.%d' ).date()
            return ipo_days
        except AttributeError:
            pass

    # 상장일 가져오기
    def get_debut_days(self, soup):
        try:
            table = soup.find('table', {'summary': '공모청약일정'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 5:
                    tds = tr.find_all("td")
                    #                 debut_col = tds[0].text
                    debut_days = tds[1].text.strip()
            return debut_days
        except AttributeError:
            pass

    # 확정 공모가 가져오기
    def get_ipo_price(self, soup):
        try:
            table = soup.find('table', {'summary': '공모정보'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                # 확정 공모가
                if idx == 3:
                    tds = tr.find_all("td")
                    #                 price_col = tds[0].text
                    price = tds[1].text.strip()
            return price
        except AttributeError:
            pass

    # 주간사 가져오기
    def get_ipo_company(self, soup):
        try:
            table = soup.find('table', {'summary': '공모정보'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx == 4:
                    tds = tr.find_all("td")
                    #                 company_col = tds[0].text
                    company = tds[1].text.strip()
            return company
        except AttributeError:
            pass

    # 청약한도 가져오기
    def get_limit(self, soup):
        try:
            table = soup.find('table', {'summary': '공모정보'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                # 확정 공모가
                if idx == 4:
                    tds = tr.find_all("td")
                    #                 price_col = tds[0].text
                    limit = tds[2].text.strip().split('/')[1].strip()
            return limit
        except AttributeError:
            pass
