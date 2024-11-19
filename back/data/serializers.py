from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts,SavingOptions
# from .models import SavingProducts, SavingOptions


# 예금 serializer
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionSerializer(serializers.ModelSerializer):
    product = DepositProductSerializer(read_only=True)

    class Meta:
        model = DepositOptions
        fields = ['fin_prdt_cd', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm', 'product']

    def validate_intr_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("이자율은 0보다 작을 수 없습니다.")
        return value


# 적금 serializer
class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        # fields = ['fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'etc_note']  # 필요한 필드만 포함
        fields = '__all__'
class SavingOptionSerializer(serializers.ModelSerializer):
    product2 = SavingProductSerializer(read_only=True)
    class Meta:
        model = SavingOptions
        fields = ['fin_prdt_cd', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm', 'product2']
        # fields = '__all__'

    def validate_intr_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("이자율은 0보다 작을 수 없습니다.")
        return value


# # 적금 serializer
# class SavingProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavingProducts
#         # fields = ['fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'etc_note']  # 필요한 필드만 포함
#         fields = '__all__'
# class SavingOptionSerializer(serializers.ModelSerializer):
#     product2 = SavingProductSerializer(read_only=True)
#     class Meta:
#         model = SavingOptions
#         fields = ['fin_prdt_cd', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm', 'product2']
#         # fields = '__all__'

#     def validate_intr_rate(self, value):
#         if value < 0:
#             raise serializers.ValidationError("이자율은 0보다 작을 수 없습니다.")
#         return value
from rest_framework import serializers
from .models import Incomepergenderage, Incomeperjob, Incomepergrade

# 성별 연령별 소득 Serializer
class IncomePerGenderAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomepergenderage
        fields = '__all__'

# 직업별 소득 Serializer
class IncomePerJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomeperjob
        fields = '__all__'

# 학력별 소득 Serializer
class IncomePerGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomepergrade
        fields = '__all__'