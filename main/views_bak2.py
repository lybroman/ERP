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
import uuid
from main.models import salesExetable, salesStatisticstable
from main.serializers import salesExetableSerializer, salesStatisticstableSerializer
from django.contrib.auth import authenticate, login

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import socket

from django.http import HttpResponseRedirect

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
                         #return  HttpResponse(json.dumps({"status" : request.user.username}))
                         """
                         if sales
                         """
                         #return render_to_response('sales.html', context_instance=RequestContext(request))
                         #return HttpResponse(request.user.has_perm('user_control.create_a_new') )
                         if request.user.has_perm('main.is_a_salesman'):
                            return HttpResponseRedirect('/ERP/sales_main/')
                         else:
                            return HttpResponse('Not a salesman!')
                     else:
                        return HttpResponse('Not active')
                else:
                      return HttpResponse('Not a valid user')
            elif request.POST.has_key('register'):
                return STATUS_OK
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_main(request):
    try:
        if request.method == 'GET':
            return render_to_response('sales_main.html', context_instance=RequestContext(request))
        elif request.method == 'POST':
            pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_form(request, form_uuid=None):
     productDictionary = {"带材":1, "铁芯":2, "器件":3}
     try:
        if request.method == 'GET':
            if not form_uuid:
                """
                add a new form
                """
                data_to_render = {}
                data_to_render['uuid'] = uuid.uuid1()
                data_to_render['specification'] = None
                data_to_render['sampleNo'] = None
                data_to_render['smallOrder'] = None
                data_to_render['quoteOrder'] = None
                data_to_render['orderNo'] = None
                data_to_render['contractNo'] = None
                data_to_render['contractReviewNoS'] = None
                data_to_render['salesNoS'] = None
                data_to_render['contractReviewNoP'] = None
                data_to_render['salesNoP'] = None
                data_to_render['produceNo'] = None
                data_to_render['productType'] = 1
                return render_to_response('sales_form.html', {'data': data_to_render}, context_instance=RequestContext(request))
            else:
                """
                query form from MYSQL
                """
                selectedExetable = salesExetable.objects.filter(uuid = form_uuid)
                if len(selectedExetable) > 1:
                    return HttpResponse("uuid conflict!")
                elif len(selectedExetable) < 1:
                    return HttpResponse("uuid not found!")
                serializer=salesExetableSerializer(selectedExetable[0])
                data_to_render = serializer.data
                #data_to_render['uuid'] = uuid.uuid1()
                return render_to_response('sales_form.html', {'data': data_to_render}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            # If click download button
            if request.POST.has_key('operation'):
                data = json.loads(str(request.POST["operation"]))
                selectedExetable = salesExetable.objects.filter(uuid = data["uuid"])
                # When adding a new form
                if len(selectedExetable) < 1:
                    return HttpResponse("Add a new form: do nothing!")
                # When update an existing form
                elif len(selectedExetable) == 1:
                    if "download" in data["operation"]:
                        if "specification" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['specification']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "sampleNo" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['sampleNo']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "smallOrder" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['smallOrder']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "quoteOrder" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['quoteOrder']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "orderNo" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['orderNo']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "contractNo" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['contractNo']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "contractReviewNoS" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['contractReviewNoS']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "salesNoS" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['salesNoS']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "contractReviewNoP" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['contractReviewNoP']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "salesNoP" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['salesNoP']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        elif "produceNo" in data["target"]:
                            serializer=salesExetableSerializer(selectedExetable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['produceNo']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        else:
                            return HttpResponse(repr('No xxx in "target" feature...'))
                    else:
                        return HttpResponse(repr('No xxx in "operation" feature...'))
                # TOO MUCH inquiry uuid
                else:
                    return HttpResponse("TOO MUCH this uuid! " + str(len(selectedExetable)) + request.POST.get("uuid"))
            else:
                selectedExetable = salesExetable.objects.filter(uuid = request.POST.get("uuid"))
                # When adding a new form
                if len(selectedExetable) < 1:
                    submitSalesExetable(request, 'add')
                    return HttpResponse("Add a new form!")
                # When update an existing form
                elif len(selectedExetable) == 1:
                    serializer=salesExetableSerializer(selectedExetable[0])
                    content = serializer.data
                    content['isLatest'] = 0
                    serializer.update(selectedExetable[0],content)
                    submitSalesExetable(request, 'update', content)
                    return HttpResponse("Update the form!")
                else:
                    return HttpResponse("Error, too much this uuid!")
     except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_list(request):
     try:
        if request.method == 'GET':
            selectedExetable = salesExetable.objects.filter(salesman = request.user.username)
            selectedExetable = selectedExetable.filter(isLatest = 1)
            data_to_render = []
            for i in range(0, len(selectedExetable)):
                serializer=salesExetableSerializer(selectedExetable[i])
                serializer_data = serializer.data
                iter_data = {'index': i+1,
                             'status': 1,
                             'customer': serializer_data["companyName"],
                             'salesman': serializer_data["salesman"],
                             'company': serializer_data["companyInfo"],
                             'nation': serializer_data["country"],
                             'category': serializer_data["productType"],
                             'status_content': 'status_content',
                             'uuid': serializer_data["uuid"],
                             }
                data_to_render.append(iter_data)
            return render_to_response('sales_list.html', {'data':data_to_render}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            pass
     except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_list(request):
    try:
        if request.method == 'GET':
            selectedStatisticstable = salesStatisticstable.objects.filter(isLatest = 1)
            data_to_render = []
            for i in range(0, len(selectedStatisticstable)):
                serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                serializer_data = serializer.data
                iter_data = {'index': i+1,
                             'date': serializer_data["date"],
                             'contractNo': serializer_data["contractNo"],
                             'customer': serializer_data["companyName"],
                             'productName': serializer_data["productType"],
                             'uuid': serializer_data["uuid"],
                             }
                data_to_render.append(iter_data)
            return render_to_response('sales_statistics_list.html', {'data':data_to_render}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_form(request, form_uuid=None):
    try:
        if request.method == 'GET':
            if not form_uuid:
                """
                add a new form
                """
                data_to_render = {}
                data_to_render['uuid'] = uuid.uuid1()
                data_to_render['contractNo'] = None
                data_to_render['productType'] = 1
                return render_to_response('sales_statistics_form.html', {'data': data_to_render}, context_instance=RequestContext(request))
            else:
                """
                query form from MYSQL
                """
                selectedStatisticstable = salesStatisticstable.objects.filter(uuid = form_uuid)
                if len(selectedStatisticstable) > 1:
                    return HttpResponse("uuid conflict!")
                elif len(selectedStatisticstable) < 1:
                    return HttpResponse("uuid not found!")
                serializer=salesStatisticstableSerializer(selectedStatisticstable[0])
                data_to_render = serializer.data
                #data_to_render['index'] = 1024
                return render_to_response('sales_statistics_form.html', {'data': data_to_render}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            if request.POST.has_key('operation'):
                data = json.loads(str(request.POST["operation"]))
                selectedStatisticstable = salesStatisticstable.objects.filter(uuid = data["uuid"])
                # When adding a new form
                if len(selectedStatisticstable) < 1:
                    return HttpResponse("Add a new statistics form: do nothing!")
                # When update an existing form
                elif len(selectedStatisticstable) == 1:
                    if "download" in data["operation"]:
                        if "contractNo" in data["target"]:
                            serializer=salesStatisticstableSerializer(selectedStatisticstable[0])
                            data_to_render = serializer.data
                            filename = data_to_render['contractNo']
                            if filename == None:
                                return HttpResponse("No such file could be download")
                            else:
                                response = HttpResponse(readFile(filename))
                                response['Content-Type'] = 'application/octet-stream'
                                response['Content-Disposition'] = 'attachment;filename=%s' %filename
                                return response # download request data
                        else:
                            return HttpResponse(repr('No xxx in "target" feature...'))
                    else:
                        return HttpResponse(repr('No xxx in "operation" feature...'))
                # TOO MUCH inquiry uuid
                else:
                    return HttpResponse("TOO MUCH this uuid! " + str(len(selectedStatisticstable)) + request.POST.get("uuid"))
            else:
                selectedStatisticstable = salesStatisticstable.objects.filter(uuid = request.POST.get("uuid"))
                # When adding a new form
                if len(selectedStatisticstable) < 1:
                    submitSalesStatisticstable(request, 'add')
                    return HttpResponse("Add a new Statistics form!")
                # When update an existing form
                elif len(selectedStatisticstable) == 1:
                    serializer=salesStatisticstableSerializer(selectedStatisticstable[0])
                    content = serializer.data
                    content['isLatest'] = 0
                    serializer.update(selectedStatisticstable[0],content)
                    submitSalesStatisticstable(request, 'update', content)
                    return HttpResponse("Update the form!")
                else:
                    return HttpResponse("Error, too much this uuid!")
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_nation(request, nation=None, person=None):
    try:
        if request.method == 'GET':
            if not nation:
               return HttpResponse('Invalid GET request')
               """
               should return all the nations
               """
            else:
                data_to_render = {'nation':nation,\
                'selectedYear':2014,
                'years':[2012, 2013, 2014, 2015],
                'items':[
                {'index' : '1', 'status' : 1, 'customer' : '光华世通', 'salesman':request.user.username, 'company':'c1', 'category':'d1', 'salesAmount':'3000', 'uuid':'uuid1'},
                {'index' : '2', 'status' : 2, 'customer' : '高通', 'salesman':request.user.username, 'company':'c2', 'category':'d2', 'salesAmount':'4000', 'uuid':'uuid2'},
                {'index' : '3', 'status' : 3, 'customer' : '苹果', 'salesman':request.user.username, 'company':'c3', 'category':'d3', 'salesAmount':'12000', 'uuid':'uuid3'},
                {'index' : '4', 'status' : 4, 'customer' : 'AMD', 'salesman':request.user.username, 'company':'c4', 'category':'d4', 'salesAmount':'134000', 'uuid':'uuid4'},],
                'salesCustomerList': json.dumps(['光华世通', '高通', '苹果', 'AMD']),
                'salesAmountByCustomer':[3000, 4000, 12000, 13400],
                'salesAmountByMonth':[3000, 4000, 12000, 6000, 7000, 9000, 12000, 6000, 9000, 10000, 1200, 24000]}
                #return HttpResponse(json.dumps({"YOU HAVE request" : data}))
                return render_to_response('sales_statistics_nation.html', {'data' : data_to_render}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            if request.POST.has_key('year'):
                return HttpResponse(json.dumps({"YOU HAVE SELECTED year" : request.POST['year']}))
            else:
                return HttpResponse('Invalid request')
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_statistics_customer(request, customer=None):
    try:
        if request.method == 'GET':
            if not customer:
               return HttpResponse('Invalid GET request')
               """
               should return all the nations
               """
            else:
                '''
                selectedStatisticstable = salesStatisticstable.objects.filter(companyName = customer)
                data_to_render = {'customer':customer}
                data_items = []
                data_years = []
                data_size = []
                data_orderAmoutBySize = {}
                sumorderPrice = 0
                for i in range(0, len(selectedStatisticstable)):
                    serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                    serializer_data = serializer.data
                    orderAmout = float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                    iter_data = {'index': i+1,
                                 'size': serializer_data["Size"],
                                 'orderAmout': serializer_data["orderAmount"],
                                 'priceUnit': serializer_data["priceUnit"],
                                 'orderPrice': orderAmout,
                                 }
                    data_items.append(iter_data)
                    sumorderPrice += float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                    data_years.append(serializer_data["date"][0:4])
                    data_size.append(serializer_data["Size"])
                    try:
                        data_orderAmoutBySize[serializer_data["Size"]+serializer_data["date"][0:4]] = data_orderAmoutBySize[serializer_data["Size"]] + orderAmout
                    except:
                        data_orderAmoutBySize[serializer_data["Size"]+serializer_data["date"][0:4]] = orderAmout
                data_items.append({'index':'总计', 'size': '', 'orderAmout':'', 'priceUnit':'', 'orderPrice' : str(sumorderPrice)})
                data_to_render["items"] = data_items
                data_to_render["years"] = sorted(list(set(data_years)),reverse=True)
                data_to_render["selectedYear"] = sorted(list(set(data_years)),reverse=True)[0]
                data_to_render["orderAmoutSizeList"] = json.dumps(list(set(data_size)))
                num_orderAmoutBySize=[]
                for i in range(0, len(list(set(data_size)))):
                    try:
                        num_orderAmoutBySize.append(data_orderAmoutBySize[list(set(data_size))[i]+data_to_render["selectedYear"]])
                    except:
                        num_orderAmoutBySize.append(0)
                data_to_render["orderAmoutBySize"] = num_orderAmoutBySize
                data_to_render["orderAmountByMonth"] = [3000, 4000, 12000, 6000, 7000, 9000, 12000, 6000, 9000, 10000, 1200, 24000]
                """
                 <td>{{ item.index }}</td>
				 <td>{{ item.customer }}</td>
				 <td>{{ item.orderAmount }}</td>
				 <td>{{ item.priceUnit }}</td>
				 <td>{{ item.orderPrice }}</td>
                data_to_render = {'customer':customer,\
                'items':[{'index':1, 'size': 'a*b*c', 'orderAmout':1000, 'priceUnit':200, 'orderPrice' : 1000*200},
                {'index':2, 'size': 'c*d*e', 'orderAmout':1000, 'priceUnit':200, 'orderPrice' : 1000*200},
                {'index':3, 'size': 'r*p*q', 'orderAmout':1000, 'priceUnit':200, 'orderPrice' : 1000*200},
                # last row implies subtotal
                {'index':'总计', 'size': '', 'orderAmout':'', 'priceUnit':'', 'orderPrice' : 1000*200 + 1000*200 + 1000*200}],
                'selectedYear':2014,
                'years':[2012, 2013, 2014, 2015],
                'orderAmoutSizeList': json.dumps(['a*b*c', 'c*d*e', 'r*p*q']),
                'orderAmoutBySize':[1000, 1000, 1000],
                'orderAmountByMonth':[3000, 4000, 12000, 6000, 7000, 9000, 12000, 6000, 9000, 10000, 1200, 24000]
               }
               """
               '''
                selectedStatisticstable = salesStatisticstable.objects.filter(companyName = customer)
                selectedStatisticstable = selectedStatisticstable.filter(date__year= "2016")
                data_to_render = {'customer':customer}
                data_items = []
                data_years = []
                data_size = []
                data_orderAmoutBySize = {}
                sumorderPrice = 0
                for i in range(0, len(selectedStatisticstable)):
                    serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                    serializer_data = serializer.data
                    orderAmout = float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                    iter_data = {'index': i+1,
                                 'size': serializer_data["Size"],
                                 'orderAmout': serializer_data["orderAmount"],
                                 'priceUnit': serializer_data["priceUnit"],
                                 'orderPrice': orderAmout,
                                 }
                    data_items.append(iter_data)
                    sumorderPrice += float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                    data_years.append(serializer_data["date"][0:4])
                    data_size.append(serializer_data["Size"])
                    try:
                        data_orderAmoutBySize[serializer_data["Size"]+serializer_data["date"][0:4]] = data_orderAmoutBySize[serializer_data["Size"]] + orderAmout
                    except:
                        data_orderAmoutBySize[serializer_data["Size"]+serializer_data["date"][0:4]] = orderAmout
                data_items.append({'index':'总计', 'size': '', 'orderAmout':'', 'priceUnit':'', 'orderPrice' : str(sumorderPrice)})
                data_to_render["items"] = data_items
                data_to_render["years"] = sorted(list(set(data_years)),reverse=True)
                data_to_render["selectedYear"] = sorted(list(set(data_years)),reverse=True)[0]
                data_to_render["orderAmoutSizeList"] = json.dumps(list(set(data_size)))
                num_orderAmoutBySize=[]
                for i in range(0, len(list(set(data_size)))):
                    try:
                        num_orderAmoutBySize.append(data_orderAmoutBySize[list(set(data_size))[i]+data_to_render["selectedYear"]])
                    except:
                        num_orderAmoutBySize.append(0)
                data_to_render["orderAmoutBySize"] = num_orderAmoutBySize
                data_to_render["orderAmountByMonth"] = [3000, 4000, 12000, 6000, 7000, 9000, 12000, 6000, 9000, 10000, 1200, 24000]
                return render_to_response('sales_statistics_customer.html', {'data' : data_to_render}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            if request.POST.has_key('year'):
                return HttpResponse(json.dumps({"YOU HAVE SELECTED year" : request.POST['year']}))
            else:
                return HttpResponse('Invalid request')
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

def submitSalesExetable(request, type, content=None):
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

        q.specification = request.FILES.get('specification') # FILES
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
        q.sampleNo = request.FILES.get('sampleNo') # FILES
        q.test = request.POST.get('test')
        q.smallOrder = request.FILES.get('smallOrder') # FILES

        q.dateQuote = request.POST.get('dateQuote')
        if q.dateQuote == '':
            q.dateQuote = None
        q.quoteApply = request.POST.get('quoteApply')
        q.quoteOrder = request.FILES.get('quoteOrder') #FILES

        q.dateOrder = request.POST.get('dateOrder')
        if q.dateOrder == '':
            q.dateOrder = None
        q.orderNo = request.FILES.get('orderNo') # FILES
        q.orderInfo = request.POST.get('orderInfo')

        q.dateContract = request.POST.get('dateContract')
        if q.dateContract == '':
            q.dateContract = None
        q.contractNo = request.FILES.get('contractNo') # FILES
        q.contractInfo = request.POST.get('contractInfo')

        q.contractReviewNoS = request.FILES.get('contractReviewNoS') # FILES
        q.salesNoS = request.FILES.get('salesNoS') # FILES

        q.contractReviewNoP = request.FILES.get('contractReviewNoP') # FILES
        q.salesNoP = request.FILES.get('salesNoP') # FILES

        q.produceNo = request.FILES.get('produceNo') # FILES
        q.produceStatus = request.POST.get('produceStatus')
        q.transNo = request.POST.get('transNo')

        q.comments = request.POST.get('comments')
        q.personCharge = request.POST.get('personCharge')
        q.personSupervise = request.POST.get('personSupervise')
        q.conclusion = request.POST.get('conclusion')


        q.isLatest = 1
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            q.specification = content['specification']
            q.sampleNo = content['sampleNo']
            q.smallOrder = content['smallOrder']
            q.quoteOrder = content['quoteOrder']
            q.orderNo = content['orderNo']
            q.contractNo = content['contractNo']
            q.contractReviewNoS = content['contractReviewNoS']
            q.salesNoS = content['salesNoS']
            q.contractReviewNoP = content['contractReviewNoP']
            q.salesNoP = content['salesNoP']
            q.produceNo = content['produceNo']
        else:
            return  HttpResponse("No such type!")
        q.save()
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def submitSalesStatisticstable(request, type, content=None):
    try:
        q = salesStatisticstable()
        #
        q.No = request.POST.get('No')
        q.date = request.POST.get('date')
        if q.date == '':
            q.date = None
        q.companyName = request.POST.get('companyName')
        q.contractNo = request.FILES.get('contractNo')
        q.productType = request.POST.get('productType')
        #
        q.Size = request.POST.get('Size')
        q.orderAmount = request.POST.get('orderAmount')
        q.confirmDate = request.POST.get('confirmDate')
        q.productDue = request.POST.get('productDue')
        q.remainStorage = request.POST.get('remainStorage')
        #
        q.priceUnit = request.POST.get('priceUnit')
        q.orderPrice = request.POST.get('orderPrice')
        q.paymentMethod = request.POST.get('paymentMethod')
        q.paymentDate = request.POST.get('paymentDate')
        if q.paymentDate == '':
            q.paymentDate = None
        #
        q.shippingAmount = request.POST.get('shippingAmount')
        q.shippingAmountActual = request.POST.get('shippingAmountActual')
        q.shippingAmountDue = request.POST.get('shippingAmountDue')
        #
        q.taxStatus = request.POST.get('taxStatus')
        q.deliveryStatus = request.POST.get('deliveryStatus')
        #
        q.comments = request.POST.get('comments')

        q.isLatest = 1
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            q.contractNo = content['contractNo']
        else:
            return  HttpResponse("No such type!")
        q.save()
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")