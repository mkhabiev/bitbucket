from random import randint
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from web.models import Customer, ConfirmationCode
from .forms import UserOurRegistration
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response


def register(request):
    if request.method == 'POST':
        form = UserOurRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('home')
    else:
        form = UserOurRegistration()
    return render(request, 'registration.html', {'form': form})


def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('redirect to a new page')


class RegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = Customer.objects.create_user(username=username, password=password)
        user.save()
        code = randint(100000, 999999)
        send_mail(subject='New subject', message='http://127.0.0.1:8000/confirm/{code}',
                  from_email=settings.EMAIL_HOST,
                  recipient_list=[email])
        return Response(status=status.HTTP_200_OK)


class ConfirmApiView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        codes = ConfirmationCode.objects.get(code=code,
                                             valid_until__gte=datetime.now())
        user = codes.user
        user.is_active = True
        user.save()
        codes.delete()
        try:
            token = Token.objects.get(user=self.request.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=self.request.user)
        return Response(data={'token': token.key},
                        status=status.HTTP_200_OK)


class LoginApiView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'],
                            password=request.data.get('password', 'admin123'))
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User not found'})
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)