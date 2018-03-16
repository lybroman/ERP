# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        request_views
# Purpose:
#
# Author:      yuboli
#
# Created:     28/03/2016
# Copyright:   (c) yuboli 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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

from django.contrib.auth import authenticate, login

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import socket

from django.http import HttpResponseRedirect

from  main.models import message_model, sample_form_model
from main.serializers import message_model_serializer, sample_form_model_serializer
from django.contrib.auth.models import User
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
import threading
STATUS_OK = HttpResponse(json.dumps({"status" : "okay"}))

map_status = {u"待审批":"NE", u"已批准":"RE", u"已拒绝":"NO",u"已采购":"CO", u"确认生产":"CP", u"采购流程":"CO"}

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def send_email_th(title, msg, receivers):
    th = threading.Thread(target=send_email, args=(title, msg, receivers))
    th.start()

def send_email(title, msg, receivers):
    mail_host="smtp.londerful.com"
    mail_user="021@londerful.com"
    mail_pass="qweasdzxc1234"

    sender = '021@londerful.com'
    #receivers = ['021@londerful.com','005@londerful.com','zhz128ly@163.com']

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



def requests(request, request_id=None, url=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
                return HttpResponseRedirect(r'/ERP/login/')
        if request.method == 'GET':
            """
            return a new request form
            """
            # if not a log in user redirect to log in page
            if request.user.is_anonymous() or not request.user.is_authenticated():
                return HttpResponseRedirect(r'/ERP/login/')
            else:
                if not request_id:
                    data_to_render = {}
                    data_to_render["full_name"] = request.user.last_name + request.user.first_name
                    data_to_render['uuid'] = str(uuid.uuid1())
                    # default 1
                    data_to_render['category'] = u"生产材料"
                    data_to_render['applicant'] = request.user.last_name + request.user.first_name
                    data_to_render['status'] = 'NE'
                    data_to_render['date'] = datetime.datetime.now().strftime('%Y-%m-%d')

                    """
                    Get user form user modek
                    """
                    data_to_render['url']=url
                    data_to_render['title']=u"采购申请"
                    data_to_render['all_users'] = ['N/A']
                    data_to_render['approver_list'] = ['N/A']
                    data_to_render['buyer_list'] = ['N/A']
                    data_to_render['producer_list'] = ['N/A']
                    data_to_render['purchase_state'] = 'N/A'
                    user_sql = User.objects.all()
                    for user in user_sql:
                        data_to_render['all_users'].append(user.username)
                        if user.has_perm('main.is_approver'):
                            data_to_render['approver_list'].append(user.last_name + user.first_name)
                        if user.has_perm('main.is_buyer'):
                            data_to_render['buyer_list'].append(user.last_name + user.first_name)
                        if user.has_perm('main.is_producer'):
                            data_to_render['producer_list'].append(user.last_name + user.first_name)

                    return render_to_response('request.html', {'data':data_to_render}, context_instance=RequestContext(request))
                else:
                    msgs_sql = message_model.objects.filter(message_id = request_id)
                    msgs_serializer = message_model_serializer(msgs_sql[0])
                    msgs_data = msgs_serializer.data
                    data_to_render={}
                    data_to_render["full_name"] = request.user.last_name + request.user.first_name
                    data_to_render["uuid"] = msgs_data['message_id']
                    data_to_render["title"] = msgs_data['title']
                    data_to_render["approver"] = msgs_data['approver_name']
                    data_to_render["category"] = msgs_data['receiver_name']
                    data_to_render["applicant"] =  msgs_data['requester_name']
                    data_to_render["producer"] =  msgs_data['producer_name']
                    data_to_render["status"] =  msgs_data['status']
                    data_to_render["date"] = msgs_data['request_date'].split('T')[0]
                    data_to_render['content'] =  msgs_data['content']
                    data_to_render['url'] = msgs_data['url']

                    data_to_render["category"] = msgs_data['category']
                    data_to_render["size"] = msgs_data['size']
                    data_to_render["unit"] = msgs_data['unit']
                    data_to_render['orderAmount'] = msgs_data["order_amount"]
                    data_to_render["totalPrice"] = msgs_data['total_price']
                    data_to_render["dueDate"] = msgs_data['due_date'].split('T')[0]
                    data_to_render["buyer"] = msgs_data['buyer_name']
                    data_to_render["No"] = msgs_data['index']
                    if 'purchase_state' in msgs_data.keys() and msgs_data['purchase_state']:
                        data_to_render['purchase_state'] = msgs_data['purchase_state']
                    else:
                        data_to_render['purchase_state'] = 'N/A'

                    """
                    if any update it must be displayed again!
                    """
                    data_to_render["requester_display"] = msgs_data['requester_display']
                    data_to_render['approver_display'] = msgs_data['approver_display']
                    data_to_render['buyer_display'] = msgs_data['buyer_display']
                    data_to_render['receiver_display'] = msgs_data['receiver_display']
                    data_to_render['producer_display'] = msgs_data['producer_display']

                    user_sql = User.objects.all()
                    """
                    Get user form user modek
                    """
                    data_to_render['all_users'] = ['N/A']
                    data_to_render['approver_list'] = ['N/A']
                    data_to_render['buyer_list'] = ['N/A']
                    data_to_render['producer_list'] = ['N/A']
                    user_sql = User.objects.all()
                    for user in user_sql:
                        data_to_render['all_users'].append(user.username)
                        if user.has_perm('main.is_approver'):
                            data_to_render['approver_list'].append(user.last_name + user.first_name)
                        if user.has_perm('main.is_buyer'):
                            data_to_render['buyer_list'].append(user.last_name + user.first_name)
                        if user.has_perm('main.is_producer'):
                            data_to_render['producer_list'].append(user.last_name + user.first_name)
                    #return HttpResponse(json.dumps(data_to_render))

                    sample_form_sqls = sample_form_model.objects.all()
                    sample_form_sqls = sample_form_sqls.order_by('reorder')
                    category_dictionary = {'1':u'带材', '2':u'铁芯', '3':u'器件'}
                    data_to_render_item = {'submit_date':'',  'customer':'', 'index':'', 'category':'', 'amount':'', 'statement':'', 'message_id':'', 'sales_comment':'', 'belong_to':'', 'produce_status':''}
                    tabledata_to_render = []
                    count  = 1
                    for sample_form_sql in sample_form_sqls:
                        sample_form_serializer = sample_form_model_serializer(sample_form_sql)
                        data = sample_form_serializer.data
                        tmp = copy.deepcopy(data_to_render_item)
                        for key in tmp.keys():
                            tmp[key] = data[key]
                        tmp['no'] = count
                        #tmp['produce_status'] = "unknown"
                        tmp['category'] = category_dictionary[tmp['category'] ]
                        count += 1
                        tabledata_to_render.append(tmp)
                    istable = False
                    if msgs_data["title"] == u"生产顺序调整":
                        istable = True
                    else:
                        istable = False
                    return render_to_response('request.html', {'data':data_to_render, 'tabledata':tabledata_to_render, 'istable':istable}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            if 'NE' in request.POST['operation']:
                """
                if new uuid create else update
                """
                msgs_sql = message_model.objects.filter(message_id = request.POST['uuid'])
                if len(msgs_sql) > 1:
                    return HttpResponse(json.dumps({'Error':'None unique uuid for request form'}))
                else:
                    post_data_dict = dict()
                    post_data = request.POST
                    post_data_dict["title"] = post_data['title']
                    post_data_dict['message_id'] = post_data["uuid"]
                    post_data_dict['approver_name'] = post_data["approver"]
                    # backup field for CEO review
                    post_data_dict['receiver_name'] = post_data["category"]
                    post_data_dict['requester_name'] = post_data["applicant"]
                    post_data_dict['status'] = map_status[post_data["status"]]
                    post_data_dict['request_date'] = str(post_data["date"]) + 'T16:00'
                    post_data_dict['content'] = post_data["content"]
                    post_data_dict['url'] = post_data["url"]

                    post_data_dict['category'] = post_data["category"]
                    post_data_dict['size'] = post_data["size"]
                    post_data_dict['unit'] = post_data["unit"]
                    post_data_dict['order_amount'] = post_data["orderAmount"]
                    post_data_dict['total_price'] = post_data["totalPrice"]
                    post_data_dict['due_date'] = str(post_data["dueDate"]) + 'T16:00'
                    post_data_dict['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                    post_data_dict['buyer_name'] = post_data["buyer"]
                    post_data_dict['producer_name'] = post_data["producer"]
                    post_data_dict['index'] = post_data["No"]

                    post_data_dict['purchase_state'] = 'N/A'

                    """
                    if any update it must be displayed again!
                    """
                    post_data_dict['requester_display']=True
                    post_data_dict['approver_display']=True
                    post_data_dict['buyer_display']=True
                    post_data_dict['receiver_display']=True
                    post_data_dict['producer_display']=True
                    post_data_dict['render_content']='N/A'
                    if len(msgs_sql) == 1:
                        msgs_serializer = message_model_serializer(msgs_sql[0])
                        msgs_data = msgs_serializer.data
                        if msgs_data['status'] == 'CO':
                            return HttpResponse(json.dumps({'Error':'This request has been in purchase process!'}))
                        elif msgs_data['status'] == 'RE':
                            return HttpResponse(json.dumps({'Error':'This request has been approved!'}))
                        elif msgs_data['status'] == 'CP':
                            return HttpResponse(json.dumps({'Error':'This request has been in producing!'}))
                        for key in msgs_data.keys():
                            msgs_data[key] = post_data_dict[key]
                        msgs_serializer.update(msgs_sql[0], msgs_data)

                        email_reveivers = []
                        email_reveivers_names = ''
                        email_reveivers.append('zhz128ly@163.com')
                        user_sql = User.objects.all()
                        receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                        for user in user_sql:
                            if (user.last_name + user.first_name) in receiver_str:
                                email_reveivers.append(user.email)
                                email_reveivers_names += (user.last_name + user.first_name + ' ')
                        email_title = '请求信息已更新'
                        email_msg = post_data['title'].encode('utf8') + ' 请求信息已更新，请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                        send_email_th(email_title,email_msg,email_reveivers)
                        return HttpResponse(json.dumps({'SUCCESS':"message updated!"}))
                    else:
                        request_serializer = message_model_serializer(data=post_data_dict)
                        if request_serializer.is_valid():
                            request_serializer.create(post_data_dict)
                            #return HttpResponse(json.dumps(post_data_dict))
                            email_reveivers = []
                            email_reveivers_names = ''
                            email_reveivers.append('zhz128ly@163.com')
                            user_sql = User.objects.all()
                            receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                            for user in user_sql:
                                if (user.last_name + user.first_name) in receiver_str:
                                    email_reveivers.append(user.email)
                                    email_reveivers_names += (user.last_name + user.first_name + ' ')
                            email_title = '新增请求信息'
                            email_msg = '新增' + post_data['title'].encode('utf8') + ' 请求信息，请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                            send_email_th(email_title,email_msg,email_reveivers)
                            return HttpResponse(json.dumps({'SUCCESS':'You have made a new request!'}))
                        else:
                            #return HttpResponse(json.dumps(post_data_dict))
                            return HttpResponse(json.dumps({'Error':request_serializer.errors}))
            elif 'RE' in request.POST['operation']:
                """
              approver with authentication
              """
                request_uuid = request.POST['uuid']
                post_data= request.POST
                target_approver = request.user.last_name + request.user.first_name
                if request.user.has_perm('main.is_approver') and target_approver == post_data["approver"]:
                    msgs_sql = message_model.objects.filter(message_id = request_uuid)
                    if len(msgs_sql) != 1:
                        return HttpResponse(json.dumps({'Error':'None unique uuid for request form!'}))
                    msgs_serializer = message_model_serializer(msgs_sql[0])
                    msgs_data = msgs_serializer.data
                    msgs_data['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                    if msgs_data['status'] == 'NE':

                        if msgs_data['title'] == u"生产顺序调整":
                            sample_form_sql = sample_form_model.objects.all()
                            for i in range(0, len(sample_form_sql)):
                                sample_form_serializer = sample_form_model_serializer(sample_form_sql[i])
                                sample_form_data = sample_form_serializer.data
                                sample_form_data['sequence'] = sample_form_data['reorder']
                                sample_form_serializer.update(sample_form_sql[i],sample_form_data)


                        for key in request.POST.keys():
                            if key in msgs_data.keys():
                                msgs_data[key] = request.POST[key]
                        msgs_data['status'] = 'RE'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        email_reveivers = []
                        email_reveivers_names = ''
                        email_reveivers.append('zhz128ly@163.com')
                        user_sql = User.objects.all()
                        receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                        for user in user_sql:
                            if (user.last_name + user.first_name) in receiver_str:
                                email_reveivers.append(user.email)
                                email_reveivers_names += (user.last_name + user.first_name + ' ')
                        email_title = '请求信息已审批通过'
                        email_msg = post_data['title'].encode('utf8') + '请求信息已审批通过，请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                        send_email_th(email_title,email_msg,email_reveivers)
                        return HttpResponse(json.dumps({'SUCCESS':'You have approved the request'}))
                    elif msgs_data['status'] == 'CO':
                        return HttpResponse(json.dumps({'Error':u'Purchase is in process, Do no need to approve again!'}))
                    elif msgs_data['status'] == 'CP':
                        return HttpResponse(json.dumps({'Error':'This request has been in producing !'}))
                    elif msgs_data['status'] == 'RE':
                        msgs_data['status'] = 'RE'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        return HttpResponse(json.dumps({'WARNING':'This request has been approved!'}))
                else:
                    return HttpResponse(json.dumps({'Error':'You do not have permission to approve the request!'}))
            elif 'NO' in request.POST['operation']:
                """
                approver with authentication
                """
                request_uuid = request.POST['uuid']
                post_data= request.POST
                target_approver = request.user.last_name + request.user.first_name
                if request.user.has_perm('main.is_approver') and target_approver == post_data["approver"]:
                    msgs_sql = message_model.objects.filter(message_id = request_uuid)
                    if len(msgs_sql) != 1:
                        return HttpResponse(json.dumps({'Error':'None unique uuid for request form!'}))
                    msgs_serializer = message_model_serializer(msgs_sql[0])
                    msgs_data = msgs_serializer.data
                    msgs_data['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                    if msgs_data['status'] == 'NE':
                        if msgs_data['title'] == u"生产顺序调整":
                            sample_form_sql = sample_form_model.objects.all()
                            for i in range(0, len(sample_form_sql)):
                                sample_form_serializer = sample_form_model_serializer(sample_form_sql[i])
                                sample_form_data = sample_form_serializer.data
                                sample_form_data['reorder'] = sample_form_data['sequence']
                                sample_form_serializer.update(sample_form_sql[i],sample_form_data)
                        msgs_data['status'] = 'NO'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        email_reveivers = []
                        email_reveivers_names = ''
                        email_reveivers.append('zhz128ly@163.com')
                        user_sql = User.objects.all()
                        receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                        for user in user_sql:
                            if (user.last_name + user.first_name) in receiver_str:
                                email_reveivers.append(user.email)
                                email_reveivers_names += (user.last_name + user.first_name + ' ')
                        email_title = '请求信息已被拒绝'
                        email_msg = post_data['title'].encode('utf8') + '请求信息已被审核人员拒绝，请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                        send_email_th(email_title,email_msg,email_reveivers)
                        return HttpResponse(json.dumps({'SUCCESS':'You have reject the request'}))
                    elif msgs_data['status'] == 'CO':
                        return HttpResponse(json.dumps({'Error':u'Purchase is in process, Do no need to approve again!'}))
                    elif msgs_data['status'] == 'CP':
                        return HttpResponse(json.dumps({'Error':'This request has been in producing !'}))
                    elif msgs_data['status'] == 'RE':
                        msgs_data['status'] = 'RE'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        return HttpResponse(json.dumps({'WARNING':'This request has been approved!'}))
                else:
                    return HttpResponse(json.dumps({'Error':'You do not have permission to approve the request!'}))
            elif 'CO' in request.POST['operation']:
                """
                buyer with authentication
                """
                request_uuid = request.POST['uuid']
                post_data = request.POST
                target_buyer = request.user.last_name + request.user.first_name
                if request.user.has_perm('main.is_buyer') and target_buyer == post_data["buyer"]:
                    """
                    if not approved, cannot buy it.
                    """
                    msgs_sql = message_model.objects.filter(message_id = request_uuid)
                    if len(msgs_sql) != 1:
                        return HttpResponse(json.dumps({'Error':'None unique uuid for request form'}))
                    msgs_serializer = message_model_serializer(msgs_sql[0])
                    msgs_data = msgs_serializer.data
                    msgs_data['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                    if msgs_data['status'] == 'RE':
                        msgs_data['status'] = 'CO'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        email_reveivers = []
                        email_reveivers_names = ''
                        email_reveivers.append('zhz128ly@163.com')
                        user_sql = User.objects.all()
                        receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                        for user in user_sql:
                            if (user.last_name + user.first_name) in receiver_str:
                                email_reveivers.append(user.email)
                                email_reveivers_names += (user.last_name + user.first_name + ' ')
                        email_title = '请求信息已确认采购'
                        email_msg = post_data['title'].encode('utf8') + '请求信息已确认采购，请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                        send_email_th(email_title,email_msg,email_reveivers)
                        return HttpResponse(json.dumps({'SUCCESS':'You have confirmed purhcase of the request'}))
                    elif msgs_data['status'] == 'CO':
                         msgs_sql = message_model.objects.filter(message_id = request.POST['uuid'])
                         if len(msgs_sql) == 1:
                            msgs_serializer = message_model_serializer(msgs_sql[0])
                            msgs_data = msgs_serializer.data
                            msgs_data["purchase_state"] = post_data['purchase_state']
                            msgs_serializer.update(msgs_sql[0], msgs_data)
                            email_reveivers = []
                            email_reveivers_names = ''
                            email_reveivers.append('zhz128ly@163.com')
                            user_sql = User.objects.all()
                            receiver_str = post_data['applicant']+','+post_data['approver']+','+post_data['buyer']+','+post_data['producer']
                            for user in user_sql:
                                if (user.last_name + user.first_name) in receiver_str:
                                    email_reveivers.append(user.email)
                                    email_reveivers_names += (user.last_name + user.first_name + ' ')
                            email_title = '请求信息已确认采购（再次更新）'
                            email_msg = post_data['title'].encode('utf8') + '请求信息已确认采购（再次更新），请相关人员('+ email_reveivers_names.encode('utf8') +')注意！'
                            send_email_th(email_title,email_msg,email_reveivers)
                            return HttpResponse(json.dumps({'SUCCESS':'status update!'}))
                         else:
                             return HttpResponse(json.dumps({'Error':'wrong operation, please contact lybroman@hotmal.com'}))
                    elif msgs_data['status'] == 'NE':
                        return HttpResponse(json.dumps({'Error':'This request has not been approved!'}))
                else:
                    return HttpResponse(json.dumps({'Error':'You do not have permission to confirm purchasing!'}))
            elif 'CP' in request.POST['operation']:
                """
                buyer with authentication
                """
                request_uuid = request.POST['uuid']
                post_data = request.POST
                target_buyer = request.user.last_name + request.user.first_name
                if request.user.has_perm('main.is_producer') and target_buyer == post_data["producer"]:
                    """
                    if not approved, cannot produce it.
                    """
                    msgs_sql = message_model.objects.filter(message_id = request_uuid)
                    if len(msgs_sql) != 1:
                        return HttpResponse(json.dumps({'Error':'None unique uuid for request form'}))
                    msgs_serializer = message_model_serializer(msgs_sql[0])
                    msgs_data = msgs_serializer.data
                    msgs_data['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                    if msgs_data['status'] == 'RE':
                        msgs_data['status'] = 'CP'
                        msgs_serializer.update(msgs_sql[0], msgs_data)
                        return HttpResponse(json.dumps({'SUCCESS':'You have confirmed to produce'}))
                    elif msgs_data['status'] == 'NE':
                        return HttpResponse(json.dumps({'Error':'This request has not been approved!'}))
                else:
                    return HttpResponse(json.dumps({'Error':'You do not have permission to confirm PRODUCING!'}))
            elif 'DELETE' in request.POST['operation']:
                request_uuid = request.POST['uuid']
                msgs_sql = message_model.objects.filter(message_id = request_uuid)
                if len(msgs_sql) != 1:
                    return HttpResponse(json.dumps({'Error':'None unique uuid for request form'}))
                msgs_serializer = message_model_serializer(msgs_sql[0])
                msgs_data = msgs_serializer.data
                msgs_data['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d') + 'T16:00'
                operator_name = request.user.last_name + request.user.first_name
                if operator_name == msgs_data['requester_name']:
                   msgs_data['requester_display'] = False
                if operator_name == msgs_data['approver_name']:
                    msgs_data['approver_display'] = False
                if operator_name == msgs_data['buyer_name']:
                    msgs_data['buyer_display'] = False
                if operator_name == msgs_data['receiver_name']:
                    msgs_data['receiver_display'] = False
                msgs_serializer.update(msgs_sql[0], msgs_data)
            else:
                return HttpResponse(json.dumps({'Error':"Not a valid operation"}))

    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

import operator

def messages(request, request_id=None):
    try:
        if request.method == 'GET':
            """
            return a new request form
            """
            # if not a log in user redirect to log in page
            if request.user.is_anonymous() or not request.user.is_authenticated():
                return HttpResponseRedirect(r'/ERP/login/')
            else:
                item_template = {'index':'', 'status':'', 'category':'', 'date':'', 'due_date':'', 'applicant':'', 'uuid':'', 'duration':'', 'update_date':'', 'purchase_state':''}
                data_to_render = []
                uuid_list = []
                msgs_sql = []
                user_name = request.user.last_name + request.user.first_name
                msgs_sql.append(message_model.objects.filter(receiver_name__icontains = user_name, receiver_display=True))
                msgs_sql.append(message_model.objects.filter(requester_name = user_name, requester_display=True))
                msgs_sql.append(message_model.objects.filter(approver_name = user_name, approver_display=True))
                msgs_sql.append(message_model.objects.filter(buyer_name = user_name, buyer_display=True))
                msgs_sql.append(message_model.objects.filter(producer_name = user_name, producer_display=True))

                msgs_serializer = []
                for it in msgs_sql:
                    msgs_serializer = message_model_serializer(it, many=True)
                    msgs_serializer_data = msgs_serializer.data
                    for item_data in msgs_serializer_data:
                        if item_data['message_id'] in uuid_list:
                            pass
                        else:
                            uuid_list.append(item_data['message_id'])
                            tmp = copy.deepcopy(item_template)
                            tmp['index'] = item_data['index']
                            tmp['status'] = item_data['status']
                            tmp['category'] = item_data['category']
                            tmp['date'] = item_data['request_date'].split('T')[0]
                            tmp['due_date'] = item_data['due_date'].split('T')[0]
                            tmp['applicant'] = item_data['requester_name']
                            tmp['uuid'] = item_data['message_id']
                            tmp['title'] = item_data['title']
                            if 'purchase_state'in item_data.keys() and item_data['purchase_state']:
                                tmp['purchase_state'] = item_data['purchase_state']
                            else:
                                tmp['purchase_state'] = 'N/A'
                            tmp['duration'] = (datetime.datetime.strptime(item_data['due_date'].split('T')[0], "%Y-%m-%d") - datetime.datetime.strptime(item_data['request_date'].split('T')[0], "%Y-%m-%d")).days
                            tmp['update_date'] = item_data['update_date'].split('T')[0]
                            data_to_render.append(tmp)
                data_to_render.sort(key=operator.itemgetter('date'),reverse=True)
                #return  HttpResponse(data_to_render)

                return render_to_response('message.html', {'data':data_to_render}, context_instance=RequestContext(request))

            return HttpResponse(json.dumps(data_to_render))
        elif request.method == 'POST':
            """
            update to db
            """
            return HttpResponse(json.dumps({"data":"post"}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def adjust_sequence(request):
    try:
        if request.method == 'POST':
            if request.user.has_perm("main.is_producer_manager"):
                data = json.loads(request.body)
                #return  HttpResponse(json.dumps(data["data"]["info"]))
                """
                save a request to the request system
                """
                post_data_dict = dict()
                post_data = request.POST
                post_data_dict["title"] = u"生产顺序调整"
                post_data_dict['message_id'] = uuid.uuid1()
                post_data_dict['approver_name'] = data["data"]["approver"]
                # backup field for CEO review
                #post_data_dict['receiver_name'] = 'N/A'
                receiver_name = ''
                for key_num in data['data']['info'].keys():
                    sample_form_sql = sample_form_model.objects.filter(message_id = data['data']['info'][key_num]['uuid'])
                    sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
                    sample_form_data = sample_form_serializer.data
                    user_sql = User.objects.filter(username = sample_form_data['belong_to'])
                    user_name = user_sql[0].last_name + user_sql[0].first_name
                    if user_name not in receiver_name:
                        receiver_name = receiver_name + user_name + ';'
                #receiver_name = list(set(receiver_name))
                post_data_dict['receiver_name'] = receiver_name

                post_data_dict['requester_name'] = request.user.last_name + request.user.first_name
                post_data_dict['status'] = 'NE'
                post_data_dict['request_date'] = str(datetime.datetime.now().strftime('%Y-%m-%d')) + 'T16:00'
                post_data_dict['content'] = ""
                post_data_dict['url'] = ""

                post_data_dict['category'] = u"生产材料"
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
                    result = adjust_sequence_sql(data)
                    if result == 'OK':
                        #return HttpResponse(json.dumps(post_data_dict))
                        request_serializer.create(post_data_dict)
                        return HttpResponse(json.dumps({'SUCCESS':'申请调序成功！'}))
                    else:
                        return  HttpResponse(json.dumps({'Error':result}))
                else:
                    #return HttpResponse(json.dumps(post_data_dict))
                    return HttpResponse(json.dumps({'Error':request_serializer.errors}))
    except:
         return HttpResponse(json.dumps({'error':traceback.format_exc()}), content_type="json")

def adjust_sequence_sql(data):
    for key_num in data['data']['info'].keys():
        sample_form_sql = sample_form_model.objects.filter(message_id = data['data']['info'][key_num]['uuid'])
        sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
        sample_form_data = sample_form_serializer.data
        if sample_form_data['sequence'] != sample_form_data['reorder']:
            return "不可进行申请调序！已有别人申请！"
    for key_num in data['data']['info'].keys():
        sample_form_sql = sample_form_model.objects.filter(message_id = data['data']['info'][key_num]['uuid'])
        sample_form_serializer = sample_form_model_serializer(sample_form_sql[0])
        sample_form_data = sample_form_serializer.data
        sample_form_data['reorder'] = int(key_num) + 1
        sample_form_serializer.update(sample_form_sql[0],sample_form_data)
    return "OK"