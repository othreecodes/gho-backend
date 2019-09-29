import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from gho.core.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
        Balance.objects.create(owner=instance)

class Phonenumber(BaseModel):
    number = models.CharField(max_length=24)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    owner_email = models.EmailField()

class UserProfile(BaseModel):
    referral_code = models.CharField(max_length=120)
    user = models.OneToOneField('users.User',on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_new_referal_code()
        return super(UserProfile, self).save(*args, **kwargs)


    def generate_new_referal_code(self):
        """
        Returns a unique passcode
        """
        def _passcode():
            return str(uuid.uuid4().hex)[0:8]
        passcode = _passcode()
        while UserProfile.objects.filter(referral_code=passcode).exists():
            passcode = _passcode()
        return passcode


class PhoneVerification(BaseModel):
   
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    verification_code = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.msisdn)+'-'+ str(self.verification_code)

    class Meta:
        verbose_name_plural = "Existing User Verification Codes"


class NewUserPhoneVerification(BaseModel):

    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    verification_code = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    email = models.CharField(max_length=100)
 
    def __str__(self):
        return str(self.phone_number)+'-'+ str(self.verification_code)

    class Meta:
        verbose_name_plural = "New User Verification Codes"



class Referral(BaseModel):
    owner = models.OneToOneField('users.User',on_delete=models.CASCADE,related_name="owner")
    referred = models.OneToOneField('users.User',on_delete=models.CASCADE, related_name="referred")


class Subscription(BaseModel):
    name = models.CharField(max_length=256)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    discount = models.FloatField(0.0)
    number_of_refferal_for_free = models.IntegerField()


class UserSubscription(BaseModel):
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE)
    is_free = models.BooleanField(default=False)

class Balance(BaseModel):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book_balance = models.FloatField(default=0.0) 
    available_balance = models.FloatField(default=0.0) 
    active = models.BooleanField(default=True)
