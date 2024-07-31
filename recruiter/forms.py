from django import forms 
from .models import CommentOnRecruiter, RecruiterProfile,RecruiterProject
from django.core.exceptions import ValidationError

class CommentOnRecruiterForm(forms.ModelForm):
    class Meta: 
        model = CommentOnRecruiter
        fields = ['content', 'stars']

    def __str__(self):
        return f"{self.pk} - {self.created_by}"
    
      
    def __init__(self, *args, **kwargs):
        super(CommentOnRecruiterForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['stars'].widget.attrs.update({'class':'form-input w-full rounded-md'})       
    

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model =  RecruiterProfile
        fields = ['bio', 'image']

    def __str__(self):
        return f"{self.pk} - {self.fkRec}"
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.endswith(('jpg', 'jpeg', 'png')):
            raise ValidationError("Only JPEG and PNG images are allowed.")
        return image

    def __init__(self, *args, **kwargs):
        super(RecruiterProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'form-input w-full rounded-md'})
        self.fields['image'].widget.attrs.update({'class': 'form-input w-full rounded-md'})
    

class RecruiterProjectForm(forms.ModelForm):
    class Meta: 
        model = RecruiterProject
        fields = ['title', 'desc', 'catOne', 'catTwo', 'vacancies']

    def __str__(self):
        return f"{self.pk} - {self.title}"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['desc'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['catOne'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['catTwo'].widget.attrs.update({'class':'form-input w-full rounded-md'})
        self.fields['vacancies'].widget.attrs.update({'class':'form-input w-full rounded-md'})

    

class UpdateRecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['bio', 'active','image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class':'form-input w-full rounded-md'})
