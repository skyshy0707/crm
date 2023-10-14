import requests

from django.utils import timezone
from django.core.signing import BadSignature
from django.db.models import Q, F, Sum
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework import permissions as rest_perm
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

from api import models, serializers
from api.services.whatsapp.models import WhatsappAPIConfig
from api.utilities import signer, get_whatsapp_message

from crm_transfer.email_settings import MAIN_URL, FRONTEND_URL
from .tasks import *


@api_view(['GET', 'POST'])
@permission_classes([rest_perm.IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        month = timezone.datetime.now().month
        COUNT_CARRIERS = models.Carrier.objects.filter(created_at__month=month).count()
        COUNT_CLOSED_LEADS = models.Lead.objects.filter(Q(created__month=month) & Q(category=True)).count()
        COUNT_OPENED_LEADS = models.Lead.objects.filter(Q(created__month=month) & Q(category=False)).count()
        COUNT_CLOSED_ORDERS = models.Lead.objects.filter(Q(created__month=month) & Q(status=True)).count()
        return Response({
            'carriers': {
                'value': COUNT_CARRIERS,
                'name': 'Carriers'
            },
            'closed_leads': {
                'value': COUNT_CLOSED_LEADS,
                'name': 'Closed Leads'
            },
            'opened_leads': {
                'value': COUNT_OPENED_LEADS,
                'name': 'Open Leads'
            },
            'closed_orders': {
                'value': COUNT_CLOSED_ORDERS,
                'name': 'Closed Orders'
            },
        }, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # За последний месяц
        if request.data['type'] == 1:
            month = timezone.datetime.now().month - 1
            COUNT_CARRIERS = models.Carrier.objects.filter(created_at__month=month).count()
            COUNT_CLOSED_LEADS = models.Lead.objects.filter(Q(created__month=month) & Q(category=True)).count()
            COUNT_OPENED_LEADS = models.Lead.objects.filter(Q(created__month=month) & Q(category=False)).count()
            COUNT_CLOSED_ORDERS = models.Lead.objects.filter(Q(created__month=month) & Q(status=True)).count()
        # За посление 3 месяца
        elif request.data['type'] == 2:
            month = timezone.datetime.now().month
            months = [
                month,
                month - 1,
                month - 2
            ]
            COUNT_CARRIERS = models.Carrier.objects.filter(created_at__month__in=months).count()
            COUNT_CLOSED_LEADS = models.Lead.objects.filter(Q(created__month__in=months) & Q(category=True)).count()
            COUNT_OPENED_LEADS = models.Lead.objects.filter(Q(created__month__in=months) & Q(category=False)).count()
            COUNT_CLOSED_ORDERS = models.Lead.objects.filter(Q(created__month__in=months) & Q(status=True)).count()
        # За последний год
        elif request.data['type'] == 3:
            year = timezone.datetime.now().year
            COUNT_CARRIERS = models.Carrier.objects.filter(created_at__year=year).count()
            COUNT_CLOSED_LEADS = models.Lead.objects.filter(Q(created__year=year) & Q(category=True)).count()
            COUNT_OPENED_LEADS = models.Lead.objects.filter(Q(created__year=year) & Q(category=False)).count()
            COUNT_CLOSED_ORDERS = models.Lead.objects.filter(Q(created__year=year) & Q(status=True)).count()
        # За всё время
        elif request.data['type'] == 0:
            COUNT_CARRIERS = models.Carrier.objects.count()
            COUNT_CLOSED_LEADS = models.Lead.objects.filter(category=True).count()
            COUNT_OPENED_LEADS = models.Lead.objects.filter(category=False).count()
            COUNT_CLOSED_ORDERS = models.Lead.objects.filter(status=True).count()
        else:
            COUNT_CARRIERS = 0
            COUNT_CLOSED_LEADS = 0
            COUNT_OPENED_LEADS = 0
            COUNT_CLOSED_ORDERS = 0
        return Response({
            'carriers': {
                'value': COUNT_CARRIERS,
                'name': 'Carriers'
            },
            'closed_leads': {
                'value': COUNT_CLOSED_LEADS,
                'name': 'Closed Leads'
            },
            'opened_leads': {
                'value': COUNT_OPENED_LEADS,
                'name': 'Open Leads'
            },
            'closed_orders': {
                'value': COUNT_CLOSED_ORDERS,
                'name': 'Closed Orders'
            },
        }, status=status.HTTP_200_OK)


'''
*                            *                             *

.   .   .
'''

class CreateLead(generics.CreateAPIView):
    permission_classes = [rest_perm.IsAdminUser]
    serializer_class = serializers.CreateLeadSerializer
    queryset = models.Lead.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data

        author = models.CrmUser.objects.get(pk=request.user.id)
        if author.is_carrier and not data['category']:
            carrier = models.Carrier.objects.get(email=author.email)
            carrier.extra_leads_per_month += models.Settings.objects.first().count_of_extra_open_leads
            carrier.save()

        data['author_lead'] = author
        region = models.Region.objects.get(pk=data['region'])
        data['region'] = region

        if data['type_transport'] == "":
            data.pop('type_transport')
        else:
            transport = models.TypeTransport.objects.get(pk=data['type_transport'])
            data['type_transport'] = transport

        if data['type_car'] == "":
            data.pop('type_car')
        else:
            car = models.AbstractCar.objects.get(pk=data['type_car'])
            data['type_car'] = car

        if data['transportation_cost'] == '':
            data.pop('transportation_cost')

        if data['hot'] == '':
            data.pop('hot')

        lead = models.Lead.objects.create(**data)

        if lead.hot:
            msg = get_whatsapp_message(lead.pk, hot=True)
            send_hot_lead.apply_async([lead.pk, msg], countdown=models.Settings.objects.first().send_hot_lead * 60)

        serializer = self.get_serializer(lead)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

'''
. . .

*                            *                             *
'''