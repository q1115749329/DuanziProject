from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import sqlite3
import json
# Create your views here.

def index(request):
    return render(request,"index.html")

def search(request):
    page = request.GET.get("page","1")
    page = int(page)
    con = sqlite3.connect("duanzi.db")
    cur = con.cursor()
    cur.execute("select text,user_name from duanzi_db limit {},20".format((page-1)*20))
    result = cur.fetchall()
    cur.execute("select count(*) from duanzi_db")
    total_page = cur.fetchone()[0]
    total_page = int(total_page)
    if total_page%10==0:
        total_page = total_page//10
    else:
        total_page = total_page//10 +1
    start_page = page -6
    if start_page <=0:
        start_page = 0
    end_page = page +4
    if start_page==0:
        end_page=10
    if end_page > total_page:
        end_page = total_page
        start_page = end_page -10
    pages = range(total_page)[start_page:end_page]
    list1 = [x for x in pages]
    info = {
        "result":result,
        "list1":list1
    }
    return HttpResponse(json.dumps(info),content_type="application/json")
