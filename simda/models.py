from django.db import models
from django.contrib.auth.models import User
import random
import uuid


def generate_acct_no():
    n = 10
    value = int(''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)]))
    return value


def generate_ref_no():
    code = str(uuid.uuid4())[:13].replace('-', '').lower()
    return code


class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default='profile_pic.svg', upload_to='profile')

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name


class AccountModel(models.Model):
    acct_type = models.CharField(max_length=4)

    class Meta:
        db_table = 'account type'

    def __str__(self):
        return self.acct_type


class AccountDetailsModel(models.Model):
    acct_type = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)
    acct_no = models.IntegerField(unique=True, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'account details'

    def __str__(self):
        return self.owner.username



class TransactionModel(models.Model):
    trans_id = models.CharField(max_length=15)
    from_acct = models.ForeignKey(AccountDetailsModel, on_delete=models.CASCADE, related_name='from_acct')
    to_acct = models.ForeignKey(AccountDetailsModel, on_delete=models.CASCADE, related_name='to_acct', null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=20)
    amount = models.FloatField()
    type = models.CharField(null=True, blank=True, max_length=15)

    class Meta:
        db_table = 'transfers'

    def save(self, *args, **kwargs):
        self.trans_id = generate_ref_no()
        super(TransactionModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.trans_id

