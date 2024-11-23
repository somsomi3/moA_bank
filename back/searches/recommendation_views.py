# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse
# from django.db.models import Q
# from data.models import DepositProducts, SavingProducts, DepositOptions, SavingOptions
# from data.serializers import DepositOptionSerializer, SavingOptionSerializer


# # 1. 높은 금리 상품 추천 (예금)
# @api_view(['GET'])
# def top_rate(request):
#     """
#     예금 중 가장 높은 금리 상품 반환
#     """
#     deposit = DepositOptions.objects.select_related('product').order_by('-intr_rate2').first()
#     if deposit:
#         serializer = DepositOptionSerializer(deposit)
#         return Response(serializer.data)
#     return Response({"message": "추천할 수 있는 예금 상품이 없습니다."}, status=404)


# # 2. 높은 금리 상품 추천 (적금)
# @api_view(['GET'])
# def top_rate_saving(request):
#     """
#     적금 중 가장 높은 금리 상품 반환
#     """
#     saving = SavingOptions.objects.select_related('product').order_by('-intr_rate2').first()
#     if saving:
#         serializer = SavingOptionSerializer(saving)
#         return Response(serializer.data)
#     return Response({"message": "추천할 수 있는 적금 상품이 없습니다."}, status=404)


# # 3. 유사한 상품 추천 API (예금)
# @api_view(['GET'])
# def recommend_deposit_products(request):
#     """
#     사용자의 희망 금액과 기간을 기반으로 유사한 예금 상품 추천
#     """
#     try:
#         desired_amount = float(request.query_params.get("desired_amount", 0))
#         desired_period = int(request.query_params.get("desired_period", 0))
#     except (TypeError, ValueError):
#         return JsonResponse({"message": "유효한 금액 및 기간 값을 입력해 주세요."}, status=400)

#     if not desired_amount or not desired_period:
#         return JsonResponse({"message": "금액과 기간을 모두 입력해 주세요."}, status=400)

#     # 오차 범위 설정
#     period_margin = desired_period * 1  # 20% 범위
#     amount_margin = desired_amount * 1  # 20% 범위

#     # 조건에 맞는 예금 옵션 필터링
#     recommended_options = DepositOptions.objects.filter(
#         save_trm__gte=desired_period - period_margin,
#         save_trm__lte=desired_period + period_margin,
#         intr_rate__gte=desired_amount - amount_margin,
#         intr_rate__lte=desired_amount + amount_margin
#     ).order_by('-intr_rate')  # 이자율이 높은 순으로 정렬

#     if recommended_options.exists():
#         serializer = DepositOptionSerializer(recommended_options, many=True)
#         return Response(serializer.data)
#     return JsonResponse({"message": "추천할 수 있는 예금 상품이 없습니다."}, status=404)


# # 4. 유사한 상품 추천 API (적금)
# @api_view(['GET'])
# def recommend_saving_products(request):
#     """
#     사용자의 희망 금액과 기간을 기반으로 유사한 적금 상품 추천
#     """
#     try:
#         desired_amount = float(request.query_params.get("desired_amount", 0))
#         desired_period = int(request.query_params.get("desired_period", 0))
#     except (TypeError, ValueError):
#         return JsonResponse({"message": "유효한 금액 및 기간 값을 입력해 주세요."}, status=400)

#     if not desired_amount or not desired_period:
#         return JsonResponse({"message": "금액과 기간을 모두 입력해 주세요."}, status=400)

#     # 오차 범위 설정
#     period_margin = desired_period * 1  # 20% 범위
#     amount_margin = desired_amount * 1  # 20% 범위

#     # 조건에 맞는 적금 옵션 필터링
#     recommended_options = SavingOptions.objects.filter(
#         save_trm__gte=desired_period - period_margin,
#         save_trm__lte=desired_period + period_margin,
#         intr_rate__gte=desired_amount - amount_margin,
#         intr_rate__lte=desired_amount + amount_margin
#     ).order_by('-intr_rate')  # 이자율이 높은 순으로 정렬

#     if recommended_options.exists():
#         serializer = SavingOptionSerializer(recommended_options, many=True)
#         return Response(serializer.data)
#     return JsonResponse({"message": "추천할 수 있는 적금 상품이 없습니다."}, status=404)

