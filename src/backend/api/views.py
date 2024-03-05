from pprint import pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from scraper.scraper import Weather_API


# Create your views here.
@api_view(['GET'])
def getData(request, location):
    print(request)
    response = Weather_API(location).get_weather_result()
    # pprint(response)
    return Response(response)