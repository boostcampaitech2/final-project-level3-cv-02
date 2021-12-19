import pymysql
import pandas as pd

class DBController:
	def __init__(self, user='cv02', pw='boostcampcv02', host='cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com', db='cv02'):
		self.connect = pymysql.connect(
			user=user, 
			passwd=pw, 
			host=host, 
			db=db, 
			charset='utf8'
		)
		self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)
	
	def load_data(self):
		sql = 'SELECT * FROM inference_result;'
		self.cursor.execute(sql)
		res = cursor.fetchall()

	def out_csv(self), result):
		with open('mycsvfile.csv','w') as f:
			w = csv.writer(f)
			w.writerow(result.keys())
			w.writerow(result.values())

	def save_data(self):
		sql = ''
		self.cursor.execute(sql)
		res = cursor.fetchall()

	