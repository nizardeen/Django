from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from datetime import datetime
import traceback
from django.http import JsonResponse
from . import stock

global_stocks = None


@csrf_exempt
def index(request):

	return render_to_response('index.html',{})


@csrf_exempt
def getStocksData(request):
	symbols_list = None
	try:
	    requestData = json.loads(request.body)
	except:
	    requestData = request.POST

	try:
		date = requestData.get('date',datetime.strftime(datetime.now(), '%d-%b-%Y'))
		days = requestData.get('days',5)
		
		dates_opt = datetime.strptime(date.upper(), '%d-%b-%Y')
		stock_obj = stock.Stocks(dates_opt)
		stocks,unavailable_dates = stock_obj.get_prev_days_stocks(int(days))

		global global_stocks
		global_stocks = stocks

		symbol_list = stocks.SYMBOL.unique().tolist()

	except Exception as e:
		traceback.print_exc()

	return JsonResponse({"status":'success',"symbols":symbol_list},status=200)


@csrf_exempt
def getSymbolData(request):

	global global_stocks

	try:
	    requestData = json.loads(request.body)
	except:
	    requestData = request.POST

	symbol = requestData.get('symbol',None)
	data_stocks = global_stocks.loc[global_stocks.SYMBOL == symbol].reset_index()


	symbol_stocks = dict()
	for index, rows in data_stocks.iterrows():
		symbol_stocks.update({int(index)+1:{"SYMBOL":rows.SYMBOL,"SERIES":rows.SERIES,"OPEN":rows.OPEN,"HIGH":rows.HIGH,
			"LOW":rows.LOW,"CLOSE":rows.CLOSE,"LAST":rows.LAST,"PREVCLOSE":rows.PREVCLOSE,"TOTTRDQTY":rows.TOTTRDQTY,"TIMESTAMP":rows.TIMESTAMP}})


	return render(request, 'data_table.html', {'stocks':symbol_stocks})