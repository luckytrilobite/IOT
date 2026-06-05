from django.shortcuts import render
from django.http import HttpResponse
import requests

def news(request):
    url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    return HttpResponse(r.text, content_type="application/xml")

def home(request):
    return render(request, "web/home.html")

