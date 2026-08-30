from django.contrib import admin
from .models import MemberRegistration
from django.contrib import admin
from .models import ContactMessage

@admin.register(MemberRegistration)
class MemberRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile', 'membership_plan', 'amount', 'utr_number', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'membership_plan', 'created_at')
    search_fields = ('first_name', 'last_name', 'mobile', 'utr_number')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'category', 'subject', 'is_resolved', 'created_at')
    list_filter = ('category', 'is_resolved', 'created_at')
    search_fields = ('name', 'mobile', 'subject', 'message')