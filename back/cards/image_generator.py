from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont

def generate_card_image(prompt: str, font_path: str, text: str) -> Image:
    # 1. Stable Diffusion을 사용하여 배경 이미지 생성
    pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-v1-4")
    pipe.to("cuda")
    generated_image = pipe(prompt).images[0]

    # 2. LF-Font 또는 PIL로 텍스트 추가
    draw = ImageDraw.Draw(generated_image)
    font = ImageFont.truetype(font_path, size=40)
    draw.text((50, 50), text, fill="white", font=font)

    return generated_image
