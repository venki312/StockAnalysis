import argparse
import requests
import os
import pandas as pd

class Company:

	def __init__(self, open_high_diff, last_no_of_days):

		self.open_high_diff = open_high_diff
		self.last_no_of_days = last_no_of_days

	def get_open_high_diff(self, company, type='NS'):

		url = self.get_url(company, type)
		r = requests.get(url, allow_redirects=True)

		home = os.path.expanduser("~")
		file_path = os.path.join(home, "Downloads/")

		open(file_path+company+'.'+type+'.csv', 'wb').write(r.content)

		#read the CSV file downloaded
		df_read = pd.read_csv(file_path+company+"."+type+".csv")

		col_list = ["Open", "High"]
		StockDfObj = pd.DataFrame(df_read, columns=col_list)

		#applying filter based on the high and open value difference
		seriesObj = StockDfObj.apply(lambda x: True if x['High'] - x['Open'] > int(self.open_high_diff) else False , axis=1)
		seriesObj = seriesObj.head(int(self.last_no_of_days))

		numOfRows = len(seriesObj[seriesObj == True].index)

		#returning the number of rows which has high to open value > specified value
		return numOfRows

	def get_url(self, company, type):
		try:
			return "https://query1.finance.yahoo.com/v7/finance/download/"+company+"."+type+"?period1=1567765404&period2=1599387804&interval=1d&events=history"
		except Exception:
			print("{0} data not appicable for this company".format(type))
			pass


if __name__=="__main__":

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--list", nargs="+", default=["HDFC", 3, 15])
	args = parser.parse_args()
	print("See below {0} company with {1} as high to open diff in {2} days".format(args.list[0], args.list[1], args.list[2]))

	c1 = Company(args.list[1], args.list[2])
	result = c1.get_open_high_diff(args.list[0])
	print("NSE high to open diff is {0} for {1} in last {2} days".format(args.list[1], result, args.list[2]))

	c2 = Company(args.list[1], args.list[2])
	result = c2.get_open_high_diff(args.list[0], type='BO')
	print("BSE high to open diff is {0} for {1} in last {2} days".format(args.list[1], result, args.list[2]))
