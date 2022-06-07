from django.contrib.auth.models import User
from .models import TransactionModel, AccountDetailsModel
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import random

