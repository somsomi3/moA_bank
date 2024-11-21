from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Incomepergenderage, Incomeperjob, Incomepergrade, DepositProducts, Card, IncomeSpend
from .utils import analyze_income_and_spending, recommend_cards, recommend_savings_and_deposits, calculate_tax_refund

@csrf_exempt
def recommend_view(request):
    """
    Handles user input and provides recommendations based on income, spending, and preferences.
    """
    if request.method == 'POST':
        data = {
            "gender": request.POST.get('gender'),
            "age": request.POST.get('age'),
            "income": request.POST.get('income'),
            "consume": request.POST.get('consume'),
            "job": request.POST.get('job'),
            "grade": request.POST.get('grade'),
            "use_bank": request.POST.get('use_bank'),
            "save_trm": request.POST.get('save_trm'),
        }

        # Get recommendations
        income_analysis = analyze_income_and_spending(data)
        card_recommendations = recommend_cards(data.get('use_bank'))
        deposit_recommendations, saving_recommendations = recommend_savings_and_deposits(
            data.get('use_bank'), data.get('save_trm')
        )
        tax_refund = calculate_tax_refund(float(data.get('income', 0)), data.get('job'))

        # Combine all recommendations into a single context
        context = {
            "income_analysis": income_analysis,
            "card_recommendations": card_recommendations,
            "deposit_recommendations": deposit_recommendations,
            "saving_recommendations": saving_recommendations,
            "tax_refund": tax_refund,
        }

        return render(request, 'recommendations.html', context)

    return render(request, 'input_form.html')
