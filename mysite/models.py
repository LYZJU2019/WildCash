from django.db import models
from .config import *
from datetime import datetime


class UserInfo(models.Model):
    """
    A table that stores (nearly) static information of each user
    """

    # personal information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)           # TODO: check email requirements (no duplication!) & sending verification code
    phone_number = models.CharField(max_length=30)      # TODO: check phone number requirements (no duplication) & sending verification code
    password = models.CharField(max_length=30)          # TODO: check password requirements
    birthday = models.DateField()                       # TODO: check birthday requirements (age >= 18)
    user_id = models.CharField(max_length=30, primary_key=True)           # This field should be unique!

    # tracing purpose
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_logged_in = models.BooleanField(default=False)
    logged_in_at = models.DateTimeField(auto_now=True)
    logged_in_ip = models.GenericIPAddressField(default='0.0.0.0') 
    
    # verification
    has_email_verified = models.BooleanField(default=False)
    has_phone_verified = models.BooleanField(default=False)
    has_KYC_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserLevel(models.Model):
    """
        A table that stores dynamic information (level, points, friends, digspeed, etc.) of each user
    """

    # primary key
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)

    # user level information
    level = models.IntegerField(default=START_LEVEL)
    level_progress = models.IntegerField(default=0)
    num_friends_invited = models.IntegerField(default=0)
    num_friends_joined = models.IntegerField(default=0)
    friends_list = models.ManyToManyField("self", blank=True)
    num_videos_watched = models.IntegerField(default=0)
    dig_speed = models.IntegerField(default=START_DIG_SPEED)
    total_points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_id}: {self.level}"

class UserWallet(models.Model):
    """
        A table that stores the wallet information of each user
    """

    # primary key
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)

    # wallet information
    balance = models.IntegerField(default=0)
    num_coins = models.IntegerField(default=0)
    num_diamonds = models.IntegerField(default=0)
    num_tickets = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_id}: {self.balance}"

