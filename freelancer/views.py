from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import FreelancerProfile, ProjectOffer, Skills
from .forms import SkillsForm, FreelancerProfileForm, ProjectOfferForm 
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.

#Cruds para todos los modelos (para posteriormente implementarlos en el fronted)


class CreateFreelancerProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if FreelancerProfile.objects.filter(user=request.user).exists():
            return redirect('profile:<pk>')  
        form = FreelancerProfileForm()
        context = {
            'form':form
        }
        return render(request, 'createFreelancer.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = FreelancerProfileForm(request.POST, request.FILES)
            if form.is_valid():
                if FreelancerProfile.objects.filter(user=request.user).exists():
                    return redirect('profile:<pk>')
                user = User.username
                bio = form.cleaned_data.get('bio')
                active = True
                stars = 0
                image = form.cleaned_data.get('image')
                f, created = FreelancerProfile.objects.get_or_create(user=user, bio=bio, active=active, stars=stars, image=image)
                f.save()
                return redirect('profile:<pk>')            
        context = {
            'form':form
        }
        return render(request, 'freelancer_create.html', context)

class CreateSkill(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
    
        result = checkFreelancerExist(self, request)
        if result:    
            return result
    
        form = SkillsForm()
        context = {
            'form':form
        }
        return render(request, 'createSkill.html', context)
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = SkillsForm(request.POST)
            if form.is_valid():
                
                result = checkFreelancerExist(self, request)
                if result:
                    return result
                
                name = form.cleaned_data.get('name')

                freelancer_profile = FreelancerProfile.objects.get(user=request.user)

                if Skills.objects.filter(fkFler=freelancer_profile, name=name).exists():
                    return redirect('createSkill.html')
                
                s, created = Skills.objects.get_or_create(fkFler=freelancer_profile, name=name)
                s.save()
                return redirect('profile:<pk>')
            context = {
                'form':form
            }
            return render(request, 'skill_create.html', context)
        
class CreateProjectOffer(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        result = checkFreelancerExist(self, request)
        if result:
            return result
        
        form = ProjectOfferForm()
        context = {
            'form':form
        }
        return render(request, 'createProject.html', context)
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ProjectOfferForm(request.POST, request.FILES)
            if form.is_valid():
                
                result = checkFreelancerExist(self, request)
                if result:
                    return result


                title = form.cleaned_data.get('title') 
                desc = form.cleaned_data.get('desc') 
                price = form.cleaned_data.get('price') 
                time_in_days = form.cleaned_data.get('time_in_days') 
                revisions = form.cleaned_data.get('revisions') 
                image =form.cleaned_data.get('image') 
                freelance_profile = FreelancerProfile.objects.get(user=request.user)

                p, created = ProjectOffer.objects.get_or_create(fkFler=freelance_profile, title=title, desc=desc, price=price, time_in_days=time_in_days, revisions=revisions, image=image)
                p.save()
                return redirect('profile:<pk>')
            context= {
                'form':form
            }
            return render(request, 'createProject.html', context)

class UpdateFreelancerProfile(LoginRequiredMixin, UpdateView):
    model = FreelancerProfile
    fields = ['bio', 'active', 'image']
    template_name = 'update_freelancer.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk':self.object.user.id})
    
    def get_object(self):
       obj = super().get_object()
       if obj.user != self.request.user:
           redirect('profile', kwargs={'pk':self.object.user.id})
       return obj

class UpdateProjectOffer(LoginRequiredMixin, UpdateView):
    model = ProjectOffer
    fields = [ 'title', 'desc' , 'price' , 'time_in_days' , 'revisions', 'image']
    template_name = 'update_project.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk':self.object.user.id})
    
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            redirect('profile', kwargs = {'pk':self.object.user.id})
        return obj

class DeleteProjectOffer(LoginRequiredMixin, DeleteView):
    model = ProjectOffer
    template_name = 'delete_project_offer.html'
    success_url = reverse_lazy('profile:<pk>')
    
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            redirect('profile', kwargs={'pk':self.object.user.id})
        return obj
    

class DeleteSkill(LoginRequiredMixin, DeleteView):
    model = Skills
    template_name = 'delete_skill.html'
    success_url = reverse_lazy('profile:<pk>')

    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            redirect('profile', kwargs={'pk':self.object.user.id})
        return obj


class OwnProfileDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(FreelancerProfile, pk=pk)
        
        if profile.user != request.user:
            return redirect('profile', kwargs={'pk': self.object.user.id})
        
        skills = Skills.objects.filter(fkFler=profile)
        project_offers = ProjectOffer.objects.filter(fkFler=profile)
        context = {
            'profile':profile,
            'skills':skills,
            'project_offers':project_offers
        }
        return render(request, 'own_profile_detail.html', context)


class OtherProfileDetailView(View):
     def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(FreelancerProfile, pk=pk)
        
        skills = Skills.objects.filter(fkFler=profile)
        project_offers = ProjectOffer.objects.filter(fkFler=profile)
        context = {
            'profile':profile,
            'skills':skills,
            'project_offers':project_offers
        }
        return render(request, 'other_profile_detail.html', context)


def checkFreelancerExist(self, request):
    try:    
        FreelancerProfile.objects.get(user=request.user)
    except FreelancerProfile.DoesNotExist:
        return redirect('freelancer_create')
    return None


