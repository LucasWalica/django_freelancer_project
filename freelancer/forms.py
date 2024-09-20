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
    
      
    def __init__(self, *args, **kwargs):
        super(FreelancerProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['image'].widget.attrs.update({'class':'form-input w-full rounded-md'})
    


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['name']

      
    def __init__(self, *args, **kwargs):
        super(SkillsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-input w-full rounded-md'})
    

class ProjectOfferForm(forms.ModelForm):
    class Meta:
        model = ProjectOffer
        fields = ['title', 'desc', 'price', 'time_in_days', 'revisions', 'image', 'catOne', 'catTwo']
        permissions = [
            ("can_upload_image", "Can upload image to Project"),
            ("can_update_image", "Can update image to Project")
        ]

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.endswith(('jpg', 'jpeg', 'png')):
            raise ValidationError("Only JPEG and PNG images are allowed.")
        return image

        
    def __init__(self, *args, **kwargs):
        super(ProjectOfferForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['desc'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['price'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['time_in_days'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['revisions'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['image'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['catOne'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['catTwo'].widget.attrs.update({'class':'form-input w-full rounded-md'})

        
