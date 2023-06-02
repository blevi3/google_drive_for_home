from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)


from .models import OTP

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ['code']

