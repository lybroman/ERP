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
from main.models import salesExetable, salesStatisticstable, sample_form_model, user_model_extend, customer_model, currency_model, amount_model, setting_size_model, storage_delivery_model
from main.serializers import salesExetableSerializer, salesStatisticstableSerializer, sample_form_model_serializer, user_model_extend_serializer, customer_model_serializer
from django.contrib.auth import authenticate, login, logout
from main.storage_delivery_serializers import storageDeliverySerializers

from  main.models import message_model
from main.serializers import message_model_serializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import socket
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
import logging
from urllib import unquote

STATUS_OK = HttpResponse(json.dumps({"status" : "okay"}))
logger = logging.getLogger(__name__)
NOSP_num = 50

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
import threading
from models import produce_statistics_pendai_model, produce_statistics_gunjian_model, produce_statistics_tiexin_model
from produce_serializers import produce_statistics_pendai_model_serializer, produce_statistics_gunjian_model_serializer, produce_statistics_tiexin_model_serializer

def send_email(title, msg):
    mail_host="smtp.londerful.com"
    mail_user="021@londerful.com"
    mail_pass="qweasdzxc1234"

    sender = '021@londerful.com'
    receivers = ['021@londerful.com','005@londerful.com']

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("ERP System", 'utf-8')
    message['To'] =  Header("YOUR ACTION REQUIRED", 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        #print "sent!"
    except smtplib.SMTPException:
        print traceback.format_exc()


def send_email_th(title, msg):
    th = threading.Thread(target=send_email, args=(title, msg))
    th.start()


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
                         if request.user.is_superuser:
                            return HttpResponseRedirect('/ERP/superuser/{}'.format(request.user.username))

                         if request.user.has_perm('main.is_sales_manager'):
                            return HttpResponseRedirect('/ERP/sales_manager/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_special_user'):
                             return HttpResponseRedirect('/ERP/special_user_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_quality'):
                             return HttpResponseRedirect('/ERP/quality_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_a_salesman'):
                            return HttpResponseRedirect('/ERP/sales_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_producer') and not request.user.has_perm('main.is_a_salesman'):
                            return HttpResponseRedirect('/ERP/produce_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_storage'):
                            return HttpResponseRedirect('/ERP/storage_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_buyer'):
                            return HttpResponseRedirect('/ERP/purchase_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_ranker'):
                            return HttpResponseRedirect('/ERP/hr_main/{}'.format(request.user.username))
                         if request.user.has_perm('main.is_approver'):
                            return HttpResponseRedirect('/ERP/message/')
                         #elif request.user.has_perm('main.is_approver'):
                         #   return HttpResponse("He is a approver! (No main page now)")
                         #elif request.user.has_perm('main.is_buyer'):
                         #   return HttpResponse("He is a buyer! (No main page now)")
                         else:
                            return HttpResponse('A person with no permissions now!!')
                     else:
                        return HttpResponse('Not active')
                else:
                      return HttpResponse('Not a valid user')
            elif request.POST.has_key('register'):
                return STATUS_OK
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def log_out(request):
    try:
        logout(request)
        return render_to_response('login.html', context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_main(request, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                data_to_render = {'target_user' : target_user}
                return render_to_response('sales_main.html', {'data': data_to_render} , context_instance=RequestContext(request))
                #return render_to_response('sales_main.html', context_instance=RequestContext(request))
            elif request.method == 'POST':
                pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_form(request, form_uuid=None, target_user=None):
     productDictionary = {u"带材":1, u"铁芯":2, u"器件":3}

     try:
         if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
         else:
            if not request.user.has_perm('main.is_a_salesman') and not request.user.has_perm('main.is_sales_manager') and not request.user.has_perm('main.is_approver'):
                return HttpResponse("ACCESS level 0 DENIED!")

            if (request.user.has_perm('main.is_a_salesman') and not request.user.has_perm('main.is_sales_manager')) and not request.user.has_perm('main.is_approver'):
                if request.user.username != target_user:
                    return HttpResponse("ACCESS level 1DENIED!")

            if request.user.has_perm('main.is_sales_manager'):
                pass

            if request.user.has_perm('main.is_approver'):
                pass

            if request.method == 'GET':
                if form_uuid == 'new_form':
                    """
                    add a new form
                    """
                    data_to_render = {}
                    data_to_render['uuid'] = uuid.uuid1()
                    time.sleep(0.01)
                    data_to_render['message_id'] = uuid.uuid1()
                    data_to_render['salesman'] = request.user.username
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
                    data_to_render['approver_list'] = ['N/A']
                    user_sql = User.objects.all()
                    for user in user_sql:
                        if user.has_perm('main.is_approver'):
                            data_to_render['approver_list'].append(user.last_name + user.first_name)

                    """
                    query currency and amount from
                    """
                    currency_sql = currency_model.objects.all()
                    currency_unit_list = [i.currency_name for i in currency_sql]
                    amount_sql = amount_model.objects.all()
                    amount_unit_list = [i.amount_name for i in amount_sql]

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]

                    return render_to_response('sales_form.html', {'data': data_to_render, 'current_user':request.user.username,'target_user':target_user, 'amount_unit_list' : amount_unit_list, 'currency_unit_list' : currency_unit_list, 'companyName_list' : companyName_list}, context_instance=RequestContext(request))
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                    selectedExetable = salesExetable.objects.filter(uuid = form_uuid)
                    if len(selectedExetable) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selectedExetable) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=salesExetableSerializer(selectedExetable[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selectedExetable[0],content)
                    return HttpResponseRedirect('/ERP/sales_list/{}'.format(target_user))
                else:
                    """
                    query form from MYSQL
                    """
                    selectedExetable = salesExetable.objects.filter(uuid = form_uuid)
                    if len(selectedExetable) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selectedExetable) < 1:
                        return HttpResponse("uuid not found!!!!!")
                    serializer=salesExetableSerializer(selectedExetable[0])
                    data_to_render = serializer.data
                    data_to_render['productType'] = productDictionary[data_to_render['productType']]

                    sample_form_sql = sample_form_model.objects.filter(message_id = data_to_render['sample_form_uuid'])
                    if len(sample_form_sql) == 0:
                        data_to_render['sample_form_uuid'] = None
                        data_to_render['sample_form_index'] = None
                    else:
                        sample_form_sql_serializer = sample_form_model_serializer(sample_form_sql[0])
                        sample_form_content = sample_form_sql_serializer.data
                        data_to_render['sample_form_uuid'] = sample_form_content['message_id']
                        data_to_render['sample_form_index'] = sample_form_content['index']


                    for key in ['specification', 'sampleNo', 'smallOrder', 'quoteOrder', 'orderNo',
                                'contractNo', 'contractReviewNoS',
                                'salesNoS', 'contractReviewNoP', 'salesNoP', 'produceNo']:
                        if data_to_render[key] != None:
                            data_to_render[key] = unquote(data_to_render[key])
                            data_to_render['full_' + key] = data_to_render[key]
                            data_to_render[key] = data_to_render[key][23:len(data_to_render[key])]

                    data_to_render['approver_list'] = ['N/A']
                    user_sql = User.objects.all()
                    for user in user_sql:
                        if user.has_perm('main.is_approver'):
                            data_to_render['approver_list'].append(user.last_name + user.first_name)

                    """
                    query currency and amount from
                    """
                    currency_sql = currency_model.objects.all()
                    currency_unit_list = [i.currency_name for i in currency_sql]
                    amount_sql = amount_model.objects.all()
                    amount_unit_list = [i.amount_name for i in amount_sql]

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]

                    return render_to_response('sales_form.html', {'data': data_to_render, 'current_user':request.user.username, 'target_user':target_user, 'amount_unit_list' : amount_unit_list, 'currency_unit_list' : currency_unit_list, 'companyName_list' : companyName_list}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                # If click download button
                if request.POST.has_key('operation'):
                    data = json.loads(str(request.POST["operation"]))
                    selectedExetable = salesExetable.objects.filter(uuid = data["uuid"])
                    # When adding a new form
                    if len(selectedExetable) < 1:
                        pass
                    # When update an existing form
                    elif len(selectedExetable) == 1:
                        if "download" in data["operation"]:
                            flag = False
                            for key in ['specification', 'sampleNo', 'smallOrder', 'quoteOrder', 'orderNo',
                                    'contractNo', 'contractReviewNoS',
                                    'salesNoS', 'contractReviewNoP', 'salesNoP', 'produceNo']:
                                if key in data["target"]:
                                    flag = True
                                    serializer=salesExetableSerializer(selectedExetable[0])
                                    data_to_render = serializer.data
                                    filename = data_to_render[key]
                                    if filename == None:
                                        return HttpResponse("No such file could be download")
                                    else:
                                        filename1 = 'C:'+ unquote(filename).decode('utf-8')
                                        response = HttpResponse(readFile(filename1))
                                        response['Content-Type'] = 'application/octet-stream'
                                        response['Content-Disposition'] = 'attachment;filename=%s' % filename[23:len(filename)]
                                        return response # download request data
                            if flag == False:
                                return HttpResponse(repr('No required feature in "target" feature...'))

                        else:
                            return HttpResponse(repr('No xxx in "operation" feature...'))
                    # TOO MUCH inquiry uuid
                    else:
                        return HttpResponse("TOO MUCH this uuid! " + str(len(selectedExetable)) + request.POST.get("uuid"))
                else:
                    selectedExetable = salesExetable.objects.filter(uuid = request.POST.get("uuid"))
                    # When adding a new form
                    if len(selectedExetable) < 1:
                        isvalid = submitSalesExetable(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sales_list/{}/'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selectedExetable) == 1:
                        serializer=salesExetableSerializer(selectedExetable[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        for key in ['specification', 'sampleNo', 'smallOrder', 'quoteOrder', 'orderNo',
                                    'contractNo', 'contractReviewNoS',
                                    'salesNoS', 'contractReviewNoP', 'salesNoP', 'produceNo']:
                            if content[key] != None:
                                content[key] = unquote(content[key])
                        serializer.update(selectedExetable[0],content)

                        isvalid = submitSalesExetable(request, 'update', content)

                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sales_list/{}/'.format(target_user))
                        else:
                            content['isLatest'] = 1
                            serializer.update(selectedExetable[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
     except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_list(request, target_user=None):
     try:
         if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
         else:
            if request.method == 'GET':
                selectedExetable = salesExetable.objects.all()

                if request.user.has_perm('main.is_sales_manager'):
                    if request.user.username == target_user:
                        selectedExetable = salesExetable.objects.all()
                    else:
                        selectedExetable = salesExetable.objects.filter(salesman = target_user)
                else:
                    selectedExetable = salesExetable.objects.filter(salesman = target_user)

                selectedExetable = selectedExetable.filter(isLatest = 1)
                selectedExetable = selectedExetable.filter(b_display=1)
                selectedExetable = selectedExetable.order_by("-date")

                data_to_render = []

                for i in range(0, len(selectedExetable)):
                    serializer=salesExetableSerializer(selectedExetable[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i + 1,
                                 'index': serializer_data["No"],
                                 #'status': 1,
                                 'customer': serializer_data["companyName"],
                                 'salesman': serializer_data["salesman"],
                                 'company': serializer_data["companyInfo"],
                                 'nation': serializer_data["country"],
                                 'category': serializer_data["productType"],
                                 #'status_content': 'status_content',
                                 'uuid': serializer_data["uuid"],
                                 }
                    '''
                    decide status
                    '''
                    if (serializer_data["dateContract"] != None or serializer_data["contractInfo"] != "" or serializer_data["contractNo"] != None):
                        iter_data['status'] = 4
                        iter_data['status_content'] = "合同"
                    elif (serializer_data["dateOrder"] != None or serializer_data["orderInfo"] != "" or serializer_data["orderNo"] != None):
                        iter_data['status'] = 3
                        iter_data['status_content'] = "订单"
                    elif (serializer_data["contractReviewNoS"] != None or serializer_data["salesNoS"] != None):
                        iter_data['status'] = 2
                        iter_data['status_content'] = "样品"
                    else:
                        iter_data['status'] = 1
                        iter_data['status_content'] = "报价"
                    data_to_render.append(iter_data)
                return render_to_response('sales_list.html', {'data':data_to_render, 'target_user':target_user, 'current_user':request.user.username}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                pass
     except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_list(request, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                selectedStatisticstable = salesStatisticstable.objects.filter(isLatest = 1, b_display='1')
                if request.user.has_perm('main.is_sales_manager') or request.user.has_perm('main.is_special_user'):
                    if request.user.username == target_user:
                        pass;
                    else:
                        selectedStatisticstable = selectedStatisticstable.filter(salesman = target_user)
                else:
                    selectedStatisticstable = selectedStatisticstable.filter(salesman = target_user)

                selectedStatisticstable = selectedStatisticstable.order_by("-date")
                data_to_render = []
                #return HttpResponse(len(selectedStatisticstable))
                for i in range(0, len(selectedStatisticstable)):
                    serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                    serializer_data = serializer.data
                    if serializer_data["contractNo"] == None:
                        contractNo = "None"
                    else:
                        contractNo = serializer_data["contractNo"]
                        contractNo = unquote(contractNo)
                        contractNo = contractNo[23:len(contractNo)]
                    iter_data = {'no': i+1,
                                 'index': serializer_data["No"],
                                 'date': serializer_data["date"],
                                 'contractNo': contractNo,
                                 'customer': serializer_data["companyName"],
                                 'productName': serializer_data["productType"],
                                 'uuid': serializer_data["uuid"],
                                 'nation':serializer_data["country"],
                                 'salesman':serializer_data["salesman"],
                                 'currency_unit' : serializer_data["currency_unit"],
                                 'amount_unit' : serializer_data["amount_unit"],
                                 'orderAmount' : serializer_data["orderAmount"],
                                 'orderPrice' : serializer_data["orderPrice"],
                                 'last_revise_date' : serializer_data["last_revise_date"],
                                 }
                    data_to_render.append(iter_data)
                    """
                    sync the customer info
                    """
                    try:
                        customer_sql = customer_model.objects.filter(customer_name=serializer_data["companyName"])
                        if len(customer_sql) > 0:
                            pass
                        else:
                            data_to_save = {}
                            data_to_save["customer_name"] = serializer_data["companyName"]
                            data_to_save["customer_rank"] = 'N/A'
                            data_to_save["customer_address"] = 'N/A'
                            data_to_save["customer_contact"] = 'N/A'
                            data_to_save["customer_mobile"] = 'N/A'
                            data_to_save["customer_comment"] = 'N/A'
                            data_to_save["customer_email"] = 'N/A'

                            customer_model_serializer_ser = customer_model_serializer(data=data_to_save)
                            if customer_model_serializer_ser.is_valid():
                                customer_model_serializer_ser.create(data_to_save)
                    except:
                        return HttpResponse(traceback.format_exc())

                return render_to_response('sales_statistics_list.html', {'data':data_to_render, 'current_user':request.user.username, 'target_user':target_user}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_form(request, form_uuid=None, target_user=None):
    productDictionary = {u"带材":1, u"铁芯":2, u"器件":3}
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                if form_uuid == 'new_form':
                    """
                    add a new form
                    """
                    data_to_render = {}
                    year = str(int(datetime.datetime.now().year) % 100)
                    count = len(salesStatisticstable.objects.filter(date__year = str(datetime.datetime.now().year))) + 1
                    index = 'LF{}XX{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                    data_to_render['No'] = index
                    data_to_render['uuid'] = uuid.uuid1()
                    data_to_render['contractNo'] = None
                    data_to_render['productType'] = 1
                    data_to_render['currency_rate'] = 1.0
                    data_to_render['salesman'] = request.user.username

                    """
                    query currency and amount from
                    """
                    currency_sql = currency_model.objects.all()
                    currency_unit_list = [i.currency_name for i in currency_sql]
                    amount_sql = amount_model.objects.all()
                    amount_unit_list = [i.amount_name for i in amount_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]
                    if request.user.has_perm('main.is_a_salesman'):
                        is_salesman = True
                    else:
                        is_salesman = False
                    return render_to_response('sales_statistics_form.html', {'data': data_to_render,  'current_user':request.user.username, 'target_user':target_user, 'currency_unit_list' : currency_unit_list, 'amount_unit_list' : amount_unit_list, 'companyName_list' : companyName_list, 'setting_size_unit_list':setting_size_unit_list, 'is_salesman':is_salesman}, context_instance=RequestContext(request))
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':

                    selectedStatisticstable = salesStatisticstable.objects.filter(uuid = form_uuid)
                    if len(selectedStatisticstable) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selectedStatisticstable) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=salesStatisticstableSerializer(selectedStatisticstable[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selectedStatisticstable[0],content)
                    return HttpResponseRedirect('/ERP/sales_statistics_list/{}'.format(target_user))
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
                    data_to_render['productType'] = productDictionary[data_to_render['productType']]
                    #data_to_render['contractNo'] = u'{}'.format(data_to_render['contractNo'])
                    if data_to_render['contractNo'] == None:
                        pass
                    else:
                        data_to_render['contractNo'] = unquote(data_to_render['contractNo'])
                        data_to_render['contractNo'] = data_to_render['contractNo'][23:len(data_to_render['contractNo'])]

                    """
                    query currency and amount from
                    """
                    currency_sql = currency_model.objects.all()
                    currency_unit_list = [i.currency_name for i in currency_sql]
                    amount_sql = amount_model.objects.all()
                    amount_unit_list = [i.amount_name for i in amount_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = ['未找到']
                    setting_size_unit_list += [i.size_name for i in setting_size_sql]

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]

                    """
                    update delivery data from storage delivery model
                    """

                    delivery_sql = storage_delivery_model.objects.filter(sales_No=data_to_render["No"], b_display='1')
                    if len(delivery_sql) < 0:
                        pass
                    else:
                        data_to_render['shippingAmount'] = ''
                        data_to_render['shippingAmountActual'] = ''
                        data_to_render['shippingAmountDue'] = ''
                        data_to_render['shippingAmountDate'] = ''
                        for i_d in range(0, len(delivery_sql)):
                             serializer=storageDeliverySerializers(delivery_sql[i_d])
                             data = serializer.data
                             data_to_render['shippingAmount'] += u'第{}单:{}\r\n'.format(data['delivery_No'], data['delivery_status'])
                             data_to_render['shippingAmountActual'] += u'第{}单物流单号:{}\r\n'.format(data['delivery_No'],  data['delivery_track_No'])
                             data_to_render['shippingAmountDue'] += u'第{}单物流量:{}\r\n'.format(data['delivery_No'],  data['delivery_amount'])
                             data_to_render['shippingAmountDate'] += u'第{}单物流发货日期:{}\r\n'.format(data['delivery_No'],  data['update_date'])

                    if request.user.has_perm('main.is_a_salesman'):
                        is_salesman = True
                    else:
                        is_salesman = False

                    return render_to_response('sales_statistics_form.html', {'data': data_to_render,  'current_user':request.user.username, 'target_user':target_user, 'currency_unit_list' : currency_unit_list, 'amount_unit_list' : amount_unit_list, 'setting_size_unit_list':setting_size_unit_list, 'companyName_list' : companyName_list, 'is_salesman':is_salesman}, context_instance=RequestContext(request))

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
                                    filename1 = unquote(filename).decode('utf-8')
                                    filename1 = 'C:'+ filename1
                                    response = HttpResponse(readFile(filename1))
                                    response['Content-Type'] = 'application/octet-stream'
                                    response['Content-Disposition'] = 'attachment;filename=%s' % filename[23:len(filename)]
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
                        isvalid = submitSalesStatisticstable(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sales_statistics_list/{}'.format(target_user))
                            #return HttpResponse("Add a new Statistics form!")
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selectedStatisticstable) == 1:
                        serializer=salesStatisticstableSerializer(selectedStatisticstable[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        if content['contractNo'] != None:
                            content['contractNo'] = unquote(content['contractNo'])
                        serializer.update(selectedStatisticstable[0],content)
                        isvalid = submitSalesStatisticstable(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sales_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_statistics_nation(request, nation=None, person=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                if not nation:
                   return HttpResponse('Invalid GET request')
                   """
                   should return all the nations
                   """
                else:
                    selectedExetable = salesStatisticstable.objects.filter(country = nation)
                    selectedExetable = selectedExetable.filter(isLatest = 1)
                    selectedExetable = selectedExetable.filter(b_display = 1)
                    if person == None:
                        person = request.user.username
                    if request.user.has_perm('main.is_sales_manager') or request.user.has_perm('main.is_special_user'):
                        if request.user.username == person:
                            pass;
                        else:
                            selectedExetable = selectedExetable.filter(salesman = person)
                    else:
                        selectedExetable = selectedExetable.filter(salesman = person)
                    if len(selectedExetable) < 1:
                        return HttpResponse("No such nation & salesman!")
                    else:
                        data_to_render = {'nation':nation}
                        data_to_render["person"] = person
                        startDate = str(datetime.date(datetime.date.today().year-1, datetime.date.today().month, datetime.date.today().day))
                        endDate = str(datetime.date.today())
                        data_to_render["startDate"] = startDate
                        data_to_render["endDate"] = endDate
                        selectedExetable = selectedExetable.filter(date__range=(startDate,endDate))
                        selectedExetable.order_by('-date')
                        data_customer = []
                        data_items = []
                        data_salesAmoutByCustomer = {}
                        for i in range(0, len(selectedExetable)):
                            serializer=salesStatisticstableSerializer(selectedExetable[i])
                            serializer_data = serializer.data
                            try:
                                float(serializer_data["orderPrice"])
                                iter_data ={'index':i+1,
                                        'status':1,
                                        'customer':serializer_data["companyName"],
                                        'date':serializer_data["date"],
                                        'salesman':serializer_data["salesman"],
                                        #'company':serializer_data["companyInfo"],
                                        'category':serializer_data["productType"],
                                        'salesAmount':serializer_data["orderPrice"],
                                        'uuid':serializer_data["uuid"]
                                        }
                            except:
                                iter_data ={'index':i+1,
                                        'status':1,
                                        'customer':serializer_data["companyName"],
                                        'date':serializer_data["date"],
                                        'salesman':person,
                                        #'company':serializer_data["companyInfo"],
                                        'category':serializer_data["productType"],
                                        'salesAmount':"未知数据",
                                        'uuid':serializer_data["uuid"]
                                        }
                                serializer_data["orderPrice"] = 0

                            data_items.append(iter_data)
                            data_customer.append(serializer_data["companyName"])

                            try:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = data_salesAmoutByCustomer[serializer_data["companyName"]] + float(serializer_data["orderPrice"])
                            except:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = float(serializer_data["orderPrice"])
                        data_to_render["items"] = data_items
                        data_to_render["salesCustomerList"] = json.dumps(list(set(data_customer)))
                        num_salesAmountByCustomer=[]
                        for i in range(0, len(list(set(data_customer)))):
                            try:
                                num_salesAmountByCustomer.append(data_salesAmoutByCustomer[list(set(data_customer))[i]])
                            except:
                                num_salesAmountByCustomer.append(0)
                        data_to_render["salesAmountByCustomer"] = num_salesAmountByCustomer

                        monthList = []
                        salesAmountByMonth = []
                        startYear = startDate[0:4]
                        startMonth = startDate[5:7]
                        startYM = int(startYear) * 12 + int(startMonth)
                        endYear = endDate[0:4]
                        endMonth = endDate[5:7]
                        endYM = int(endYear) * 12 + int(endMonth)
                        monthDic = {1:"01", 2:"02", 3:"03", 4:"04", 5:"05", 6:"06", 7:"07", 8:"08", 9:"09", 10:"10", 11:"11", 12:"12"}
                        for ym in range(startYM,endYM+1):
                            chooseYear = int((ym - 1) / 12)
                            chooseMonth = ym % 12
                            if (chooseMonth == 0):
                                chooseMonth = 12
                            monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                            selectedYear = selectedExetable.filter(date__year = chooseYear)
                            selectedMonth = selectedYear.filter(date__month = chooseMonth)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderAmout = float(serializer_data["orderPrice"])
                                    except:
                                        orderAmout = 0
                                    data_per_month = data_per_month + orderAmout
                                salesAmountByMonth.append(data_per_month)
                        data_to_render['salesAmountByMonth']=salesAmountByMonth
                        data_to_render['monthList']=json.dumps(monthList)
                        return render_to_response('sales_statistics_nation.html', {'data' : data_to_render,  'current_user':request.user.username, 'target_user':person}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                if request.POST.has_key('startDate') and request.POST.has_key('endDate'):
                    selectedExetable = salesStatisticstable.objects.filter(country = nation)
                    selectedExetable = selectedExetable.filter(isLatest = 1)
                    selectedExetable = selectedExetable.filter(b_display = 1)
                    if person == None:
                        person = request.user.username
                    if request.user.has_perm('main.is_sales_manager'):
                        if request.user.username == person:
                            pass;
                        else:
                            selectedExetable = selectedExetable.filter(salesman = person)
                    else:
                        selectedExetable = selectedExetable.filter(salesman = person)
                    if len(selectedExetable) < 1:
                        return HttpResponse("No such nation & salesman!")
                    else:
                        data_to_render = {'nation':nation}
                        data_to_render["person"] = person
                        startDate = request.POST["startDate"]
                        endDate = request.POST["endDate"]
                        data_to_render["startDate"] = startDate
                        data_to_render["endDate"] = endDate
                        selectedExetable = selectedExetable.filter(date__range=(startDate,endDate))
                        data_customer = []
                        data_items = []
                        data_salesAmoutByCustomer = {}
                        for i in range(0, len(selectedExetable)):
                            serializer=salesStatisticstableSerializer(selectedExetable[i])
                            serializer_data = serializer.data
                            try:
                                float(serializer_data["orderPrice"])
                                iter_data ={'index':i+1,
                                        'status':1,
                                        'customer':serializer_data["companyName"],
                                        'salesman':serializer_data["salesman"],
                                        #'company':serializer_data["companyInfo"],
                                        'category':serializer_data["productType"],
                                        'salesAmount':serializer_data["orderPrice"],
                                        'uuid':serializer_data["uuid"]
                                        }
                            except:
                                iter_data ={'index':i+1,
                                        'status':1,
                                        'customer':serializer_data["companyName"],
                                        'salesman':serializer_data["salesman"],
                                        #'company':serializer_data["companyInfo"],
                                        'category':serializer_data["productType"],
                                        'salesAmount':"未知数据",
                                        'uuid':serializer_data["uuid"]
                                        }
                                serializer_data["orderPrice"] = 0

                            data_items.append(iter_data)
                            data_customer.append(serializer_data["companyName"])

                            try:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = data_salesAmoutByCustomer[serializer_data["companyName"]] + float(serializer_data["orderPrice"])
                            except:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = float(serializer_data["orderPrice"])
                        data_to_render["items"] = data_items
                        data_to_render["salesCustomerList"] = json.dumps(list(set(data_customer)))
                        num_salesAmountByCustomer=[]
                        for i in range(0, len(list(set(data_customer)))):
                            try:
                                num_salesAmountByCustomer.append(data_salesAmoutByCustomer[list(set(data_customer))[i]])
                            except:
                                num_salesAmountByCustomer.append(0)
                        data_to_render["salesAmountByCustomer"] = num_salesAmountByCustomer

                        monthList = []
                        salesAmountByMonth = []
                        startYear = startDate[0:4]
                        startMonth = startDate[5:7]
                        startYM = int(startYear) * 12 + int(startMonth)
                        endYear = endDate[0:4]
                        endMonth = endDate[5:7]
                        endYM = int(endYear) * 12 + int(endMonth)
                        monthDic = {1:"01", 2:"02", 3:"03", 4:"04", 5:"05", 6:"06", 7:"07", 8:"08", 9:"09", 10:"10", 11:"11", 12:"12"}
                        for ym in range(startYM,endYM+1):
                            chooseYear = int((ym - 1) / 12)
                            chooseMonth = ym % 12
                            if (chooseMonth == 0):
                                chooseMonth = 12
                            monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                            selectedYear = selectedExetable.filter(date__year = chooseYear)
                            selectedMonth = selectedYear.filter(date__month = chooseMonth)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderAmout = float(serializer_data["orderPrice"])
                                    except:
                                        orderAmout = 0
                                    data_per_month = data_per_month + orderAmout
                                salesAmountByMonth.append(data_per_month)
                        data_to_render['salesAmountByMonth']=salesAmountByMonth
                        data_to_render['monthList']=json.dumps(monthList)
                        return render_to_response('sales_statistics_nation.html', {'data' : data_to_render,  'current_user':request.user.username}, context_instance=RequestContext(request))
                else:
                    return HttpResponse('Invalid request! No start or end date!')
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_statistics_customer(request, customer=None, target_size=None, person=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                if not customer:
                   return HttpResponse('Invalid GET request')
                   """
                   should return all the customers
                   """
                else:
                    selectedStatisticstable = salesStatisticstable.objects.filter(companyName = customer)
                    selectedStatisticstable = selectedStatisticstable.filter(isLatest = 1)
                    selectedStatisticstable = selectedStatisticstable.filter(b_display = 1)
                    if target_size != None:
                        selectedStatisticstable = selectedStatisticstable.filter(Size = target_size)
                    if person == None:
                        person = request.user.username
                    if request.user.has_perm('main.is_sales_manager') or request.user.has_perm('main.is_special_user'):
                        if request.user.username == person:
                            pass;
                        else:
                            selectedStatisticstable = selectedStatisticstable.filter(salesman = person)
                    else:
                        selectedStatisticstable = selectedStatisticstable.filter(salesman = person)
                    selectedStatisticstable.order_by('-date')
                    if len(selectedStatisticstable) < 1:
                        return HttpResponse("No such customer:" + customer + ', person:' + person)
                    else:
                        data_to_render = {'customer':customer}
                        data_items = []
                        data_years = []
                        sumorderPrice = 0

                        for i in range(0, len(selectedStatisticstable)):
                            serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                            serializer_data = serializer.data
                            try:
                                orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                            except:
                                orderPrice = float(serializer_data["orderPrice"])*1
                            iter_data = {'index': i+1,
                                         'size': serializer_data["Size"],
                                         'date': serializer_data["date"],
                                         'orderAmount': serializer_data["orderAmount"],
                                         'priceUnit': serializer_data["priceUnit"],
                                         'orderPrice': orderPrice,
                                         }
                            data_items.append(iter_data)
                            sumorderPrice += float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                            data_years.append(serializer_data["date"][0:4])
                        data_items.append({'index':'总计', 'size': '总计', 'orderAmount':'', 'priceUnit':'', 'orderPrice' : str(sumorderPrice)})
                        data_to_render["items"] = data_items
                        data_to_render["years"] = sorted(list(set(data_years)),reverse=True)
                        data_to_render["selectedYear"] = sorted(list(set(data_years)),reverse=True)[0]

                        selectedStatisticstable=selectedStatisticstable.filter(date__year = int(data_to_render["selectedYear"]))
                        data_size = []
                        data_orderAmoutBySize = {}
                        for i in range(0, len(selectedStatisticstable)):
                            serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                            serializer_data = serializer.data
                            try:
                                orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                            except:
                                orderPrice = float(serializer_data["orderPrice"])*1
                            data_size.append(serializer_data["Size"])
                            try:
                                data_orderAmoutBySize[serializer_data["Size"]] = data_orderAmoutBySize[serializer_data["Size"]] + orderPrice
                            except:
                                data_orderAmoutBySize[serializer_data["Size"]] = orderPrice
                        data_to_render["orderAmoutSizeList"] = json.dumps(list(set(data_size)))

                        num_orderAmoutBySize=[]
                        for i in range(0, len(list(set(data_size)))):
                            try:
                                num_orderAmoutBySize.append(data_orderAmoutBySize[list(set(data_size))[i]])
                            except:
                                num_orderAmoutBySize.append(0)
                        data_to_render["orderAmoutBySize"] = num_orderAmoutBySize
                        #return HttpResponse(data_to_render["orderAmoutBySize"])

                        # month data
                        data_month=[]
                        for m in range(0, 12):
                            selectedMonth=selectedStatisticstable.filter(date__month = m+1)
                            if len(selectedMonth) < 1:
                                data_month.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                                    except:
                                        orderPrice = float(serializer_data["orderPrice"])*1
                                    data_per_month = data_per_month + orderPrice
                                data_month.append(data_per_month)
                        data_to_render["orderAmountByMonth"] = data_month
                        '''
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
                        '''
                        return render_to_response('sales_statistics_customer.html', {'data' : data_to_render,  'current_user':request.user.username, 'target_user':person, 'target_size':target_size}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if request.POST.has_key('yearSelectedOrder'):
                    selectedStatisticstable = salesStatisticstable.objects.filter(companyName = customer)
                    #return HttpResponse(target_size)
                    if target_size != None and target_size != 'None':
                        selectedStatisticstable = selectedStatisticstable.filter(Size = target_size)
                    selectedStatisticstable = selectedStatisticstable.filter(isLatest = 1)
                    selectedStatisticstable = selectedStatisticstable.filter(b_display = 1)
                    if person == None:
                        person = request.user.username
                    if request.user.has_perm('main.is_sales_manager'):
                        if request.user.username == person:
                            pass;
                        else:
                            selectedStatisticstable = selectedStatisticstable.filter(salesman = person)
                    else:
                        selectedStatisticstable = selectedStatisticstable.filter(salesman = person)
                    if len(selectedStatisticstable) < 1:

                        return HttpResponse("No such customer!")
                    else:
                        data_to_render = {'customer':customer}
                        data_items = []
                        data_years = []
                        sumorderPrice = 0
                        for i in range(0, len(selectedStatisticstable)):
                            serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                            serializer_data = serializer.data
                            try:
                                orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                            except:
                                orderPrice = float(serializer_data["orderPrice"])*1
                            iter_data = {'index': i+1,
                                         'size': serializer_data["Size"],
                                         'orderAmount': serializer_data["orderAmount"],
                                         'priceUnit': serializer_data["priceUnit"],
                                         'orderPrice': orderPrice,
                                         }
                            data_items.append(iter_data)
                            sumorderPrice += float(serializer_data["orderAmount"])*float(serializer_data["priceUnit"])
                            data_years.append(serializer_data["date"][0:4])
                        data_items.append({'index':'总计', 'size': '', 'orderAmout':'', 'priceUnit':'', 'orderPrice' : str(sumorderPrice)})
                        data_to_render["items"] = data_items
                        data_to_render["years"] = sorted(list(set(data_years)),reverse=True)
                        data_to_render["selectedYear"] = request.POST['yearSelectedOrder']

                        selectedStatisticstable=selectedStatisticstable.filter(date__year = int(data_to_render["selectedYear"]))
                        data_size = []
                        data_orderAmoutBySize = {}
                        for i in range(0, len(selectedStatisticstable)):
                            serializer=salesStatisticstableSerializer(selectedStatisticstable[i])
                            serializer_data = serializer.data
                            try:
                                orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                            except:
                                orderPrice = float(serializer_data["orderPrice"])*1
                            data_size.append(serializer_data["Size"])
                            try:
                                data_orderAmoutBySize[serializer_data["Size"]] = data_orderAmoutBySize[serializer_data["Size"]] + orderPrice
                            except:
                                data_orderAmoutBySize[serializer_data["Size"]] = orderPrice
                        data_to_render["orderAmoutSizeList"] = json.dumps(list(set(data_size)))
                        num_orderAmoutBySize=[]
                        for i in range(0, len(list(set(data_size)))):
                            try:
                                num_orderAmoutBySize.append(data_orderAmoutBySize[list(set(data_size))[i]])
                            except:
                                num_orderAmoutBySize.append(0)
                        data_to_render["orderAmoutBySize"] = num_orderAmoutBySize
                        # month data
                        data_month=[]
                        for m in range(0, 12):
                            selectedMonth=selectedStatisticstable.filter(date__month = m+1)
                            if len(selectedMonth) < 1:
                                data_month.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderPrice = float(serializer_data["orderPrice"])*float(serializer_data["currency_rate"])
                                    except:
                                        orderPrice = float(serializer_data["orderPrice"])*1
                                    data_per_month = data_per_month + orderPrice
                                data_month.append(data_per_month)
                        data_to_render["orderAmountByMonth"] = data_month
                        return render_to_response('sales_statistics_customer.html', {'data' : data_to_render,  'current_user':request.user.username, 'target_user':person, 'target_size':target_size}, context_instance=RequestContext(request))
                else:
                    return HttpResponse('Invalid request')
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_statistics_agent(request, agent=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                if not agent:
                   return HttpResponse('Invalid GET request: Not agent selected!')
                else:
                    selectedExetable = salesStatisticstable.objects.filter(salesman = agent)
                    selectedExetable = selectedExetable.filter(isLatest = 1)
                    selectedExetable = selectedExetable.filter(b_display = 1)
                    if len(selectedExetable) < 1:
                        return HttpResponse("No such  salesman!")
                    else:
                        '''
                        data_to_render = {
                        'salesAgent': agent,
                        'startDate':'2015-03-04',
                        'endDate':'2016-03-04',
                        'salesAmountByMonth_dict':{'2015-03':100,'2015-04':200,'2015-05':300,'2015-06':400,'2015-07':200,'2015-08':500,'2015-09':700,'2015-10':300,'2015-11':400,'2015-12':200,'2016-01':500,'2016-02':700},
                        'monthList':json.dumps(['2015-03', '2015-04', '2015-05','2015-06', '2015-07', '2015-08','2015-09', '2015-10', '2015-11','2015-12', '2016-01', '2015-02']),
                        'salesAmountByMonth':[100,200,300,400,200,500,700,300,400,200,500,700],
                        'salesCustomerList':json.dumps(["阿里xxx",'Intel', 'AMD', 'Quantum']),
                        'salesCustomerList_ls': ["阿里xxx",'Intel', 'AMD', 'Quantum'],
                        'salesAmountByCustomer':[7200, 6000, 1200, 8000],
                        'salesAmountByCustomer_dict':{"阿里xxx":7200, 'Intel':6000, 'AMD':1200, 'Quantum':8000},
                        }
                        '''
                        data_to_render = {'salesAgent':agent}
                        startDate = str(datetime.date(datetime.date.today().year-3, datetime.date.today().month, datetime.date.today().day))
                        endDate = str(datetime.date.today())

                        data_to_render["startDate"] = startDate
                        data_to_render["endDate"] = endDate
                        selectedExetable = selectedExetable.filter(date__range=(startDate,endDate))

                        monthList = []
                        salesAmountByMonth = []
                        salesAmountByMonth_dict = {}
                        startYear = startDate[0:4]
                        startMonth = startDate[5:7]
                        startYM = int(startYear) * 12 + int(startMonth)
                        endYear = endDate[0:4]
                        endMonth = endDate[5:7]
                        endYM = int(endYear) * 12 + int(endMonth)
                        monthDic = {1:"01", 2:"02", 3:"03", 4:"04", 5:"05", 6:"06", 7:"07", 8:"08", 9:"09", 10:"10", 11:"11", 12:"12"}
                        for ym in range(startYM,endYM+1):
                            chooseYear = int((ym - 1) / 12)
                            chooseMonth = ym % 12
                            if (chooseMonth == 0):
                                chooseMonth = 12
                            monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                            selectedYear = selectedExetable.filter(date__year = chooseYear)
                            selectedMonth = selectedYear.filter(date__month = chooseMonth)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderAmout = float(serializer_data["orderPrice"])
                                    except:
                                        orderAmout = 0
                                    data_per_month = data_per_month + orderAmout
                                salesAmountByMonth.append(data_per_month)
                                salesAmountByMonth_dict[str(chooseYear)+"."+monthDic[chooseMonth]] = data_per_month
                        data_to_render['salesAmountByMonth']=salesAmountByMonth
                        data_to_render['monthList']=json.dumps(monthList)
                        data_to_render['salesAmountByMonth_dict'] = salesAmountByMonth_dict
                        #return  HttpResponse(salesAmountByMonth_dict)

                        data_customer = []
                        data_salesAmoutByCustomer = {}
                        for i in range(0, len(selectedExetable)):
                            serializer=salesStatisticstableSerializer(selectedExetable[i])
                            serializer_data = serializer.data
                            serializer_data["companyName"] = serializer_data["companyName"].encode('utf8')
                            data_customer.append(serializer_data["companyName"])
                            try:
                                float(serializer_data["orderPrice"])
                            except:
                                serializer_data["orderPrice"] = 0
                            try:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = data_salesAmoutByCustomer[serializer_data["companyName"]] + float(serializer_data["orderPrice"])
                            except:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = float(serializer_data["orderPrice"])
                        data_to_render["salesCustomerList"] = json.dumps(list(set(data_customer)))
                        #data_to_render["salesCustomerList_ls"] = [u"intel".encode('utf8'), u"华为".encode('utf8'),u"阿里".encode('utf8'),u"苹果".encode('utf8'),u"阿里xxx".encode('utf8'),u"Microsoft".encode('utf8')]
                        data_to_render["salesCustomerList_ls"] = list(set(data_customer))

                        num_salesAmountByCustomer = []
                        salesAmountByCustomer_dict = {}
                        for i in range(0, len(list(set(data_customer)))):
                            try:
                                num_salesAmountByCustomer.append(data_salesAmoutByCustomer[list(set(data_customer))[i]])
                                salesAmountByCustomer_dict[list(set(data_customer))[i]] = data_salesAmoutByCustomer[list(set(data_customer))[i]]
                            except:
                                num_salesAmountByCustomer.append(0)
                                salesAmountByCustomer_dict[list(set(data_customer))[i]] = 0
                        data_to_render["salesAmountByCustomer"] = num_salesAmountByCustomer
                        data_to_render["salesAmountByCustomer_dict"] = salesAmountByCustomer_dict
                        return render_to_response('sales_statistics_agent.html', {'data' : data_to_render,  'current_user':request.user.username}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                if request.POST.has_key('startDate') and request.POST.has_key('endDate'):
                    selectedExetable = salesStatisticstable.objects.filter(salesman = agent)
                    selectedExetable = selectedExetable.filter(isLatest = 1)
                    selectedExetable = selectedExetable.filter(b_display = 1)
                    if len(selectedExetable) < 1:
                        return HttpResponse("No such  salesman!")
                    else:
                        '''
                        data_to_render = {
                        'salesAgent': agent,
                        'startDate':'2015-03-04',
                        'endDate':'2016-03-04',
                        'salesAmountByMonth_dict':{'2015-03':100,'2015-04':200,'2015-05':300,'2015-06':400,'2015-07':200,'2015-08':500,'2015-09':700,'2015-10':300,'2015-11':400,'2015-12':200,'2016-01':500,'2016-02':700},
                        'monthList':json.dumps(['2015-03', '2015-04', '2015-05','2015-06', '2015-07', '2015-08','2015-09', '2015-10', '2015-11','2015-12', '2016-01', '2015-02']),
                        'salesAmountByMonth':[100,200,300,400,200,500,700,300,400,200,500,700],
                        'salesCustomerList':json.dumps(["阿里xxx",'Intel', 'AMD', 'Quantum']),
                        'salesCustomerList_ls': ["阿里xxx",'Intel', 'AMD', 'Quantum'],
                        'salesAmountByCustomer':[7200, 6000, 1200, 8000],
                        'salesAmountByCustomer_dict':{"阿里xxx":7200, 'Intel':6000, 'AMD':1200, 'Quantum':8000},
                        }
                        '''
                        data_to_render = {'salesAgent':agent}
                        startDate = request.POST["startDate"]
                        endDate = request.POST["endDate"]

                        data_to_render["startDate"] = startDate
                        data_to_render["endDate"] = endDate
                        selectedExetable = selectedExetable.filter(date__range=(startDate,endDate))

                        monthList = []
                        salesAmountByMonth = []
                        salesAmountByMonth_dict = {}
                        startYear = startDate[0:4]
                        startMonth = startDate[5:7]
                        startYM = int(startYear) * 12 + int(startMonth)
                        endYear = endDate[0:4]
                        endMonth = endDate[5:7]
                        endYM = int(endYear) * 12 + int(endMonth)
                        monthDic = {1:"01", 2:"02", 3:"03", 4:"04", 5:"05", 6:"06", 7:"07", 8:"08", 9:"09", 10:"10", 11:"11", 12:"12"}
                        for ym in range(startYM,endYM+1):
                            chooseYear = int((ym - 1) / 12)
                            chooseMonth = ym % 12
                            if (chooseMonth == 0):
                                chooseMonth = 12
                            monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                            selectedYear = selectedExetable.filter(date__year = chooseYear)
                            selectedMonth = selectedYear.filter(date__month = chooseMonth)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth.append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    serializer=salesStatisticstableSerializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        orderAmout = float(serializer_data["orderPrice"])
                                    except:
                                        orderAmout = 0
                                    data_per_month = data_per_month + orderAmout
                                salesAmountByMonth.append(data_per_month)
                                salesAmountByMonth_dict[str(chooseYear)+"."+monthDic[chooseMonth]] = data_per_month
                        data_to_render['salesAmountByMonth']=salesAmountByMonth
                        data_to_render['monthList']=json.dumps(monthList)
                        data_to_render['salesAmountByMonth_dict'] = salesAmountByMonth_dict

                        data_customer = []
                        data_salesAmoutByCustomer = {}
                        for i in range(0, len(selectedExetable)):
                            serializer=salesStatisticstableSerializer(selectedExetable[i])
                            serializer_data = serializer.data
                            serializer_data["companyName"] = serializer_data["companyName"].encode('utf8')
                            data_customer.append(serializer_data["companyName"])
                            try:
                                float(serializer_data["orderPrice"])
                            except:
                                serializer_data["orderPrice"] = 0
                            try:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = data_salesAmoutByCustomer[serializer_data["companyName"]] + float(serializer_data["orderPrice"])
                            except:
                                data_salesAmoutByCustomer[serializer_data["companyName"]] = float(serializer_data["orderPrice"])
                        data_to_render["salesCustomerList"] = json.dumps(list(set(data_customer)))
                        #data_to_render["salesCustomerList_ls"] = [u"intel".encode('utf8'), u"华为".encode('utf8'),u"阿里".encode('utf8'),u"苹果".encode('utf8'),u"阿里xxx".encode('utf8'),u"Microsoft".encode('utf8')]
                        data_to_render["salesCustomerList_ls"] = list(set(data_customer))

                        num_salesAmountByCustomer = []
                        salesAmountByCustomer_dict = {}
                        for i in range(0, len(list(set(data_customer)))):
                            try:
                                num_salesAmountByCustomer.append(data_salesAmoutByCustomer[list(set(data_customer))[i]])
                                salesAmountByCustomer_dict[list(set(data_customer))[i]] = data_salesAmoutByCustomer[list(set(data_customer))[i]]
                            except:
                                num_salesAmountByCustomer.append(0)
                                salesAmountByCustomer_dict[list(set(data_customer))[i]] = 0
                        data_to_render["salesAmountByCustomer"] = num_salesAmountByCustomer
                        data_to_render["salesAmountByCustomer_dict"] = salesAmountByCustomer_dict
                        return render_to_response('sales_statistics_agent.html', {'data' : data_to_render,  'current_user':request.user.username}, context_instance=RequestContext(request))
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


def price_message_declare(request, form_id, method, target_user):

    """
    add to message model
    """
    msg_sql = message_model.objects.filter(message_id=request.POST["message_id"])
    if method == 'add' and len(msg_sql) == 0:
        post_data_dict = dict()
        post_data = request.POST
        post_data_dict["title"] = u"报价批准"
        post_data_dict['message_id'] = request.POST["message_id"]
        post_data_dict['approver_name'] = post_data["approver"]
        post_data_dict['receiver_name'] = 'N/A'

        post_data_dict['requester_name'] = request.user.last_name + request.user.first_name
        post_data_dict['status'] = 'NE'
        post_data_dict['request_date'] = str(datetime.datetime.now().strftime('%Y-%m-%d')) + 'T16:00'
        post_data_dict['content'] = ""
        post_data_dict['url'] = "/ERP/sales_form/{}/{}/".format(form_id, target_user)

        post_data_dict['category'] = u"报价审批"
        post_data_dict['size'] = ""
        post_data_dict['unit'] = ""
        post_data_dict['order_amount'] = ""
        post_data_dict['total_price'] = ""
        post_data_dict['due_date'] = str((datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')) + 'T16:00'
        post_data_dict['update_date'] = str(datetime.datetime.now().strftime('%Y-%m-%d')) + 'T16:00'
        post_data_dict['buyer_name'] = 'N/A'
        post_data_dict['index'] = 'N/A'

        """
        if any update it must be displayed again!
        """
        post_data_dict['requester_display']=True
        post_data_dict['approver_display']=True
        post_data_dict['buyer_display']=True
        post_data_dict['receiver_display']=True
        request_serializer = message_model_serializer(data=post_data_dict)

        if request_serializer.is_valid():
            request_serializer.create(post_data_dict)
        return 'add'
    elif method == 'update' and len(msg_sql) == 1:
        message_model_serializer_ser = message_model_serializer(msg_sql[0])
        data = message_model_serializer_ser.data
        data["approver_name"] = request.POST["approver"]
        data['url'] = "/ERP/sales_form/{}/{}/".format(form_id, target_user)
        message_model_serializer_ser.update(msg_sql[0],data)
        return 'update'
    else:
        return 'error'


def submitSalesExetable(request, type, content=None):
    try:
        q = salesExetable()
        q.No = request.POST.get('No')
        q.companyName = request.POST.get('companyName') # required
        if q.companyName == '':
            return "请填写 客户名称！"
        q.salesman = request.POST.get('salesman')
        if q.salesman == '':
            return "请填写 业务员！"
        q.companyInfo = request.POST.get('companyInfo')
        q.country = request.POST.get('country')
        if q.country == '':
            return "请填写 国家信息！"
        q.productType = request.POST.get('productType') # required

        q.date = request.POST.get('date') # required
        if q.date == '':
            return "请填写 日期！"
        q.productCode = request.POST.get('productCode')
        if q.productCode == '':
            return "请填写 产品代码！"
        q.mag = request.POST.get('mag')

        q.specification = request.FILES.get('specification') # FILES
        q.quantityDemand = request.POST.get('quantityDemand')
        if q.quantityDemand != "":
            try:
                float(q.quantityDemand)
            except:
                return "请填写有效的 需求量！"
        q.opponent = request.POST.get('opponent')
        q.quantityActual = request.POST.get('quantityActual')
        q.assessment = request.POST.get('assessment')
        q.priceUnit = request.POST.get('priceUnit')
        if q.priceUnit != "":
            try:
                float(q.priceUnit)
            except:
                return "请填写有效的 单价！"
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
        q.sample_form_uuid = request.POST.get('sample_form_uuid')
        if q.sample_form_uuid == '':
            q.sample_form_uuid = None

        q.contractReviewNoP = request.FILES.get('contractReviewNoP') # FILES
        q.salesNoP = request.FILES.get('salesNoP') # FILES

        q.produceNo = request.FILES.get('produceNo') # FILES
        q.produceStatus = request.POST.get('produceStatus')
        q.transNo = request.POST.get('transNo')

        q.comments = request.POST.get('comments')
        q.personCharge = request.POST.get('personCharge')
        q.personSupervise = request.POST.get('personSupervise')
        q.conclusion = request.POST.get('conclusion')

        q.message_id = request.POST.get('message_id')
        q.approver = request.POST.get('approver')

        """
        currency unit and amount unit
        """
        q.currency_unit = request.POST.get('currency_unit')
        q.currency_rate = request.POST.get('currency_rate')
        q.amount_unit = request.POST.get('amount_unit')

        q.isLatest = 1

        if type == 'add':
            q.uuid = request.POST.get('uuid')
            price_message_declare(request, q.uuid, 'add', request.POST.get('target_user'))
        elif type == 'update':
            q.uuid = uuid.uuid1()
            rc = price_message_declare(request, q.uuid, 'update', request.POST.get('target_user'))
            if rc == 'error':
                return "fail to update"
            if (q.specification == None):
                if content['specification'] != None:
                    q.specification = unquote(content['specification'])
            if (q.sampleNo == None):
                if content['sampleNo'] != None:
                    q.sampleNo = unquote(content['sampleNo'])
            if (q.smallOrder == None):
                if content['smallOrder'] != None:
                    q.smallOrder = unquote(content['smallOrder'])
            if (q.quoteOrder == None):
                if content['quoteOrder'] != None:
                    q.quoteOrder = unquote(content['quoteOrder'])
            if (q.orderNo == None):
                if content['orderNo'] != None:
                    q.orderNo = unquote(content['orderNo'])
            if (q.contractNo == None):
                if content['contractNo'] != None:
                    q.contractNo = unquote(content['contractNo'])
            if (q.contractReviewNoS == None):
                if content['contractReviewNoS'] != None:
                    q.contractReviewNoS = unquote(content['contractReviewNoS'])
            if (q.salesNoS == None):
                if content['salesNoS'] != None:
                    q.salesNoS = unquote(content['salesNoS'])
            if (q.contractReviewNoP == None):
                if content['contractReviewNoP'] != None:
                    q.contractReviewNoP = unquote(content['contractReviewNoP'])
            if (q.salesNoP == None):
                if content['salesNoP'] != None:
                    q.salesNoP = unquote(content['salesNoP'])
            if (q.produceNo == None):
                if content['produceNo'] != None:
                    q.produceNo = unquote(content['produceNo'])
        else:
            return  "No such type!"
        q.save()

        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def submitSalesStatisticstable(request, type, content=None):
    try:
        q = salesStatisticstable()
        #
        q.No = request.POST.get('No')
        if q.No == '':
            return "请填写 序号！"
        q.date = request.POST.get('date')
        if q.date == '':
            return "请填写 日期！"
        q.companyName = request.POST.get('companyName')
        if q.companyName == '':
            return "请填写 客户名称！"
        q.country = request.POST.get('country')
        if q.country == '':
            return "请填写 国家！"
        q.salesman = request.POST.get('salesman')
        if q.salesman == '':
            return "请填写 业务员！"
        q.contractNo = request.FILES.get('contractNo')
        q.productType = request.POST.get('productType')
        #
        q.Size = request.POST.get('Size')
        if q.Size == '':
            return "请填写 规格/型号！"
        q.orderAmount = request.POST.get('orderAmount')
        try:
            float(q.orderAmount)
        except:
            return "请填写有效的 订单量！"
        q.confirmDate = request.POST.get('confirmDate')
        if q.confirmDate == '':
            q.confirmDate = None
        q.productDue = request.POST.get('productDue')
        q.remainStorage = request.POST.get('remainStorage')
        #
        q.priceUnit = request.POST.get('priceUnit')
        try:
            float(q.priceUnit)
        except:
            return "请填写有效的 单价！"
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
        q.moneyStatus = request.POST.get('moneyStatus')
        #
        q.comments = request.POST.get('comments')

        q.isLatest = 1

        q.currency_unit = request.POST.get('currency_unit')
        q.currency_rate = request.POST.get('currency_rate')
        q.amount_unit = request.POST.get('amount_unit')
        if type == 'add':
            q.uuid = request.POST.get('uuid')
            productDictionary_NOSP = {u"带材":"DC", u"铁芯":"CX", u"器件":"QJ"}
            year = str(int(datetime.datetime.now().year) % 100)
            sample_in_year = salesStatisticstable.objects.filter(date__year = str(datetime.datetime.now().year))
            sample_in_year = sample_in_year.filter(isLatest = 1)
            sample_in_productType = sample_in_year.filter(productType = q.productType)
            count = len(sample_in_productType) + 1
            index = 'LF{}{}{}{}{}{}'.format(year, productDictionary_NOSP[q.productType], count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
            q.No = index
        elif type == 'update':
            q.uuid = uuid.uuid1()
            if request.FILES.get('contractNo') == None:
                if content['contractNo'] == None:
                    q.contractNo = None
                else:
                    q.contractNo = unquote(content['contractNo'])
            else:
                q.contractNo = request.FILES.get('contractNo')
        else:
            return  "No such type!"
        q.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def registration(request):
    try:
        if request.method == 'GET':
            return render_to_response('register.html', context_instance=RequestContext(request))
        elif request.method == 'POST':
            if request.POST.has_key('register'):
                username = request.POST['username']
                user_sql = User.objects.filter(username=username)
                if len(user_sql) !=0:
                    return HttpResponse(json.dumps({"ERROR" : "username has been already existed"}))
                password = request.POST['password']
                password_again = request.POST['password_again']
                if password != password_again:
                    return HttpResponse(json.dumps({"ERROR" : "password is not same!"}))
                last_name = request.POST['last_name']
                first_name = request.POST['first_name']
                email_address = request.POST['email_address']
                if '@' not in email_address:
                    return HttpResponse(json.dumps({"ERROR" : "email address is not valid!"}))

                """
                user extend model
                """
                user_data = {
                'username' : request.POST['username'],
                'backup_email' : request.POST['backup_email'],
                'mobile' : request.POST['mobile'],
                'backup_mobile' : request.POST['backup_mobile'],
                'birthday' : request.POST['birthday'],
                'address' : request.POST['address'],
                'identity' : request.POST['identity'],

                }

                if 'profile_image' in request.FILES.keys():
                    user_data["profile_image"] = request.FILES["profile_image"]
                else:
                    user_data["profile_image"] = None

                if 'birthday' not in request.FILES.keys() or len(request.POST['birthday'].split('-')) !=3:
                    user_data["birthday"] = "1900-01-01"

                user_model_extend_serializer_ser =user_model_extend_serializer(data=user_data)
                if user_model_extend_serializer_ser.is_valid():
                    user_model_extend_serializer_ser.create(user_data)
                    #return HttpResponse(json.dumps({'SUCCESS':user_data}))
                else:
                    return HttpResponse(json.dumps({'Error':user_model_extend_serializer_ser.errors}))

                """
                add user
                """
                user = User.objects.create_user(username, email_address, password)
                # At this point, user is a User object that has already been saved
                # to the database. You can continue to change its attributes
                # if you want to change other fields.
                user.last_name = last_name
                user.first_name = first_name
                user.save()

                """
                send email to admin
                """
                try:
                    msg = "{}{} has registered a new account:{}, please grant him the supposed permissions!".format(user.last_name, user.first_name, username)
                    send_email_th("New Registration Required!",msg)
                except:
                    pass

                return HttpResponseRedirect('/ERP/login/')
            elif request.POST.has_key('register'):
                return STATUS_OK
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sample_form(request, form_uuid=None, sample_form_uuid=None, target_user=None):
    try:
        if request.method == 'GET':
            if request.user.has_perm('main.is_a_salesman') or request.user.has_perm('main.is_producer') or\
                    request.user.has_perm('main.is_sample_producer') or request.user.has_perm('main.is_storage'):
                data_to_render = {}
                if request.user.has_perm('main.is_a_salesman'):
                    form_sql = salesExetable.objects.filter(uuid = form_uuid)
                    if len(form_sql) == 0:
                        return HttpResponse("没有与之匹配的 销售执行表！")
                    else:
                        data_to_render = {}

                        sample_form_sql =  sample_form_model.objects.filter(message_id=sample_form_uuid)


                        if len(sample_form_sql) == 0:
                            data_to_render['is_a_salesman'] =True
                            """
                            auto generate index
                            """
                            year = str(int(datetime.datetime.now().year) % 100)
                            sample_in_year = sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))
                            sample_in_is_sample_form = sample_in_year.filter(is_sample_form = '1')
                            count = len(sample_in_is_sample_form) + 1 + NOSP_num
                            index = 'SP{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                            data_to_render['count'] = count
                            data_to_render['index'] = index
                            data_to_render['create_date'] = str(datetime.datetime.now().year)
                            data_to_render['message_id'] = uuid.uuid1()
                            """
                            unicode is important
                            """
                            data_to_render['produce_status'] = u"待审批"
                            data_to_render['statement'] = u"重要"
                            data_to_render['category'] = u"带材"
                            data_to_render['submit_date'] = datetime.datetime.now().strftime('%Y-%m-%d')

                            user_sql = User.objects.all()
                            data_to_render['target_user'] = request.user.username
                            data_to_render['producer_list'] = ['N/A']
                            for user in user_sql:
                                if user.has_perm('main.is_producer'):
                                    data_to_render['producer_list'].append(user.last_name + user.first_name)

                            if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_sample_producer'):
                                is_producer = True
                            else:
                                is_producer = False

                            if request.user.has_perm('main.is_storage'):
                                is_storage = True
                            else:
                                is_storage = False

                            data_to_render['sales_form_uuid'] = form_uuid
                            """
                            query customer model
                            """
                            customer_sql = customer_model.objects.all()
                            companyName_list = [i.customer_name for i in customer_sql]

                            return render_to_response('sample_form.html', {'data' : data_to_render,'target_user':target_user, 'is_producer':is_producer, 'is_storage':is_storage,  'current_user':request.user.username, "companyName_list" : companyName_list}, context_instance=RequestContext(request))
                        elif len(sample_form_sql) == 1:
                            sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                            sample_form_data = sample_form_serializer.data
                            users = User.objects.all()
                            user_sql = User.objects.all()
                            username_select = sample_form_data['producer']
                            for user in users:
                                if user.username == sample_form_data['producer']:
                                    username_select = user.last_name+user.first_name
                                    break
                            sample_form_data['producer_list'] = [username_select]
                            for user in user_sql:
                                if user.has_perm('main.is_producer'):
                                    if user.username == sample_form_data['producer']:
                                        continue
                                    else:
                                        sample_form_data['producer_list'].append(user.last_name + user.first_name)
                            sample_form_data['target_user'] = sample_form_data['belong_to']
                            sample_form_data['sales_form_uuid'] = form_uuid

                            if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_sample_producer'):
                                is_producer = True
                            else:
                                is_producer = False

                            if request.user.has_perm('main.is_storage'):
                                is_storage = True
                            else:
                                is_storage = False
                            """
                            query customer model
                            """
                            customer_sql = customer_model.objects.all()
                            companyName_list = [i.customer_name for i in customer_sql]

                            '''
                            生产批次显示
                            '''
                            produce_Nos = sample_form_data['produce_Nos']
                            if produce_Nos != None and produce_Nos != '':
                                produce_No_list = produce_Nos.split(';')
                            else:
                                produce_No_list = []
                                sample_form_data['produce_Nos'] = ''
                            produce_No_html = []
                            for i in range(0,len(produce_No_list)):
                                produce_sql = produce_statistics_pendai_model.objects.filter(item_id=produce_No_list[i])
                                produce_sql = produce_sql.filter(isLatest=1)
                                produce_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=produce_No_list[i])
                                produce_sql2 = produce_sql2.filter(isLatest=1)
                                produce_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=produce_No_list[i])
                                produce_sql3 = produce_sql3.filter(isLatest=1)
                                if((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==1):
                                    if(len(produce_sql)==1):
                                        serializer=produce_statistics_pendai_model_serializer(produce_sql[0])
                                        produce_type = 'pendai'
                                    elif(len(produce_sql2)==1):
                                        serializer=produce_statistics_gunjian_model_serializer(produce_sql2[0])
                                        produce_type = 'gunjian'
                                    else:
                                        serializer=produce_statistics_tiexin_model_serializer(produce_sql3[0])
                                        produce_type = 'tiexin'
                                    serializer_data = serializer.data
                                    produce_uuid = serializer_data['uuid']
                                elif((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==0):
                                    produce_uuid = 'no-such-uuid'
                                    produce_type = 'pendai'
                                else:
                                    produce_uuid = 'too-much-such-uuid'
                                    produce_type = 'pendai'
                                iter_produce_No = {
                                        'produce_No': produce_No_list[i],
                                        'produce_uuid': produce_uuid,
                                        'produce_type': produce_type,
                                    }
                                produce_No_html.append(iter_produce_No)

                            return render_to_response('sample_form.html', {'data' : sample_form_data,'target_user':target_user,  'is_producer':is_producer, 'is_storage':is_storage, 'current_user':request.user.username, "companyName_list":companyName_list,  'produce_No_html':produce_No_html}, context_instance=RequestContext(request))
        if request.method == 'POST':
            data = request.POST
            """
            must fill in area
            """
            for key in ["customer", "submit_date", "due_date", "size", "amount", 'delivery_address']:
                if len(data[key]) == 0:
                    return HttpResponse(json.dumps({"ERROR" : "please fill in {} area".format(key)}))
            """
            save to database
            """
            sample_form_sql = sample_form_model.objects.filter(message_id=sample_form_uuid)
            productDictionary = {u"带材":1, u"铁芯":2, u"器件":3}
            if len(sample_form_sql) == 0:
                """
                re-update the index
                """
                data_to_save = {}
                for key in data:
                    data_to_save[key] = data[key]

                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if data_to_save['producer'] == (user.last_name + user.first_name) :
                        data_to_save['producer'] = user.username
                        break

                year = str(int(datetime.datetime.now().year) % 100)
                sample_in_year = sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))
                #sample_in_productType = sample_in_year.filter(category = productDictionary[data["category"]])
                sample_in_is_sample_form = sample_in_year.filter(is_sample_form = '1')
                count = len(sample_in_is_sample_form) + 1 + NOSP_num

                data_to_save['category'] = productDictionary[data["category"]]

                index = 'SP{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                data_to_save['index'] = index

                data_to_save["belong_to"] = request.user.username

                data_to_save["is_sample_form"] = False

                if len(data["producer_date"].split('-')) != 3:
                    data_to_save["producer_date"] =  None

                if len(data["approver_date"].split('-')) != 3:
                    data_to_save["approver_date"] =  None

                if len(data["technician_date"].split('-')) != 3:
                    data_to_save["technician_date"] = None

                if len(data["producian_date"].split('-')) != 3:
                    data_to_save["producian_date"] = None

                data_to_save["sales_editable"] = False
                data_to_save["technical_editable"] = False
                data_to_save["produce_editable"] = False
                data_to_save["delivery_editable"] = False

                if len(data["producer_step_date_0"].split('-')) != 3:
                    data_to_save["producer_step_date_0"] =  None
                if len(data["producer_step_date_1"].split('-')) != 3:
                    data_to_save["producer_step_date_1"] =  None
                if len(data["producer_step_date_2"].split('-')) != 3:
                    data_to_save["producer_step_date_2"] =  None
                if len(data["producer_step_date_3"].split('-')) != 3:
                    data_to_save["producer_step_date_3"] =  None
                if len(data["producer_step_date_4"].split('-')) != 3:
                    data_to_save["producer_step_date_4"] =  None

                data_to_save["producer_step_date_5"] =  None

                if len(data["planner_date"].split('-')) != 3:
                    data_to_save["planner_date"] =  None

                data_to_save["deliver"] = "undefined"

                if len(data["delivery_date"].split('-')) != 3:
                    data_to_save["delivery_date"] =  None

                if len(data["manager_date"].split('-')) != 3:
                    data_to_save["manager_date"] =  None

                sample_form_all_num = len(sample_form_model.objects.all())

                data_to_save['sequence'] = sample_form_all_num + 1
                data_to_save['reorder'] = sample_form_all_num + 1

                data_to_save['is_sample_form'] = 1
                sample_form_serializer = sample_form_model_serializer(data=data_to_save)
                if sample_form_serializer.is_valid():
                    sample_form_serializer.create(data_to_save)
                    '''
                    sales exe table insert sample form uuid
                    '''
                    sales_form_sql = salesExetable.objects.filter(uuid = data_to_save['sales_form_uuid'])
                    if len(sales_form_sql) == 0:
                        return HttpResponse("没有找到对应的 销售执行表！")
                    else:
                        sales_form_serializer = salesExetableSerializer(sales_form_sql[0])
                        sales_form_data = sales_form_serializer.data
                        sales_form_data['sample_form_uuid'] = data_to_save['message_id']
                        sales_form_serializer.update(sales_form_sql[0],sales_form_data)
                        #return HttpResponse(json.dumps({'SUCCESS':data_to_save}))
                        if request.user.has_perm('main.is_a_salesman') :
                            return HttpResponseRedirect('/ERP/sales_list/{}'.format(target_user))
                        elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                            return HttpResponseRedirect('/ERP/produce_executive_list/{}'.format(target_user))
                        else: #storage
                            pass
                else:
                    return HttpResponse(json.dumps({'Error':sample_form_serializer.errors}))
            elif len(sample_form_sql) == 1:
                sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                sample_form_data = sample_form_serializer.data
                """
                backup field
                """
                data['belong_to'] = sample_form_data["belong_to"]
                data['deliver'] = "undefined"
                data["sales_editable"] = False
                data["technical_editable"] = False
                data["produce_editable"] = False
                data["delivery_editable"] = False
                data["is_display"] = True
                data["isnot_completed"] = True
                data["sequence"] = sample_form_data['sequence']
                data["reorder"] = sample_form_data['reorder']
                data["producer_step_date_5"] =  ""
                data["is_sample_form"] = False
                for key in sample_form_data.keys():
                    if 'date' in key and 'create_date' not in key:
                        if not data[key] or len(data[key].split('-')) != 3:
                            sample_form_data[key] = None
                    else:
                       sample_form_data[key] = data[key]
                sample_form_data['category'] = productDictionary[data["category"]]
                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if sample_form_data['producer'] == (user.last_name + user.first_name):
                        sample_form_data['producer'] = user.username
                        break
                sample_form_data['is_sample_form'] = 1
                sample_form_serializer.update(sample_form_sql[0], sample_form_data)
                '''
                sales exe table insert sample form uuid
                '''
                sales_form_sql = salesExetable.objects.filter(uuid = sample_form_data['sales_form_uuid'])
                if len(sales_form_sql) == 0:
                    return HttpResponse("没有找到对应的 销售执行表！")
                else:
                    sales_form_serializer = salesExetableSerializer(sales_form_sql[0])
                    sales_form_data = sales_form_serializer.data
                    sales_form_data['sample_form_uuid'] = sample_form_data['message_id']
                    sales_form_serializer.update(sales_form_sql[0],sales_form_data)
                #return HttpResponse(json.dumps({'SUCCESS':"update the produce form!"}))
                if request.user.has_perm('main.is_a_salesman') :
                    return HttpResponseRedirect('/ERP/sales_list/{}'.format(target_user))
                elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                    return HttpResponseRedirect('/ERP/produce_executive_list/{}'.format(target_user))
                else: #storage
                    pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def sales_producer_request_list(request, target_user=None):
    if request.method == 'GET':
        if request.user.has_perm('main.is_a_salesman'):
            if request.user.has_perm('main.is_sales_manager'):
                if request.user.username == target_user:
                    sample_form_sql = sample_form_model.objects.all()
                else:
                    sample_form_sql = sample_form_model.objects.filter(belong_to = target_user)
            else:
                sample_form_sql = sample_form_model.objects.filter(belong_to = target_user)
            sample_form_sql = sample_form_sql.order_by('-sequence')
            data_to_render = {'target_user':'', 'data_items':[]}
            data_to_render['target_user'] = target_user
            for i in range(0, len(sample_form_sql)):
                sample_form_serializer = sample_form_model_serializer(sample_form_sql[i])
                data = sample_form_serializer.data
                template = {}
                template['no'] = i + 1
                template['index'] = data['index']
                template['uuid'] = data['message_id']
                template['statement'] = data['statement']
                template['customer'] = data['customer']
                template['submit_date'] = data['submit_date']
                template['contact_person'] = data['contact_person']
                template['contact_person_phone'] = data['contact_person_phone']
                template['due_date'] = data['due_date']
                if(data['is_sample_form']==True):
                    template['is_sample_form'] = u'样品单'
                else:
                    template['is_sample_form'] = u'生产单'
                data_to_render['data_items'].append(template)
            return render_to_response('sales_producer_request_list.html', {'data' : data_to_render,  'current_user':request.user.username}, context_instance=RequestContext(request))
    else:
        return HttpResponse('Invalid request!')

def produce_request_form(request, target_user=None, form_uuid=None):
    try:
        if request.method == 'GET':
            if request.user.has_perm('main.is_a_salesman') or request.user.has_perm('main.is_producer') or \
                request.user.has_perm('main.is_producer_manager') or request.user.has_perm('main.is_storage') :
                data_to_render = {}
                sample_form_sql =  sample_form_model.objects.filter(message_id=form_uuid)
                if len(sample_form_sql) == 0:
                    data_to_render['is_a_salesman'] =True
                    """
                    auto generate index
                    """
                    year = str(int(datetime.datetime.now().year) % 100)
                    count = len(sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))) + 1
                    index = 'SP{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                    data_to_render['count'] = count
                    data_to_render['index'] = index
                    data_to_render['create_date'] = str(datetime.datetime.now().year)
                    data_to_render['message_id'] = uuid.uuid1()
                    """
                    unicode is important
                    """
                    data_to_render['statement'] = u"重要"
                    data_to_render['category'] = u"带材"
                    data_to_render['submit_date'] = datetime.datetime.now().strftime('%Y-%m-%d')

                    user_sql = User.objects.all()
                    data_to_render['target_user'] = target_user
                    data_to_render['producer_list'] = ['N/A']
                    data_to_render['produce_status'] = u"待审批"
                    for user in user_sql:
                        if user.has_perm('main.is_producer'):
                            data_to_render['producer_list'].append(user.last_name + user.first_name)
                    if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        is_producer = True
                    else:
                        is_producer = False

                    if request.user.has_perm('main.is_storage') and not request.user.is_superuser:
                        is_storage = True
                    else:
                        is_storage = False

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]

                    return render_to_response('sales_produce_request_form.html', {'data' : data_to_render, 'is_producer':is_producer, 'is_storage':is_storage,  'current_user':request.user.username, "companyName_list" : companyName_list,  'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif len(sample_form_sql) == 1:
                    sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                    sample_form_data = sample_form_serializer.data
                    users = User.objects.all()
                    user_sql = User.objects.all()
                    username_select = sample_form_data['producer']+u'(未找到)'
                    for user in users:
                        if user.username == sample_form_data['producer']:
                            username_select = user.last_name+user.first_name
                            break
                    sample_form_data['producer_list'] = [username_select]
                    for user in user_sql:
                        if user.has_perm('main.is_producer'):
                            if user.username == sample_form_data['producer']:
                                continue
                            else:
                                sample_form_data['producer_list'].append(user.last_name + user.first_name)
                    #sample_form_data['target_user'] = sample_form_data['belong_to']
                    sample_form_data['target_user'] = target_user
                    if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        is_producer = True
                    else:
                        is_producer = False

                    if request.user.has_perm('main.is_storage') and not request.user.is_superuser:
                        is_storage = True
                    else:
                        is_storage = False

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = ['未找到']
                    setting_size_unit_list += [i.size_name for i in setting_size_sql]

                    '''
                    生产批次显示
                    '''
                    produce_Nos = sample_form_data['produce_Nos']
                    if produce_Nos != None and produce_Nos != '':
                        produce_No_list = produce_Nos.split(';')
                    else:
                        produce_No_list = []
                        sample_form_data['produce_Nos'] = ''
                    produce_No_html = []
                    for i in range(0,len(produce_No_list)):
                        produce_sql = produce_statistics_pendai_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql = produce_sql.filter(isLatest=1)
                        produce_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql2 = produce_sql2.filter(isLatest=1)
                        produce_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql3 = produce_sql3.filter(isLatest=1)
                        if((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==1):
                            if(len(produce_sql)==1):
                                serializer=produce_statistics_pendai_model_serializer(produce_sql[0])
                                produce_type = 'pendai'
                            elif(len(produce_sql2)==1):
                                serializer=produce_statistics_gunjian_model_serializer(produce_sql2[0])
                                produce_type = 'gunjian'
                            else:
                                serializer=produce_statistics_tiexin_model_serializer(produce_sql3[0])
                                produce_type = 'tiexin'
                            serializer_data = serializer.data
                            produce_uuid = serializer_data['uuid']
                        elif((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==0):
                            produce_uuid = 'no-such-uuid'
                            produce_type = 'pendai'
                        else:
                            produce_uuid = 'too-much-such-uuid'
                            produce_type = 'pendai'
                        iter_produce_No = {
                                'produce_No': produce_No_list[i],
                                'produce_uuid': produce_uuid,
                                'produce_type': produce_type,
                            }
                        produce_No_html.append(iter_produce_No)


                    return render_to_response('sales_produce_request_form.html', {'data' : sample_form_data, 'is_producer':is_producer,'is_storage':is_storage,  'current_user':request.user.username, 'companyName_list' : companyName_list, 'produce_No_html':produce_No_html,  'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))

        if request.method == 'POST':
            data = request.POST
            """
            must fill in area
            """
            for key in ["customer", "submit_date", "due_date", "size", "amount"]:
                if len(data[key]) == 0:
                    return HttpResponse(json.dumps({"ERROR" : "please fill in {} area".format(key)}))
            """
            save to database
            """
            sample_form_sql = sample_form_model.objects.filter(message_id=form_uuid)
            productDictionary = {u"带材":1, u"铁芯":2, u"器件":3}
            productDictionary_NOSP = {u"带材":"DC", u"铁芯":"CX", u"器件":"QJ"}
            if len(sample_form_sql) == 0:
                """
                re-update the index
                """
                data_to_save = {}
                for key in data:
                    data_to_save[key] = data[key]

                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if data_to_save['producer'] == (user.last_name + user.first_name) :
                        data_to_save['producer'] = user.username
                        break

                year = str(int(datetime.datetime.now().year) % 100)
                sample_in_year = sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))
                sample_in_productType = sample_in_year.filter(category = productDictionary[data["category"]])
                count = len(sample_in_productType) + 1

                data_to_save['category'] = productDictionary[data["category"]]

                index = 'SP{}{}{}{}{}{}'.format(year, productDictionary_NOSP[data["category"]], count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                data_to_save['index'] = index

                data_to_save["belong_to"] = request.user.username

                data_to_save["is_sample_form"] = False

                if len(data["producer_date"].split('-')) != 3:
                    data_to_save["producer_date"] =  None

                if len(data["approver_date"].split('-')) != 3:
                    data_to_save["approver_date"] =  None

                if len(data["technician_date"].split('-')) != 3:
                    data_to_save["technician_date"] = None

                if len(data["producian_date"].split('-')) != 3:
                    data_to_save["producian_date"] = None

                data_to_save["sales_editable"] = False
                data_to_save["technical_editable"] = False
                data_to_save["produce_editable"] = False
                data_to_save["delivery_editable"] = False

                if len(data["producer_step_date_0"].split('-')) != 3:
                    data_to_save["producer_step_date_0"] =  None
                if len(data["producer_step_date_1"].split('-')) != 3:
                    data_to_save["producer_step_date_1"] =  None
                if len(data["producer_step_date_2"].split('-')) != 3:
                    data_to_save["producer_step_date_2"] =  None
                if len(data["producer_step_date_3"].split('-')) != 3:
                    data_to_save["producer_step_date_3"] =  None
                if len(data["producer_step_date_4"].split('-')) != 3:
                    data_to_save["producer_step_date_4"] =  None

                data_to_save["producer_step_date_5"] =  None

                if len(data["planner_date"].split('-')) != 3:
                    data_to_save["planner_date"] =  None

                data_to_save["deliver"] = "undefined"

                if len(data["delivery_date"].split('-')) != 3:
                    data_to_save["delivery_date"] =  None

                if len(data["manager_date"].split('-')) != 3:
                    data_to_save["manager_date"] =  None

                data_to_save["sales_form_uuid"] = "None_need_sales_form_uuid"

                sample_form_all_num = len(sample_form_model.objects.all())

                data_to_save['sequence'] = sample_form_all_num + 1
                data_to_save['reorder'] = sample_form_all_num + 1


                sale_statistics_form_sql = salesStatisticstable.objects.filter(No=data_to_save['sale_index'])
                sale_statistics_form_sql = sale_statistics_form_sql.filter(isLatest=1)
                sale_statistics_form_sql = sale_statistics_form_sql.filter(b_display=1)
                '''
                # 修改为不需要判断销售单号是否存在
                if (len(sale_statistics_form_sql)==0):
                    return HttpResponse("没有找到对应的销售单号，请按后退按钮重新填写！")
                elif(len(sale_statistics_form_sql)>1):
                    return HttpResponse("找到多个销售单号，请联系管理员处理！")
              '''





                sample_form_serializer = sample_form_model_serializer(data=data_to_save)
                if sample_form_serializer.is_valid():

                    if request.POST.has_key('operation'):
                        if data['produce_Nos'] == None or data['produce_Nos'] == '':
                            return HttpResponse("未填写生产批次号，请按后退按钮重新填写！（若暂无生产批次号，请填写“无”）")
                        if data['produce_status'] != u'完成':
                            return HttpResponse("生产状态未修改为“完成”，请按后退按钮重新填写！（仅当生产状态为完成时方可点击该按钮）")
                        sample_form_finish_sql = sample_form_model.objects.all()
                        for i in range(0,len(sample_form_finish_sql)):
                            sample_form_finish_serializer = sample_form_model_serializer(sample_form_finish_sql[i])
                            sample_form_finish_data = sample_form_finish_serializer.data
                            if sample_form_finish_data['sequence'] != sample_form_finish_data['reorder']:
                                return "有员工正在申请该或其他生产单调序，请等待经理批准以后再完成该生产单！"
                        data_to_save['isnot_completed'] = False
                        sample_form_serializer = sample_form_model_serializer(data=data_to_save)

                    sample_form_serializer.create(data_to_save)
                    #return HttpResponse(len(sale_statistics_form_sql)+3)
                    #return HttpResponse(json.dumps({'SUCCESS':data_to_save}))
                    if request.user.has_perm('main.is_a_salesman') :
                        return HttpResponseRedirect('/ERP/sales_producer_request_list/{}'.format(target_user))
                    elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        return HttpResponseRedirect('/ERP/produce_executive_list/{}'.format(target_user))
                    else: #storage
                        pass
                else:
                    return HttpResponse(json.dumps({'Error':sample_form_serializer.errors}))
            elif len(sample_form_sql) == 1:
                sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                sample_form_data = sample_form_serializer.data
                """
                backup field
                """
                data['belong_to'] = sample_form_data["belong_to"]
                data['deliver'] = "undefined"
                data["sales_editable"] = False
                data["technical_editable"] = False
                data["produce_editable"] = False
                data["delivery_editable"] = False
                data["is_display"] = True
                data["isnot_completed"] = True
                data["sequence"] = sample_form_data['sequence']
                data["reorder"] = sample_form_data['reorder']
                data["producer_step_date_5"] =  ""
                data["is_sample_form"] = sample_form_data['is_sample_form']
                data["sales_form_uuid"] = "None_need_sales_form_uuid"
                for key in sample_form_data.keys():
                    if 'date' in key and 'create_date' not in key:
                        if not data[key] or len(data[key].split('-')) != 3:
                            sample_form_data[key] = None
                        else:
                            sample_form_data[key] = data[key]
                    else:
                       sample_form_data[key] = data[key]
                sample_form_data['category'] = productDictionary[data["category"]]
                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if sample_form_data['producer'] == (user.last_name + user.first_name):
                        sample_form_data['producer'] = user.username
                        break

                if(sample_form_data['is_sample_form']!=True):

                    sale_statistics_form_sql = salesStatisticstable.objects.filter(No=sample_form_data['sale_index'])
                    sale_statistics_form_sql = sale_statistics_form_sql.filter(isLatest=1)
                    sale_statistics_form_sql = sale_statistics_form_sql.filter(b_display=1)
                    if (len(sale_statistics_form_sql)==0):
                        return HttpResponse("没有找到对应的销售单号，请按后退按钮重新填写！")
                    elif(len(sale_statistics_form_sql)>1):
                        return HttpResponse("找到多个销售单号，请联系管理员处理！")

                if sample_form_data['produce_status'] == '':
                    return HttpResponse('请填写 生产状态！')
                else:
                    if request.POST.has_key('operation'):
                        if data['produce_Nos'] == None or data['produce_Nos'] == '':
                            return HttpResponse("未填写生产批次号，请按后退按钮重新填写！（若暂无生产批次号，请填写“无”）")
                        if data['produce_status'] != u'完成':
                            return HttpResponse("生产状态未修改为“完成”，请按后退按钮重新填写！（仅当生产状态为完成时方可点击该按钮）")
                        sample_form_finish_sql = sample_form_model.objects.all()
                        for i in range(0,len(sample_form_finish_sql)):
                            sample_form_finish_serializer = sample_form_model_serializer(sample_form_finish_sql[i])
                            sample_form_finish_data = sample_form_finish_serializer.data
                            if sample_form_finish_data['sequence'] != sample_form_finish_data['reorder']:
                                return "有员工正在申请该或其他生产单调序，请等待经理批准以后再完成该生产单！"
                        sample_form_data['isnot_completed'] = False
                        sample_form_serializer = sample_form_model_serializer(data=sample_form_data)
                    sample_form_serializer.update(sample_form_sql[0], sample_form_data)
                    #return HttpResponse(json.dumps({'SUCCESS':"update the produce form!"}))
                    if request.user.has_perm('main.is_a_salesman') :
                        return HttpResponseRedirect('/ERP/sales_producer_request_list/{}'.format(target_user))
                    elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        return HttpResponseRedirect('/ERP/produce_executive_list/{}'.format(target_user))
                    else: #storage
                        pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sample_request_form(request, target_user=None, form_uuid=None):
    try:
        if request.method == 'GET':
            if request.user.has_perm('main.is_a_salesman') or request.user.has_perm('main.is_producer') or \
                request.user.has_perm('main.is_producer_manager') or request.user.has_perm('main.is_storage') :
                data_to_render = {}
                sample_form_sql =  sample_form_model.objects.filter(message_id=form_uuid)
                if len(sample_form_sql) == 0:
                    data_to_render['is_a_salesman'] =True
                    """
                    auto generate index
                    """
                    year = str(int(datetime.datetime.now().year) % 100)
                    count = len(sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))) + 1
                    index = 'SP{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                    data_to_render['count'] = count
                    data_to_render['index'] = index
                    data_to_render['create_date'] = str(datetime.datetime.now().year)
                    data_to_render['message_id'] = uuid.uuid1()
                    """
                    unicode is important
                    """
                    data_to_render['statement'] = u"重要"
                    data_to_render['category'] = u"带材"
                    data_to_render['submit_date'] = datetime.datetime.now().strftime('%Y-%m-%d')

                    user_sql = User.objects.all()
                    data_to_render['target_user'] = target_user
                    data_to_render['producer_list'] = ['N/A']
                    data_to_render['produce_status'] = u"待审批"
                    for user in user_sql:
                        if user.has_perm('main.is_producer'):
                            data_to_render['producer_list'].append(user.last_name + user.first_name)
                    if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        is_producer = True
                    else:
                        is_producer = False

                    if request.user.has_perm('main.is_storage'):
                        is_storage = True
                    else:
                        is_storage = False

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]

                    return render_to_response('sales_sample_request_form.html', {'data' : data_to_render, 'is_producer':is_producer, 'is_storage':is_storage,  'current_user':request.user.username, "companyName_list" : companyName_list,  'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif len(sample_form_sql) == 1:
                    sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                    sample_form_data = sample_form_serializer.data
                    users = User.objects.all()
                    user_sql = User.objects.all()
                    username_select = sample_form_data['producer']+u'(未找到)'
                    for user in users:
                        if user.username == sample_form_data['producer']:
                            username_select = user.last_name+user.first_name
                            break
                    sample_form_data['producer_list'] = [username_select]
                    for user in user_sql:
                        if user.has_perm('main.is_producer'):
                            if user.username == sample_form_data['producer']:
                                continue
                            else:
                                sample_form_data['producer_list'].append(user.last_name + user.first_name)
                    #sample_form_data['target_user'] = sample_form_data['belong_to']
                    sample_form_data['target_user'] = target_user
                    if request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        is_producer = True
                    else:
                        is_producer = False

                    if request.user.has_perm('main.is_storage'):
                        is_storage = True
                    else:
                        is_storage = False

                    """
                    query customer model
                    """
                    customer_sql = customer_model.objects.all()
                    companyName_list = [i.customer_name for i in customer_sql]
                    setting_size_sql = setting_size_model.objects.all()
                    setting_size_unit_list = ['未找到']
                    setting_size_unit_list += [i.size_name for i in setting_size_sql]

                    '''
                    生产批次显示
                    '''
                    produce_Nos = sample_form_data['produce_Nos']
                    if produce_Nos != None and produce_Nos != '':
                        produce_No_list = produce_Nos.split(';')
                    else:
                        produce_No_list = []
                        sample_form_data['produce_Nos'] = ''
                    produce_No_html = []
                    for i in range(0,len(produce_No_list)):
                        produce_sql = produce_statistics_pendai_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql = produce_sql.filter(isLatest=1)
                        produce_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql2 = produce_sql2.filter(isLatest=1)
                        produce_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=produce_No_list[i])
                        produce_sql3 = produce_sql3.filter(isLatest=1)
                        if((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==1):
                            if(len(produce_sql)==1):
                                serializer=produce_statistics_pendai_model_serializer(produce_sql[0])
                                produce_type = 'pendai'
                            elif(len(produce_sql2)==1):
                                serializer=produce_statistics_gunjian_model_serializer(produce_sql2[0])
                                produce_type = 'gunjian'
                            else:
                                serializer=produce_statistics_tiexin_model_serializer(produce_sql3[0])
                                produce_type = 'tiexin'
                            serializer_data = serializer.data
                            produce_uuid = serializer_data['uuid']
                        elif((len(produce_sql)+len(produce_sql2)+len(produce_sql3))==0):
                            produce_uuid = 'no-such-uuid'
                            produce_type = 'pendai'
                        else:
                            produce_uuid = 'too-much-such-uuid'
                            produce_type = 'pendai'
                        iter_produce_No = {
                                'produce_No': produce_No_list[i],
                                'produce_uuid': produce_uuid,
                                'produce_type': produce_type,
                            }
                        produce_No_html.append(iter_produce_No)


                    return render_to_response('sales_sample_request_form.html', {'data' : sample_form_data, 'is_producer':is_producer,'is_storage':is_storage,  'current_user':request.user.username, 'companyName_list' : companyName_list, 'produce_No_html':produce_No_html,  'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))

        if request.method == 'POST':
            data = request.POST
            """
            must fill in area
            """
            for key in ["customer", "submit_date", "due_date", "size", "amount"]:
                if len(data[key]) == 0:
                    return HttpResponse(json.dumps({"ERROR" : "please fill in {} area".format(key)}))
            """
            save to database
            """
            sample_form_sql = sample_form_model.objects.filter(message_id=form_uuid)
            productDictionary = {u"带材":1, u"铁芯":2, u"器件":3}
            productDictionary_NOSP = {u"带材":"DC", u"铁芯":"CX", u"器件":"QJ"}
            if len(sample_form_sql) == 0:
                """
                re-update the index
                """
                data_to_save = {}
                for key in data:
                    data_to_save[key] = data[key]

                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if data_to_save['producer'] == (user.last_name + user.first_name) :
                        data_to_save['producer'] = user.username
                        break


                year = str(int(datetime.datetime.now().year) % 100)
                sample_in_year = sample_form_model.objects.filter(create_date = str(datetime.datetime.now().year))
                #sample_in_productType = sample_in_year.filter(category = productDictionary[data["category"]])
                sample_in_is_sample_form = sample_in_year.filter(is_sample_form = '1')
                count = len(sample_in_is_sample_form) + 1 + NOSP_num


                data_to_save['category'] = productDictionary[data["category"]]

                index = 'SP{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                data_to_save['index'] = index

                data_to_save["belong_to"] = request.user.username

                data_to_save["is_sample_form"] = True

                if len(data["producer_date"].split('-')) != 3:
                    data_to_save["producer_date"] =  None

                if len(data["approver_date"].split('-')) != 3:
                    data_to_save["approver_date"] =  None

                if len(data["technician_date"].split('-')) != 3:
                    data_to_save["technician_date"] = None

                if len(data["producian_date"].split('-')) != 3:
                    data_to_save["producian_date"] = None

                data_to_save["sales_editable"] = False
                data_to_save["technical_editable"] = False
                data_to_save["produce_editable"] = False
                data_to_save["delivery_editable"] = False

                if len(data["producer_step_date_0"].split('-')) != 3:
                    data_to_save["producer_step_date_0"] =  None
                if len(data["producer_step_date_1"].split('-')) != 3:
                    data_to_save["producer_step_date_1"] =  None
                if len(data["producer_step_date_2"].split('-')) != 3:
                    data_to_save["producer_step_date_2"] =  None
                if len(data["producer_step_date_3"].split('-')) != 3:
                    data_to_save["producer_step_date_3"] =  None
                if len(data["producer_step_date_4"].split('-')) != 3:
                    data_to_save["producer_step_date_4"] =  None

                data_to_save["producer_step_date_5"] =  None

                if len(data["planner_date"].split('-')) != 3:
                    data_to_save["planner_date"] =  None

                data_to_save["deliver"] = "undefined"

                if len(data["delivery_date"].split('-')) != 3:
                    data_to_save["delivery_date"] =  None

                if len(data["manager_date"].split('-')) != 3:
                    data_to_save["manager_date"] =  None

                data_to_save["sales_form_uuid"] = "None_need_sales_form_uuid"

                sample_form_all_num = len(sample_form_model.objects.all())

                data_to_save['sequence'] = sample_form_all_num + 1
                data_to_save['reorder'] = sample_form_all_num + 1


                sale_statistics_form_sql = salesStatisticstable.objects.filter(No=data_to_save['sale_index'])
                sale_statistics_form_sql = sale_statistics_form_sql.filter(isLatest=1)
                sale_statistics_form_sql = sale_statistics_form_sql.filter(b_display=1)
                '''
                # 修改为不需要判断销售单号是否存在
                if (len(sale_statistics_form_sql)==0):
                    return HttpResponse("没有找到对应的销售单号，请按后退按钮重新填写！")
                elif(len(sale_statistics_form_sql)>1):
                    return HttpResponse("找到多个销售单号，请联系管理员处理！")
              '''





                sample_form_serializer = sample_form_model_serializer(data=data_to_save)
                if sample_form_serializer.is_valid():

                    if request.POST.has_key('operation'):
                        if data['produce_Nos'] == None or data['produce_Nos'] == '':
                            return HttpResponse("未填写生产批次号，请按后退按钮重新填写！（若暂无生产批次号，请填写“无”）")
                        if data['produce_status'] != u'完成':
                            return HttpResponse("生产状态未修改为“完成”，请按后退按钮重新填写！（仅当生产状态为完成时方可点击该按钮）")
                        sample_form_finish_sql = sample_form_model.objects.all()
                        for i in range(0,len(sample_form_finish_sql)):
                            sample_form_finish_serializer = sample_form_model_serializer(sample_form_finish_sql[i])
                            sample_form_finish_data = sample_form_finish_serializer.data
                            if sample_form_finish_data['sequence'] != sample_form_finish_data['reorder']:
                                return "有员工正在申请该或其他生产单调序，请等待经理批准以后再完成该生产单！"
                        data_to_save['isnot_completed'] = False
                        sample_form_serializer = sample_form_model_serializer(data=data_to_save)

                    sample_form_serializer.create(data_to_save)
                    #return HttpResponse(len(sale_statistics_form_sql)+3)
                    #return HttpResponse(json.dumps({'SUCCESS':data_to_save}))
                    if request.user.has_perm('main.is_a_salesman') :
                        return HttpResponseRedirect('/ERP/sales_producer_request_list/{}'.format(target_user))
                    elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        return HttpResponseRedirect('/ERP/sample_executive_list/{}'.format(target_user))
                    else: #storage
                        pass
                else:
                    return HttpResponse(json.dumps({'Error':sample_form_serializer.errors}))
            elif len(sample_form_sql) == 1:
                sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                sample_form_data = sample_form_serializer.data
                """
                backup field
                """
                data['belong_to'] = sample_form_data["belong_to"]
                data['deliver'] = "undefined"
                data["sales_editable"] = False
                data["technical_editable"] = False
                data["produce_editable"] = False
                data["delivery_editable"] = False
                data["is_display"] = True
                data["isnot_completed"] = True
                data["sequence"] = sample_form_data['sequence']
                data["reorder"] = sample_form_data['reorder']
                data["producer_step_date_5"] =  ""
                data["is_sample_form"] = sample_form_data['is_sample_form']
                data["sales_form_uuid"] = "None_need_sales_form_uuid"
                for key in sample_form_data.keys():
                    if 'date' in key and 'create_date' not in key:
                        if not data[key] or len(data[key].split('-')) != 3:
                            sample_form_data[key] = None
                        else:
                            sample_form_data[key] = data[key]
                    else:
                       sample_form_data[key] = data[key]
                sample_form_data['category'] = productDictionary[data["category"]]
                """
                deal w/ produer name
                """
                users = User.objects.all()
                for user in users:
                    if sample_form_data['producer'] == (user.last_name + user.first_name):
                        sample_form_data['producer'] = user.username
                        break

                if(sample_form_data['is_sample_form']!=True):

                    sale_statistics_form_sql = salesStatisticstable.objects.filter(No=sample_form_data['sale_index'])
                    sale_statistics_form_sql = sale_statistics_form_sql.filter(isLatest=1)
                    sale_statistics_form_sql = sale_statistics_form_sql.filter(b_display=1)
                    if (len(sale_statistics_form_sql)==0):
                        return HttpResponse("没有找到对应的销售单号，请按后退按钮重新填写！")
                    elif(len(sale_statistics_form_sql)>1):
                        return HttpResponse("找到多个销售单号，请联系管理员处理！")

                if sample_form_data['produce_status'] == '':
                    return HttpResponse('请填写 生产状态！')
                else:
                    if request.POST.has_key('operation'):
                        if data['produce_Nos'] == None or data['produce_Nos'] == '':
                            return HttpResponse("未填写生产批次号，请按后退按钮重新填写！（若暂无生产批次号，请填写“无”）")
                        if data['produce_status'] != u'完成':
                            return HttpResponse("生产状态未修改为“完成”，请按后退按钮重新填写！（仅当生产状态为完成时方可点击该按钮）")
                        sample_form_finish_sql = sample_form_model.objects.all()
                        for i in range(0,len(sample_form_finish_sql)):
                            sample_form_finish_serializer = sample_form_model_serializer(sample_form_finish_sql[i])
                            sample_form_finish_data = sample_form_finish_serializer.data
                            if sample_form_finish_data['sequence'] != sample_form_finish_data['reorder']:
                                return "有员工正在申请该或其他生产单调序，请等待经理批准以后再完成该生产单！"
                        sample_form_data['isnot_completed'] = False
                        sample_form_serializer = sample_form_model_serializer(data=sample_form_data)
                    sample_form_serializer.update(sample_form_sql[0], sample_form_data)
                    #return HttpResponse(json.dumps({'SUCCESS':"update the produce form!"}))
                    if request.user.has_perm('main.is_a_salesman') :
                        return HttpResponseRedirect('/ERP/sales_producer_request_list/{}'.format(target_user))
                    elif request.user.has_perm('main.is_producer') or request.user.has_perm('main.is_producer_manager'):
                        return HttpResponseRedirect('/ERP/sample_executive_list/{}'.format(target_user))
                    else: #storage
                        pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))



def superuser(request, target_user=None):
    try:
        if request.method == 'GET':
            if request.user.is_superuser or request.user.has_perm('main.is_special_user'):
                data_to_render = {"sales":[], "producer":[], "storage":[], "buyer":[],"hr":[], "quality":[], "all":[], "target_user":target_user}
                users = User.objects.all()
                for user in users:
                    user_extension_sql = user_model_extend.objects.filter(username=user.username)
                    if len(user_extension_sql) > 0:
                        user_model_extend_serializer_ser = user_model_extend_serializer(user_extension_sql[0])
                        extension = user_model_extend_serializer_ser.data
                        import urllib
                        if 'profile_image' in extension.keys() and extension["profile_image"] and len(extension["profile_image"]) > 0:
                            profile_image = urllib.unquote(extension["profile_image"].decode("utf-8"))
                        else:
                            profile_image = {}
                    else:
                        extension = {}
                        profile_image = ''

                    is_valid = True
                    if user.last_login:
                        is_valid = True
                        last_login = '{}-{}-{} {}:{}'.format(user.last_login.year, user.last_login.month, user.last_login.day, user.last_login.hour, user.last_login.minute)
                    else:
                        last_login = "UNACTIVATED ACCOUNT!"
                        is_valid = False

                    data_to_render["all"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login , "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    if user.has_perm('main.is_a_salesman') and not user.is_superuser and not user.has_perm('main.is_quality'):
                        data_to_render["sales"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image":profile_image, "email":user.email})
                    elif user.has_perm('main.is_producer') and not user.is_superuser and not user.has_perm('main.is_quality'):
                        data_to_render["producer"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_storage') and not user.is_superuser and not user.has_perm('main.is_quality'):
                        data_to_render["storage"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_buyer') and not user.is_superuser and not user.has_perm('main.is_quality'):
                        data_to_render["buyer"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_ranker') and not user.is_superuser and not user.has_perm('main.is_quality'):
                        data_to_render["hr"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_quality') and not user.is_superuser:
                        data_to_render["quality"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})

                #return HttpResponse(repr(data_to_render))
                return render_to_response("superuser.html", data_to_render, context_instance=RequestContext(request))
                #return HttpResponse("Permission GRANTED!")
            else:
                return HttpResponse("Permission DENIED!")
        else:
            return HttpResponse("ERROR POST REQUEST, please contact yubo.li@hotmail.com")
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_manager(request, target_user=None):
    try:
        if request.method == 'GET':
            if request.user.has_perm("main.is_sales_manager"):
                data_to_render = {"sales":[], "target_user":target_user}
                users = User.objects.all()
                for user in users:
                    user_extension_sql = user_model_extend.objects.filter(username=user.username)
                    if len(user_extension_sql) > 0:
                        user_model_extend_serializer_ser = user_model_extend_serializer(user_extension_sql[0])
                        extension = user_model_extend_serializer_ser.data
                        import urllib
                        if 'profile_image' in extension.keys() and extension["profile_image"] and len(extension["profile_image"]) > 0:
                            profile_image = urllib.unquote(extension["profile_image"].decode("utf-8"))
                        else:
                            profile_image = {}
                    else:
                        extension = {}
                        profile_image = ''

                    is_valid = True
                    if user.last_login:
                        is_valid = True
                        last_login = '{}-{}-{} {}:{}'.format(user.last_login.year, user.last_login.month, user.last_login.day, user.last_login.hour, user.last_login.minute)
                    else:
                        is_valid = False
                        last_login = "UNACTIVATED ACCOUNT!"

                    if user.has_perm('main.is_a_salesman') and not user.is_superuser:
                        data_to_render["sales"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image":profile_image, "email":user.email})


                return render_to_response("sales_manager.html", data_to_render, context_instance=RequestContext(request))

            else:
                return HttpResponse("Permission DENIED!")
        else:
            return HttpResponse("ERROR POST REQUEST, please contact yubo.li@hotmail.com")
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))


def sales_customer_archive(request):
    if request.user.has_perm('main.is_sales_manager') or request.user.has_perm('main.is_a_salesman'):
        try:
            if request.method== 'GET':

                if 'customer_name' not in request.GET.keys():
                    customer_model_data = customer_model.objects.filter(b_display='1')
                    data_to_render = []
                    for i in range(0, len(customer_model_data)):
                         serializer=customer_model_serializer(customer_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'customer_name': serializer_data['customer_name'],
                                     'customer_address': serializer_data['customer_address'],
                                     'customer_contact': serializer_data["customer_contact"],
                                     'customer_mobile': serializer_data["customer_mobile"],
                                     'customer_fax': serializer_data["customer_fax"],
                                     'customer_email': serializer_data["customer_email"],
                                     'customer_rank': serializer_data["customer_rank"],
                                     'customer_comment': serializer_data["customer_comment"],
                                     }
                         data_to_render.append(iter_data)
                    return render_to_response('sales_customer_archive.html', {'data':data_to_render, 'target_user':request.GET["target_user"]}, context_instance=RequestContext(request))
                else:

                    customer_model_data = customer_model.objects.filter(b_display='1', customer_name=request.GET["customer_name"])
                    if len(customer_model_data) == 0:
                        return HttpResponse(u"Customer NOT FOUND!")
                    serializer=customer_model_serializer(customer_model_data[0])
                    serializer_data = serializer.data
                    data_to_render = {
                                 'customer_name': serializer_data['customer_name'],
                                 'customer_address': serializer_data['customer_address'],
                                 'customer_contact': serializer_data["customer_contact"],
                                 'customer_mobile': serializer_data["customer_mobile"],
                                 'customer_fax': serializer_data["customer_fax"],
                                 'customer_email': serializer_data["customer_email"],
                                 'customer_rank': serializer_data["customer_rank"],
                                 'customer_comment': serializer_data["customer_comment"],
                                 'customer_backup': serializer_data["customer_backup"],
                                 'customer_contact2': serializer_data["customer_contact2"],
                                 'customer_mobile2': serializer_data["customer_mobile2"],
                                 'customer_fax2': serializer_data["customer_fax2"],
                                 'customer_email2': serializer_data["customer_email2"],
                                 }
                    return  render_to_response('sales_customer_archive_detail.html', {'data':data_to_render, 'target_user':request.GET["target_user"]}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if 'customer_comment' not in request.POST.keys():
                    if request.POST["operation"] == 'update' :
                        customer_model_data = customer_model.objects.filter(b_display='1', customer_name=request.POST["customer_name"])
                        if len(customer_model_data) != 1:
                            return HttpResponse("item not unique or not exists! please contact lybroman@hotmail.com")
                        serializer=customer_model_serializer(customer_model_data[0])
                        serializer_data = serializer.data
                        for key in serializer_data:
                            if key in request.POST:
                                serializer_data[key] =  request.POST[key]

                        serializer.update(customer_model_data[0], serializer_data)
                        return HttpResponseRedirect('/ERP/sales_customer_archive?target_user={}'.format(request.POST["target_user"]))
                    elif request.POST["operation"] == 'add':
                        # add a new item
                        customer_model_data = customer_model.objects.filter(customer_name=request.POST["customer_name"])
                        if len(customer_model_data) != 0:
                            return HttpResponse("客户信息已存在!")
                        iter_data = {
                                    'customer_name': request.POST['customer_name'],
                                     'customer_address': request.POST['customer_address'],
                                     'customer_contact': request.POST["customer_contact"],
                                     'customer_mobile': request.POST["customer_mobile"],
                                     'customer_fax': request.POST["customer_fax"],
                                     'customer_email': request.POST["customer_email"],
                                     'customer_rank': request.POST["customer_rank"],
                                     'b_display' : '1',
                                     }
                        customer_model_serializer_ser =customer_model_serializer(data=iter_data)
                        if customer_model_serializer_ser.is_valid():
                            customer_model_serializer_ser.create(iter_data)
                            return HttpResponseRedirect('/ERP/sales_customer_archive?target_user={}'.format(request.POST["target_user"]))
                        else:
                            return HttpResponse(json.dumps({'Error':customer_model_serializer_ser.errors}))
                else:
                    customer_model_data = customer_model.objects.filter(b_display='1', customer_name=request.POST["customer_name"])
                    if len(customer_model_data) != 1:
                        return HttpResponse("item not unique or not exists! please contact lybroman@hotmail.com")
                    serializer=customer_model_serializer(customer_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]

                    serializer.update(customer_model_data[0], serializer_data)
                    return HttpResponseRedirect('/ERP/sales_customer_archive?target_user={}'.format(request.POST["target_user"]))
        except:
            return HttpResponse(traceback.format_exc())
    else:
        return HttpResponse('Permission Denied')


def hr_main(request, target_user=None):
    try:
        if request.method == 'GET':
            if request.user.is_superuser or request.user.has_perm('main.is_ranker'):
                data_to_render = {"sales":[], "producer":[], "storage":[], "buyer":[], "hr":[], "all":[], "target_user":target_user}
                users = User.objects.all()
                for user in users:
                    user_extension_sql = user_model_extend.objects.filter(username=user.username)
                    if len(user_extension_sql) > 0:
                        user_model_extend_serializer_ser = user_model_extend_serializer(user_extension_sql[0])
                        extension = user_model_extend_serializer_ser.data
                        import urllib
                        if 'profile_image' in extension.keys() and extension["profile_image"] and len(extension["profile_image"]) > 0:
                            profile_image = urllib.unquote(extension["profile_image"].decode("utf-8"))
                        else:
                            profile_image = {}
                    else:
                        extension = {}
                        profile_image = ''

                    is_valid = True
                    if user.last_login:
                        is_valid = True
                        last_login = '{}-{}-{} {}:{}'.format(user.last_login.year, user.last_login.month, user.last_login.day, user.last_login.hour, user.last_login.minute)
                    else:
                        last_login = "UNACTIVATED ACCOUNT!"
                        is_valid = False

                    data_to_render["all"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    if user.has_perm('main.is_a_salesman') and not user.is_superuser:
                        data_to_render["sales"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image":profile_image, "email":user.email})
                    elif user.has_perm('main.is_producer') and not user.is_superuser:
                        data_to_render["producer"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_storage') and not user.is_superuser:
                        data_to_render["storage"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_buyer') and not user.is_superuser:
                        data_to_render["buyer"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})
                    elif user.has_perm('main.is_ranker') and not user.is_superuser:
                        data_to_render["hr"].append({"username":user.username, "last_name":user.last_name, "first_name":user.first_name, "full_name":user.last_name + user.first_name,\
                        "active": is_valid, "last_login":last_login, "date_joined":user.date_joined, "profile_image": profile_image, "email":user.email})

                #return HttpResponse(repr(data_to_render))
                data_to_render["target_user"]=target_user
                return render_to_response("hr_main.html", data_to_render, context_instance=RequestContext(request))
                #return HttpResponse("Permission GRANTED!")
            else:
                return HttpResponse("Permission DENIED!")
        else:
            return HttpResponse("ERROR POST REQUEST, please contact yubo.li@hotmail.com")
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def quality_main(request, target_user=None):
    return render_to_response("quality_main.html", {'target_user':target_user}, context_instance=RequestContext(request))


def special_user_main(request, target_user):
    return render_to_response("special_user_main.html", {'target_user':target_user}, context_instance=RequestContext(request))