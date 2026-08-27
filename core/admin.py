from django.contrib import admin
from .models import MemberRegistration

@admin.register(MemberRegistration)
class MemberRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile', 'membership_plan', 'amount', 'utr_number', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'membership_plan', 'created_at')
    search_fields = ('first_name', 'last_name', 'mobile', 'utr_number')