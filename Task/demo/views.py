from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import traceback

from .models import User
from .models import Document

# This method is used for both the cases for POST and GET
@csrf_exempt
def index(request):

    if request.method == 'POST':
        status = ""

        try:
            requestData = json.loads(request.body)
        except:
            requestData = request.POST

        mobile = requestData.get('mobile',None)
        types = requestData.get('type','Document')
        source_type = requestData.get('source_type',None)
        source_id = requestData.get('source_id',None)
        input_meta_data = requestData.get('meta_data',dict())

        try:
            user_obj = User.objects.get(mobile=mobile)

            document_chck = Document.objects.filter(owner = user_obj,source_id = source_id)

            if document_chck.count() < 1:

                document_obj = Document.objects.get_or_create(owner = user_obj,types=types,source_type=source_type,
                source_id=source_id,input_meta_data=input_meta_data)

                status = 'Created successfully'
            else:
                status = 'User with same source id exists'

        except Exception as e:
            status = 'User not found'
        
        
        return JsonResponse({'status':status},status=200)

    elif request.method == 'GET':

        document_obj = Document.objects.all()
        data = list(document_obj.values())

        status = 'success'
        return JsonResponse({'status':status,'data':data},status=200)



# This method is used for Delete Data
@csrf_exempt
def delete(request,mobile,id):
    status = ''
    try:
        document_obj = Document.objects.get(owner__mobile=mobile,source_id=id)
        document_obj.delete()
        status = 'Deleted successfully'
    except Exception as e:
        traceback.print_exc()
        status = 'Document Not Found'

    return JsonResponse({'status':status})


