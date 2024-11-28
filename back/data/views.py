from django.shortcuts import render
import json
from .models import Incomepergenderage, Incomeperjob, Incomepergrade  # 대문자로 수정된 모델 임포트
from django.shortcuts import render

from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from django.http import JsonResponse

from .models import DepositOptions, DepositProducts
from .serializers import DepositProductSerializer, DepositOptionSerializer
# Create your views here.

def savedata_view(request):
    with open('data/output_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        temp1 = item.get("2022년 월임금총액 (원)", 0)
        temp2 = item.get("2023년 월임금총액 (원)", 0)
        result = (int(temp1) + int(temp2)) / 2

        new_data = Incomepergenderage(
            gender=item.get('성별', '미정'),
            agerange=item.get("연령별", 0),
            avgallincome=result,
        )
        new_data.save()

    return render(request, 'your_template.html')

def savedata_view2(request):
    with open('data/output_data2.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        new_data = Incomepergrade(
        grade=item.get('학력', '미정'),
        avgincome=item.get("소득", 0),
        )
        new_data.save()

    return render(request, 'your_template2.html')

def savedata_view3(request):
    with open('data/output_data3.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        new_data = Incomeperjob(
        job=item.get('직업', '미정'),
        avgincome=item.get("소득", 0),
        )
        new_data.save()

    return render(request, 'your_template3.html')

@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    # url=f'http://finlife.fss.or.kr/finlife/fdrmDpstApi/list.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    url =f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response =requests.get(url).json()

    # return Response(response)
    
    # print(api_key,1)
    for li in response['result'].get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')
        fin_prdt_nm = li.get('fin_prdt_nm')

        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd):
            continue
        
        save_data = {
            "fin_prdt_cd" : fin_prdt_cd, 
            "kor_co_nm" : kor_co_nm,
            "fin_prdt_nm" : fin_prdt_nm, 
            "etc_note" : etc_note,
            "join_deny" : join_deny,
            "join_member" : join_member,
            "join_way" : join_way,
            "spcl_cnd" : spcl_cnd,
        }
        serializer = DepositProductSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response['result'].get('optionList', []):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm') 
        intr_rate = li.get('intr_rate')
        intr_rate2 = li.get('intr_rate2')
        save_trm = li.get('save_trm')

        if DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd):
            continue

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': intr_rate_type_nm,  
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
        }

        deposit, created = DepositProducts.objects.get_or_create(fin_prdt_cd=fin_prdt_cd)

        serializer = DepositOptionSerializer(data=save_data)  
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=deposit)
            
    return JsonResponse({'message': '저장완료'})  

@api_view(['GET','POST'])
def deposit_products(request):
    if request.method == 'GET':
        depositProducts = DepositProducts.objects.all()
        serializer = DepositProductSerializer(depositProducts,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepositProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    if request.method == 'GET':
        depositOptions = DepositOptions.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializer = DepositOptionSerializer(depositOptions)
        return Response(serializer.data)
    

@api_view(['GET'])
def top_rate(request):
    if request.method == 'GET':
        # deposit  = DepositOptions.objects.order_by('-intr_rate2').first()
        deposit = DepositOptions.objects.select_related('product').order_by('-intr_rate2').first()
        serializer = DepositOptionSerializer(deposit)
        return Response(serializer.data)
    
from django.shortcuts import render
from .models import Card
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from django.core.files.base import ContentFile
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def save_card_data(request):
    def download_image_to_model(image_url, card_name):
        try:
            img_response = requests.get(image_url, stream=True)
            if img_response.status_code == 200:
                # 이미지 파일을 메모리에 저장
                image_content = ContentFile(img_response.content)
                image_name = f"{card_name}.jpg"
                return image_name, image_content
            else:
                print(f"이미지 다운로드 실패: {image_url}")
        except Exception as e:
            print(f"이미지 다운로드 중 오류 발생: {e}")
        return None, None

    def get_all_card_links(driver):
        url = 'https://card-search.naver.com/list?sortMethod=ri&ptn=1&bizType=CPC&companyCode=&brandNames=&benefitCategoryIds=&subBenefitCategoryIds=&affiliateIds=&minAnnualFee=0&maxAnnualFee=0&basePayment=0'
        driver.get(url)  # 페이지 로딩
        time.sleep(2)

        try:
            # "더보기" 버튼이 있는 동안 반복
            while True:
                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # 페이지 끝으로 이동
                    time.sleep(1)

                    # "더보기" 버튼 찾기
                    button = driver.find_element(By.CLASS_NAME, 'more')
                    button.click()
                    print("더보기 버튼 클릭")
                    time.sleep(1)
                except Exception:
                    print('더보기 버튼이 더 이상 없습니다.')
                    break

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            base_url = "https://card-search.naver.com"
            card_links = [
                base_url + anchor["href"]
                for anchor in soup.select("div.info a.anchor")
            ]
            print(f"총 {len(card_links)}개의 카드 링크를 찾았습니다.")

        except Exception as e:
            print(f"링크 가져오기 중 오류 발생: {e}")
        return card_links

    def get_card_details(driver, card_links):
        card_info = []

        try:
            for link in card_links:
                driver.get(link)
                time.sleep(2)

                detail_html = driver.page_source
                detail_soup = BeautifulSoup(detail_html, 'html.parser')

                card_info_div = detail_soup.select_one("div.cardinfo")
                card_info_name = detail_soup.select_one("div.cardname").get_text()
                card_image = detail_soup.select_one("img")['src']
                card_btn = detail_soup.select_one("div.btns > a.apply")['href']

                if card_info_div:
                    image_name, image_content = download_image_to_model(card_image, card_info_name)

                    list_elements = card_info_div.find_all(class_='list')
                    card_data = []

                    for list_item in list_elements:
                        dt_tags = list_item.find_all('dt')
                        dd_tags = list_item.find_all('dd')

                        for dt, dd in zip(dt_tags, dd_tags):
                            dt_text = dt.get_text(strip=True)
                            dd_text = dd.get_text(strip=True)
                            card_data.append({dt_text : dd_text})

                    card_info.append({
                        'url': link,
                        'card_data': card_data,
                        'card_name': card_info_name,
                        'card_image_name': image_name,
                        'card_image_content': image_content,
                        'card_btn': card_btn,
                    })
                    print(f"카드 정보 수집 완료: {link}")
                else:
                    print(f"카드 정보가 없습니다: {link}")
        except Exception as e:
            print(f"카드 상세 정보 수집 중 오류 발생: {e}")

        return card_info

    def save_to_database(card_info):
        for card in card_info:
            card_name = card['card_name']
            card_link = card['url']
            card_apply_link = card['card_btn']
            card_image_name = card['card_image_name']
            card_image_content = card['card_image_content']

            notification = None
            annual_fee = None
            base_performance = None
            base_performance_last_month = None
            merit_summary = None


            for temp in card['card_data']:
                for key, value in temp.items():
                    if key == '공지':
                        notification = value
                    elif key == '연회비':
                        annual_fee = value
                    elif key == '기준실적':
                        base_performance = value  # 기준실적 저장
                    elif key == '전월실적':
                        base_performance_last_month = value  # 전월실적 저장
                    elif key == '혜택요약':
                        merit_summary = value

            card_instance, created = Card.objects.update_or_create(
                card_name=card_name,
                defaults={ 
                    'notification' :notification,
                    'card_link': card_link,
                    'card_apply_link': card_apply_link,
                    'annual_fee': annual_fee,
                    'base_performance': base_performance,
                    'base_performance_last_month': base_performance_last_month,
                    'merit_summary': merit_summary
                }
            )

            # 이미지가 있을 경우 image 필드에 저장
            if card_image_content:
                card_instance.card_image.save(card_image_name, card_image_content)
                card_instance.save()
                print(f"이미지 저장 완료: {card_image_name}")

    # 크롬 드라이버를 한 번만 생성하고, 이후 함수들에 전달
    driver = webdriver.Chrome()
    all_card_links = get_all_card_links(driver)  # 카드 링크를 가져옴
    card_info = get_card_details(driver, all_card_links)  # 각 카드의 상세 정보 수집
    save_to_database(card_info)  # DB에 카드 정보 저장
    
    # 함수가 끝나면 driver.quit()을 호출하여 드라이버 종료
    driver.quit()
    
    return JsonResponse({'status': 'success', 'message': '카드 정보 저장 완료'})

from django.shortcuts import render
import json
from .models import IncomeSpend, Decile_consume, Decile_income

def savedata_view4(request):
    with open('data/output_data4.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        new_data = IncomeSpend(
        per_range = item.get('월소득 10분위별가계수지항목별', '미정'),
        worker= item.get('근로자가구2년평균', 0),
        not_worker=item.get("근로자외가구2년평균", 0),
        )
        new_data.save()

    return render(request, 'your_template4.html')


def savedata_view5(request):
    with open('data/decile_consume.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        new_data = Decile_consume(
        per_range = item.get('월소득 10분위별가계수지항목별', '미정'),
        worker= item.get('근로자가구2년평균', 0),
        not_worker=item.get("근로자외가구2년평균", 0),
        )
        new_data.save()

    return render(request, 'your_template5.html')

def savedata_view6(request):
    with open('data/decile_income.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        new_data = Decile_income(
        per_range = item.get('월소득 10분위별가계수지항목별', '미정'),
        worker= item.get('근로자가구2년평균', 0),
        not_worker=item.get("근로자외가구2년평균", 0),
        )
        new_data.save()

    return render(request, 'your_template6.html')





############ 2. 여기는 적금
from .models import SavingOptions, SavingProducts
from .serializers import SavingOptionSerializer, SavingProductSerializer

@api_view(['GET'])
def save_saving_products(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()

    # 2. 원하는 필드 
    for baseli in response['result'].get('baseList'):
        dcls_month = baseli.get('dcls_month') # 공시 제출월[YYYYMM]: 사용자에게 얼마나 최근에 만들어졌는지 정보 제공을 
        # 위해 필요해 보임
        fin_co_no = baseli.get('fin_co_no') # 금융회사 코드
        fin_prdt_cd = baseli.get('fin_prdt_cd') # 금융상품 코드
        kor_co_nm = baseli.get('kor_co_nm') # 금융회사 명
        fin_prdt_nm = baseli.get('fin_prdt_nm') # 금융상품명 
    
        join_way = baseli.get('join_way')   #가입 방법
        mtrt_int = baseli.get('mtrt_int')   # 만기후이자율
        spcl_cnd = baseli.get('spcl_cnd')   # 우대조건 등
        join_deny = baseli.get('join_deny') #가입제한(1:제한없음, 2:서민전용, 3:일부제한)
        join_member = baseli.get('join_member') # 가입대상

        etc_note = baseli.get('etc_note')   # 기타 유의사항
        max_limit = baseli.get('max_limit') # 최고한도
        dcls_strt_day = baseli.get('dcls_strt_day') # 공시 시작일
        dcls_end_day = baseli.get('dcls_end_day')   # 공시 종료일
        fin_co_subm_day = baseli.get('fin_co_subm_day') # 금융회사 제출일[YYYYMMDDHH24MI]

        # DB에 이미 저장되어있는지 중복확인
        if SavingProducts.objects.filter(
            dcls_month=dcls_month,
            fin_co_no=fin_co_no,
            fin_prdt_cd=fin_prdt_cd,
            kor_co_nm=kor_co_nm,
            fin_prdt_nm=fin_prdt_nm,

            join_way=join_way,
            mtrt_int = mtrt_int,
            spcl_cnd=spcl_cnd,
            join_deny=join_deny,
            join_member=join_member,

            etc_note= etc_note,
            max_limit = max_limit,
            dcls_strt_day = dcls_strt_day,
            dcls_end_day = dcls_end_day,
            fin_co_subm_day = fin_co_subm_day,
            ).exists():
            continue

        save_data = {
            'dcls_month':dcls_month,
            'fin_co_no':fin_co_no,
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,

            'join_way':join_way,            
            'mtrt_int' : mtrt_int,
            'spcl_cnd':spcl_cnd,
            'join_deny':join_deny,
            'join_member':join_member,

            'etc_note':etc_note,
            'max_limit' : max_limit,
            'dcls_strt_day' : dcls_strt_day,
            'dcls_end_day' : dcls_end_day,
            'fin_co_subm_day' : fin_co_subm_day,
        }

        serializer = SavingProductSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # 옵션 만들기
    for li in response['result'].get('optionList'):
        # dcls_month
        # fin_co_no
        fin_prdt_cd = li.get('fin_prdt_cd') # 
        intr_rate_type_nm= li.get('intr_rate_type_nm')  # 저축 금리 유형명
        rsrv_type = li.get('rsrv_type') # 적립 유형명: 정액적립식, 자유적립식 
        save_trm = li.get('save_trm')   # 저축기간[단위: 개월]
        intr_rate = li.get('intr_rate') # 저축 금리[소수점 2자리]
        intr_rate2 = li.get('intr_rate2')   # 최고 우대금리[소수점 2자리]

        if SavingOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            ).exists():
            continue
        save_data = { 
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'rsrv_type':rsrv_type,
            'save_trm':save_trm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            }

        serializer = SavingOptionSerializer(data=save_data)
        saving = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product2=saving)

    return JsonResponse({'message': '적금!!저장 성공!'})
        # return Response(serializer.data)




# ==============2024.11.19 시작==================

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import os
from django.conf import settings
from .models import Incomepergenderage, Incomeperjob, Incomepergrade, DepositProducts, Card, IncomeSpend

DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')

# Function to fetch cards from the database
def fetch_cards():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = "SELECT card_name, merit_summary, base_performance, annual_fee FROM data_card"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    cards = []
    for row in rows:
        cards.append({
            'card_name': row[0],
            'merit_summary': row[1],
            'base_performance': row[2],
            'annual_fee': row[3],
        })

    connection.close()
    return cards

# Function to fetch savings and deposits
# def fetch_savings_and_deposits(use_bank, save_trm, spending_ratio=None):
#     connection = sqlite3.connect(DB_PATH)
#     cursor = connection.cursor()

#     deposit_query = (
#         "SELECT d.fin_prdt_nm, o.intr_rate2 FROM articles_depositproducts d "
#         "JOIN articles_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE d.kor_co_nm = ? AND o.save_trm = ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 3"
#     )
#     cursor.execute(deposit_query, (use_bank, save_trm))
#     deposits = cursor.fetchall()

#     saving_query = (
#         "SELECT s.fin_prdt_nm, o.intr_rate2 FROM articles_savingproducts s "
#         "JOIN articles_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE s.kor_co_nm = ? AND o.save_trm = ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 3"
#     )
#     cursor.execute(saving_query, (use_bank, save_trm))
#     savings = cursor.fetchall()

#     connection.close()
#     return deposits, savings


# ==========================기존 예적금 추천 알고리즘
# def recommend_savings_and_deposits(use_bank, save_trm):
#     """
#     Recommend 2 savings/deposit products from the user's bank and 1 from other banks.
#     """
#     # Extract the first two characters of the user's bank
#     bank_prefix = use_bank[:2] if use_bank else ""

#     connection = sqlite3.connect(DB_PATH)
#     cursor = connection.cursor()

#     # Fetch deposits from user's bank
#     deposit_query = (
#         "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_depositproducts d "
#         "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE d.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 2"
#     )
#     print(deposit_query)
#     cursor.execute(deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     user_bank_deposits = cursor.fetchall()

#     # Fetch savings from user's bank
#     saving_query = (
#         "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_savingproducts s "
#         "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE s.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 2"
#     )
#     cursor.execute(saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     user_bank_savings = cursor.fetchall()

#     # Fetch deposits from other banks
#     other_deposit_query = (
#         "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_depositproducts d "
#         "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE d.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 1"
#     )
#     cursor.execute(other_deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     other_deposits = cursor.fetchall()

#     # Fetch savings from other banks
#     other_saving_query = (
#         "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_savingproducts s "
#         "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE s.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 1"
#     )
#     cursor.execute(other_saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     other_savings = cursor.fetchall()

#     connection.close()

#     # Combine user bank and other bank recommendations
#     deposit_recommendations = user_bank_deposits + other_deposits
#     saving_recommendations = user_bank_savings + other_savings
#     print("Deposit Recommendations:", deposit_recommendations)
#     print("Saving Recommendations:", saving_recommendations)
#     return deposit_recommendations, saving_recommendations
#==============================================================================================


# import sqlite3

# DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')

# def recommend_savings_and_deposits(use_bank, save_trm, financial_products):
#     """
#     Recommend savings and deposit products based on user's bank, term, and existing products.
    
#     If has_savings_or_deposits == 1:
#         - Recommend 1 deposit and 1 savings from user's bank.
#     If has_savings_or_deposits == 0:
#         - Recommend 1 deposit from user's bank and 2 savings from other banks.
#     """
#     bank_prefix = use_bank[:2] if use_bank else ""

#     connection = sqlite3.connect(DB_PATH)
#     cursor = connection.cursor()

#     # Fetch deposits from user's bank
#     user_deposit_query = (
#         "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_depositproducts d "
#         "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE d.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 1"
#     )
#     cursor.execute(user_deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     user_deposit = cursor.fetchall()

#     # Fetch savings from user's bank
#     user_saving_query = (
#         "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_savingproducts s "
#         "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE s.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 1"
#     )
#     cursor.execute(user_saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     user_saving = cursor.fetchall()

#     # Fetch additional savings from other banks
#     other_saving_query = (
#         "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_savingproducts s "
#         "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE s.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 2"
#     )
#     cursor.execute(other_saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     other_savings = cursor.fetchall()

#     # Fetch additional deposits from other banks
#     other_deposit_query = (
#         "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm FROM data_depositproducts d "
#         "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
#         "WHERE d.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
#         "ORDER BY o.intr_rate2 DESC LIMIT 1"
#     )
#     cursor.execute(other_deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
#     other_deposit = cursor.fetchall()

#     connection.close()

#     # Determine recommendations based on `has_savings_or_deposits`
#     if financial_products == 1:
#         # Recommend 1 deposit and 1 saving from user's bank
#         deposit_recommendations = user_deposit
#         saving_recommendations = user_saving
        
#     else:
#         # Recommend 1 deposit from user's bank and 2 savings from other banks
#         deposit_recommendations = user_deposit + other_deposit
#         saving_recommendations = other_savings

    
#     print("Deposit Recommendations:", deposit_recommendations)
#     print("Saving Recommendations:", saving_recommendations)
#     return deposit_recommendations, saving_recommendations

#-============================================================================

# from django.http import JsonResponse
# from .models import SavingOptions, DepositOptions

# def recommend_savings_and_deposits(use_bank, save_trm, financial_products):
#     """
#     Recommend savings and deposit products based on user's preferences and current holdings.

#     Args:
#         use_bank (str): User's preferred bank.
#         save_trm (str): Desired savings/deposit term (e.g., "12").
#         financial_products (int): Whether the user already has financial products (1: Yes, 0: No).

#     Returns:
#         JsonResponse: Recommended deposit and savings products.
#     """
#     def filter_products(option_model, product_field, exclude_bank=False):
#         """
#         Filter products based on user's bank and save term.
#         Args:
#             option_model: Model for options (SavingOptions or DepositOptions).
#             product_field: Field name for the foreign key (e.g., 'product2' or 'product').
#             exclude_bank: Exclude the user's bank if True.
        
#         Returns:
#             QuerySet: Filtered and sorted options.
#         """
#         # Step 1: Filter by bank and term
#         query = option_model.objects.filter(
#             save_trm=save_trm,
#         ).select_related(product_field).order_by("-intr_rate2")
        
#         if exclude_bank:
#             query = query.exclude(**{f"{product_field}__kor_co_nm__icontains": use_bank})
#         else:
#             query = query.filter(**{f"{product_field}__kor_co_nm__icontains": use_bank})

#         # Step 2: If no match, return options for term only
#         if not query.exists():
#             query = option_model.objects.filter(
#                 save_trm=save_trm
#             ).select_related(product_field).order_by("-intr_rate2")

#         # Step 3: If still no match, return all products sorted by interest
#         if not query.exists():
#             query = option_model.objects.all().select_related(product_field).order_by("-intr_rate2")

#         return query

#     # Determine recommendations based on financial_products
#     if financial_products == 1:  # User already has financial products
#         # 예금: product_id를 사용
#         deposit_options = filter_products(DepositOptions, "product")[:1]
#         # 적금: product2_id를 사용
#         saving_options = filter_products(SavingOptions, "product2")[:1]
#     else:  # User does not have financial products
#         # 예금: product_id를 사용
#         deposit_options = filter_products(DepositOptions, "product")[:1]
#         # 적금: product2_id를 사용하며 사용자의 은행 제외
#         saving_options = filter_products(SavingOptions, "product2", exclude_bank=True)[:2]

#     def format_results(options, product_field):
#         return [
#             {
#                 "product_name": getattr(option, product_field).fin_prdt_nm,
#                 "bank_name": getattr(option, product_field).kor_co_nm,
#                 "term": option.save_trm,
#                 "interest_rate": option.intr_rate,
#                 "max_interest_rate": option.intr_rate2,
#                 "special_conditions": getattr(option, product_field).spcl_cnd,
#             }
#             for option in options
#         ]
    
    
#     return JsonResponse({
#         "deposit_recommendations": format_results(deposit_options, "product"),
#         "saving_recommendations": format_results(saving_options, "product2"),
#     })


# from django.http import JsonResponse
# from .models import SavingOptions, DepositOptions

# def recommend_savings_and_deposits(use_bank, save_trm, has_savings_or_deposits):
    
#     """
#     Recommend savings and deposit products based on user's preferences.

#     Args:
#         use_bank (str): User's preferred bank.
#         save_trm (str): Desired savings or deposit term (e.g., "12").
#         has_savings_or_deposits (int): Whether the user already has financial products (1: Yes, 0: No).

#     Returns:
#         tuple: Two lists containing deposit and saving recommendations.
#     """
#     def filter_products(option_model, product_field, exclude_bank=False):
#         """
#         Filter products based on user's bank and save term.

#         Args:
#             option_model: The model to query (e.g., SavingOptions, DepositOptions).
#             product_field: The field name for the related product (e.g., 'product', 'product2').
#             exclude_bank: Exclude products from the user's bank if True.

#         Returns:
#             QuerySet: Filtered and sorted products.
#         """
#         query = option_model.objects.filter(
#             save_trm=save_trm,
#         ).select_related(product_field).order_by("-intr_rate2")

#         if exclude_bank:
#             query = query.exclude(**{f"{product_field}__kor_co_nm__icontains": use_bank})
#         else:
#             query = query.filter(**{f"{product_field}__kor_co_nm__icontains": use_bank})

#         # If no match, fall back to filtering by term only
#         if not query.exists():
#             query = option_model.objects.filter(
#                 save_trm=save_trm
#             ).select_related(product_field).order_by("-intr_rate2")

#         # If still no match, return all products sorted by interest rate
#         if not query.exists():
#             query = option_model.objects.all().select_related(product_field).order_by("-intr_rate2")

#         return query

#     # Recommendations
#     if has_savings_or_deposits == 1:
#         deposit_options = filter_products(DepositOptions, "product")[:1]
#         saving_options = filter_products(SavingOptions, "product2")[:1]
#     else:
#         deposit_options = filter_products(DepositOptions, "product")[:1]
#         saving_options = filter_products(SavingOptions, "product2", exclude_bank=True)[:2]

#     # Format results for both deposits and savings
#     def format_results(options, product_field):
#         return [
#             {
#                 "product_name": getattr(option, product_field).fin_prdt_nm,
#                 "bank_name": getattr(option, product_field).kor_co_nm,
#                 "term": option.save_trm,
#                 "interest_rate": option.intr_rate,
#                 "max_interest_rate": option.intr_rate2,
#                 "special_conditions": getattr(option, product_field).spcl_cnd,
#             }
#             for option in options
#         ]

#     deposit_recommendations = format_results(deposit_options, "product")
#     saving_recommendations = format_results(saving_options, "product2")

#     return deposit_recommendations, saving_recommendations


from django.http import JsonResponse
from .models import SavingOptions, DepositOptions
from .models import DepositProducts, SavingProducts
from .serializers import DepositOptionSerializer, SavingOptionSerializer, SavingProductSerializer, DepositProductSerializer
from pprint import pprint
def recommend_savings_and_deposits(use_bank, save_trm, has_savings_or_deposits):
    deposit_products = DepositProducts.objects.all()
    saving_products = SavingProducts.objects.all()
    deposit_options = DepositOptions.objects.all()
    saving_options = SavingOptions.objects.all()

    setted_deposit_products = DepositProductSerializer(deposit_products, many = True)
    setted_saving_products = SavingProductSerializer(saving_products, many = True)
    setted_Deposit_Options = DepositOptionSerializer(deposit_options, many = True)
    setted_Saving_Options = SavingOptionSerializer(saving_options, many = True)
    sorted_Deposit_rate_datas = sorted(setted_Deposit_Options.data, key=lambda x: x["intr_rate2"])
    sorted_Saving_rate_datas = sorted(setted_Saving_Options.data, key=lambda x: x["intr_rate2"])
    
    recommend_deposits = []
    recommend_savings = []
    for deposit_product in setted_deposit_products.data:
        if use_bank[:2] == deposit_product['kor_co_nm'][:2] and save_trm == setted_Deposit_Options.data[deposit_product['id']]['save_trm']:
            recommend_deposits.append(deposit_product)
        elif use_bank[:2] == deposit_product['kor_co_nm'][:2] and deposit_product not in recommend_deposits:
            recommend_deposits.append(deposit_product)
    for saving_product in setted_saving_products.data:
        if use_bank[:2] == saving_product['kor_co_nm'][:2] and save_trm == setted_Saving_Options.data[saving_product['id']]['save_trm']:
            recommend_savings.append(saving_product)
        elif use_bank[:2] == saving_product['kor_co_nm'][:2] and saving_product not in recommend_savings:
            recommend_savings.append(saving_product)

    if len(recommend_deposits) >= 2:
        for j in range(len(recommend_deposits)):
            for i in range(len(recommend_deposits)-1):
                if setted_Deposit_Options.data[recommend_deposits[i]['id']-1]['intr_rate2'] >= setted_Deposit_Options.data[recommend_deposits[i+1]['id']-1]['intr_rate2']:
                    recommend_deposits[i],recommend_deposits[i+1] = recommend_deposits[i+1],recommend_deposits[i]
        while len(recommend_deposits) > 2:
            recommend_deposits.pop(0)
    
    if len(recommend_savings) >= 2:
        for j in range(len(recommend_savings)):
            for i in range(len(recommend_savings)-1):
                if setted_Saving_Options.data[recommend_savings[i]['id']-1]['intr_rate2'] >= setted_Saving_Options.data[recommend_savings[i+1]['id']-1]['intr_rate2']:
                    recommend_savings[i],recommend_savings[i+1] = recommend_savings[i+1],recommend_savings[i]
        while len(recommend_savings) > 2:
            recommend_savings.pop(0)
    # print(sorted_Deposit_rate_datas)
    if len(recommend_deposits) == 0:
        recommend_deposits.append(sorted_Deposit_rate_datas[-1]['product'])
    if len(recommend_deposits) == 1:
        recommend_deposits.append(sorted_Deposit_rate_datas[-2]['product'])
    if len(recommend_savings) == 0:
        recommend_savings.append(sorted_Saving_rate_datas[-1]['product2'])
    if len(recommend_savings) == 1:
        recommend_savings.append(sorted_Saving_rate_datas[-2]['product2'])
    # print(recommend_deposits)
    for recommend_deposit in recommend_deposits:
        recommend_deposit['intr_rate2'] = setted_Deposit_Options.data[recommend_deposit['id']-1]['intr_rate2']
        recommend_deposit['save_trm'] = setted_Deposit_Options.data[recommend_deposit['id']-1]['save_trm']
    # print(recommend_savings)
    for recommend_saving in recommend_savings:
        recommend_saving['intr_rate2'] = setted_Saving_Options.data[recommend_saving['id']-1]['intr_rate2']
        recommend_saving['save_trm'] = setted_Deposit_Options.data[recommend_deposit['id']-1]['save_trm']
    # print(recommend_deposits, 123123123123)
    return recommend_deposits, recommend_savings



# 소득 및 소비 분석 함수
def analyze_income_and_spending(data):
    gender = data.get('gender')
    age = data.get('age')
    income = float(data.get('income', 0))
    consume = float(data.get('consume', 0))
    
    if age:
        if int(age) <= 19 :
            age = '19세이하'  # 25 → "20-29"
        elif 20<= int(age) <= 24:
            age = '20~24세'
        elif 25<= int(age) <= 29:
            age = '25~29세'
        elif 30<= int(age) <= 34:
            age = '30~34세'
        elif 35<= int(age) <= 39:
            age = '35~39세'
        elif 40<= int(age) <= 44:
            age = '40~44세'
        elif 45<= int(age) <= 49:
            age = '45~49세'
        elif 50<= int(age) <= 54:
            age = '50~54세'
        elif 55<= int(age) <= 59:
            age = '55~59세'
        elif 60<= int(age):
            age = '60세이상'

    # 소득 분석
    avg_income_entry = Incomepergenderage.objects.filter(gender=gender, agerange=age).first()
    avg_income = avg_income_entry.avgallincome if avg_income_entry else 0

    if avg_income == 0:
        income_analysis = "평균 소득 데이터를 찾을 수 없습니다."
    elif income > avg_income * 1.1:
        income_analysis = "소득이 해당 성별 및 연령대의 평균보다 높습니다."
    elif avg_income * 0.9 <= income <= avg_income * 1.1:
        income_analysis = "소득이 해당 성별 및 연령대의 평균과 비슷합니다."
    else:
        income_analysis = "소득이 해당 성별 및 연령대의 평균보다 낮습니다."

    # 1. 소득 분위 계산

    decile_entry = (
        Decile_income.objects.filter(worker__lte=income)  # 소득 이하의 분위 필터링
        .order_by('-worker')  # 가장 큰 worker 값을 선택
        .first()
    )
   
    if decile_entry:
        income_decile = decile_entry.per_range
    else:
        # 모든 분위의 소득을 초과하는 경우 최상위 분위로 설정
        income_decile = Decile_income.objects.order_by('-worker').first().per_range

    # 2. 소비 분석
    consume_entry = Decile_consume.objects.filter(per_range__startswith=income_decile[:3]).first()
    if consume_entry:
        avg_consume = consume_entry.worker
        if consume > avg_consume * 1.1:
            spending_analysis = f"소비가 {income_decile} 분위의 평균보다 높습니다."
        elif avg_consume * 0.9 <= consume <= avg_consume * 1.1:
            spending_analysis = f"소비가 {income_decile} 분위의 평균과 비슷합니다."
        else:
            spending_analysis = f"소비가 {income_decile} 분위의 평균보다 낮습니다."
    else:
        spending_analysis = "해당 소득 분위의 소비 데이터를 찾을 수 없습니다."

    return {
        "income_decile": income_decile,
        "spending_analysis": spending_analysis,
        'income_analysis' : income_analysis
    }
    

# 종합소득세 환급 계산 함수
def calculate_tax_refund(income, job):
    """
    월 소득(income)을 기반으로 근로소득세와 예상 환급액 계산
    """
    # 월 소득 → 연 소득 변환
    annual_salary = income * 12  # 한 달 소득을 기준으로 연 소득 계산

    # 근로 직군 리스트
    worker_jobs = list(Incomeperjob.objects.values_list('job', flat=True))

    # 근로소득세 계산
    def calculate_income_tax(salary):
        """
        연 소득 기준 근로소득세 계산
        """
        # 근로소득공제 (2023년 기준)
        if salary <= 5000000:
            deduction = salary * 0.7
        elif salary <= 15000000:
            deduction = 3500000 + (salary - 5000000) * 0.4
        elif salary <= 45000000:
            deduction = 7500000 + (salary - 15000000) * 0.15
        elif salary <= 100000000:
            deduction = 12000000 + (salary - 45000000) * 0.05
        else:
            deduction = 14750000

        # 과세표준
        taxable_income = max(0, salary - deduction)

        # 누진세율 적용 (2023년 기준)
        tax_brackets = [
            (12000000, 0.06),  # 1,200만 원 이하: 6%
            (46000000, 0.15),  # 4,600만 원 이하: 15%
            (88000000, 0.24),  # 8,800만 원 이하: 24%
            (150000000, 0.35), # 1억 5천만 원 이하: 35%
            (float('inf'), 0.42) # 초과: 42%
        ]

        # 세금 계산
        tax = 0
        for limit, rate in tax_brackets:
            if taxable_income > limit:
                tax += limit * rate
                taxable_income -= limit
            else:
                tax += taxable_income * rate
                break

        # 세액 공제 (5% 예시)
        tax_credit = tax * 0.05

        # 최종 세액
        final_tax = max(0, tax - tax_credit)
        return final_tax

    # 근로소득세 계산
    annual_tax = calculate_income_tax(annual_salary)

    # 근로소득세 환급 계산
    if job in worker_jobs:
        # 근로소득자 환급 비율 (33% 기준)
        refund_rate = 0.33
        estimated_refund = annual_tax * refund_rate
        refund_message = f"추정되는 근로소득세 환급액은 {estimated_refund:,.0f}원입니다."
    else:
        refund_message = "비근로자는 환급 계산 대상이 아닙니다."

    return {
        "annual_income_tax": f"{annual_tax:,.0f}원",  # 연간 근로소득세
        "refund_estimation": refund_message  # 환급 예측 결과
    }



def recommend_cards(use_bank):
    """
    Recommend 2 cards from the user's bank and 1 card from other banks.
    """
    # Extract the first two characters of the user's bank
    bank_prefix = use_bank[:2] if use_bank else ""
    
    if bank_prefix == "부산":
        bank_prefix = "BNK"
    if bank_prefix in ['롯데', '롯데카드']:
        bank_prefix = '디지'
    if bank_prefix in ["농협", "농협은행","농협카드"]:
        bank_prefix = 'NH'
    if bank_prefix in ['국민', '국민카드']:
        bank_prefix = '국민'
    if bank_prefix in ['기업은행','기업', 'IBK기업', 'IBK기업은행']:
        bank_prefix = 'IBK'
    if bank_prefix in ['삼성', '삼성카드']:
        bank_prefix = '삼성'
    # Fetch all cards from the database
    all_cards = fetch_cards()
    
    # Filter cards by the user's bank
    user_bank_cards = [card for card in all_cards if bank_prefix in card['card_name']]
    # Select 2 cards from the user's bank
    user_bank_recommendations = user_bank_cards[:2]

    # Select 1 card from other banks
    other_bank_cards = [card for card in all_cards if bank_prefix not in card['card_name']]
    other_bank_recommendations = other_bank_cards[:1]
    if len(user_bank_recommendations) == 0:
        other_bank_recommendations = other_bank_cards[:3]
    # Combine the recommendations
    recommendations = user_bank_recommendations + other_bank_recommendations

    return recommendations


from accounts.models import User

# 추천 로직 함수
def get_recommendations(user_id):
    try:
        # 유저 정보 조회
        profile = User.objects.get(id=user_id)
        
        data = {
            "gender": profile.gender,
            "age": profile.age,
            "income": profile.income*10000,
            "consume": profile.consume*10000,
            "job": profile.job,
            "grade": profile.grade,
            "use_bank": profile.main_bank,
            "save_trm": profile.desire_period,
            "financial_products" : profile.financial_products,
        }
        
    
    
        income_analysis, income_decile, spending_analysis = analyze_income_and_spending(data)['income_analysis'],analyze_income_and_spending(data)['income_decile'],analyze_income_and_spending(data)['spending_analysis']

    
    
    # 종합소득세 환급 계산
        tax_refund_estimation = calculate_tax_refund(data['income'], profile.job)

    # 직업과 학력에 따른 소득 분석
        job_analysis, grade_analysis = compare_income_by_job_and_grade(data['income'], profile.job, profile.grade)


    # 카드 추천 (2개는 주거래 은행, 1개는 다른 은행)
        card_recommendations = recommend_cards(profile.main_bank)

    # 예적금 추천

    
        depositjj, savings = recommend_savings_and_deposits(profile.main_bank, profile.desire_period, profile.financial_products)
        deposits = reversed(depositjj)

        deposit_recommendations = [
            {"name": deposit['fin_prdt_nm'], "bank_name": deposit['kor_co_nm'],"term": deposit['save_trm'], "max_interest_rate": deposit['intr_rate2']} for deposit in deposits
        ]
        saving_recommendations = [
            {"name": saving['fin_prdt_nm'], "bank_name": saving['kor_co_nm'],"term": saving['save_trm'], "max_interest_rate": saving['intr_rate2']} for saving in savings
        ]
        return {
            "income_analysis": income_analysis,
            "income_decile": income_decile,
            "spending_analysis": spending_analysis,
            "tax_refund_estimation": tax_refund_estimation,
            "card_recommendations": card_recommendations[:3],
            # "savings_and_deposits": savings_and_deposits,
            "deposit_recommendations": deposit_recommendations,
            "saving_recommendations": saving_recommendations,
            "job_analysis": job_analysis,
            "grade_analysis": grade_analysis,
        }
    except User.DoesNotExist:
        return {"error": "User profile not found"}
    
@csrf_exempt
def recommend_view(request, user_id):
    if request.method == 'GET':
        recommendations = get_recommendations(user_id)
        return JsonResponse(recommendations)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def input_form_view(request):
    if request.method == 'POST':
        
        data = {
            "gender": request.POST.get('gender'),
            "age": request.POST.get('age'),
            "income": request.POST.get('income'),
            "consume": request.POST.get('consume'),
            "carduseratio": request.POST.get('carduseratio'),
            "job": request.POST.get('job'),
            "grade": request.POST.get('grade'),
            "use_bank": request.POST.get('use_bank'),
            "save_trm": request.POST.get('save_trm'),
        }
        recommendations = get_recommendations(data)
        
        
        return render(request, 'input_form.html', {
            'recommendations': recommendations,
            'jobs': Incomeperjob.objects.values_list('job', flat=True),
        })
    return render(request, 'input_form.html', {
        'jobs': Incomeperjob.objects.values_list('job', flat=True),
    })

# 직업과 학력에 따른 소득 비교 함수
def compare_income_by_job_and_grade(income, job, grade):
    # 직업 평균 소득 가져오기
    job_entry = Incomeperjob.objects.filter(job=job).first()
    avg_job_income = job_entry.avgincome if job_entry else 0

    if avg_job_income:
        if income > avg_job_income * 1.1:
            job_analysis = f"소득이 동일 직업({job}) 평균보다 높습니다."
        elif avg_job_income * 0.9 <= income <= avg_job_income * 1.1:
            job_analysis = f"소득이 동일 직업({job}) 평균과 비슷합니다."
        else:
            job_analysis = f"소득이 동일 직업({job}) 평균보다 낮습니다."
    else:
        job_analysis = f"직업({job})에 대한 평균 소득 데이터를 찾을 수 없습니다."

    # 학력 평균 소득 가져오기
    grade_entry = Incomepergrade.objects.filter(grade=grade).first()
    avg_grade_income = grade_entry.avgincome if grade_entry else 0

    if avg_grade_income:
        if income > avg_grade_income * 1.1:
            grade_analysis = f"소득이 동일 학력({grade}) 평균보다 높습니다."
        elif avg_grade_income * 0.9 <= income <= avg_grade_income * 1.1:
            grade_analysis = f"소득이 동일 학력({grade}) 평균과 비슷합니다."
        else:
            grade_analysis = f"소득이 동일 학력({grade}) 평균보다 낮습니다."
    else:
        grade_analysis = f"학력({grade})에 대한 평균 소득 데이터를 찾을 수 없습니다."

    return job_analysis, grade_analysis


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProducts
import random

class RandomDepositProductsTitlesAPIView(APIView):
    """
    예금 상품의 제목(fin_prdt_nm)을 랜덤으로 5개 반환합니다.
    """
    def get(self, request):
        # 예금 상품 제목을 랜덤으로 5개 가져오기
        titles = list(
            DepositProducts.objects.values_list('fin_prdt_nm', flat=True)
        )
        random_titles = random.sample(titles, min(len(titles), 5))  # 5개 또는 전체 개수 중 작은 값 사용
        return Response(random_titles, status=status.HTTP_200_OK)
