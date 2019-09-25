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

class Phonenumber(BaseModel):
    number = models.CharField(max_length=24)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    owner_email = models.EmailField()

class UserProfile(BaseModel):
    referral_code = models.CharField(max_length=120)

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