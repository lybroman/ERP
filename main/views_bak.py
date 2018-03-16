
# -*- coding: utf-8 -*-
from rest_framework import generics
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render_to_response

from django.template import RequestContext
import sys, os, time, copy, json
import datetime
import traceback

from django.contrib.auth import authenticate, login

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import socket
from main.models import salesExetable
from main.serializers import salesExetableSerializer
from django.utils import timezone
import uuid, json
from django.http import StreamingHttpResponse

STATUS_OK = HttpResponse(json.dumps({"status" : "okay"}))

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def log_in(request):
    try:
        if request.method == 'GET':
            return render_to_response('login.html', context_instance=RequestContext(request))
        elif request.method == 'POST':
            if request.POST.has_key('login'):
                username = request.POST.get('USERNAME')
                password = request.POST.get('PASSWORD')
                user = authenticate(username=username, password=password)
                if user is not None:
                     if user.is_active:
                         login(request, user)
                         return STATUS_OK
                     else:
                        return HttpResponse('Not active')
                else:
                      return HttpResponse('Not a valid user')
            elif request.POST.has_key('register'):
                return STATUS_OK
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_form(request, form_uuid=None):
     try:
        if form_uuid != None:
            if request.method == 'GET':
                return render_to_response('sales_form.html',
                                          {'data':{'uuid':uuid.uuid1(), 'specification':'未上传'}},
                                          context_instance=RequestContext(request))
            elif request.method == 'POST':
                submitSalesExetable(request)
                return HttpResponse(repr('status: Add success!'))
        else:
            selectedExetable = salesExetable.objects.filter(uuid = 'fdeb9fe1-f022-11e5-b19a-001bfcc605c0')
            if len(selectedExetable) != 1:
                return HttpResponse("uuid conflict!")
            serializer=salesExetableSerializer(selectedExetable[0])

            if request.method == 'GET':
                content = serializer.data
                content['uuid'] = uuid.uuid1()
                return render_to_response('sales_form.html', {'data': content},context_instance=RequestContext(request))
            elif request.method == 'POST':
                '''
                filename = 'uploadFiles/2.jpg'
                response = HttpResponse(readFile(filename))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=%s' % filename
                return response
                '''
                try:
                    data = json.loads(request.body)
                    if 'operation' in data.keys():
                        if "download" in data["operation"]:
                            if "specification" in data["target"]:
                                filename = r'uploadFiles/2.jpg'
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename="aaa.jpg"'
                                return response
                            else:
                                return HttpResponse(repr('No defined area...'))
                        else:
                            return HttpResponse(repr('Cannot be downloaded...'))
                except:
                    content = serializer.data
                    content['isLatest'] = 0
                    serializer.update(selectedExetable[0],content)
                    submitSalesExetable(request)
                    return HttpResponse(repr('status: Revise success!'+str(request.POST.get('uuid'))))
                '''
                if request.POST.has_key('specification'):
                    filename = 'uploadFiles/2.jpg'
                    response = HttpResponse(readFile(filename))
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment;filename=%s' % filename
                    return response
                '''




     except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def readFile(fn, buf_size=262120):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()

def submitSalesExetable(request):
    try:
        q = salesExetable()
        q.No = request.POST.get('No')
        q.companyName = request.POST.get('companyName') # required
        q.salesman = request.POST.get('salesman')
        q.companyInfo = request.POST.get('companyInfo')
        q.country = request.POST.get('country')
        q.productType = request.POST.get('productType') # required

        q.date = request.POST.get('date') # required
        if q.date == '':
            q.date = None
        q.productCode = request.POST.get('productCode')
        q.mag = request.POST.get('mag')

        #form = fileUploadForm( request.POST, request.FILES )
        #if form.is_valid():
            #q.specification = form.cleaned_data['specification']
        q.specification = request.FILES.get('specification')
        q.quantityDemand = request.POST.get('quantityDemand')
        q.opponent = request.POST.get('opponent')
        q.quantityActual = request.POST.get('quantityActual')
        q.assessment = request.POST.get('assessment')
        q.priceUnit = request.POST.get('priceUnit')
        q.priceTotal = request.POST.get('priceTotal')
        q.payment = request.POST.get('payment')

        q.supplierP = request.POST.get('supplierP')
        q.inquiryP = request.POST.get('inquiryP')
        q.quoteP = request.POST.get('quoteP')
        q.sampleP = request.POST.get('sampleP')
        q.testP = request.POST.get('testP')
        q.smallOrderP = request.POST.get('smallOrderP')

        q.supplier = request.POST.get('supplier')
        q.dateDeliver = request.POST.get('dateDeliver')
        if q.dateDeliver == '':
            q.dateDeliver = None
        q.sampleNum = request.POST.get('sampleNum')
        q.sampleNo = request.POST.get('sampleNo')
        q.test = request.POST.get('test')
        q.smallOrder = request.POST.get('smallOrder')

        q.dateQuote = request.POST.get('dateQuote')
        if q.dateQuote == '':
            q.dateQuote = None
        q.quoteApply = request.POST.get('quoteApply')
        q.quoteOrder = request.POST.get('quoteOrder')

        q.dateOrder = request.POST.get('dateOrder')
        if q.dateOrder == '':
            q.dateOrder = None
        q.orderNo = request.POST.get('orderNo')
        q.orderInfo = request.POST.get('orderInfo')

        q.dateContract = request.POST.get('dateContract')
        if q.dateContract == '':
            q.dateContract = None
        q.contractNo = request.POST.get('contractNo')
        q.contractInfo = request.POST.get('contractInfo')

        q.contractReviewNoS = request.POST.get('contractReviewNoS')
        q.salesNoS = request.POST.get('salesNoS')

        q.contractReviewNoP = request.POST.get('contractReviewNoP')
        q.salesNoP = request.POST.get('salesNoP')

        q.produceNo = request.POST.get('produceNo')
        q.produceStatus = request.POST.get('produceStatus')
        q.transNo = request.POST.get('transNo')

        q.comments = request.POST.get('comments')
        q.personCharge = request.POST.get('personCharge')
        q.personSupervise = request.POST.get('personSupervise')
        q.conclusion = request.POST.get('conclusion')

        q.uuid = request.POST.get('uuid')
        q.isLatest = 1
        q.save()
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")
