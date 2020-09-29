# from rest_framework import viewsets
# from profiles.models import SellerProfile
# from .serializers import SellerSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class=SellerSerializer
#     queryset = SellerProfile.objects.all()


from .serializers import *
from profiles.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(username=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.key
            return Response({
                "message": "success",
                "status": status.HTTP_200_OK,
                "user": context
            })
        else:
            context['message'] = 'failure'
            context['status'] = status.HTTP_422_UNPROCESSABLE_ENTITY

        return Response(context)


class SellerViewSet(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    queryset = SellerProfile.objects.all()
    def get(self, format=None):

        seller = SellerProfile.objects.all()
        serializer = SellerSerializer(seller, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class CreateAPIView(CreateAPIView):
    def create(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({"message": "success", "status": True, 'Records': serializer.data, })


@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            # data['response']="successfully registerd new user"
            # data['email']=user.email
            # data['username']=user.username
            token = Token.objects.get(user=account).key
            return Response({
                "message": "success",
                "status": status.HTTP_201_CREATED,
                "user": serializer.data,
                "token": token
            })
        else:
            data = serializer.errors
        return Response(data)


class BuyerViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        print("retrieve method called")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return user

    # def get(self, format=None):
    # #     print("get called")
    #     seller = ClientProfile.objects.all()
    #     serializer = UserSerializer(seller, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     print("list called")
    #     ret = super(BuyerViewSet, self)
    #     return Response({"user":request.data, "message":"success"})

    # def retrieve(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})

    # def list(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})

    # def get(self, format=None):
    #     print("get called")
    #     seller = ClientProfile.objects.all()
    #     serializer = UserSerializer(seller, many=True)
    #     return Response(serializer.data)

    # def post(self, request,*args, **kwargs):
    #     if request.method=='POST':
    #         print('called')
    #         serializer = UserSerializer(data=request.data)
    #         if serializer.is_valid(raise_exception=ValueError):
    #             data=serializer.create(validated_data=request.data)
    #             # return Response(serializer.data, status=status.HTTP_201_CREATED)
    #             return JsonResponse(
    #                 {
    #                     "user": data,
    #                     "message":"Successfully.",
    #                     "status" : True,
    #                 }
    #             )
    #         return Response(serializer.error_messages,
    #                         status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def registration_view(request):
#     if request.method=='POST':
#         serializer=User
