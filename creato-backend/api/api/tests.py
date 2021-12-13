from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import CreatoUser, Balance, Subscription, Token
import json
import uuid
# c = APIClient()

# Create your tests here.


class SetupTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='test@gmail.com',
            password='12345',
            username='tester')
        CreatoUser.objects.create(
            user=user,
            usdBalance=0,
            balance=None
        )
        Token.objects.create(
            uuid=12345, name="testToken", issueLimit=1000000
        )

    def test_response(self):
        """Testing whether api endpoint is properly working"""
        response = self.client.get('/hello')
        body = response.content.decode('utf-8')
        val = json.loads(body)
        self.assertEqual(val['message'], 'hello')

    def test_signUp(self):
        data = {
            "username": 'newtester',
            "password": '12345',
            "email": 's@gmail.com'
        }
        response = self.client.post('/signUp', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        testuser = User.objects.filter(username=data['username'])
        self.assertEqual(testuser.count(), 1)

    def test_signIn(self):
        data = {
            "username": 'tester',
            "password": '12345'
        }
        response = self.client.post('/signIn', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tokens(self):
        response = self.client.get('/tokens')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscribe(self):
        data = {
            'username': 'tester',
            'tokenUuid': '12345',
            'amount': 1000,
        }
        response = self.client.post('/subscribe', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = Token.objects.get(uuid='12345')

    def test_getSubscriptions(self):
        data = {
            'username': 'tester'
        }
        response = self.client.post('/subscriptions', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_issueToken(self):
        data = {
            'uuid': '12345'
        }
        response = self.client.post('/token/issue', data, format='json')
        token = Token.objects.get(uuid='12345')
        self.assertEqual(token.isIssued, True)

    def test_listToken(self):
        data = {
            'uuid': '12345'
        }
        self.client.post('/token/list', data, format='json')
        token = Token.objects.get(uuid='12345')
        self.assertEqual(token.isListed, True)
