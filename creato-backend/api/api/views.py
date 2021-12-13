from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, login
from .models import Token, Subscription, Balance, CreatoUser
from .serializers import TokenSerializers, SubscriptionSerializers, BalanceSerializers, CreatoUserSerializers, UserSerializers
from django.forms.models import model_to_dict

import uuid

# Create your views here.


@api_view(['GET'])
def get(request):
    """
    This is just a test response for pinging.
    """
    return Response({'message': 'hello'})


@api_view(['POST'])
def signUp(request):
    """
    Method: POST
    URL: /signUp
    Content Type: application/json
    :param request: username (string), email (string), password (string)
    :return: success message

    Creates a new user and registers it inside the User Database.
    """
    user = User.objects.create_user(
        email=request.data['email'],
        password=request.data['password'],
        username=request.data['username'])
    creatouser = CreatoUser.objects.create(
        user=user, usdBalance=0, balance=None)
    user.creatouser = creatouser
    user.creatouser.save()
    user.save()
    return Response({'message': 'received'}, status=201)


@api_view(['POST'])
def signIn(request):
    """
    Method: POST
    URL: /signIn
    Content Type: application/json
    :param request: username (string), password (string)
    :return: success message

    Signs the user in. The user must be registered in to the Creato User Database.
    """
    user = authenticate(
        request,
        username=request.data['username'],
        password=request.data['password'])
    serializer = UserSerializers(user)
    print(serializer.data)
    if user is not None:
        login(request, user)
        return JsonResponse(serializer.data, safe=False, status=201)
    else:
        return JsonResponse({'message': 'Credentials are incorrect'})

# Token URLS


@api_view(['GET'])
def tokens(request):
    """
    Method: GET
    URL: /tokens
    Content Type: application/json
    :return: All tokens that are registered in the Database.
    """
    tokens = Token.objects.values()
    serializedTokens = TokenSerializers(tokens, many=True)

    return JsonResponse(serializedTokens.data, safe=False, status=201)


@api_view(['POST'])
def subscribe(request):
    """
    Method: POST
    URL: /susbscribe
    Content Type: application/json
    :param request: tokenUuid, username, amount
    :return: Serialized data of the current added subscription
    """
    token = Token.objects.get(uuid=request.data.pop('tokenUuid'))
    user = User.objects.get(username=request.data.pop('username'))
    totalPrice = request.data['amount'] * token.price
    if (totalPrice > user.creatouser.usdBalance):
        return JsonResponse({'error': 'Not enough balance'}, status=400)
    print(request.data)
    if (Subscription.objects.filter(token=token, user=user,
                                    status=Subscription.SUBSCRIBED).exists()):
        subscription = Subscription.objects.get(token=token, user=user)
        subscription.amount += request.data['amount']
    else:
        subscription = Subscription.objects.create(
            token=token, user=user, uuid=str(
                uuid.uuid4()), amount=request.data['amount'])
    token.subscribedAmount += request.data['amount']
    user.creatouser.usdBalance -= totalPrice
    print(user.creatouser.usdBalance)
    subscription.save()
    token.save()
    user.creatouser.save()
    serializer = SubscriptionSerializers(subscription)
    # print(subscription)
    return JsonResponse(serializer.data, status=201, safe=False)


@api_view(['DELETE'])
def unsubscribe(request, uuid):
    """
    Method: DELETE
    URL: /unsubscribe
    Content Type: application/json
    :param uuid: string
    :return: Empty response
    """
    subscription = Subscription.objects.get(uuid=uuid)
    print(uuid)
    user = subscription.user
    token = subscription.token
    token.subscribedAmount -= subscription.amount
    print(model_to_dict(user.creatouser))
    user.creatouser.usdBalance += subscription.amount * subscription.token.price
    subscription.delete()
    token.save()
    user.creatouser.save()
    return Response(status=204)


@api_view(['POST'])
def getSubscriptions(request):
    """
    URL: /subscriptions
    Content Type: application/json
    :param request: username
    :return: List of all subscriptions of the user for each token.
    """
    user = User.objects.get(username=request.data['username'])
    print(user.subscription_set.all())
    subscriptions = SubscriptionSerializers(
        user.subscription_set.filter(
            status=Subscription.SUBSCRIBED).all(), many=True)
    print(subscriptions)
    return JsonResponse(subscriptions.data, safe=False, status=201)


@api_view(['POST'])
def getIssuedTokens(request):
    """
    Method: POST
    URL: /tokens/issued
    Content Type: application/json
    :param request: username
    :return: List of all issued tokens
    """
    user = User.objects.get(username=request.data['username'])
    subscriptions = SubscriptionSerializers(
        user.subscription_set.filter(
            status=Subscription.ISSUED).all(), many=True)
    return JsonResponse(subscriptions.data, safe=False, stauts=201)


@api_view(['POST'])
def addBalance(request):
    """
    Method: POST
    URL: /addBalance
    Content Type: application/json
    :param request: username, amount
    :return: Serialized balance data of the user

    Adds balance to the specified user in the mock bank.
    """
    user = User.objects.get(username=request.data['username'])
    user.creatouser.usdBalance += request.data['amount']
    user.creatouser.save()
    serialized = CreatoUserSerializers(user.creatouser)
    return JsonResponse(serialized.data, status=201, safe=False)


@api_view(['POST'])
def getBalance(request):
    """
    Method: POST
    URL: /balance
    Content Type: application/json
    :param request:  username
    :return: balance data of the user
    """
    user = User.objects.get(username=request.data['username'])
    serializer = CreatoUserSerializers(user.creatouser)

    return JsonResponse(serializer.data, safe=False, status=201)


@api_view(['POST'])
def issueToken(request):
    """
    Method: POST
    URL: /token/issue
    Content Type: application/json
    :param request:  uuid
    :return: Empty Response

    ONLY FOR ADMIN PURPOSES. Issues the specified token.
    """
    token = Token.objects.get(uuid=request.data['uuid'])
    token.isIssued = True
    token.save()

    return JsonResponse({'message': 'success'}, status=201)


@api_view(['POST'])
def listToken(request):
    """
    Method: POST
    URL: /token/list
    Content Type: application/json
    :param request: uuid
    :return: Empty response

    ONLY FOR ADMIN PURPOSES. Lists tbe token.
    """
    token = Token.objects.get(uuid=request.data['uuid'])
    token.isListed = True
    token.save()

    return Response(status=204)


@api_view(['POST'])
def setOrder(request):
    """
    Method: POST
    URL: /order
    Content Type: application/json
    :param request: tokenUuid, type, amount
    :return: Order details

    Receives order and sends it to the trading engine.
    """
    return Response(status=204)


@api_view(['POST'])
def getOrders(request):
    """
    Method: POST
    URL: /orders
    Content Type: application/json
    :param request: id (TokenUuid), username
    :return: List of order details for a token.

    Sends a list of orders that are tied to the token and the user.
    """
