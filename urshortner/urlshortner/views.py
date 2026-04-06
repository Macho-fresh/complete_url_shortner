from django.shortcuts import render
from .models import Url
from .serializers import UrlSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
OFFSET = 1000000

def encode_base62(num):
    num += OFFSET
    value = ''

    while num > 0:
        remainder = num % 62
        value = CHARS[remainder] + value  
        num //= 62
    return value

def decode_base62(str):
    num = 0
    for i in str:   
        num = num * 62 + CHARS.index(i) 
        print(num)
    return num - OFFSET    

class UrlView(generics.ListCreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        url_obj = serializer.save()
        url_obj.shorturl = encode_base62(url_obj.id)
        url_obj.save()

        return Response({
            'id': url_obj.id,
            "long_url": url_obj.longurl,
            "short_url": request.build_absolute_uri('/') + url_obj.shorturl,
            "createdAt": url_obj.createdAt,
            "updatedAt": url_obj.updatedAt,
            "clickcount": url_obj.click_count
        },status=status.HTTP_201_CREATED)

def redirect_url(request, shorturl):
    url_obj = get_object_or_404(Url, shorturl = shorturl)

    url_obj.click_count += 1
    url_obj.save()
    return redirect(url_obj.longurl)

class show_url(generics.RetrieveAPIView):
    serializer_class = UrlSerializer
    queryset = Url.objects.all()
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
       
        url_obj = self.get_object()
        return Response({
            'id': url_obj.id,
            "long_url":   url_obj.longurl,
            "short_url":  request.build_absolute_uri('/') + url_obj.shorturl,
            "createdAt":  url_obj.createdAt,
            "updatedAt":  url_obj.updatedAt,
            "clickcount": url_obj.click_count
        },status=status.HTTP_201_CREATED)

        
class update_url(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    lookup_field = 'id'

        