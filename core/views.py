from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from freelancer.models import FreelancerProfile
from recruiter.models import RecruiterProfile

class Home(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main') 
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        has_freelancer_profile = FreelancerProfile.objects.filter(user=request.user).exists()
        has_recruiter_profile = RecruiterProfile.objects.filter(user=request.user).exists() 
    
          
        recruiter_profile = None
        if has_recruiter_profile:
            recruiter_profile = RecruiterProfile.objects.get(user=request.user)

        context = {
            'has_freelancer_profile':has_freelancer_profile,
            'has_recruiter_profile':has_recruiter_profile,
            'recruiter_profile':recruiter_profile
        }
        return render(request, 'home.html', context)