import os
import sqlite3
from django.conf import settings
from .models import Incomepergenderage, Incomeperjob, Incomepergrade, Decile_income, Decile_consume

DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')

# Function to fetch cards from the database
def fetch_cards():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # 테이블 이름 수정: data_card
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


def recommend_savings_and_deposits(use_bank, save_trm):
    """
    Recommend 2 savings/deposit products from the user's bank and 1 from other banks.
    """
    bank_prefix = use_bank[:2] if use_bank else ""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # 예금 쿼리 - data_depositproducts와 data_depositoptions 테이블 사용
    deposit_query = (
        "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm "
        "FROM data_depositproducts d "
        "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
        "WHERE d.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
        "ORDER BY o.intr_rate2 DESC LIMIT 2"
    )
    cursor.execute(deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
    user_bank_deposits = cursor.fetchall()

    # 적금 쿼리 - data_savingproducts와 data_savingoptions 테이블 사용
    saving_query = (
        "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm "
        "FROM data_savingproducts s "
        "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
        "WHERE s.kor_co_nm LIKE ? AND o.save_trm LIKE ? "
        "ORDER BY o.intr_rate2 DESC LIMIT 2"
    )
    cursor.execute(saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
    user_bank_savings = cursor.fetchall()

    # 기타 은행 예금 쿼리
    other_deposit_query = (
        "SELECT d.fin_prdt_nm, o.intr_rate2, o.save_trm "
        "FROM data_depositproducts d "
        "JOIN data_depositoptions o ON d.fin_prdt_cd = o.fin_prdt_cd "
        "WHERE d.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
        "ORDER BY o.intr_rate2 DESC LIMIT 1"
    )
    cursor.execute(other_deposit_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
    other_deposits = cursor.fetchall()

    # 기타 은행 적금 쿼리
    other_saving_query = (
        "SELECT s.fin_prdt_nm, o.intr_rate2, o.save_trm "
        "FROM data_savingproducts s "
        "JOIN data_savingoptions o ON s.fin_prdt_cd = o.fin_prdt_cd "
        "WHERE s.kor_co_nm NOT LIKE ? AND o.save_trm LIKE ? "
        "ORDER BY o.intr_rate2 DESC LIMIT 1"
    )
    cursor.execute(other_saving_query, (f"%{bank_prefix}%", f"%{save_trm}%"))
    other_savings = cursor.fetchall()

    connection.close()

    deposit_recommendations = user_bank_deposits + other_deposits
    saving_recommendations = user_bank_savings + other_savings

    return deposit_recommendations, saving_recommendations


def analyze_income_and_spending(data):
    gender = data.get('gender')
    age = data.get('age')
    income = float(data.get('income', 0))
    consume = float(data.get('consume', 0))
    
    if age.isdigit():
        age_ranges = {
            19: "19세이하", 24: "20~24세", 29: "25~29세", 34: "30~34세",
            39: "35~39세", 44: "40~44세", 49: "45~49세", 54: "50~54세",
            59: "55~59세", 60: "60세이상"
        }
        for max_age, label in age_ranges.items():
            if int(age) <= max_age:
                age = label
                break

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

    decile_entry = Decile_income.objects.filter(worker__lte=income).order_by('-worker').first()
    income_decile = decile_entry.per_range if decile_entry else Decile_income.objects.order_by('-worker').first().per_range

    consume_entry = Decile_consume.objects.filter(per_range__startswith=income_decile[:3]).first()
    avg_consume = consume_entry.worker if consume_entry else 0
    if consume > avg_consume * 1.1:
        spending_analysis = f"소비가 {income_decile} 분위의 평균보다 높습니다."
    elif avg_consume * 0.9 <= consume <= avg_consume * 1.1:
        spending_analysis = f"소비가 {income_decile} 분위의 평균과 비슷합니다."
    else:
        spending_analysis = f"소비가 {income_decile} 분위의 평균보다 낮습니다."

    return {
        "income_decile": income_decile,
        "spending_analysis": spending_analysis,
        "income_analysis": income_analysis
    }


def calculate_tax_refund(income, job):
    annual_salary = income * 12
    worker_jobs = list(Incomeperjob.objects.values_list('job', flat=True))

    def calculate_income_tax(salary):
        brackets = [
            (12000000, 0.06), (46000000, 0.15), (88000000, 0.24),
            (150000000, 0.35), (float('inf'), 0.42)
        ]
        deduction = (
            salary * 0.7 if salary <= 5000000 else
            3500000 + (salary - 5000000) * 0.4 if salary <= 15000000 else
            7500000 + (salary - 15000000) * 0.15 if salary <= 45000000 else
            12000000 + (salary - 45000000) * 0.05 if salary <= 100000000 else
            14750000
        )
        taxable_income = max(0, salary - deduction)
        tax = sum(min(limit, taxable_income) * rate for limit, rate in brackets)
        return max(0, tax - tax * 0.05)

    annual_tax = calculate_income_tax(annual_salary)
    refund_message = f"추정되는 근로소득세 환급액은 {annual_tax * 0.33:,.0f}원입니다." if job in worker_jobs else "비근로자는 환급 계산 대상이 아닙니다."
    return {
        "annual_income_tax": f"{annual_tax:,.0f}원",
        "refund_estimation": refund_message
    }


def recommend_cards(use_bank):
    bank_prefix = use_bank[:2] if use_bank else ""
    all_cards = fetch_cards()
    user_bank_cards = [card for card in all_cards if bank_prefix in card['card_name']]
    other_bank_cards = [card for card in all_cards if bank_prefix not in card['card_name']]
    return user_bank_cards[:2] + other_bank_cards[:1]


def get_recommendations(data):
    income_analysis = analyze_income_and_spending(data)
    card_recommendations = recommend_cards(data.get('use_bank'))
    deposits, savings = recommend_savings_and_deposits(data.get('use_bank'), data.get('save_trm'))
    tax_refund = calculate_tax_refund(float(data.get('income', 0)), data.get('job'))
    return {
        "income_analysis": income_analysis,
        "card_recommendations": card_recommendations,
        "deposit_recommendations": deposits,
        "saving_recommendations": savings,
        "tax_refund": tax_refund,
    }
