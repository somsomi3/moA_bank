# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from .models import Card, CardDesign
# from .serializers import CardSerializer, CardDesignSerializer
# from PIL import Image, ImageDraw, ImageFont
# import torch
# from diffusers import StableDiffusionPipeline
# import os
# from django.conf import settings
# from django.http import HttpResponse

# # ============================
# # 카드 디자인 상세 조회, 수정, 삭제
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def card_design_detail(request, card_design_id):
#     card_design = get_object_or_404(CardDesign, pk=card_design_id)

#     if request.method == 'GET':
#         serializer = CardDesignSerializer(card_design)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = CardDesignSerializer(card_design, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         card_design.delete()
#         return Response({"message": "Card design deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# from django.views.decorators.csrf import csrf_exempt
# # ============================
# # GPU를 활용한 Stable Diffusion으로 카드 생성
# @csrf_exempt
# def generate_card(request):
#     # Stable Diffusion 설정
#     pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
#     pipe = pipe.to("cuda")

#     # 사용자로부터 Prompt를 받음
#     prompt = request.GET.get("prompt")
    
#     # 이미지 생성
#     background_image = pipe(prompt).images[0]

#     # 손글씨 폰트 로드
#     font_path = os.path.join(settings.BASE_DIR, "cards/static/fonts/MaruBuri-Bold.ttf")
#     if not os.path.exists(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     font = ImageFont.truetype(font_path, 50)

#     # 카드 디자인
#     card = Image.new("RGB", (800, 600), "white")
#     card.paste(background_image.resize((800, 400)), (0, 0))

#     # 텍스트 추가
#     draw = ImageDraw.Draw(card)
#     text = request.GET.get("text")
#     draw.text((50, 500), text, font=font, fill="black")

#     # 카드 저장
#     output_path = os.path.join(settings.BASE_DIR, "cards/static/generated_card.png")
#     card.save(output_path)
#     print(f"Card saved to {output_path}")

#     # 카드 반환
#     response = HttpResponse(content_type="image/png")
#     card.save(response, "PNG")
#     return response


# # ============================
# # REST API를 사용한 카드 생성 뷰
# class CardImageAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         prompt = request.data.get("prompt")
#         text = request.data.get("text")
#         font_path = os.path.join(settings.BASE_DIR, "cards/static/fonts/MaruBuri-Bold.ttf")

#         if not prompt or not text:
#             return Response({"error": "Both 'prompt' and 'text' are required."}, status=status.HTTP_400_BAD_REQUEST)

#         if not os.path.exists(font_path):
#             return Response({"error": f"Font file not found: {font_path}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             # Stable Diffusion 설정
#             pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
#             pipe = pipe.to("cuda")

#             # 이미지 생성
#             background_image = pipe(prompt).images[0]

#             # 카드 디자인
#             card = Image.new("RGB", (800, 600), "white")
#             card.paste(background_image.resize((800, 400)), (0, 0))

#             # 텍스트 추가
#             draw = ImageDraw.Draw(card)
#             font = ImageFont.truetype(font_path, 50)
#             draw.text((50, 500), text, font=font, fill="black")

#             # 카드 저장
#             output_path = os.path.join(settings.BASE_DIR, "cards/static/generated_card.png")
#             card.save(output_path)
#             print(f"Card image saved to {output_path}")

#             return Response({"message": "Card image created successfully!", "image_path": output_path})

#         except Exception as e:
#             return Response({"error": f"Failed to generate card: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
