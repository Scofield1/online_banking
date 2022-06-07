from django.db import models
from django.contrib.auth.models import User
import random


def generate_acct_no():
    n = 10
    value = int(''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)]))
    return value

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

    def save(self, *args, **kwargs):
        if self.acct_no:
            self.acct_no = self.acct_no
            super(AccountDetailsModel, self).save(*args, **kwargs)
        else:
            self.acct_no = generate_acct_no()
            super(AccountDetailsModel, self).save(*args, **kwargs)


class TransactionModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    from_acct = models.ForeignKey(AccountDetailsModel, on_delete=models.CASCADE, related_name='from_acct')
    to_acct = models.ForeignKey(AccountDetailsModel, on_delete=models.CASCADE, related_name='to_acct', null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=20)
    amount = models.FloatField()
    status = models.CharField(max_length=10, null=True, blank=True,)

    class Meta:
        db_table = 'transfers'

    def __str__(self):
        return self.amount
