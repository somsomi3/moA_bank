# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from .models import UserMakingCard, CardDesign
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
# from accounts.models import User

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def generate_card(request):
#     print(request.POST)
#     # Stable Diffusion 설정
#     pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
#     pipe = pipe.to("cuda")
    
#     # 사용자로부터 Prompt를 받음
#     prompt = request.POST.get("prompt", "A realistic image of an airplane flying in the sky")
#     print(prompt,44334) 
    
#     # 이미지 생성
#     background_image = pipe(prompt).images[0]

#     # 손글씨 폰트 로드
#     font_path = os.path.join(settings.BASE_DIR, "cards/static/fonts/MaruBuri-Bold.ttf")
#     if not os.path.exists(font_path):
#         return HttpResponse("Font not found", status=500)
#     font = ImageFont.truetype(font_path, 50)

#     # 카드 디자인
#     card = Image.new("RGB", (800, 400), "white")
#     card.paste(background_image.resize((800, 400)), (0, 0))
    

#     # 텍스트 추가
#     draw = ImageDraw.Draw(card)
#     card_name = request.POST.get("card_name")
#     # print(card_name, 12233)
#     # 텍스트 배치 위치를 조정합니다.
# # background_image의 높이를 고려해 텍스트를 중앙에 배치
#     text_x = 350  # 텍스트의 x 좌표
#     text_y = 350  # 텍스트의 y 좌표 (이미지 위로 올리기 위해 조정)

#     # 글꼴 설정
#     font = ImageFont.truetype(font_path, 50)

#     # 텍스트 그리기
#     draw.text((text_x, text_y), card_name, font=font, fill="black")
#     # draw.text((50, 500), card_name, font=font, fill="black")
#     user_instance = User.objects.get(pk=request.POST.get("user_id"))
#     print(card)
#     # 카드 저장
#     # output_path = os.path.join(settings.BASE_DIR, "cards/static/generated_card.png")

#     # card.save(output_path)
#     # print(f"Card saved to {output_path}")
    
#     # # # **카드 정보를 데이터베이스에 저장하고 사용자와 연결**
#     if request.user.is_authenticated:  # 로그인한 사용자만 저장 가능
        
#         new_card = UserMakingCard.objects.create(
#             user=user_instance,  # 현재 로그인한 사용자
#             card_name=request.POST.get("card_name"),
#             card_image=card,  # 카드 이미지 경로
#             # text=text,  # 카드 텍스트
#             # prompt=prompt  # 프롬프트
#         )
#     else:
#         return HttpResponse("Authentication required", status=401)
#     ##

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
