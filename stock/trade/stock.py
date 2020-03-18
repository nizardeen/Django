from zipfile import ZipFile
# from StringIO import StringIO
from datetime import datetime, timedelta
import pandas as pd
# import urllib2
import requests,io
import traceback



class Stocks:


    def __init__(self, date):
        self.date = date


    def checkTime(self,checkdate):
        check_status = False
        from_date_time = datetime.now()

        if checkdate.date() == from_date_time.date():

            # The file uploading time will be around 18:15 P.M on the nseindia website
            today_evng = from_date_time.replace(hour=18, minute=30, second=0, microsecond=0)

            if from_date_time > today_evng:
                check_status = True
            else:
                from_date_time = datetime.now() - timedelta(days=1)

        else:
            check_status = True
            from_date_time = checkdate

        return check_status,from_date_time



    def get_prev_days_stocks(self,num_of_days):

        columns_lists = ['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TIMESTAMP']
        stock_pd = pd.DataFrame(columns=columns_lists)
        unavailable_lists = list()
        weekend = set([5, 6])

        status,dates = self.checkTime(self.date)

        if dates == None:
            dates = datetime.now()
        

        for i in range(0,num_of_days):

            date_N_days_ago = dates - timedelta(days=i)
            
            if date_N_days_ago.weekday() not in weekend:
            
                date,month,year = str(datetime.strftime(date_N_days_ago,'%d-%b-%Y')).split('-')
                
                new_date = str(date+month.upper()+year)
                

                try:
                    req = requests.get('https://archives.nseindia.com/content/historical/EQUITIES/'+year+'/'+month.upper()+'/cm'+new_date+'bhav.csv.zip',timeout=2.0)

                    file = ZipFile(io.BytesIO(req.content))
                    
                    stock_csv = file.open("cm"+new_date+"bhav.csv")
                    stocks_df = pd.read_csv(stock_csv,usecols = columns_lists)
                    stock_pd = stock_pd.append(stocks_df)
                except Exception as e:
                    print('Exception occurred')
                    unavailable_lists.append(new_date)
                    
                else:
                    pass


        return stock_pd,unavailable_lists

