import json

# 기존 JSON 파일 로드
with open("depositproducts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 새로운 JSON 구조 생성
new_data = []
for entry in data:
    new_entry = {
        "model": "data.depositproducts",  # 앱 이름과 모델 이름 수정
        "pk": entry["id"],  # id를 pk로 매핑
        "fields": {
            "fin_prdt_cd": entry["fin_prdt_cd"],
            "kor_co_nm": entry["kor_co_nm"],
            "fin_prdt_nm": entry["fin_prdt_nm"],
            "etc_note": entry["etc_note"],
            "join_deny": entry["join_deny"],
            "join_member": entry["join_member"],
            "join_way": entry["join_way"],
            "spcl_cnd": entry["spcl_cnd"]
        }
    }
    new_data.append(new_entry)

# 수정된 JSON 파일 저장
with open("depositproducts2.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("JSON 파일 변환 완료")