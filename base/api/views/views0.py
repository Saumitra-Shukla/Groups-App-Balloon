from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Item
from api.serializers import ItemSerializer


@csrf_exempt
def item_list(request,pk=0):
    """
    List all code item, or create a new sitem.
    """
    if request.method == 'GET':
        items = Item.objects.all()
        if int(pk) > 0 :
        	items=Item.objects.filter(pk=pk)
        serializer = ItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)