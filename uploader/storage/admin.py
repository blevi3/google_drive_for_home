from django.contrib import admin
from storage.models import Document, OTP


# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    pass
