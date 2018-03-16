# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yuboli
#
# Created:     09/04/2016
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
from models import sample_statistics_pendai_model, sample_statistics_gunjian_model, sample_statistics_tiexin_model, setting_size_model, sample_form_model, produce_statistics_pendai_model, produce_statistics_gunjian_model, produce_statistics_tiexin_model
from produce_model import item_model
from serializers import sample_form_model_serializer
from produce_serializers import produce_statistics_pendai_model_serializer, produce_statistics_gunjian_model_serializer, produce_statistics_tiexin_model_serializer
from produce_serializers import item_model_serializer, sample_statistics_pendai_model_serializer, sample_statistics_gunjian_model_serializer, sample_statistics_tiexin_model_serializer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from purchase_models import purchase_model
from purchase_serilaizers import purchase_model_serializers

def produce_main(request, target_user=None):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                if target_user:
                    current_target_user = target_user
                else:
                    current_target_user = request.user.username

                data_to_render = {'target_user': current_target_user}
                return render_to_response('produce_main.html', {'data':data_to_render, 'target_user':target_user}, context_instance=RequestContext(request))
            else:
                return HttpResponse(json.dumps({'Error':'INVALID POST request!'}))
        else:
            return HttpResponse(json.dumps({'Error':'No permission granted'}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def produce_executive_list(request, target_user=None):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_producer_manager"):
            if request.method == 'GET':
                is_produce_manager = False
                if request.user.has_perm("main.is_producer_manager"):
                    is_produce_manager = True
                    sample_form_sqls = sample_form_model.objects.all()
                else:
                    sample_form_sqls = sample_form_model.objects.filter(producer=target_user)
                sample_form_sqls = sample_form_sqls.filter(is_sample_form = 0)

                last_7_days = datetime.date.today()-datetime.timedelta(days=7)
                very_beginning = datetime.date(1900,1,1)

                sample_form_sqls_hide = sample_form_sqls.filter(produce_status = '完成')

                sample_form_sqls_hide = sample_form_sqls_hide.filter(submit_date__range=(very_beginning,last_7_days))
                for hide_sql in sample_form_sqls_hide:
                    sample_form_serializer = sample_form_model_serializer(hide_sql)
                    data = sample_form_serializer.data
                    data['is_display'] = 0
                    sample_form_serializer.update(hide_sql,data)


                sample_form_sqls_show = sample_form_sqls.filter(is_display = 1)

                sample_form_sqls_show = sample_form_sqls_show.order_by('sequence')
                """
                序号	日期	客户名称／代号	生产单号	产品类别	数量 kg／pcs	状态	备注
                """
                category_dictionary = {'1':u'带材', '2':u'铁芯', '3':u'器件'}
                data_to_render_item = {'submit_date':'', 'is_sample_form':'', 'customer':'', 'index':'', 'category':'', 'amount':'', 'statement':'', 'message_id':'', 'sales_comment':'', 'belong_to':'', 'produce_status':''}
                data_to_render = []
                count  = 1

                approver_list = []
                user_sql = User.objects.all()
                for user in user_sql:
                    if user.has_perm('main.is_approver'):
                        approver_list.append(user.last_name + user.first_name)

                for sample_form_sql in sample_form_sqls_show:
                    sample_form_serializer = sample_form_model_serializer(sample_form_sql)
                    data = sample_form_serializer.data
                    tmp = copy.deepcopy(data_to_render_item)
                    for key in tmp.keys():
                        tmp[key] = data[key]
                    tmp['no'] = count
                    #tmp['produce_status'] = "unknown"
                    tmp['category'] = category_dictionary[tmp['category'] ]
                    count += 1
                    if(tmp['is_sample_form']==True):
                        tmp['is_sample_form'] = u'样品单'
                    else:
                        tmp['is_sample_form'] = u'生产单'
                    data_to_render.append(tmp)
                #return HttpResponse(json.dumps({'data':data_to_render, 'is_produce_manager' : is_produce_manager}))
                return render_to_response('produce_executive_list.html', {'data':data_to_render, 'is_produce_manager' : is_produce_manager, 'approver_list':approver_list, 'target_user':target_user}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def sample_executive_list(request, target_user=None):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_producer_manager"):
            if request.method == 'GET':
                is_produce_manager = False
                if request.user.has_perm("main.is_producer_manager"):
                    is_produce_manager = True
                    sample_form_sqls = sample_form_model.objects.all()
                else:
                    sample_form_sqls = sample_form_model.objects.filter(producer=target_user)
                sample_form_sqls = sample_form_sqls.filter(is_sample_form = 1)

                last_7_days = datetime.date.today()-datetime.timedelta(days=7)
                very_beginning = datetime.date(1900,1,1)

                sample_form_sqls_hide = sample_form_sqls.filter(produce_status = '完成')

                sample_form_sqls_hide = sample_form_sqls_hide.filter(submit_date__range=(very_beginning,last_7_days))
                for hide_sql in sample_form_sqls_hide:
                    sample_form_serializer = sample_form_model_serializer(hide_sql)
                    data = sample_form_serializer.data
                    data['is_display'] = 0
                    sample_form_serializer.update(hide_sql,data)


                sample_form_sqls_show = sample_form_sqls.filter(is_display = 1)

                sample_form_sqls_show = sample_form_sqls_show.order_by('sequence')
                """
                序号	日期	客户名称／代号	生产单号	产品类别	数量 kg／pcs	状态	备注
                """
                category_dictionary = {'1':u'带材', '2':u'铁芯', '3':u'器件'}
                data_to_render_item = {'submit_date':'', 'is_sample_form':'', 'customer':'', 'index':'', 'category':'', 'amount':'', 'statement':'', 'message_id':'', 'sales_comment':'', 'belong_to':'', 'produce_status':''}
                data_to_render = []
                count  = 1

                approver_list = []
                user_sql = User.objects.all()
                for user in user_sql:
                    if user.has_perm('main.is_approver'):
                        approver_list.append(user.last_name + user.first_name)

                for sample_form_sql in sample_form_sqls_show:
                    sample_form_serializer = sample_form_model_serializer(sample_form_sql)
                    data = sample_form_serializer.data
                    tmp = copy.deepcopy(data_to_render_item)
                    for key in tmp.keys():
                        tmp[key] = data[key]
                    tmp['no'] = count
                    #tmp['produce_status'] = "unknown"
                    tmp['category'] = category_dictionary[tmp['category'] ]
                    count += 1
                    if(tmp['is_sample_form']==True):
                        tmp['is_sample_form'] = u'样品单'
                    else:
                        tmp['is_sample_form'] = u'生产单'
                    data_to_render.append(tmp)
                #return HttpResponse(json.dumps({'data':data_to_render, 'is_produce_manager' : is_produce_manager}))
                return render_to_response('sample_executive_list.html', {'data':data_to_render, 'is_produce_manager' : is_produce_manager, 'approver_list':approver_list, 'target_user':target_user}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def produce_statistics_list(request, target_user=None):
    """
    序号	日期	规格	班组	炉号	A级	B级	C级	D级	重量	母合金使用情况	合格率	备注
    """
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.is_special_user"):
            if request.method == 'GET':
                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_pendai_data"):
                    can_add_item_pendai = True
                else:
                    can_add_item_pendai = False

                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_gunjian_data"):
                    can_add_item_gunjian = True
                else:
                    can_add_item_gunjian = False

                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_tiexin_data"):
                    can_add_item_tiexin = True
                else:
                    can_add_item_tiexin = False
                """
              pendai
              """
                selected_pendai_table = produce_statistics_pendai_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.order_by("-produce_date")
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=produce_statistics_pendai_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_class': serializer_data["item_class"],
                                 'item_container': serializer_data["item_container"],
                                 'item_A': serializer_data["item_A"],
                                 'item_B': serializer_data["item_B"],
                                 'item_C': serializer_data["item_C"],
                                 'item_D': serializer_data["item_D"],
                                 'item_weight': round(float(serializer_data["item_weight"]),4),
                                 'item_usage': round(float(serializer_data["item_usage"]),4),
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_pendai.append(iter_data)

                '''
                data_to_render_pendai=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2,'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.7, 'item_comment' : 'fine!'},
                {'no' : 3,'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.5, 'item_comment' : 'bad!'},]
                '''
                """
                gunjian
                """
                selected_gunjian_table = produce_statistics_gunjian_model.objects.filter(isLatest = 1)
                selected_gunjian_table = selected_gunjian_table.filter(b_display=1)
                selected_gunjian_table = selected_gunjian_table.order_by("-produce_date")
                data_to_render_gunjian = []
                for i in range(0, len(selected_gunjian_table)):
                    serializer=produce_statistics_gunjian_model_serializer(selected_gunjian_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_staff': serializer_data["item_staff"],
                                 'item_machine': serializer_data["item_machine"],
                                 'item_pass': round(float(serializer_data["item_pass"]),4),
                                 'item_fail': round(float(serializer_data["item_fail"]),4),
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_gunjian.append(iter_data)
                '''
                data_to_render_gunjian=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.7, 'item_comment' : 'good!'},
                {'no' : 3, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.4, 'item_comment' : 'good!'},]
                '''
                """
                tiexin
                """
                selected_tiexin_table = produce_statistics_tiexin_model.objects.filter(isLatest = 1)
                selected_tiexin_table = selected_tiexin_table.filter(b_display=1)
                selected_tiexin_table = selected_tiexin_table.order_by("-produce_date")
                data_to_render_tiexin = []
                for i in range(0, len(selected_tiexin_table)):
                    serializer=produce_statistics_tiexin_model_serializer(selected_tiexin_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_staff': serializer_data["item_staff"],
                                 'item_material': serializer_data["item_material"],
                                 'item_amount': round(float(serializer_data["item_amount"]),4),
                                 'item_pass': round(float(serializer_data["item_pass"]),4),
                                # 'item_fail': serializer_data["item_fail"],
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_tiexin.append(iter_data)
                '''
                data_to_render_tiexin=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024, 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024,'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.7, 'item_comment' : 'good!'},
                {'no' : 3, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024, 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.4, 'item_comment' : 'good!'},]
                '''
                return render_to_response('produce_statistics_list.html',
                {'data_pendai':data_to_render_pendai, 'can_add_item_pendai': can_add_item_pendai,
                'data_gunjian':data_to_render_gunjian, 'can_add_item_gunjian': can_add_item_gunjian,
                'data_texin':data_to_render_tiexin, 'can_add_item_texin': can_add_item_tiexin, 'target_user':target_user}, context_instance=RequestContext(request))
            else:
                return HttpResponse(json.dumps({'Error':'INVALID POST request!'}))
        else:
            return HttpResponse(json.dumps({'Error':'No permission granted'}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def sample_statistics_list(request, target_user=None):
    """
    序号	日期	规格	班组	炉号	A级	B级	C级	D级	重量	母合金使用情况	合格率	备注
    """
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.is_special_user"):
            if request.method == 'GET':
                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_pendai_data"):
                    can_add_item_pendai = True
                else:
                    can_add_item_pendai = False

                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_gunjian_data"):
                    can_add_item_gunjian = True
                else:
                    can_add_item_gunjian = False

                if request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.add_tiexin_data"):
                    can_add_item_tiexin = True
                else:
                    can_add_item_tiexin = False
                """
              pendai
              """
                selected_pendai_table = sample_statistics_pendai_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.order_by("-produce_date")
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=sample_statistics_pendai_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_class': serializer_data["item_class"],
                                 'item_container': serializer_data["item_container"],
                                 'item_A': serializer_data["item_A"],
                                 'item_B': serializer_data["item_B"],
                                 'item_C': serializer_data["item_C"],
                                 'item_D': serializer_data["item_D"],
                                 'item_weight': round(float(serializer_data["item_weight"]),4),
                                 'item_usage': round(float(serializer_data["item_usage"]),4),
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_pendai.append(iter_data)

                '''
                data_to_render_pendai=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2,'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.7, 'item_comment' : 'fine!'},
                {'no' : 3,'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_class':'a', 'item_container' : 'lu1', 'item_A' : 0,
                'item_B' : 1,'item_C' : 3,'item_D' : 5, 'item_weight' : 9, 'item_usage' : 10, 'item_rate': 0.5, 'item_comment' : 'bad!'},]
                '''
                """
                gunjian
                """
                selected_gunjian_table = sample_statistics_gunjian_model.objects.filter(isLatest = 1)
                selected_gunjian_table = selected_gunjian_table.filter(b_display=1)
                selected_gunjian_table = selected_gunjian_table.order_by("-produce_date")
                data_to_render_gunjian = []
                for i in range(0, len(selected_gunjian_table)):
                    serializer=sample_statistics_gunjian_model_serializer(selected_gunjian_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_staff': serializer_data["item_staff"],
                                 'item_machine': serializer_data["item_machine"],
                                 'item_pass': round(float(serializer_data["item_pass"]),4),
                                 'item_fail': round(float(serializer_data["item_fail"]),4),
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_gunjian.append(iter_data)
                '''
                data_to_render_gunjian=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.7, 'item_comment' : 'good!'},
                {'no' : 3, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_machine':'b', 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.4, 'item_comment' : 'good!'},]
                '''
                """
                tiexin
                """
                selected_tiexin_table = sample_statistics_tiexin_model.objects.filter(isLatest = 1)
                selected_tiexin_table = selected_tiexin_table.filter(b_display=1)
                selected_tiexin_table = selected_tiexin_table.order_by("-produce_date")
                data_to_render_tiexin = []
                for i in range(0, len(selected_tiexin_table)):
                    serializer=sample_statistics_tiexin_model_serializer(selected_tiexin_table[i])
                    serializer_data = serializer.data
                    iter_data = {'no': i+1,
                                 'item_id': serializer_data['item_id'],
                                 'item_uuid': serializer_data['uuid'],
                                 'produce_date': serializer_data["produce_date"],
                                 'item_size': serializer_data["item_size"],
                                 'item_staff': serializer_data["item_staff"],
                                 'item_material': serializer_data["item_material"],
                                 'item_amount': round(float(serializer_data["item_amount"]),4),
                                 'item_pass': round(float(serializer_data["item_pass"]),4),
                                # 'item_fail': serializer_data["item_fail"],
                                 'item_rate': round(float(serializer_data["item_rate"]),4),
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_tiexin.append(iter_data)
                '''
                data_to_render_tiexin=[
                {'no' : 1, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024, 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.9, 'item_comment' : 'good!'},
                {'no' : 2, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024,'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.7, 'item_comment' : 'good!'},
                {'no' : 3, 'item_id' :'uuid1', 'produce_date' : '2015-03-04', 'item_size':'a*b*c', 'item_staff':'a','item_material':'b','item_amount':1024, 'item_pass' : 9, 'item_fail' : 1, 'item_rate': 0.4, 'item_comment' : 'good!'},]
                '''
                return render_to_response('sample_statistics_list.html',
                {'data_pendai':data_to_render_pendai, 'can_add_item_pendai': can_add_item_pendai,
                'data_gunjian':data_to_render_gunjian, 'can_add_item_gunjian': can_add_item_gunjian,
                'data_texin':data_to_render_tiexin, 'can_add_item_texin': can_add_item_tiexin, 'target_user':target_user}, context_instance=RequestContext(request))
            else:
                return HttpResponse(json.dumps({'Error':'INVALID POST request!'}))
        else:
            return HttpResponse(json.dumps({'Error':'No permission granted'}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def produce_statistics_pendai(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':

                    if not form_uuid:
                        '''
                    add a new form
                     '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('produce_statistics_pendai.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = produce_statistics_pendai_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_pendai_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                    else:
                        '''
                    query from SQL
                    '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_pendai_table = produce_statistics_pendai_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_pendai_model_serializer(selected_pendai_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            #return HttpResponse("No such id: " + data_to_render['item_buyNo'])
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = ''
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        data_to_render['item_pass_weight'] = float(data_to_render['item_A'])+float(data_to_render['item_B'])+float(data_to_render['item_C'])
                        try:
                            data_to_render['item_muhejin_rate'] = float(data_to_render['item_weight'])/float(data_to_render['item_usage'])
                        except:
                            data_to_render['item_muhejin_rate'] = 'N/A'

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)


                        return render_to_response('produce_statistics_pendai.html', {'data':data_to_render, 'purchase_No_html':purchase_No_html,'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_pendai_table = produce_statistics_pendai_model.objects.filter(uuid = request.POST.get("uuid"))
                    if len(selected_pendai_table) == 1 and selected_pendai_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")
                    # When adding a new form
                    if len(selected_pendai_table) < 1:
                        isvalid = submit_produce_statistics_pendai_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_pendai_table) == 1:
                        serializer=produce_statistics_pendai_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_pendai_table[0],content)
                        isvalid = submit_produce_statistics_pendai_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:
                            content['isLatest'] = 1
                            serializer.update(selected_pendai_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")

            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_produce_statistics_pendai_table(request, type, content=None):
    try:
        q = produce_statistics_pendai_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = produce_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = ''
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_class = request.POST.get('item_class')
        q.item_container = request.POST.get('item_container')
        #if q.item_container == '':
        #    return "请填写 炉号！"
        q.item_A = request.POST.get('item_A')
        q.item_B = request.POST.get('item_B')
        q.item_C = request.POST.get('item_C')
        q.item_D = request.POST.get('item_D')
        q.item_weight = request.POST.get('item_weight')
        try:
            float(q.item_weight)
        except:
            return "请填写有效的 重量（数字、小数）！"
        q.item_usage = request.POST.get('item_usage')

        q.item_goback_usage = request.POST.get('item_goback_usage')
        q.item_new_usage = request.POST.get('item_new_usage')
        q.item_londerful_usage = request.POST.get('item_londerful_usage')

        try:
            float(q.item_usage)
        except:
            return "请填写有效的 母合金使用情况（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        #return HttpResponse(json.dumps(request.POST))

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '1'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_class')
        q2.item_weight = request.POST.get('item_weight')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.is_stored = '0'
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_container')

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def produce_statistics_gunjian(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    if not form_uuid:
                        '''
                        add a new form
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('produce_statistics_gunjian.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = produce_statistics_gunjian_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_gunjian_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                    else:
                        '''
                        query from SQL
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_gunjian_table = produce_statistics_gunjian_model.objects.filter(uuid = form_uuid)
                        if len(selected_gunjian_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_gunjian_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_gunjian_model_serializer(selected_gunjian_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            return HttpResponse("未找到对应生产单号" + data_to_render['item_buyNo'])
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)

                        return render_to_response('produce_statistics_gunjian.html', {'data':data_to_render, 'purchase_No_html':purchase_No_html, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_gunjian_table = produce_statistics_gunjian_model.objects.filter(uuid = request.POST.get("uuid"))
                    # When adding a new form
                    if len(selected_gunjian_table) == 1 and selected_gunjian_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")

                    if len(selected_gunjian_table) < 1:
                        isvalid = submit_produce_statistics_gunjian_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_gunjian_table) == 1:

                        serializer=produce_statistics_gunjian_model_serializer(selected_gunjian_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_gunjian_table[0],content)
                        isvalid = submit_produce_statistics_gunjian_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:

                            content['isLatest'] = 1
                            serializer.update(selected_gunjian_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_produce_statistics_gunjian_table(request, type, content=None):
    try:
        q = produce_statistics_gunjian_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = produce_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = request.POST.get('item_buyNo')
        index_sql = sample_form_model.objects.filter(index = q.item_buyNo)
        if len(index_sql)<1:
            return "请填写有效的 生产单号！（生产单号不存在）"
        else:
            serializer=sample_form_model_serializer(index_sql[0])
            data_index_sql = serializer.data
            if data_index_sql['category'] != '1':
                return "请填写有效的 生产单号！（产品类型不符）"
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_staff = request.POST.get('item_staff')
        q.item_machine = request.POST.get('item_machine')
        #if q.item_machine == '':
        #    return "请填写 机器号！"
        q.item_pass = request.POST.get('item_pass')
        try:
            float(q.item_pass)
        except:
            return "请填写有效的 合格（数字、小数）！"
        q.item_fail = request.POST.get('item_fail')
        try:
            float(q.item_fail)
        except:
            return "请填写有效的 不合格（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        try:
            float(q.item_rate)
        except:
            return "请填写有效的 合格率（数字、小数）！"
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '3'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_staff')
        q2.item_weight = request.POST.get('item_pass')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.item_warning = ''
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_machine')

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def produce_statistics_tiexin(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    if not form_uuid:
                        '''
                        add a new form
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('produce_statistics_tiexin.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = produce_statistics_tiexin_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_tiexin_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                    else:
                        '''
                        query from SQL
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_tiexin_table = produce_statistics_tiexin_model.objects.filter(uuid = form_uuid)
                        if len(selected_tiexin_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_tiexin_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=produce_statistics_tiexin_model_serializer(selected_tiexin_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            return HttpResponse("未找到对应生产单号" + data_to_render['item_buyNo'])
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)

                        return render_to_response('produce_statistics_tiexin.html', {'data':data_to_render,  'purchase_No_html':purchase_No_html, 'target_user':target_user,'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_tiexin_table = produce_statistics_tiexin_model.objects.filter(uuid = request.POST.get("uuid"))
                    if len(selected_tiexin_table) == 1 and selected_tiexin_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")
                    # When adding a new form
                    if len(selected_tiexin_table) < 1:
                        isvalid = submit_produce_statistics_tiexin_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_tiexin_table) == 1:
                        serializer=produce_statistics_tiexin_model_serializer(selected_tiexin_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_tiexin_table[0],content)
                        isvalid = submit_produce_statistics_tiexin_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/produce_statistics_list/{}'.format(target_user))
                        else:
                            content['isLatest'] = 1
                            serializer.update(selected_tiexin_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_produce_statistics_tiexin_table(request, type, content=None):
    try:
        q = produce_statistics_tiexin_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = produce_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = produce_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = produce_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = request.POST.get('item_buyNo')
        index_sql = sample_form_model.objects.filter(index = q.item_buyNo)
        if len(index_sql)<1:
            return "请填写有效的 生产单号！（生产单号不存在）"
        else:
            serializer=sample_form_model_serializer(index_sql[0])
            data_index_sql = serializer.data
            if data_index_sql['category'] != '2':
                return "请填写有效的 生产单号！（产品类型不符）"
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_staff = request.POST.get('item_staff')
        q.item_material = request.POST.get('item_material')
        q.item_amount = request.POST.get('item_amount')
        try:
            float(q.item_amount)
        except:
            return "请填写有效的 数量（数字、小数）！"
        q.item_pass = request.POST.get('item_pass')
        try:
            float(q.item_pass)
        except:
            return "请填写有效的 合格（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        try:
            float(q.item_rate)
        except:
            return "请填写有效的 合格率（数字、小数）！"
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '2'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_staff')
        q2.item_weight = request.POST.get('item_pass')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.item_warning = ''
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_material')

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")



def sample_statistics_pendai(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':

                    if not form_uuid:
                        '''
                        add a new form
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('sample_statistics_pendai.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = sample_statistics_pendai_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_pendai_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                    else:
                        '''
                        query from SQL
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_pendai_table = sample_statistics_pendai_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_pendai_model_serializer(selected_pendai_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            #return HttpResponse("No such id: " + data_to_render['item_buyNo'])
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = ''
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        data_to_render['item_pass_weight'] = float(data_to_render['item_A'])+float(data_to_render['item_B'])+float(data_to_render['item_C'])
                        try:
                            data_to_render['item_muhejin_rate'] = float(data_to_render['item_weight'])/float(data_to_render['item_usage'])
                        except:
                            data_to_render['item_muhejin_rate'] = 'N/A'

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)


                        return render_to_response('sample_statistics_pendai.html', {'data':data_to_render, 'purchase_No_html':purchase_No_html,'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_pendai_table = sample_statistics_pendai_model.objects.filter(uuid = request.POST.get("uuid"))
                    if len(selected_pendai_table) == 1 and selected_pendai_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")
                    # When adding a new form
                    if len(selected_pendai_table) < 1:
                        isvalid = submit_sample_statistics_pendai_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_pendai_table) == 1:
                        serializer=sample_statistics_pendai_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_pendai_table[0],content)
                        isvalid = submit_sample_statistics_pendai_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:
                            content['isLatest'] = 1
                            serializer.update(selected_pendai_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")

            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_sample_statistics_pendai_table(request, type, content=None):
    try:
        q = sample_statistics_pendai_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = sample_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = sample_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = sample_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = ''
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_class = request.POST.get('item_class')
        q.item_container = request.POST.get('item_container')
        #if q.item_container == '':
        #    return "请填写 炉号！"
        q.item_A = request.POST.get('item_A')
        q.item_B = request.POST.get('item_B')
        q.item_C = request.POST.get('item_C')
        q.item_D = request.POST.get('item_D')
        q.item_weight = request.POST.get('item_weight')
        try:
            float(q.item_weight)
        except:
            return "请填写有效的 重量（数字、小数）！"
        q.item_usage = request.POST.get('item_usage')
        try:
            float(q.item_usage)
        except:
            return "请填写有效的 母合金使用情况（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        #return HttpResponse(json.dumps(request.POST))

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '1'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_class')
        q2.item_weight = request.POST.get('item_weight')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.is_stored = '0'
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_container')
        q2.is_sample_form = 1

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def sample_statistics_gunjian(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    if not form_uuid:
                        '''
                        add a new form
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('sample_statistics_gunjian.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = sample_statistics_gunjian_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_gunjian_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                    else:
                        '''
                        query from SQL
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_gunjian_table = sample_statistics_gunjian_model.objects.filter(uuid = form_uuid)
                        if len(selected_gunjian_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_gunjian_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_gunjian_model_serializer(selected_gunjian_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            return HttpResponse("未找到对应生产单号" + data_to_render['item_buyNo'])
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)

                        return render_to_response('sample_statistics_gunjian.html', {'data':data_to_render, 'purchase_No_html':purchase_No_html, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_gunjian_table = sample_statistics_gunjian_model.objects.filter(uuid = request.POST.get("uuid"))
                    # When adding a new form
                    if len(selected_gunjian_table) == 1 and selected_gunjian_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")

                    if len(selected_gunjian_table) < 1:
                        isvalid = submit_sample_statistics_gunjian_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_gunjian_table) == 1:

                        serializer=sample_statistics_gunjian_model_serializer(selected_gunjian_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_gunjian_table[0],content)
                        isvalid = submit_sample_statistics_gunjian_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:

                            content['isLatest'] = 1
                            serializer.update(selected_gunjian_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_sample_statistics_gunjian_table(request, type, content=None):
    try:
        q = sample_statistics_gunjian_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = sample_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = sample_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = sample_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = request.POST.get('item_buyNo')
        index_sql = sample_form_model.objects.filter(index = q.item_buyNo)
        if len(index_sql)<1:
            return "请填写有效的 生产单号！（生产单号不存在）"
        else:
            serializer=sample_form_model_serializer(index_sql[0])
            data_index_sql = serializer.data
            if data_index_sql['category'] != '1':
                return "请填写有效的 生产单号！（产品类型不符）"
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_staff = request.POST.get('item_staff')
        q.item_machine = request.POST.get('item_machine')
        #if q.item_machine == '':
        #    return "请填写 机器号！"
        q.item_pass = request.POST.get('item_pass')
        try:
            float(q.item_pass)
        except:
            return "请填写有效的 合格（数字、小数）！"
        q.item_fail = request.POST.get('item_fail')
        try:
            float(q.item_fail)
        except:
            return "请填写有效的 不合格（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        try:
            float(q.item_rate)
        except:
            return "请填写有效的 合格率（数字、小数）！"
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '3'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_staff')
        q2.item_weight = request.POST.get('item_pass')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.item_warning = ''
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_machine')
        q2.is_sample_form = 1

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def sample_statistics_tiexin(request, form_uuid=None, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    if not form_uuid:
                        '''
                        add a new form
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                        data_to_render = {}
                        data_to_render['uuid'] = uuid.uuid1()
                        data_to_render['target_user'] = request.user.username
                        data_to_render['produce_uuid'] = 'None'
                        return render_to_response('sample_statistics_tiexin.html', {'data':data_to_render, 'target_user':target_user, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                    elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete':
                        selected_pendai_table = sample_statistics_tiexin_model.objects.filter(uuid = form_uuid)
                        if len(selected_pendai_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_pendai_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_tiexin_model_serializer(selected_pendai_table[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_pendai_table[0],content)
                        selected_item_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
                        if len(selected_item_sql) > 1:
                            return HttpResponse("storage item uuid conflict!")
                        elif len(selected_item_sql) < 1:
                            return HttpResponse("storage item uuid not found!")
                        serializer=item_model_serializer(selected_item_sql[0])
                        content = serializer.data
                        content['b_display'] = '0'
                        serializer.update(selected_item_sql[0],content)
                        return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                    else:
                        '''
                        query from SQL
                        '''
                        setting_size_sql = setting_size_model.objects.all()
                        setting_size_unit_list = ['未找到'] + [i.size_name for i in setting_size_sql]
                        selected_tiexin_table = sample_statistics_tiexin_model.objects.filter(uuid = form_uuid)
                        if len(selected_tiexin_table) > 1:
                            return HttpResponse("uuid conflict!")
                        elif len(selected_tiexin_table) < 1:
                            return HttpResponse("uuid not found!")
                        serializer=sample_statistics_tiexin_model_serializer(selected_tiexin_table[0])
                        data_to_render = serializer.data

                        selected_sample_form_sql = sample_form_model.objects.filter(index = data_to_render['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            return HttpResponse("未找到对应生产单号" + data_to_render['item_buyNo'])
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            data_to_render['target_user'] = request.user.username
                            data_to_render['produce_uuid'] = content['message_id']

                        purchase_Nos = data_to_render['purchase_Nos']
                        if purchase_Nos != None and purchase_Nos != '':
                            purchase_No_list = purchase_Nos.split(';')
                        else:
                            purchase_No_list = []
                            data_to_render['purchase_Nos'] = ''
                        purchase_No_html = []
                        for i in range(0,len(purchase_No_list)):
                            CG_sql = purchase_model.objects.filter(purchase_index=purchase_No_list[i])
                            CG_sql = CG_sql.filter(b_display=1)
                            if(len(CG_sql)==1):
                                serializer=purchase_model_serializers(CG_sql[0])
                                serializer_data = serializer.data
                                purchase_uuid = serializer_data['purchase_id']
                            elif(len(CG_sql)==0):
                                purchase_uuid = 'no-such-uuid'
                            else:
                                purchase_uuid = 'too-much-such-uuid'
                            iter_purchase_No = {
                                    'purchase_No': purchase_No_list[i],
                                    'purchase_uuid': purchase_uuid,
                                }
                            purchase_No_html.append(iter_purchase_No)

                        return render_to_response('sample_statistics_tiexin.html', {'data':data_to_render,  'purchase_No_html':purchase_No_html, 'target_user':target_user,'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
                elif request.method == 'POST':
                    selected_tiexin_table = sample_statistics_tiexin_model.objects.filter(uuid = request.POST.get("uuid"))
                    if len(selected_tiexin_table) == 1 and selected_tiexin_table[0].isLatest==0:
                        return HttpResponse("网页已过期，请返回主页！")
                    # When adding a new form
                    if len(selected_tiexin_table) < 1:
                        isvalid = submit_sample_statistics_tiexin_table(request, 'add')
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:
                            return HttpResponse(isvalid)
                    # When update an existing form
                    elif len(selected_tiexin_table) == 1:
                        serializer=sample_statistics_tiexin_model_serializer(selected_tiexin_table[0])
                        content = serializer.data
                        content['isLatest'] = 0
                        serializer.update(selected_tiexin_table[0],content)
                        isvalid = submit_sample_statistics_tiexin_table(request, 'update', content)
                        if isvalid == "OK":
                            return HttpResponseRedirect('/ERP/sample_statistics_list/{}'.format(target_user))
                        else:
                            content['isLatest'] = 1
                            serializer.update(selected_tiexin_table[0],content)
                            return HttpResponse(isvalid)
                    else:
                        return HttpResponse("Error, too much this uuid!")
            else:
                return HttpResponse("您不具有 生产 权限！")
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def submit_sample_statistics_tiexin_table(request, type, content=None):
    try:
        q = sample_statistics_tiexin_model()
        #
        q.item_id = request.POST.get('item_id')
        item_id_sql = sample_statistics_pendai_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql = item_id_sql.filter(b_display=1)
        item_id_sql = item_id_sql.filter(isLatest=1)
        item_id_sql2 = sample_statistics_gunjian_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql2 = item_id_sql2.filter(b_display=1)
        item_id_sql2 = item_id_sql2.filter(isLatest=1)
        item_id_sql3 = sample_statistics_tiexin_model.objects.filter(item_id=request.POST.get('item_id'))
        item_id_sql3 = item_id_sql3.filter(b_display=1)
        item_id_sql3 = item_id_sql3.filter(isLatest=1)
        if ((len(item_id_sql)+len(item_id_sql2)+len(item_id_sql3))>0):
            return "生产批次不唯一，与之前填写的生产批次号重复，请重新填写！（点击后退按钮返回）"
        q.item_buyNo = request.POST.get('item_buyNo')
        index_sql = sample_form_model.objects.filter(index = q.item_buyNo)
        if len(index_sql)<1:
            return "请填写有效的 生产单号！（生产单号不存在）"
        else:
            serializer=sample_form_model_serializer(index_sql[0])
            data_index_sql = serializer.data
            if data_index_sql['category'] != '2':
                return "请填写有效的 生产单号！（产品类型不符）"
        q.produce_date = request.POST.get('produce_date')
        q.item_size = request.POST.get('item_size')
        q.item_staff = request.POST.get('item_staff')
        q.item_material = request.POST.get('item_material')
        q.item_amount = request.POST.get('item_amount')
        try:
            float(q.item_amount)
        except:
            return "请填写有效的 数量（数字、小数）！"
        q.item_pass = request.POST.get('item_pass')
        try:
            float(q.item_pass)
        except:
            return "请填写有效的 合格（数字、小数）！"
        q.item_rate = request.POST.get('item_rate')
        try:
            float(q.item_rate)
        except:
            return "请填写有效的 合格率（数字、小数）！"
        q.item_comment = request.POST.get('item_comment')
        q.purchase_Nos = request.POST.get('purchase_Nos')

        q.isLatest = 1

        q2 = item_model()
        #
        q2.item_id = request.POST.get('item_id')
        q2.item_category = '2'
        q2.produce_date = request.POST.get('produce_date')
        q2.item_buyNo = request.POST.get('item_buyNo')
        q2.item_level = ''
        q2.item_size = request.POST.get('item_size')
        q2.item_class = request.POST.get('item_staff')
        q2.item_weight = request.POST.get('item_pass')
        q2.item_sale_weight = '0'
        q2.item_inventory = '0'
        q2.item_sale_link = ''
        q2.item_warning = ''
        q2.item_comment = request.POST.get('item_comment')
        q2.item_container = request.POST.get('item_material')
        q2.is_sample_form = 1

        q2.uuid = uuid.uuid1()
        q2.isLatest = 1

        q.storage_item_uuid = q2.uuid
        if type == 'add':
            q.uuid = request.POST.get('uuid')
        elif type == 'update':
            q.uuid = uuid.uuid1()
            storage_item_uuid_sql = item_model.objects.filter(uuid = content['storage_item_uuid'])
            serializer=item_model_serializer(storage_item_uuid_sql[0])
            data_storage_item_uuid_sql = serializer.data
            data_storage_item_uuid_sql['isLatest'] = 0
            serializer.update(storage_item_uuid_sql[0],data_storage_item_uuid_sql)
        else:
            return  "No such type!"
        q2.produce_uuid = q.uuid
        q.save()
        q2.save()
        return "OK"
    except Exception, e:
        return HttpResponse(json.dumps({"error_msg":str(traceback.format_exc())}), content_type="json")

def produce_storage_mudai(request):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '1')
                selected_pendai_table = selected_pendai_table.order_by("-produce_date")
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    iter_data = {'item_no': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'item_size': serializer_data['item_size'],
                                 'item_amount': serializer_data["item_weight"],
                                 'item_cut_size': 'what?',
                                 'item_update_date': serializer_data["last_revise_date"],
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_pendai.append(iter_data)
                return render_to_response('produce_storage_item.html', {'data':data_to_render_pendai, 'storage_type':u"母带"}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                return HttpResponse(json.dumps({'data':request.POST}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def produce_storage_chengpin(request):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                selected_guanjian_table = item_model.objects.filter(isLatest = 1)
                selected_guanjian_table = selected_guanjian_table.filter(item_category = '3')
                selected_guanjian_table = selected_guanjian_table.order_by("-produce_date")
                data_to_render_guanjian = []
                for i in range(0, len(selected_guanjian_table)):
                    serializer=item_model_serializer(selected_guanjian_table[i])
                    serializer_data = serializer.data
                    iter_data = {'item_no': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'item_size': serializer_data['item_size'],
                                 'item_amount': serializer_data["item_weight"],
                                 'item_cut_size': 'what?',
                                 'item_update_date': serializer_data["last_revise_date"],
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_guanjian.append(iter_data)
                return render_to_response('produce_storage_item.html', {'data':data_to_render_guanjian, 'storage_type':u"成品"}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                return HttpResponse(json.dumps({'data':request.POST}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def produce_storage_texin(request):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                selected_tiexin_table = item_model.objects.filter(isLatest = 1)
                selected_tiexin_table = selected_tiexin_table.filter(item_category = '2')
                selected_tiexin_table = selected_tiexin_table.order_by("-produce_date")
                data_to_render_tiexin = []
                for i in range(0, len(selected_tiexin_table)):
                    serializer=item_model_serializer(selected_tiexin_table[i])
                    serializer_data = serializer.data
                    iter_data = {'item_no': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'item_size': serializer_data['item_size'],
                                 'item_amount': serializer_data["item_weight"],
                                 'item_cut_size': 'what?',
                                 'item_update_date': serializer_data["last_revise_date"],
                                 'item_comment': serializer_data["item_comment"],
                                 }
                    data_to_render_tiexin.append(iter_data)
                return render_to_response('produce_storage_item.html', {'data':data_to_render_tiexin, 'storage_type':u"铁芯"}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                return HttpResponse(json.dumps({'data':request.POST}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def produce_storage_mudai_hejin(request):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                data_to_render = [
                {'source_size' : 1, 'source_supplier':'aa', 'source_amount':40,  'source_update_date':'2015-03-04', 'source_comment':'bad!'},
                {'source_size' : 2, 'source_supplier':'ab', 'source_amount':70,  'source_update_date':'2015-03-04', 'source_comment':'fine!'},
                {'source_size' : 3, 'source_supplier':'ac', 'source_amount':90,  'source_update_date':'2015-03-04', 'source_comment':'good!'},]
                return render_to_response('produce_storage_source.html', {'data':data_to_render, 'storage_type':u"母带合金"}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                return HttpResponse(json.dumps({'data':request.POST}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def produce_storage_huhe(request):
    try:
        if request.user.has_perm("main.is_producer") or  request.user.has_perm("main.is_produce_manager"):
            if request.method == 'GET':
                data_to_render = [
                {'source_size' : 1, 'source_supplier':'aa', 'source_amount':40,  'source_update_date':'2015-03-04', 'source_comment':'bad!'},
                {'source_size' : 2, 'source_supplier':'ab', 'source_amount':70,  'source_update_date':'2015-03-04', 'source_comment':'fine!'},
                {'source_size' : 3, 'source_supplier':'ac', 'source_amount':90,  'source_update_date':'2015-03-04', 'source_comment':'good!'},]
                return render_to_response('produce_storage_source.html', {'data':data_to_render, 'storage_type':u"护盒"}, context_instance=RequestContext(request))
            elif request.method == 'POST':
                return HttpResponse(json.dumps({'data':request.POST}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def produce_chart(request, category):
    map_dict = {"pendai":u"喷带", "gunjian": u"辊剪", "tiexin":u"铁芯"}
    map_dict2 = {"pendai":'1', "gunjian": '2', "tiexin":'3'}
    try:
         if request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    data_to_render = {}
                    data_to_render['category'] = category
                    data_to_render['category_name'] = map_dict[category]
                    data_to_render['selected'] = u"所有"
                    data_to_render['selected_banzu'] = u"所有"
                    data_to_render['selected_guige'] = u"所有"
                    if category == 'pendai':
                        selected_table = produce_statistics_pendai_model.objects.filter(isLatest = 1)
                    elif category == 'gunjian':
                        selected_table = produce_statistics_gunjian_model.objects.filter(isLatest = 1)
                    elif category == 'tiexin':
                        selected_table = produce_statistics_tiexin_model.objects.filter(isLatest = 1)
                    else:
                        return  HttpResponse('未找到该类别！')
                    selected_table = selected_table.filter(b_display = 1)
                    banzu_str = ''
                    banzu = []
                    guige_str = ''
                    guige = []
                    it = []
                    for i in range(0, len(selected_table)):
                        if category == 'pendai':
                            serializer=produce_statistics_pendai_model_serializer(selected_table[i])
                        elif category == 'gunjian':
                            serializer=produce_statistics_gunjian_model_serializer(selected_table[i])
                        elif category == 'tiexin':
                            serializer=produce_statistics_tiexin_model_serializer(selected_table[i])
                        serializer_data = serializer.data
                        if category == 'pendai':
                            ''' 按班组 '''
                            if serializer_data['item_class']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_class']+';'
                                banzu.append(serializer_data['item_class'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = ['A', 'B', 'C', 'D', u'总重量']
                        elif category == 'gunjian' or category =='tiexin':
                            ''' 按班组 '''
                            if serializer_data['item_staff']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_staff']+';'
                                banzu.append(serializer_data['item_staff'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = [u'合格', u'总量']

                    startDate= str(datetime.date.today() - datetime.timedelta(days=365))
                    endDate = str(datetime.date.today())
                    data_to_render['date_start'] = startDate
                    data_to_render['date_end'] = endDate

                    monthList = []
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
                    data_to_render['date_range'] = json.dumps(monthList)

                    salesAmountByMonth = {}
                    data_list = []
                    for tag in it:
                        salesAmountByMonth[tag] = []
                        monthList = []
                        ''' 按班组
                        if category == 'pendai':
                            selected_tag = selected_table.filter(item_class = tag)
                        elif category == 'gunjian' or category == 'tiexin':
                            selected_tag = selected_table.filter(item_staff = tag)
                        '''
                        for ym in range(startYM,endYM+1):
                            chooseYear = int((ym - 1) / 12)
                            chooseMonth = ym % 12
                            if (chooseMonth == 0):
                                chooseMonth = 12
                            monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                            ''' 按班组
                            selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                            selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                            '''
                            selectedYear = selected_table.filter(produce_date__year = chooseYear)
                            selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth[tag].append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    if category == 'pendai':
                                        serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                    elif category == 'gunjian':
                                        serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                    elif category == 'tiexin':
                                        serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        if category == 'pendai':
                                            ''' 按班组
                                            produceAmount = float(serializer_data["item_weight"])
                                            '''
                                            tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                            produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                        elif category == 'gunjian':
                                            '''按班组
                                            produceAmount = float(serializer_data["item_pass"])
                                            '''
                                            if tag == u'合格':
                                                produceAmount = float(serializer_data['item_pass'])
                                            else:
                                                produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                        else:
                                            '''按班组
                                            produceAmount = float(serializer_data["item_pass"])
                                            '''
                                            tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                            produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                    except:
                                        produceAmount = 0
                                    data_per_month = data_per_month + produceAmount
                                    data_per_month = round(data_per_month,3)
                                salesAmountByMonth[tag].append(data_per_month)
                        data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                    data_to_render['data_list'] = data_list

                    it.append(u'所有')
                    banzu.sort()
                    banzu.append(u'所有')
                    guige.sort()
                    guige.append(u'所有')
                    data_to_render['it'] = it
                    data_to_render['banzu'] = banzu
                    data_to_render['guige'] = guige
                    '''
                    data_to_render = {"category" : category, "it":[u"班组A", u"班组B", u"班组C", u"班组D", u"所有"], "category_name":map_dict[category],
                    "selected": u"所有",'date_start':'2015-01-01', 'date_end':'2015-05-01',
                    'date_range' : json.dumps(['2015/1', '2015/2', '2015/3', '2015/4','2015/5']),
                    'data_list':[
                        {'tag':'班组A', 'data' :[10.1,20.2,40.5, 20.3, 92.1]},
                        {'tag':'班组B', 'data' :[56.1,50.2,30.5, 63.3, 22.1]},
                        {'tag':'班组C', 'data' :[10.1,20.2,35.5, 40.3, 52.1]},
                        {'tag':'班组D', 'data' :[15.1,10.2,45.5, 20.3, 32.1]},
                    ]}
                    '''
                    return render_to_response('produce_chart_common.html', {'data':data_to_render}, context_instance=RequestContext(request))

                elif request.method == 'POST':
                    data_to_render = {}
                    data_to_render['category'] = category
                    data_to_render['category_name'] = map_dict[category]
                    data_to_render['selected'] = request.POST.get('selection')
                    data_to_render['selected_banzu'] = request.POST.get('selection_banzu')
                    data_to_render['selected_guige'] = request.POST.get('selection_guige')
                    if category == 'pendai':
                        selected_table = produce_statistics_pendai_model.objects.filter(isLatest = 1)
                    elif category == 'gunjian':
                        selected_table = produce_statistics_gunjian_model.objects.filter(isLatest = 1)
                    elif category == 'tiexin':
                        selected_table = produce_statistics_tiexin_model.objects.filter(isLatest = 1)
                    else:
                        return  HttpResponse('未找到该类别！')
                    selected_table = selected_table.filter(b_display = 1)

                    banzu_str = ''
                    banzu =[]
                    guige_str = ''
                    guige =[]
                    it = []
                    for i in range(0, len(selected_table)):
                        if category == 'pendai':
                            serializer=produce_statistics_pendai_model_serializer(selected_table[i])
                        elif category == 'gunjian':
                            serializer=produce_statistics_gunjian_model_serializer(selected_table[i])
                        elif category == 'tiexin':
                            serializer=produce_statistics_tiexin_model_serializer(selected_table[i])
                        serializer_data = serializer.data
                        if category == 'pendai':
                            ''' 按班组 '''
                            if serializer_data['item_class']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_class']+';'
                                banzu.append(serializer_data['item_class'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = ['A', 'B', 'C', 'D', u'总重量']
                        elif category == 'gunjian' or category =='tiexin':
                            ''' 按班组 '''
                            if serializer_data['item_staff']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_staff']+';'
                                banzu.append(serializer_data['item_staff'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = [u'合格', u'总量']

                    startDate= request.POST.get('startDate')
                    endDate = request.POST.get('endDate')
                    data_to_render['date_start'] = startDate
                    data_to_render['date_end'] = endDate

                    monthList = []
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
                    data_to_render['date_range'] = json.dumps(monthList)

                    salesAmountByMonth = {}
                    data_list = []

                    ''' 按班组 '''

                    if data_to_render['selected_banzu'] != u'所有':
                        if category == 'pendai':
                            selected_banzu = selected_table.filter(item_class = data_to_render['selected_banzu'])
                        elif category == 'gunjian' or category == 'tiexin':
                            selected_banzu = selected_table.filter(item_staff = data_to_render['selected_banzu'])
                    else:
                        selected_banzu = selected_table
                    # filter guige
                    if data_to_render['selected_guige'] != u'所有':
                        selected_banzu = selected_banzu.filter(item_size = data_to_render['selected_guige'])
                    else:
                        selected_banzu = selected_banzu

                    if data_to_render['selected'] == u'所有':
                        for tag in it:
                            salesAmountByMonth[tag] = []
                            monthList = []
                            ''' 按班组
                            if category == 'pendai':
                                selected_tag = selected_table.filter(item_class = tag)
                            elif category == 'gunjian' or category == 'tiexin':
                                selected_tag = selected_table.filter(item_staff = tag)
                        '''
                            for ym in range(startYM,endYM+1):
                                chooseYear = int((ym - 1) / 12)
                                chooseMonth = ym % 12
                                if (chooseMonth == 0):
                                    chooseMonth = 12
                                monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                                ''' 按班组
                                selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                '''
                                selectedYear = selected_banzu.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                if len(selectedMonth) < 1:
                                    salesAmountByMonth[tag].append(0)
                                else:
                                    data_per_month = 0
                                    for i in range(0, len(selectedMonth)):
                                        if category == 'pendai':
                                            serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                        elif category == 'gunjian':
                                            serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                        elif category == 'tiexin':
                                            serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                        serializer_data = serializer.data
                                        try:
                                            if category == 'pendai':
                                                ''' 按班组
                                                produceAmount = float(serializer_data["item_weight"])
                                                '''
                                                tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                                produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                            elif category == 'gunjian':
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                if tag == '合格':
                                                    produceAmount = float(serializer_data['item_pass'])
                                                else:
                                                    produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                            else:
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                                produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                        except:
                                            produceAmount = 0
                                        data_per_month = data_per_month + produceAmount
                                        data_per_month = round(data_per_month,2)
                                    salesAmountByMonth[tag].append(data_per_month)
                            data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                        data_to_render['data_list'] = data_list
                    else:
                            tag = data_to_render['selected']
                            salesAmountByMonth[tag] = []
                            monthList = []
                            ''' 按班组
                            if category == 'pendai':
                                selected_tag = selected_table.filter(item_class = tag)
                            elif category == 'gunjian' or category == 'tiexin':
                                selected_tag = selected_table.filter(item_staff = tag)
                            '''
                            for ym in range(startYM,endYM+1):
                                chooseYear = int((ym - 1) / 12)
                                chooseMonth = ym % 12
                                if (chooseMonth == 0):
                                    chooseMonth = 12
                                monthList.append(str(chooseYear)+"."+monthDic[chooseMonth])
                                ''' 按班组
                                selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                '''
                                selectedYear = selected_banzu.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                if len(selectedMonth) < 1:
                                    salesAmountByMonth[tag].append(0)
                                else:
                                    data_per_month = 0
                                    for i in range(0, len(selectedMonth)):
                                        if category == 'pendai':
                                            serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                        elif category == 'gunjian':
                                            serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                        elif category == 'tiexin':
                                            serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                        serializer_data = serializer.data
                                        try:
                                            if category == 'pendai':
                                                ''' 按班组
                                                produceAmount = float(serializer_data["item_weight"])
                                                '''
                                                tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                                produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                            elif category == 'gunjian':
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                if tag == u'合格':
                                                    produceAmount = float(serializer_data['item_pass'])
                                                else:
                                                    produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                            else:
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                                produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                        except:
                                            produceAmount = 0
                                        data_per_month = data_per_month + produceAmount
                                        data_per_month = round(data_per_month,2)
                                    salesAmountByMonth[tag].append(data_per_month)
                            data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                            data_to_render['data_list'] = data_list

                    it.append(u'所有')
                    banzu.sort()
                    banzu.append(u'所有')
                    guige.sort()
                    guige.append(u'所有')
                    data_to_render['it'] = it
                    data_to_render['banzu'] = banzu
                    data_to_render['guige'] = guige
                    '''
                    data_to_render = {"category" : category, "it":[u"班组A", u"班组B", u"班组C", u"班组D", u"所有"], "category_name":map_dict[category],
                    "selected": u"所有",'date_start':'2015-01-01', 'date_end':'2015-05-01',
                    'date_range' : json.dumps(['2015/1', '2015/2', '2015/3', '2015/4','2015/5']),
                    'data_list':[
                        {'tag':'班组A', 'data' :[10.1,20.2,40.5, 20.3, 92.1]},
                        {'tag':'班组B', 'data' :[56.1,50.2,30.5, 63.3, 22.1]},
                        {'tag':'班组C', 'data' :[10.1,20.2,35.5, 40.3, 52.1]},
                        {'tag':'班组D', 'data' :[15.1,10.2,45.5, 20.3, 32.1]},
                    ]}
                    '''
                    return render_to_response('produce_chart_common.html', {'data':data_to_render}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def produce_chart_day(request, category):
    map_dict = {"pendai":u"喷带", "gunjian": u"辊剪", "tiexin":u"铁芯"}
    map_dict2 = {"pendai":'1', "gunjian": '2', "tiexin":'3'}
    try:
         if request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager"):
                if request.method == 'GET':
                    data_to_render = {}
                    data_to_render['category'] = category
                    data_to_render['category_name'] = map_dict[category]
                    data_to_render['selected'] = u"所有"
                    data_to_render['selected_banzu'] = u"所有"
                    data_to_render['selected_guige'] = u"所有"
                    if category == 'pendai':
                        selected_table = produce_statistics_pendai_model.objects.filter(isLatest = 1)
                    elif category == 'gunjian':
                        selected_table = produce_statistics_gunjian_model.objects.filter(isLatest = 1)
                    elif category == 'tiexin':
                        selected_table = produce_statistics_tiexin_model.objects.filter(isLatest = 1)
                    else:
                        return  HttpResponse('未找到该类别！')
                    selected_table = selected_table.filter(b_display = 1)
                    banzu_str = ''
                    banzu =[]
                    guige_str = ''
                    guige =[]
                    it = []
                    for i in range(0, len(selected_table)):
                        if category == 'pendai':
                            serializer=produce_statistics_pendai_model_serializer(selected_table[i])
                        elif category == 'gunjian':
                            serializer=produce_statistics_gunjian_model_serializer(selected_table[i])
                        elif category == 'tiexin':
                            serializer=produce_statistics_tiexin_model_serializer(selected_table[i])
                        serializer_data = serializer.data
                        if category == 'pendai':
                            ''' 按班组 '''
                            if serializer_data['item_class']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_class']+';'
                                banzu.append(serializer_data['item_class'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = ['A', 'B', 'C', 'D', u'总重量']
                        elif category == 'gunjian' or category =='tiexin':
                            ''' 按班组 '''
                            if serializer_data['item_staff']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_staff']+';'
                                banzu.append(serializer_data['item_staff'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = [u'合格', u'总量']

                    startDate = str(datetime.date.today())
                    startYear = startDate[0:4]
                    startMonth = startDate[5:7]
                    data_to_render['date_start'] = startDate

                    if startMonth+',' in '01,03,05,07,08,10,12':
                        monthList = [i+1 for i in range(31)]
                    elif startMonth+',' in '04,06,09,11':
                        monthList = [i+1 for i in range(30)]
                    else:
                        if int(startYear)%4==0:
                            if int(startYear)%100==0:
                                if int(startYear)%400==0:
                                    monthList = [i+1 for i in range(29)]
                                else:
                                    monthList = [i+1 for i in range(28)]
                            else:
                                monthList = [i+1 for i in range(29)]
                        else:
                            monthList = [i+1 for i in range(28)]

                    data_to_render['date_range'] = json.dumps(monthList)

                    salesAmountByMonth = {}
                    data_list = []
                    for tag in it:
                        salesAmountByMonth[tag] = []
                        ''' 按班组
                        if category == 'pendai':
                            selected_tag = selected_table.filter(item_class = tag)
                        elif category == 'gunjian' or category == 'tiexin':
                            selected_tag = selected_table.filter(item_staff = tag)
                        '''
                        for plot_day in monthList:
                            ''' 按班组
                            selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                            selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                            '''
                            selectedYear = selected_table.filter(produce_date__year = startYear)
                            selectedMonth = selectedYear.filter(produce_date__month = startMonth)
                            selectedMonth = selectedMonth.filter(produce_date__day = plot_day)
                            if len(selectedMonth) < 1:
                                salesAmountByMonth[tag].append(0)
                            else:
                                data_per_month = 0
                                for i in range(0, len(selectedMonth)):
                                    if category == 'pendai':
                                        serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                    elif category == 'gunjian':
                                        serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                    elif category == 'tiexin':
                                        serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                    serializer_data = serializer.data
                                    try:
                                        if category == 'pendai':
                                            ''' 按班组
                                            produceAmount = float(serializer_data["item_weight"])
                                            '''
                                            tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                            produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                        elif category == 'gunjian':
                                            '''按班组
                                            produceAmount = float(serializer_data["item_pass"])
                                            '''
                                            if tag == '合格':
                                                produceAmount = float(serializer_data['item_pass'])
                                            else:
                                                produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                        else:
                                            '''按班组
                                            produceAmount = float(serializer_data["item_pass"])
                                            '''
                                            tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                            produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                    except:
                                        produceAmount = 0
                                    data_per_month = data_per_month + produceAmount
                                    data_per_month = round(data_per_month,3)
                                salesAmountByMonth[tag].append(data_per_month)
                        data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                    data_to_render['data_list'] = data_list

                    it.append(u'所有')
                    banzu.sort()
                    banzu.append(u'所有')
                    guige.sort()
                    guige.append(u'所有')
                    data_to_render['it'] = it
                    data_to_render['banzu'] = banzu
                    data_to_render['guige'] = guige
                    '''
                    data_to_render = {"category" : category, "it":[u"班组A", u"班组B", u"班组C", u"班组D", u"所有"], "category_name":map_dict[category],
                    "selected": u"所有",'date_start':'2015-01-01', 'date_end':'2015-05-01',
                    'date_range' : json.dumps(['2015/1', '2015/2', '2015/3', '2015/4','2015/5']),
                    'data_list':[
                        {'tag':'班组A', 'data' :[10.1,20.2,40.5, 20.3, 92.1]},
                        {'tag':'班组B', 'data' :[56.1,50.2,30.5, 63.3, 22.1]},
                        {'tag':'班组C', 'data' :[10.1,20.2,35.5, 40.3, 52.1]},
                        {'tag':'班组D', 'data' :[15.1,10.2,45.5, 20.3, 32.1]},
                    ]}
                    '''
                    return render_to_response('produce_chart_day_common.html', {'data':data_to_render}, context_instance=RequestContext(request))

                elif request.method == 'POST':
                    data_to_render = {}
                    data_to_render['category'] = category
                    data_to_render['category_name'] = map_dict[category]
                    data_to_render['selected'] = request.POST.get('selection')
                    data_to_render['selected_banzu'] = request.POST.get('selection_banzu')
                    data_to_render['selected_guige'] = request.POST.get('selection_guige')
                    if category == 'pendai':
                        selected_table = produce_statistics_pendai_model.objects.filter(isLatest = 1)
                    elif category == 'gunjian':
                        selected_table = produce_statistics_gunjian_model.objects.filter(isLatest = 1)
                    elif category == 'tiexin':
                        selected_table = produce_statistics_tiexin_model.objects.filter(isLatest = 1)
                    else:
                        return  HttpResponse('未找到该类别！')
                    selected_table = selected_table.filter(b_display = 1)

                    banzu_str = ''
                    banzu =[]
                    guige_str = ''
                    guige =[]
                    it = []
                    for i in range(0, len(selected_table)):
                        if category == 'pendai':
                            serializer=produce_statistics_pendai_model_serializer(selected_table[i])
                        elif category == 'gunjian':
                            serializer=produce_statistics_gunjian_model_serializer(selected_table[i])
                        elif category == 'tiexin':
                            serializer=produce_statistics_tiexin_model_serializer(selected_table[i])
                        serializer_data = serializer.data
                        if category == 'pendai':
                            ''' 按班组 '''
                            if serializer_data['item_class']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_class']+';'
                                banzu.append(serializer_data['item_class'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = ['A', 'B', 'C', 'D', u'总重量']
                        elif category == 'gunjian' or category =='tiexin':
                            ''' 按班组 '''
                            if serializer_data['item_staff']+';' not in banzu_str:
                                banzu_str = banzu_str + serializer_data['item_staff']+';'
                                banzu.append(serializer_data['item_staff'])
                            if serializer_data['item_size']+';' not in guige_str:
                                guige_str = guige_str + serializer_data['item_size']+';'
                                guige.append(serializer_data['item_size'])

                            it = [u'合格', u'总量']

                    startDate= request.POST.get('startDate')
                    data_to_render['date_start'] = startDate

                    startYear = startDate[0:4]
                    startMonth = startDate[5:7]

                    if startMonth+',' in '01,03,05,07,08,10,12':
                        monthList = [i+1 for i in range(31)]
                    elif startMonth+',' in '04,06,09,11':
                        monthList = [i+1 for i in range(30)]
                    else:
                        if int(startYear)%4==0:
                            if int(startYear)%100==0:
                                if int(startYear)%400==0:
                                    monthList = [i+1 for i in range(29)]
                                else:
                                    monthList = [i+1 for i in range(28)]
                            else:
                                monthList = [i+1 for i in range(29)]
                        else:
                            monthList = [i+1 for i in range(28)]

                    data_to_render['date_range'] = json.dumps(monthList)

                    salesAmountByMonth = {}
                    data_list = []

                    ''' 按班组 '''
                    if data_to_render['selected_banzu'] != u'所有':
                        if category == 'pendai':
                            selected_banzu = selected_table.filter(item_class = data_to_render['selected_banzu'])
                        elif category == 'gunjian' or category == 'tiexin':
                            selected_banzu = selected_table.filter(item_staff = data_to_render['selected_banzu'])
                    else:
                        selected_banzu = selected_table

                    # filter guige
                    if data_to_render['selected_guige'] != u'所有':
                        selected_banzu = selected_banzu.filter(item_size = data_to_render['selected_guige'])
                    else:
                        selected_banzu = selected_banzu

                    if data_to_render['selected'] == u'所有':
                        for tag in it:
                            salesAmountByMonth[tag] = []
                            ''' 按班组
                            if category == 'pendai':
                                selected_tag = selected_table.filter(item_class = tag)
                            elif category == 'gunjian' or category == 'tiexin':
                                selected_tag = selected_table.filter(item_staff = tag)
                            '''
                            for plot_day in monthList:

                                ''' 按班组
                                selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                '''
                                selectedYear = selected_banzu.filter(produce_date__year = startYear)
                                selectedMonth = selectedYear.filter(produce_date__month = startMonth)
                                selectedMonth = selectedMonth.filter(produce_date__day = plot_day)
                                if len(selectedMonth) < 1:
                                    salesAmountByMonth[tag].append(0)
                                else:
                                    data_per_month = 0
                                    for i in range(0, len(selectedMonth)):
                                        if category == 'pendai':
                                            serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                        elif category == 'gunjian':
                                            serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                        elif category == 'tiexin':
                                            serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                        serializer_data = serializer.data
                                        try:
                                            if category == 'pendai':
                                                ''' 按班组
                                                produceAmount = float(serializer_data["item_weight"])
                                                '''
                                                tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                                produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                            elif category == 'gunjian':
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                if tag == '合格':
                                                    produceAmount = float(serializer_data['item_pass'])
                                                else:
                                                    produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                            else:
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                                produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                        except:
                                            produceAmount = 0
                                        data_per_month = data_per_month + produceAmount
                                        data_per_month = round(data_per_month,2)
                                    salesAmountByMonth[tag].append(data_per_month)
                            data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                        data_to_render['data_list'] = data_list
                    else:
                            tag = data_to_render['selected']
                            salesAmountByMonth[tag] = []
                            ''' 按班组
                            if category == 'pendai':
                                selected_tag = selected_table.filter(item_class = tag)
                            elif category == 'gunjian' or category == 'tiexin':
                                selected_tag = selected_table.filter(item_staff = tag)
                            '''
                            for plot_day in monthList:
                                ''' 按班组
                                selectedYear = selected_tag.filter(produce_date__year = chooseYear)
                                selectedMonth = selectedYear.filter(produce_date__month = chooseMonth)
                                '''
                                selectedYear = selected_banzu.filter(produce_date__year = startYear)
                                selectedMonth = selectedYear.filter(produce_date__month = startMonth)
                                selectedMonth = selectedMonth.filter(produce_date__day = plot_day)
                                if len(selectedMonth) < 1:
                                    salesAmountByMonth[tag].append(0)
                                else:
                                    data_per_month = 0
                                    for i in range(0, len(selectedMonth)):
                                        if category == 'pendai':
                                            serializer=produce_statistics_pendai_model_serializer(selectedMonth[i])
                                        elif category == 'gunjian':
                                            serializer=produce_statistics_gunjian_model_serializer(selectedMonth[i])
                                        elif category == 'tiexin':
                                            serializer=produce_statistics_tiexin_model_serializer(selectedMonth[i])
                                        serializer_data = serializer.data
                                        try:
                                            if category == 'pendai':
                                                ''' 按班组
                                                produceAmount = float(serializer_data["item_weight"])
                                                '''
                                                tagDic_pendai ={'A':'item_A', 'B':'item_B', 'C':'item_C', 'D':'item_D', u'总重量':'item_weight'}
                                                produceAmount = float(serializer_data[tagDic_pendai[tag]])
                                            elif category == 'gunjian':
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                if tag == u'合格':
                                                    produceAmount = float(serializer_data['item_pass'])
                                                else:
                                                    produceAmount = float(serializer_data['item_pass']) + float(serializer_data['item_fail'])
                                            else:
                                                '''按班组
                                                produceAmount = float(serializer_data["item_pass"])
                                                '''
                                                tagDic_tiexin ={u'合格':'item_pass', u'总量':'item_amount'}
                                                produceAmount = float(serializer_data[tagDic_tiexin[tag]])
                                        except:
                                            produceAmount = 0
                                        data_per_month = data_per_month + produceAmount
                                        data_per_month = round(data_per_month,2)
                                    salesAmountByMonth[tag].append(data_per_month)
                            data_list.append({'tag':tag,'data':salesAmountByMonth[tag]})
                            data_to_render['data_list'] = data_list

                    it.append(u'所有')
                    banzu.sort()
                    banzu.append(u'所有')
                    guige.sort()
                    guige.append(u'所有')
                    data_to_render['it'] = it
                    data_to_render['banzu'] = banzu
                    data_to_render['guige'] = guige
                    '''
                    data_to_render = {"category" : category, "it":[u"班组A", u"班组B", u"班组C", u"班组D", u"所有"], "category_name":map_dict[category],
                    "selected": u"所有",'date_start':'2015-01-01', 'date_end':'2015-05-01',
                    'date_range' : json.dumps(['2015/1', '2015/2', '2015/3', '2015/4','2015/5']),
                    'data_list':[
                        {'tag':'班组A', 'data' :[10.1,20.2,40.5, 20.3, 92.1]},
                        {'tag':'班组B', 'data' :[56.1,50.2,30.5, 63.3, 22.1]},
                        {'tag':'班组C', 'data' :[10.1,20.2,35.5, 40.3, 52.1]},
                        {'tag':'班组D', 'data' :[15.1,10.2,45.5, 20.3, 32.1]},
                    ]}
                    '''
                    return render_to_response('produce_chart_day_common.html', {'data':data_to_render}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))