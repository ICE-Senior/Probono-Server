from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps

# Mongo DB
from config import utils

# Session
from django.contrib.auth import login, logout

# User
from .models import CustomUser
from .forms import SignUpForm


db_handle = utils.db_handle
get_collection = utils.get_collection_handle

def index(request):
    return render(request, 'index.html')

def my_page(request):
    return render(request, 'my_page.html')

def transfer_info(request):
    return render(request, 'transfer_info.html')

def weather_info(request):
    return render(request, 'weather_info.html')

def dense_popul_info(request):
    return render(request, 'dense_popul_info.html')

def safety_info(request):
    return render(request, 'safety_info.html')

@require_POST
def login_view(request):
    users = get_collection(db_handle, 'User')
    user_id = request.POST.get('username') # WARN : front's parameter name
    password = request.POST.get('password')
    user_info = users.find_one({'id' : user_id})
    if user_info:
        if (password == user_info['pw']):
            login(request, user_info)
            return redirect('index')
        else:
            data = { "message": "wrong pw" }
    else:
        data = { "message": "wrong id" }
    status_code = 201
    JsonResponse(data, status=status_code)

@require_POST
def sign_up(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        users = get_collection(db_handle, 'User')
        users.insert_one(form)
    return redirect('index')

@require_POST
def id_duplicate(request):
    users = get_collection(db_handle, 'User')
    temp = users.find_one({'ID' : request.form['check_id']})
    if temp:
        data = { "message": "id duplicated" } # REMIND : front have to know its response.
        status_code = 201
    else:
        status_code = 201
    return JsonResponse(data, status=status_code)

def logout_view(request):
    logout(request)
    return redirect('index')

@require_POST
def get_subway_elvtr(request):
    collection_elvtr = get_collection(db_handle, 'subway_elevator')
    search = request.POST.get('name')
    result = collection_elvtr.find({ 'sw_nm' : search })
    result = list(result)
    if not result:
        return JsonResponse({ 'message' : 'No results' })
    return JsonResponse({ 'result' : result})

def get_bus_no_to_route(request):
    
    return

def get_bus_station_to_no(request):
    

    
    
    return


def get_safety_guard_house(request):
    base_url="http://api.data.go.kr/openapi/tn_pubr_public_female_safety_prtchouse_api"
    start_index=1
    end_index=4
    all_data=[]
    params={'serviceKey' : 'z3tbVitFT7XffZ43RQ9sMyE0ALiv+EtqOysMUKPdg9E5zTIL3lNVHqGCOS9vPqq73zYw6OhwHiskVZj4MYCJ0w==',
            'pageNo' : start_index,
            'numOfRows' : end_index,
            'type' : 'json' }
    print('sibal')
    response = requests.get(base_url,params=params)
    data = response.json()
    print(data)
    if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
        items = data['response']['body']
        print(len(items))
    
    #data = loads(data)

    # while True:
    #     params={'serviceKey' : 'z3tbVitFT7XffZ43RQ9sMyE0ALiv+EtqOysMUKPdg9E5zTIL3lNVHqGCOS9vPqq73zYw6OhwHiskVZj4MYCJ0w==',
    #             'pageNo' : start_index,
    #             'numOfRows' : end_index,
    #             'type' : 'json' }
    #     response = requests.get(base_url,params=params)
    #     data = response.json() 
    #     print(data)
    #     # if 'response' in data and 'body' in data['response']:
    #     #     all_data.extend(data['response']['body'])
    #     #     body=data['response']['body']
    #     if data['response']['header']['resultCode']=='03': # 데이터가 없을 떄 resultCode=03
    #         break
            
    #     start_index += 1
        
    print(all_data)
        
    return render(request,'index.html')