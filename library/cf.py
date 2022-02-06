import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = '/home/centos/key/concise-isotope-289621-719ca53eca75.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1oy5IjQGC1LxloIxeWmXA-4KMH6o0zSYPu2_NN9IQjxo/edit#gid=0'

db_ip = 'localhost'
db_port = '3306'
db_id = 'root'
db_passwd =''