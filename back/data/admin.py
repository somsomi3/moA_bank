from django.contrib import admin

# Register your models here.
import csv
from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects to CSV", fields=None):
    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={opts.app_label}_{opts.model_name}.csv'

        writer = csv.writer(response)
        if fields:
            field_names = fields
        else:
            field_names = [field.name for field in opts.fields]
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
from django.contrib import admin
from .models import Card
from .admin_utils import export_as_csv_action  # CSV Export 기능을 사용하는 함수

# Card 모델의 Admin 설정
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_name', 'card_link', 'card_apply_link']  # Admin에서 표시할 필드
    actions = [export_as_csv_action("Export selected cards to CSV")]  # CSV Export 기능 추가

# Admin에 Card 모델 등록
admin.site.register(Card, CardAdmin)