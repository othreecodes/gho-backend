from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
import mock
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from ..models import User, NewUserPhoneVerification
from .factories import UserFactory
import time
from random import randint
fake = Faker('en_GB')

class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.email = fake.email()
        #generate fake number
        self.phone_number = "+234902{}".format(str(time.time())[:7])
    
    def test_user_cant_get_phone_veirfication_code_without_sending_params(self):
        response = self.client.post('/api/v1/phone/')
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('gho.users.utils.generate_new_user_passcode', return_value="123456")
    def test_user_can_get_phone_veirfication_code(self, generate_new_user_passcode):
        response = self.client.post('/api/v1/phone/',{"email":self.email,"phone_number":self.phone_number})
        
        data = response.json()

        eq_(data['verification_code'],"123456")
        eq_(NewUserPhoneVerification.objects.filter(phone_number=self.phone_number,email=self.email,verification_code="123456").exists(),True)
        eq_(response.status_code, status.HTTP_201_CREATED)

    @mock.patch('gho.users.utils.generate_new_user_passcode', return_value="123456")
    def test_user_can_not_verify_phone_number_when_code_is_incorrect(self,generate_new_user_passcode):
        response = self.client.post('/api/v1/phone/',{"email":self.email,"phone_number":self.phone_number})
        
        data = response.json()

        eq_(data['verification_code'],"123456")

        response = self.client.put(f'/api/v1/phone/{data["id"]}/',{"email":self.email,"code":"456"})
        
        eq_(response.status_code,400)


    @mock.patch('gho.users.utils.generate_new_user_passcode', return_value="123456")
    def test_user_can_not_verify_phone_number_when_no_code_is_sent(self,generate_new_user_passcode):
        response = self.client.post('/api/v1/phone/',{"email":self.email,"phone_number":self.phone_number})
        
        data = response.json()

        eq_(data['verification_code'],"123456")

        response = self.client.put(f'/api/v1/phone/{data["id"]}/',{"email":self.email})
        
        eq_(response.status_code,400)

 

