from django.shortcuts import render
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

class CustomUserLogin(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user=False
    
class CustomUserPasswordReset(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    template_name = 'registration/password_reset_form.html'
    
class CustomUserPasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    
class CustomUserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    
class CustomUserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'	
    
class CustomUserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    
class CustomUserPasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'	