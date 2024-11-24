import csv
import json

# CSV 파일 경로
csv_file_path = "cards(2).csv"  # Action에서 다운로드한 CSV 파일 이름
json_file_path = "aaaaa.json"  # 변환 후 저장할 JSON 파일 이름

# CSV를 JSON으로 변환
data = []
with open(csv_file_path, encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append({
            "model": "data.card",  # 모델 이름
            "fields": row  # CSV에서 읽어온 데이터
        })

# JSON 파일로 저장
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

print(f"JSON 파일로 저장되었습니다: {json_file_path}")
