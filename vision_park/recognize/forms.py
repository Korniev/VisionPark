from django import forms
# from .models import IncomingImage



class ImageUploadForm(forms.Form):
    image = forms.ImageField()


# class IncomingImageForm(forms.ModelForm):
#     class Meta:
#         model = IncomingImage
#         fields = ['image']