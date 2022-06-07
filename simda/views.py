from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import *


def index(request):
    return render(request, 'main/index.html', {})


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return redirect('login')
    context = {'form': form}
    return render(request, 'user/register.html', context)


def login_pages(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')


def logout_page(request):
    logout(request)
    return redirect('/')


def profile(request):
    context = {}
    return render(request, 'user/profile.html', context)


@login_required(login_url='register')
def dashboard(request):
    acct_details = request.user.accountdetailsmodel_set.all()
    if request.method == 'POST':
        acct = request.POST.get('acct')
        amount = request.POST.get('amount')

        acct_no = acct_details.get(acct_no=acct)
        acct_no.balance += float(amount)
        acct_no.save()
        return redirect('dashboard')
    else:
        messages.info(request, 'invalid account')
    context = {'acct_details': acct_details}
    return render(request, 'main/dashboard.html', context)


@login_required(login_url='register')
def do_transfer(request):
    page = 'transfer'
    acct_details = request.user.accountdetailsmodel_set.all()
    if request.method == 'POST':
        from_acct = request.POST.get('aza')
        to_acct = request.POST.get('acct')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        acct_froms = acct_details.select_for_update().get(acct_no=from_acct)
        acct_frome = acct_details.select_for_update().get(acct_no=to_acct)

        with transaction.atomic():
            acct_froms.balance -= float(amount)
            acct_froms.save()

            acct_frome.balance += float(amount)
            acct_frome.description = description
            acct_frome.save()
            trans = TransactionModel.objects.create(from_acct=acct_froms,
                                                    to_acct=acct_frome,
                                                    description=description,
                                                    amount=amount
                                                    )
            trans.save()
        return redirect('dashboard')
    context = {'accts': acct_details,
               'page':page}
    return render(request, 'main/transaction.html', context)


@login_required(login_url='register')
def deposit(request):
    page = 'deposit'
    acct_details = request.user.accountdetailsmodel_set.all()
    if request.method == 'POST':
        acct = request.POST.get('aza')
        amount = request.POST.get('amount')

        acct_no = acct_details.select_for_update().get(acct_no=acct)

        with transaction.atomic():
            acct_no.balance += float(amount)
            acct_no.save()
            trans = TransactionModel.objects.create(from_acct=acct_no,
                                                    amount=amount,
                                                    type=page
                                                    )
            trans.save()
    context = {'page': page, 'accts': acct_details}
    return render(request, 'main/transaction.html', context)


@login_required(login_url='register')
def withdraw(request):
    page = 'withdraw'
    acct_details = request.user.accountdetailsmodel_set.all()
    if request.method == 'POST':
        acct = request.POST.get('aza')
        amount = request.POST.get('amount')

        acct_no = acct_details.select_for_update().get(acct_no=acct)

        with transaction.atomic():
            acct_no.balance -= float(amount)
            acct_no.save()
            trans = TransactionModel.objects.create(from_acct=acct_no,
                                                    amount=amount,
                                                    type=page
                                                    )
            trans.save()
    context = {'page': page, 'accts': acct_details}
    return render(request, 'main/transaction.html', context)


def transaction_page(request):
    context = {}
    return render(request, 'main/transaction.html', context)
