from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Card, CardDesign
from .serializers import CardSerializer, CardDesignSerializer

# # Card ViewSet
# class CardViewSet(ModelViewSet):
#     queryset = Card.objects.all()
#     serializer_class = CardSerializer


# # CardDesign ViewSet
# class CardDesignViewSet(ModelViewSet):
#     queryset = CardDesign.objects.all()
#     serializer_class = CardDesignSerializer


# # 카드 목록 조회 및 생성
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def card_list_create(request):
#     if request.method == 'GET':
#         cards = Card.objects.all()
#         serializer = CardSerializer(cards, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CardSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # 카드 상세 조회, 수정, 삭제
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def card_detail(request, card_id):
#     card = get_object_or_404(Card, pk=card_id)

#     if request.method == 'GET':
#         serializer = CardSerializer(card)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = CardSerializer(card, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         card.delete()
#         return Response({"message": "Card deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# # 카드 디자인 목록 조회 및 생성
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def card_design_list_create(request):
#     if request.method == 'GET':
#         card_designs = CardDesign.objects.all()
#         serializer = CardDesignSerializer(card_designs, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CardDesignSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카드 디자인 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def card_design_detail(request, card_design_id):
    card_design = get_object_or_404(CardDesign, pk=card_design_id)

    if request.method == 'GET':
        serializer = CardDesignSerializer(card_design)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CardDesignSerializer(card_design, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        card_design.delete()
        return Response({"message": "Card design deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# GPU 코드
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch

from PIL import Image, ImageDraw, ImageFont
import torch
from diffusers import StableDiffusionPipeline

print("All libraries imported successfully!")

def generate_card(request):
    # 1. Stable Diffusion 설정
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    
    # 2. 사용자로부터 Prompt를 받음
    prompt = request.GET.get("prompt", "A realistic image of an airplane flying in the sky")
    
    # 3. 이미지 생성
    background_image = pipe(prompt).images[0]

    # 4. 손글씨 폰트 로드 (사용자 정의 TTF 파일 경로)
    font_path = "cards/static/fonts/MaruBuri-Bold.ttf"
    font = ImageFont.truetype(font_path, 50)

    # 5. 카드 디자인
    card = Image.new("RGB", (800, 600), "white")
    card.paste(background_image.resize((800, 400)), (0, 0))

    # 6. 텍스트 추가
    draw = ImageDraw.Draw(card)
    text = "Happy Journey!"
    draw.text((50, 500), text, font=font, fill="black")

    # 7. 카드 반환
    response = HttpResponse(content_type="image/png")
    card.save(response, "PNG")
    return response

# # GPU없어서, cpu
# from django.http import HttpResponse
# from PIL import Image, ImageDraw, ImageFont
# # from diffusers import StableDiffusionPipeline
# # import torch

# def generate_card(request):
#     # 1. Stable Diffusion 설정 (CPU 사용)
#     # pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
#     pipe = StableDiffusionPipeline.from_pretrained("dreamlike-art/dreamlike-photoreal-2.0", torch_dtype=torch.float32)

#     pipe = pipe.to("cpu")  # CPU로 설정
    
#     # 2. 사용자로부터 Prompt를 받음
#     prompt = request.GET.get("prompt", "A realistic image of an airplane flying in the sky")
    
#     # 3. 이미지 생성 (Stable Diffusion 사용)
#     background_image = pipe(prompt).images[0]

#     # 4. 손글씨 폰트 로드 (사용자 정의 TTF 파일 경로)
#     font_path = "cards/static/fonts/MaruBuri-Bold.ttf"  # 실제 TTF 파일 경로로 변경
#     font = ImageFont.truetype(font_path, 50)

#     # 5. 카드 디자인
#     card = Image.new("RGB", (800, 600), "white")  # 흰색 배경의 카드 생성
#     card.paste(background_image.resize((800, 400)), (0, 0))  # 배경 이미지를 카드에 붙이기

#     # 6. 텍스트 추가
#     draw = ImageDraw.Draw(card)
#     text = "Happy Journey!"  # 카드에 들어갈 텍스트
#     draw.text((50, 500), text, font=font, fill="black")  # 카드 하단에 텍스트 추가

#     # 7. 카드 반환
#     response = HttpResponse(content_type="image/png")
#     card.save(response, "PNG")
#     return response


import torch
from diffusers import StableDiffusionPipeline

# 모델 로드
model_id = "CompVis/stable-diffusion-v1-4"  # 또는 원하는 모델 ID
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# 스케치 이미지를 보완하여 생성할 텍스트 프롬프트
prompt = "a colorful and realistic dinosaur drawing based on the sketch"

# 스케치 이미지를 읽어와 입력으로 변환
from PIL import Image
sketch_image = Image.open("cards/static/images/flower.png")

# 이미지 생성
image = pipe(prompt=prompt, init_image=sketch_image, strength=0.6).images[0]

# 결과 저장
image.save("generated_dinosaur.png")

# ===================================================


import torch
from diffusers import StableDiffusionPipeline

# 모델 로드
model_id = "CompVis/stable-diffusion-v1-4"  # 또는 원하는 모델 ID
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# 스케치 이미지를 보완하여 생성할 텍스트 프롬프트
prompt = "a colorful and realistic dinosaur drawing based on the sketch"

# 스케치 이미지를 읽어와 입력으로 변환
from PIL import Image
sketch_image = Image.open("cards/static/images/flower.png")

# 이미지 생성
image = pipe(prompt=prompt, init_image=sketch_image, strength=0.6).images[0]

# 결과 저장
image.save("generated_dinosaur.png")


# ========================
from rest_framework.response import Response
from rest_framework.views import APIView
from .image_generator import generate_card_image

class CardImageAPIView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        text = request.data.get("text")
        font_path = "/path/to/font.ttf"

        image = generate_card_image(prompt, font_path, text)
        image.save("generated_card.png")  # 이미지 저장

        return Response({"message": "Card image created successfully!"})
