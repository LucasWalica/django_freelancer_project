from django import forms 
from .models import FreelancerProfile, Skills, ProjectOffer
from django.core.exceptions import ValidationError

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'image']
        permissions = [
            ("can_upload_image", "Can upload image to profile"),
            ("can_change_image", "Can change image to profile")
        ]
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.endswith(('jpg', 'jpeg', 'png')):
            raise ValidationError("Only JPEG and PNG images are allowed.")
        return image


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['name']


class ProjectOfferForm(forms.ModelForm):
    class Meta:
        model = ProjectOffer
        fields = ['title', 'desc', 'price', 'time_in_days', 'revisions', 'image']
        permissions = [
            ("can_upload_image", "Can upload image to Project"),
            ("can_update_image", "Can update image to Project")
        ]
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.endswith(('jpg', 'jpeg', 'png')):
            raise ValidationError("Only JPEG and PNG images are allowed.")
        return image
