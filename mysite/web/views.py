from django.shortcuts import render
from django.http import HttpResponse
import requests
import time

# ===== simple memory cache =====
CACHE = {
    "news": None,
    "time": 0
}

CACHE_TTL = 60  # 60 秒 cache（避免被 Google 擋）

def news(request):
    global CACHE

    # ===== cache hit =====
    if CACHE["news"] and (time.time() - CACHE["time"] < CACHE_TTL):
        return HttpResponse(
            CACHE["news"],
            content_type="application/xml; charset=utf-8"
        )

    url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)

        # ⚠️ Google 有時回 HTML block page
        if "<rss" not in r.text.lower():
            raise Exception("Invalid RSS response (blocked or changed)")

        CACHE["news"] = r.text
        CACHE["time"] = time.time()

        return HttpResponse(
            r.content,
            content_type="application/xml; charset=utf-8"
        )

    except Exception as e:
        fallback = f"""
        <rss>
            <channel>
                <title>Error</title>
                <item>
                    <title>RSS Load Failed: {str(e)}</title>
                </item>
            </channel>
        </rss>
        """

        return HttpResponse(
            fallback,
            content_type="application/xml",
            status=200
        )


def home(request):
    return render(request, "web/home.html")

