from django.contrib.auth.models import User
from django.db import models


class SoliGroup(models.Model):
    name = models.CharField(64)
    members = models.ManyToManyField(User, through='SoliGroupMembership')


class SoliGroupMembership(models.Model):
    is_trustee = models.BooleanField(default=False)
    auto_monthly_is_active = models.BooleanField(default=False)
    auto_monthly_value = models.IntegerField()


class Balance(models.Model):  ## gilt immer fuer einen Monat
    membership = models.ForeignKey(SoliGroupMembership, on_delete=models.CASCADE)
    limit = models.IntegerField()
    # soll aus .bookings berechnet werden: value = models.Integer.Field()  #150

    is_active = models.BooleanField()
    begin_date = models.DateField(auto_now=True)
    end_date = models.DateField()  # default next month, maybe null if endless / "Einmalzahlung"?


class Transaction(models):
    """n incomingPayments, 1 outgoingPayment"""
    date = models.DateField(auto_now=True)


class IncomingPayment(models):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    value = models.IntegerField()
    balance = models.ForeignKey(Balance, on_delete=models.PROTECT)


class OutgoingPayment(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    value = models.IntegerField()
    payee = models.ForeignKey(SoliGroupMembership, on_delete=models.PROTECT)
