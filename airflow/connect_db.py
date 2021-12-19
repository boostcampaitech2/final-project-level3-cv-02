import pymysql
import csv
import os

class DBController:
	def __init__(self, user='cv02', pw='boostcampcv02', host='cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com', db='cv02'):
		self.connect = pymysql.connect(
			user=user, 
			passwd=pw, 
			host=host, 
			db=db, 
			charset='utf8'
		)
		self.cursor = self.connect.cursor()
		self.col_name = []
		self.res = []

	def createDirectory(self, directory = './csv'):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print("Error: Failed to create the directory.")

	
	def load_data(self):
		sql = 'SHOW FULL COLUMNS FROM inference_result;'
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		for i in range(len(rows)):
			self.col_name.append(rows[i][0])
		sql = 'SELECT * FROM inference_result;'
		self.cursor.execute(sql)
		rows = list(self.cursor.fetchall())
		for i in range(len(rows)):
			self.res.append(list(rows[i]))

	def out_csv(self):
		self.createDirectory()
		with open('./csv/data.csv','w', newline='') as f:
			w = csv.writer(f)
			w.writerow(self.col_name)
			for i in range(len(self.res)):
				w.writerow(self.res[i])

	def save_data(self):
		sql = ''
		self.cursor.execute(sql)
		col_name = cursor.fetchall()

# test = DBController()
# test.load_data()
# test.out_csv()