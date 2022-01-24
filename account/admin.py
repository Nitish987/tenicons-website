from django.contrib import admin
from .models import UserOTP, UserAgreement

class AgreementFields(admin.ModelAdmin):
    list_display = ('user', 'agreement')

admin.site.register(UserOTP)
admin.site.register(UserAgreement, AgreementFields)
