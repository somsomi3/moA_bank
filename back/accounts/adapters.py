# from allauth.account.adapter import DefaultAccountAdapter

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def save_user(self, request, user, form, commit=True):
#         """
#         Override the save_user method to handle numeric fields correctly.
#         """
#         user = super().save_user(request, user, form, commit=False)

#         # 숫자형 필드 처리
#         age = form.cleaned_data.get("age")
#         income = form.cleaned_data.get("income")

#         if age is not None:
#             user.age = str(age)  # 문자열로 변환
#         if income is not None:
#             user.income = str(income)  # 문자열로 변환

#         if commit:
#             user.save()
#         return user

# 이파일 연결 에러 