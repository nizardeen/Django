from django.shortcuts import render

# Create your views here.
from datetime import datetime
import traceback
from django.http import JsonResponse

@csrf_exempt
def index(request):

	return JsonResponse()