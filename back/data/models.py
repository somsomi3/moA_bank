from django.db import models

# Create your models here.

#성별 연령별 소득 모델
class Incomepergenderage(models.Model):
    gender = models.TextField()
    agerange = models.TextField()
    avgallincome = models.FloatField()

    def __str__(self):
        return self.gender  # 성별을 반환

# 직업별 소득 모델
class Incomeperjob(models.Model):
    job = models.TextField()
    avgincome = models.FloatField()

# 학력별 소득 모델
class Incomepergrade(models.Model):
    grade = models.TextField()
    avgincome = models.FloatField()


#예금상품 모델
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)    # 금융상품코드
    kor_co_nm = models.TextField()      # 금융회사명
    fin_prdt_nm = models.TextField()    # 금융 상품명
    etc_note = models.TextField()       # 금융 상품 설명
    join_deny = models.IntegerField()   # 가입제한(1: 제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()    # 가입 대상
    join_way = models.TextField()       # 가입 방법
    spcl_cnd = models.TextField()       # 우대 조건


#예금 상품 옵션 모델
class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)    # 외래 키(DepositProducts클래스)
    fin_prdt_cd = models.TextField()    # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명
    intr_rate = models.FloatField()     # 저축금리 
    intr_rate2 = models.FloatField(default=-1)    # 최고우대금리
    save_trm = models.IntegerField()    # 저축기간(단위: 개월)


# 여기는 적금 models.py
class SavingProducts(models.Model):
    dcls_month = models.IntegerField(null=True, blank=True, default=1)    # 공시제출월일
    fin_co_no = models.TextField(null=True, blank=True, default=1)      # 금융회사 코드
    fin_prdt_cd = models.TextField(unique=True, default=1) # 금융상품 코드
    kor_co_nm = models.TextField(null=True, blank=True, default=1)    # 금융회사 명
    fin_prdt_nm = models.TextField(null=True, blank=True, default=1)      # 금융 상품 명

    join_way = models.TextField(null=True, blank=True, default=1)       # 가입 방법
    mtrt_int = models.TextField(null=True, blank=True, default=1)       # 만기후이자
    spcl_cnd = models.TextField(null=True, blank=True, default=1)       # 우대 조건
    join_deny = models.IntegerField(null=True, blank=True, default=1)   # 가입제한(1: 제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(null=True, blank=True, default=1)    # 가입 대상

    etc_note = models.TextField(null=True, blank=True, default=1)       # 기타 유의 사항
    max_limit = models.TextField(null=True, blank=True, default=1)      # 최고한도
    dcls_strt_day = models.IntegerField(null=True, blank=True, default=1)   # 공시시작일
    dcls_end_day= models.IntegerField(null=True, blank=True, default=1)     # 공시종료일
    fin_co_subm_day = models.IntegerField(null=True, blank=True, default=1) # 금융회사 제출일[YYYYMMDDHH24MI]

class SavingOptions(models.Model):
    product2 = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)    # 외래 키(SavingProducts클래스)
    fin_prdt_cd = models.TextField(null=True, blank=True, default=1)    # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명
    rsrv_type = models.TextField(null=True, blank=True, default=1)      # 적립 유형명: 정액적립식, 자유적립식
    intr_rate = models.FloatField(null=True, blank=True, default=1)     # 저축금리 
    intr_rate2 = models.FloatField(default=-1)    # 최고우대금리
    save_trm = models.IntegerField(null=True, blank=True, default=1)    # 저축기간(단위: 개월)

# 소득분위별 소득
# ===================
class IncomeSpend(models.Model):
    per_range = models.TextField()
    worker = models.FloatField()
    not_worker = models.FloatField()

class Decile_consume(models.Model):
    per_range = models.TextField()
    worker = models.FloatField()
    not_worker = models.FloatField()

class Decile_income(models.Model):
    per_range = models.TextField()
    worker = models.FloatField()
    not_worker = models.FloatField()



# 카드 모델
class Card(models.Model):
    card_name = models.TextField(null=True, blank=True)
    card_link = models.URLField(null=True, blank=True)
    card_apply_link = models.URLField(null=True, blank=True)
    card_image = models.ImageField(upload_to='card_images/', null=True, blank=True)  # 이미지 필드 추가
    notification = models.TextField(null=True, blank=True)
    annual_fee = models.TextField(null=True, blank=True)
    base_performance = models.TextField(null=True, blank=True)
    base_performance_last_month = models.TextField(null=True, blank=True)
    merit_summary = models.TextField(null=True, blank=True)