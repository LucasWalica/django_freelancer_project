from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.views import View
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy  as _


from django.http import HttpResponse

# Home view
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'log/index.html')


# Logout view
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')



class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        return render(request, 'log/password_reset_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
        return render(request, 'log/password_reset_form.html', {'form': form})
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'log/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    title = _("Password reset")

class PasswordResetDoneView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'log/password_reset_done.html')


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        return render(request, 'log/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})


class PasswordResetCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'log/password_reset_complete.html')



class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'log/register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'User has been successfully registered')

            # enviar correo de bienvenida
            subject = "Welcome to our website"
            html_message = render_to_string('log/welcome_email.html', {'username': user.username})
            plain_message = strip_tags(html_message)
            from_email = 'projectwali272@gmail.com'
            to_email = user.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
            print('Form errors:', form.errors)  # Agregamos un print statement para ver errores
        return render(request, 'log/register.html', {'form': form})
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, 'log/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'log/login.html', {'form':form})
    


#test (it works)
def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'projectwali272@gmail.com'
    recipient_list = ['lucawali21@gmail.com']
    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse(f'Error: {e}')