import json
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

from api.authentication import TokenAuthentication

from products.models import Product
from products.serializers import ProductSerializer

@api_view(["GET"])
def api_home(request,*args,**kwargs):
	instance = Product.objects.all().order_by('?').first()
	data = {}
	if instance:
		data = model_to_dict(instance, fields=['id','title', 'price'])
		print(f'non-serialized: {model_to_dict}')
		data_serialized = ProductSerializer(instance).data
		print(f'serialized: {data_serialized}')
	return Response(data_serialized)

@api_view(["POST"])
def api_home_save(request,*args,**kwargs):
	print(request.data)
	serializer = ProductSerializer(data=request.data)
	if serializer.is_valid(raise_exception=True):
		data = serializer.save()
		return Response(serializer.data)
	return Response({"Invalid":"Data format incorrect"},status=400)