from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User

from .models import Organization,Partner,Offer,Anketa,Bid
from anketa.serializers import (AnketaSerializers, AnketaPostSerializers, AnketaUpdateSerializers, UserSerializer, PartnerSerializer, 
                                BidSerializers, BidPostSerializers, OfferSerializers, OrganizationSerializer, BidPostStatusSerializers)

# Разрешение для партнеров, группа 'partner'
class IsPartner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='partner'):
            return True
        return False

# Разрешение для организаций, группа 'credit'
class IsCredit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='credit'):
            return True
        return False

class Partners(viewsets.ModelViewSet):
    """
    API партнеров.
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsPartner|IsCredit|permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class Organizations(viewsets.ModelViewSet):
    """
    API кредитных организаций
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsPartner|IsCredit|permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class Ankets(viewsets.ModelViewSet):
    """
    API для анкет
    """
    queryset = Anketa.objects.all()
    serializer_class = AnketaSerializers

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsPartner|permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        #фильтр по полю qwe
        order_filter = self.request.query_params.get('qwe', 'name')        
        
        if request.user.is_staff==True:
            queryset = Anketa.objects.all().order_by(order_filter)
        else:
            queryset = Anketa.objects.filter(partner__customer=self.request.user).order_by(order_filter)

        serializer = AnketaSerializers(queryset, many=True,context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
        queryset = Anketa.objects.all()
        
        if request.user.is_staff==True:
            user = get_object_or_404(queryset, pk=pk)
        else:
            user = get_object_or_404(queryset, Q(partner__customer=self.request.user) & Q(pk=pk))
        serializer = AnketaSerializers(user,context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        quer = Partner.objects.get(customer=self.request.user)

        data = {
                'name': request.data['name'],
                "surname": request.data['surname'],
                "first_name": request.data['first_name'],
                "Birthdate": request.data['Birthdate'],
                "telefon": request.data['telefon'],
                "pasport": request.data['pasport'],
                "ball": request.data['ball'],
                "partner": quer.id
            }

        serializer = AnketaPostSerializers(data=data, context={'request': request})

        if serializer.is_valid():           
             serializer.save()           
             return Response(serializer.data)
        else:
             return Response(status=400)


class Bids(viewsets.ModelViewSet):
    """
    API заявки.
    """
    queryset = Bid.objects.all()
    serializer_class = BidSerializers

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsPartner|IsCredit|permissions.IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsPartner|permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        #фильтр по полю qwe
        order_filter = self.request.query_params.get('qwe', 'create')


        obj=Bid.objects.all().order_by(order_filter)
        

        if request.user and request.user.is_staff:
            queryset = Bid.objects.all().order_by(order_filter)
        elif request.user and request.user.groups.filter(name='credit'):
            queryset = Bid.objects.all().exclude(status='n').order_by(order_filter)
        elif request.user and request.user.groups.filter(name='partner'):
            queryset = Bid.objects.filter(anketa__partner__customer=self.request.user).order_by(order_filter)

        
        serializer = BidSerializers(queryset, many=True,context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        print(request.data['anketa'])

        data = {
                "sent": request.data['sent'],
                "status": request.data['status'],
                "anketa": request.data['anketa'],
                "offer": request.data['offer']
            }
        serializer = BidPostSerializers(data=data, context={'request': request})       
        if serializer.is_valid():  
             serializer.save()           
             return Response(serializer.data)
        else:         
             return Response(status=400)

    def update(self, request, *args, **kwargs):

        
        if request.user.is_staff==True:
            data = {
                "sent": request.data['sent'],
                "status": request.data['status'],
                "anketa": request.data['anketa'],
                "offer": request.data['offer'],
            }
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = BidPostSerializers(instance, data=data, partial=partial,context={'request': request})
        else:
            quert =Bid.objects.filter(Q(anketa__partner__customer=self.request.user)&Q(id=kwargs['pk'])&Q(status='n')|Q(status='o'))
            if request.user and request.user.groups.filter(name='partner') and request.data['status'] in ['n','o'] and quert:
               
                data = {
                "status": request.data['status']
                }
            elif request.user and request.user.groups.filter(name='credit') and request.data['status'] in ['p','e','t','d']:
                data = {
                "status": request.data['status']
                }
            else:
                return Response(status=400)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = BidPostStatusSerializers(instance, data=data, partial=partial,context={'request': request})
        
        if serializer.is_valid():           
             self.perform_update(serializer)   
             return Response(serializer.data)
        else:
             return Response(status=400)


class Offers(viewsets.ModelViewSet):
    """
    API предложений
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsPartner|IsCredit|permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]