from django.db import models

# 1. 소득/소비 분석 모델
class Incomepergenderage(models.Model):
    gender = models.CharField(max_length=10)  # 성별
    agerange = models.CharField(max_length=20)  # 연령대
    avgallincome = models.FloatField()  # 평균 소득

    def __str__(self):
        return f"{self.gender} - {self.agerange} ({self.avgallincome})"


class Incomeperjob(models.Model):
    job = models.CharField(max_length=50)  # 직업명
    avgincome = models.FloatField()  # 해당 직업의 평균 소득

    def __str__(self):
        return f"{self.job} ({self.avgincome})"


class Incomepergrade(models.Model):
    grade = models.CharField(max_length=50)  # 학력
    avgincome = models.FloatField()  # 해당 학력의 평균 소득

    def __str__(self):
        return f"{self.grade} ({self.avgincome})"


class Decile_income(models.Model):
    worker = models.FloatField()  # 소득
    per_range = models.CharField(max_length=10)  # 소득 분위

    def __str__(self):
        return f"{self.per_range} ({self.worker})"


class Decile_consume(models.Model):
    worker = models.FloatField()  # 소비 수준
    per_range = models.CharField(max_length=10)  # 소비 분위

    def __str__(self):
        return f"{self.per_range} ({self.worker})"


# 2. 카드 추천 모델
class Card(models.Model):
    card_name = models.CharField(max_length=100)  # 카드 이름
    merit_summary = models.TextField()  # 카드 혜택 요약
    base_performance = models.FloatField()  # 기본 실적 (예: 1.2%)
    annual_fee = models.FloatField()  # 연회비

    def __str__(self):
        return f"{self.card_name} (Fee: {self.annual_fee})"


# 3. 예/적금 모델
class DepositProducts(models.Model):
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    kor_co_nm = models.CharField(max_length=50)  # 은행명
    intr_rate2 = models.FloatField()  # 이율
    save_trm = models.CharField(max_length=10)  # 저축 기간

    def __str__(self):
        return f"{self.fin_prdt_nm} - {self.kor_co_nm} ({self.intr_rate2}%)"


class SavingProducts(models.Model):
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    kor_co_nm = models.CharField(max_length=50)  # 은행명
    intr_rate2 = models.FloatField()  # 이율
    save_trm = models.CharField(max_length=10)  # 저축 기간

    def __str__(self):
        return f"{self.fin_prdt_nm} - {self.kor_co_nm} ({self.intr_rate2}%)"


# 4. 사용자 소비/소득 데이터
class IncomeSpend(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)  # 사용자
    income = models.FloatField()  # 소득
    consume = models.FloatField()  # 소비
    gender = models.CharField(max_length=10)  # 성별
    age = models.IntegerField()  # 나이
    job = models.CharField(max_length=50)  # 직업
    grade = models.CharField(max_length=50)  # 학력
    use_bank = models.CharField(max_length=50)  # 이용 은행
    save_trm = models.CharField(max_length=10)  # 저축 기간

    def __str__(self):
        return f"{self.user} - Income: {self.income}, Consume: {self.consume}"
