from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import FreelancerProfile, ProjectOffer, Skills, workingSectors
from recruiter.models import RecruiterProject
from .forms import SkillsForm, FreelancerProfileForm, ProjectOfferForm 
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from recruiter.models import RecruiterProject, RecruiterProfile

#Cruds para todos los modelos (para posteriormente implementarlos en el fronted)

# Add comments logic, 
# (basically they can only be added when project finished by X freelancer 
# or project Finished)

# add update and delete project logic -> only when projects not active 

class CreateFreelancerProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if FreelancerProfile.objects.filter(user=request.user).exists():
            return redirect('profile', pk=request.user.freelancerprofile.pk)
        form = FreelancerProfileForm()
        context = {
            'form': form
        }
        return render(request, 'freelancer/createFreelancer.html', context)
    
    def post(self, request, *args, **kwargs):
        form = FreelancerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if FreelancerProfile.objects.filter(user=request.user).exists():
                return redirect('profile', pk=request.user.freelancerprofile.pk)
            user = request.user
            bio = form.cleaned_data.get('bio')
            active = True
            stars = 0
            image = form.cleaned_data.get('image')
            f = FreelancerProfile.objects.create(user=user, bio=bio, active=active, stars=stars, image=image)
            return redirect('profile', pk=f.pk)
        context = {
            'form': form
        }
        return render(request, 'freelancer/createFreelancer.html', context)

class CreateSkillView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
    
        result = checkFreelancerExist(self, request)
        if result:    
            return result
    
        form = SkillsForm()
        context = {
            'form':form
        }
        return render(request, 'freelancer/createSkill.html', context)
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
                    return redirect('freelancer/createSkill.html')
                
                s, created = Skills.objects.get_or_create(fkFler=freelancer_profile, name=name)
                s.save()
                return redirect('profile', pk=request.user.freelancerprofile.pk)
            context = {
                'form':form
            }
            return render(request, 'createSkill.html', context)
        
class CreateProjectOfferView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        result = checkFreelancerExist(self, request)
        if result:
            return result
        
        form = ProjectOfferForm()
        context = {
            'form':form
        }
        return render(request, 'freelancer/createProject.html', context)
    
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
                catOne = form.cleaned_data.get('catOne')
                catTwo = form.cleaned_data.get('catTwo')
                
                freelance_profile = FreelancerProfile.objects.get(user=request.user)

                p, created = ProjectOffer.objects.get_or_create(fkFler=freelance_profile,
                                            title=title, desc=desc, price=price, 
                                            time_in_days=time_in_days, 
                                            revisions=revisions, image=image, 
                                            catOne=catOne, catTwo=catTwo)
                p.save()
                return redirect('profile', pk=request.user.freelancerprofile.pk)
            context= {
                'form':form
            }
            return render(request, 'freelancer/createProject.html', context)

class UpdateFreelancerProfileView(LoginRequiredMixin, UpdateView):
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

class UpdateProjectOfferView(LoginRequiredMixin, UpdateView):
    model = ProjectOffer
    fields = [ 'title', 'desc' , 'price' , 'time_in_days' , 'revisions', 'image', 'catOne', 'catTwo']
    template_name = 'freelancer/update_project.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.freelancerprofile.id})
        
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            return redirect('profile', pk=self.request.user.freelancerprofile.id)
        return obj

class DeleteProjectOfferView(LoginRequiredMixin, DeleteView):
    model = ProjectOffer
    template_name = 'freelancer/delete_project_offer.html'
    
     
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.freelancerprofile.pk})
    
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            return redirect('profile', kwargs={'pk': self.request.user.freelancerprofile.pk})
        return obj
    
    

class DeleteSkillView(LoginRequiredMixin, DeleteView):
    model = Skills
    template_name = 'freelancer/delete_skill.html'
     
     # hay que testear los metodos de redireccion
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.freelancerprofile.pk})
    
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            return redirect('profile', kwargs={'pk': self.request.user.freelancerprofile.pk})
        return obj

class OwnProfileDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(FreelancerProfile, pk=pk)
        if profile.user != request.user:
            try:
                user_profile = FreelancerProfile.objects.get(user=request.user)
            except FreelancerProfile.DoesNotExist:
                return redirect('profileCreate')
            
            return redirect('profile', pk=user_profile.pk)
        skills = Skills.objects.filter(fkFler=profile)
        project_offers = ProjectOffer.objects.filter(fkFler=profile)
        context = {
            'profile': profile,
            'skills': skills,
            'project_offers': project_offers
        }
        return render(request, 'freelancer/own_profile_detail.html', context)
    
    def get_object(self):
        return get_object_or_404(FreelancerProfile, user=self.request.user)


class OtherProfileDetailView(View):
     def get(self, request, pk, *args, **kwargs):
        checkRecruiterExists(self, request)
        profile = get_object_or_404(FreelancerProfile, pk=pk)
        skills = Skills.objects.filter(fkFler=profile)
        project_offers = ProjectOffer.objects.filter(fkFler=profile)
        context = {
            'profile':profile,
            'skills':skills,
            'project_offers':project_offers
        }
        return render(request, 'freelancer/other_profile_detail.html', context)



def checkFreelancerExist(self, request):
    try:    
        FreelancerProfile.objects.get(user=request.user)
    except FreelancerProfile.DoesNotExist:
        return redirect('profileCreate')
    return None


def checkRecruiterExists(self, request):
    try:
        RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        return redirect('profileCreate')
    return None 



# Add limitator and redirections =D 
# change this view with more context
class ProjectListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        #test this
        checkFreelancerExist(self, request)
        
        query = self.request.GET.get('query')
        sector_filter = request.GET.get('sector')

        user = request.user

        recruiter_profile = RecruiterProfile.objects.get(user=user)
        freelancer_profile = FreelancerProfile.objects.get(user=user)

        projectList = RecruiterProject.objects.exclude(fkRec=recruiter_profile)

        sectors = [(sector.value, sector.name) for sector in workingSectors]
        
        if query:
            projectList = ProjectOffer.objects.filter(
                Q(title__icontains=query) | 
                Q(desc__icontains=query)
            ).exclude(fkFler=freelancer_profile).order_by('fkFler__stars')
            

        if sector_filter:
            projectList = projectList.filter(Q(catOne__iexact=sector_filter) | Q(catTwo__iexact=sector_filter))

        
        context = {
            'projectList':projectList,
            'sectors':sectors
        }
        return render(request, 'listing/freelancerSearch.html', context)



class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        checkRecruiterExists(self, request)
        freelancerProject = get_object_or_404(ProjectOffer, pk=pk)
        context = {
            'freelancerProject':freelancerProject
        }
        return render(request, 'listing/freelancer_project_detail.html', context)