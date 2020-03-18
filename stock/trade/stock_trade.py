from zipfile import ZipFile
# from StringIO import StringIO
from datetime import datetime, timedelta
import pandas as pd
# import urllib2
import requests,io



date_N_days_ago = datetime.now() - timedelta(days=29)

print(datetime.strftime(datetime.now(), '%d-%b-%Y'))
print(datetime.strftime(date_N_days_ago,'%d-%b-%Y'))

stock_pd = pd.DataFrame(columns=None)
stocks = None


weekend = set([5, 6])


def get_last_stocks():

	# current_time = datetime.strptime(datetime.strftime(datetime.now(), '%H:%M:%S'),"%H:%M:%S").time()
	current_time = datetime.now()
	# current_time = datetime.time(current_time.hour, current_time.minute,current_time.second)
	today3pm = current_time.replace(hour=15, minute=30, second=0, microsecond=0)

	if current_time > today3pm:
		print('jijij')


	for i in range(0,30):
		date_N_days_ago = datetime.now() - timedelta(days=i)


		if date_N_days_ago.weekday() not in weekend:
			# print(str(datetime.strftime(date_N_days_ago,'%d-%b-%Y')),'weekends')
		
			if current_time < today3pm:

				date,month,year = str(datetime.strftime(date_N_days_ago,'%d-%b-%Y')).split('-')
				print(date,month,year)
				new_date = str(date+month.upper()+year)
				print(new_date)


				req = requests.get('https://archives.nseindia.com/content/historical/EQUITIES/'+year+'/'+month.upper()+'/cm'+new_date+'bhav.csv.zip')

				file = ZipFile(io.BytesIO(req.content))
				print(file)
				stock_csv = file.open("cm"+new_date+"bhav.csv")
				stocks_df = pd.read_csv(stock_csv,usecols = ['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TIMESTAMP'])
				stocks = pd.concat([stock_pd,stocks_df],axis=0)

			else:
				pass


print(get_last_stocks())

print(stock_pd.shape)