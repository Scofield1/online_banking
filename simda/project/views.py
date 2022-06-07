from django.shortcuts import render, redirect
from django.db import transaction
from google_currency import convert
from .models import *
from decimal import Decimal
import json


def index(request):
    acct_details = request.user.accountdetailsmodel_set.all()
    accts = AccountModel.objects.get(id=1)
    aza = accts.accountdetailsmodel_set.all()
    context = {'acct_details': acct_details, 'aza': aza}
    return render(request, 'main/index.html', context)


def login_page(request):
    page = 'login'
    context = {'page': page}
    return render(request, 'user/register.html', context)


def register(request):
    page = 'sign-up'
    context = {'page': page}
    return render(request, 'user/register.html', context)


def trans_page(request):
    page = 'trans'
    acct_details = request.user.accountdetailsmodel_set.all()
    context = {'accts': acct_details, 'page': page}
    return render(request, 'main/transaction.html', context)


def trans_details(request):
    page = 'details'
    acct_details = request.user.accountdetailsmodel_set.all()
    if request.method == 'POST':
        from_acct = request.POST.get('from')
        to_acct = request.POST.get('to')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        acct_from = acct_details.select_for_update().get(acct_no=from_acct)
        acct_to = acct_details.select_for_update().get(acct_no=to_acct)

        get_type_from = str(acct_from.acct_type)
        get_type_to = str(acct_to.acct_type)

        sending_json = json.loads(convert(get_type_from, get_type_to, float(amount)))
        actual_amount = float(sending_json['amount'])
        charge_json = json.loads(convert('USD', get_type_from, 10))
        charge_fee = float(charge_json['amount'])
        total = f'{float(amount) + charge_fee}'

        with transaction.atomic():
            acct_from.balance -= float(total)
            acct_from.save()

            acct_to.balance += float(amount)
            acct_to.save()
            trans = TransactionModel.objects.create(from_acct=acct_from,
                                                    to_acct=acct_to,
                                                    description=description,
                                                    amount=amount
                                                    )
            trans.save()
    context = {'page': page,
               'amount': amount,
               'actual_amount': actual_amount,
               'charge_fee': charge_fee,
               'total': total,
               'to_acct': get_type_from,
               'from_acct': get_type_to,
               'aza': to_acct,
               }
    return render(request, 'main/transaction.html', context)

