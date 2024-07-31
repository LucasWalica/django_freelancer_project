from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import RecruiterProfile, RecruiterProject, CommentOnRecruiter
from .forms import RecruiterProjectForm, RecruiterProfileForm, UpdateRecruiterProfileForm
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Add comments logic, 
# (basically they can only be added when project donde by X freelancer 
# or project Finished)

class CreateRecruiterProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if RecruiterProfile.objects.filter(user=request.user).exists():
            return redirect('recruiter', pk=request.user.recruiterprofile.pk)
        form = RecruiterProfileForm()
        context = {
            'form':form
        }
        return render(request, 'recruiter/createRecruiter.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = RecruiterProfileForm(request.POST, request.FILES)
            if form.is_valid():
                if RecruiterProfile.objects.filter(user=request.user).exists():
                    return redirect('recruiter', pk=request.user.recruiterprofile.pk)
                user = request.user
                bio = form.cleaned_data.get('bio')
                active = True
                stars = 0
                image = form.cleaned_data.get('image')
                r = RecruiterProfile.objects.create(user = user, bio = bio, active=active, stars=stars, image=image)
                return redirect('recruiter', pk=r.pk)
            context = {
                'form':form
            }
            return render(request, 'recruiter/createRecruiter.html', context)
        

class CreateRecruiterProject(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        result = checkRecruiterExists(self, request)
        if result:
            return result
        
        form = RecruiterProjectForm()
        context = {
            'form':form
        }
        return render(request, 'recruiter/createProject.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = RecruiterProjectForm(request.POST)
            if form.is_valid():
                result = checkRecruiterExists(self, request)
                if result:
                    return result
                
                recruiter_profile = request.user.recruiterprofile
                title = form.cleaned_data.get('title')
                desc = form.cleaned_data.get('desc')
                catOne = form.cleaned_data.get('catOne')
                catTwo  = form.cleaned_data.get('catTwo')
                vacancies = form.cleaned_data.get('vacancies')

                rp = RecruiterProject.objects.get_or_create(fkRec=recruiter_profile,
                                                            title = title, desc=desc,
                                                            catOne =catOne, catTwo=catTwo,
                                                            vacancies=vacancies)
                return redirect('recruiter', pk=request.user.recruiterprofile.pk)
            context = {
                'form':form
            }
            return render(request, 'recruiter/createProject.html', context)



class UpdateRecruiterProfile(LoginRequiredMixin, UpdateView):
    model = RecruiterProfile
    form_class = UpdateRecruiterProfileForm
    template_name = 'recruiter/update_recruiter.html'

    def get_success_url(self):
            return reverse_lazy('recruiter', kwargs={'pk': self.object.user.id})
        
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return redirect('recruiter', pk=self.request.user.recruiterprofile.pk)
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
# this could be problematic because if its possible to update 
# meanwhile someone is working on it, could cause scammming 
# create active conditional 
 
class UpdateRecruiterProject(LoginRequiredMixin, UpdateView):
    model = RecruiterProject
    fields = ['title', 'desc', 'catOne', 'catTwo', 'vacancies']
    template_name = 'recruiter/update_recruiter_project.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.recruiter_profile.id})
        
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            return redirect('profile', pk=self.request.user.recruiter_profile.id)
        return obj

# add active atribute 
class DeleteRecruiterProject(LoginRequiredMixin, View):
    model = RecruiterProject
    template_name = 'recruiter/delete_project.html'
    
    def get_success_url(self):
        return reverse_lazy('recruiter', kwargs={'pk': self.request.user.recruiter_profile.pk})
    
    def get_object(self):
        obj = super().get_object()
        if obj.fkFler.user != self.request.user:
            return redirect('recruiter', kwargs={'pk': self.request.user.recruiter_profile.pk})
        return obj


# add commets when logic added
class OwnRecruiterView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(RecruiterProfile, pk=pk)
        if profile.user != request.user:
            try:
                user_profile = RecruiterProfile.objects.get(user=request.user)
            except RecruiterProfile.DoesNotExist:
                return redirect('profileCreate')
            return redirect('recruiter', pk=user_profile.pk)
        
        project_offers = RecruiterProject.objects.filter(fkRec=profile)
        context = {
            'profile': profile,
            'project_offers': project_offers
        }
        return render(request, 'recruiter/own_profile_detail.html', context)

    def get_object(self):
        return get_object_or_404(RecruiterProfile, user=self.request.user)

def checkRecruiterExists(self, request):
    try:
        RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        return redirect('profileCreate')
    return None 