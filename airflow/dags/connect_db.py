import pymysql
import csv
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

class DBController:
	def __init__(self):
		load_dotenv(
			dotenv_path="/opt/ml/final-project-level3-cv-02/.env",
			override=True,
			verbose=False
			)

		self.MYSQL_USER = os.getenv('MYSQL_USER')
		self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
		self.MYSQL_PORT = os.getenv('MYSQL_PORT')
		self.MYSQL_DB = os.getenv('MYSQL_DB')
		self.MYSQL_SERVER = os.getenv('MYSQL_SERVER')

		self.DB = pymysql.connect(
			user=self.MYSQL_USER, 
			passwd=self.MYSQL_PASSWORD, 
			host=self.MYSQL_SERVER,
			db=self.MYSQL_DB, 
			charset='utf8'
		)

	def createDirectory(self, directory = './csv'):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print("Error: Failed to create the directory.")

	
	def load_data(self, table_name):
		self.data = pd.read_sql(f'''select * from {table_name};''', con = self.DB)
		return

	def out_csv(self):
		self.createDirectory()
		self.data.to_csv('./csv/data.csv', index=False) # airflow/csv 
		return
		

	def save_data_to_db(self, df, table_name):
		engine = create_engine(f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4')
		engine_conn = engine.connect()
		df.to_sql(table_name , engine_conn, if_exists='replace', index=None)
		engine_conn.close()
		engine.dispose()


# if __name__ == '__main__':
# 	test = DBController()
# 	table = 'inference_result'
# 	test.load_data(table)
# 	test.out_csv()
	