from django.contrib.auth import authenticate, login, logout

from django.shortcuts import  render, redirect
from django.urls import reverse

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import F, Sum, DecimalField, Case, When, Value

from django.views import View
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, ExtractYear
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import UserSerializer
from .forms import SignUpForm, SignInForm

User = get_user_model()

import logging
logger = logging.getLogger('django')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class IndexView(View):

	def get(self, request, path=''):
            username = request.user.username
            return render(request, 'index.html', {'username': username})



def logout_view(request):
	logout(request)
	return redirect("terminal:index")


class SignInView(View):
    def post(self, request):
        form = SignInForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("terminal:index") 
            else:
                messages.error(request, "Invalid username or password.")
        else:
          
            return render(request, "sign_in.html", {"sign_in_form": form})

    def get(self, request):
        form = SignInForm()
        return render(request, "sign_in.html", {
		"sign_in_form": form
	})


class SignUpView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("terminal:index")  
        else:
            messages.error(request, form.errors)
            return render(request, "sign_up.html", {"sign_up_form": form})

    def get(self, request):
        form = SignUpForm()
        return render(request, "sign_up.html", {"sign_up_form": form})