from django import forms 
from .models import FreelancerProfile, Skills, ProjectOffer

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'image']


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['name']


class ProjectOfferForm(forms.ModelForm):
    class Meta:
        model = ProjectOffer
        fields = ['title', 'desc', 'price', 'time_in_days', 'revisions', 'image']


