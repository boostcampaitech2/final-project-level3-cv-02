import pymysql
import csv
import os
from dotenv import load_dotenv

class DBController:
	def __init__(self):
		load_dotenv(
			dotenv_path="/opt/ml/final-project-level3-cv-02/.env",
			override=True,
			verbose=False
			)
		self.connect = pymysql.connect(
			user=os.getenv('MYSQL_USER'), 
			passwd=os.getenv('MYSQL_PASSWORD'), 
			host=os.getenv('MYSQL_SERVER'),
			db=os.getenv('MYSQL_DB'), 
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
		with open('./csv/data.csv','w', newline='') as f: # airflow/csv 
			w = csv.writer(f)
			w.writerow(self.col_name)
			for i in range(len(self.res)):
				w.writerow(self.res[i])

	def save_data(self):
		sql = ''
		self.cursor.execute(sql)
		col_name = self.cursor.fetchall()

# test = DBController()
# test.load_data()
# test.out_csv()