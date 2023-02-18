from .models import *

def find_user_by_email_or_phone(email_or_phone):
    if '@' in email_or_phone:
        try:
            return UserInfo.objects.get(email=email_or_phone)
        except:
            return None
    else:
        try:
            return UserInfo.objects.get(phone_number=email_or_phone)
        except:
            return None

def erase_all_contents():
    """
        It's a destructive and irreversible operation, use it with caution!
    """
    UserInfo.objects.all().delete()
    UserLevel.objects.all().delete()
    UserWallet.objects.all().delete()