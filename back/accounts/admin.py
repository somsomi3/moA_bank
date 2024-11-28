from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Community

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'decile')