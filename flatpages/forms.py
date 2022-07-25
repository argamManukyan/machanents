from django import forms

from .models import ContactUs, Gallery, Service


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message', 'phone']

class GalleryUploadForm(forms.ModelForm):
    
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    
    class Meta:
        model = Gallery
        fields = "__all__"


class ServiceForm(forms.Form):

    title = forms.CharField()
    phone = forms.CharField()
    name = forms.CharField()
