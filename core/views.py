from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main') 
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        
        return render(request, 'home.html')