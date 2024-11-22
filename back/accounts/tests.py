from django.test import TestCase

# Create your tests here.
def get_recommendations(user_id):
    try:
        # 유저 정보 조회
        profile = UserProfile.objects.get(user_id=user_id)
        
        data = {
            "gender": profile.gender,
            "age": profile.age,
            "income": profile.income,
            "consume": profile.consume,
            "job": profile.job,
            "grade": profile.grade,
            "use_bank": profile.use_bank,
            "save_trm": profile.save_trm,
        }

        # 기존 추천 로직 호출
        income_analysis, income_decile, spending_analysis = analyze_income_and_spending(data)
        tax_refund_estimation = calculate_tax_refund(profile.income, profile.job)
        card_recommendations = recommend_cards(profile.use_bank)
        deposits, savings = recommend_savings_and_deposits(profile.use_bank, profile.save_trm)

        deposit_recommendations = [
            {"name": deposit[0], "rate": deposit[1], "term": deposit[2]} for deposit in deposits
        ]
        saving_recommendations = [
            {"name": saving[0], "rate": saving[1], "term": saving[2]} for saving in savings
        ]

        job_analysis, grade_analysis = compare_income_by_job_and_grade(profile.income, profile.job, profile.grade)

        # 추천 결과 반환
        return {
            "income_analysis": income_analysis,
            "income_decile": income_decile,
            "spending_analysis": spending_analysis,
            "tax_refund_estimation": tax_refund_estimation,
            "card_recommendations": card_recommendations[:3],
            "deposit_recommendations": deposit_recommendations,
            "saving_recommendations": saving_recommendations,
            "job_analysis": job_analysis,
            "grade_analysis": grade_analysis,
        }
    except UserProfile.DoesNotExist:
        return {"error": "User profile not found"}
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def recommend_view(request, user_id):
    if request.method == 'GET':
        recommendations = get_recommendations(user_id)
        return JsonResponse(recommendations)
    return JsonResponse({"error": "Invalid request method"}, status=405)