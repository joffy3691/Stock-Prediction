from django.shortcuts import render,redirect
from .forms import UserRegisterform
from django.views.generic import CreateView
from django.contrib.auth.models import User

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterform
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')

# Create your views here.
