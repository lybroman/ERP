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
from models import sample_form_model, check_model, capital_model, storage_delivery_model, storage_product_out_model, storage_source_out_model, warning_threshold_model
from serializers import sample_form_model_serializer, warning_threshold_model_serializer
from storage_standalone_serialization import capital_model_serializer, check_model_serializer, storage_product_out_serializers, storage_source_out_serializers
from storage_delivery_serializers import storageDeliverySerializers
from django.contrib.auth.models import User
from produce_model import item_model
from produce_serializers import item_model_serializer
import uuid as UUID
from django.utils import timezone
import datetime
from purchase_models import purchase_model
from purchase_serilaizers import purchase_model_serializers
from models import salesStatisticstable
from serializers import salesStatisticstableSerializer
from django.http import HttpResponseRedirect
from urllib import unquote
from models import setting_size_model
def storage_main(request, target_user=None):
    try:
        if request.user.has_perm("main.is_storage") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                if target_user:
                    current_target_user = target_user
                else:
                    current_target_user = request.user.username

                data_to_render = {'target_user': current_target_user}
                return render_to_response('storage_main.html', {'data':data_to_render, 'target_user':target_user}, context_instance=RequestContext(request))
            else:
                return HttpResponse(json.dumps({'Error':'INVALID POST request!'}))
        else:
            return HttpResponse(json.dumps({'Error':'No permission granted'}))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_source(request, category=None):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                source_dictionary = {u'母合金':1, u'耐火材料':2, u'辅助材料':3, u'护盒':4, u'五金电器':5}
                selected_source_table = purchase_model.objects.filter(b_display = 1)
                selected_source_table = selected_source_table.filter(is_stored=1)
                selected_source_table = selected_source_table.filter(purchase_category = source_dictionary[category])
                size_name_str = ''
                size_list = {}
                data_to_render = []
                for i in range(0, len(selected_source_table)):
                    serializer=purchase_model_serializers(selected_source_table[i])
                    serializer_data = serializer.data
                    serializer_data['size']=serializer_data['size'].strip()
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['supplier'] = serializer_data["supplier"]
                        size_list[size_name]['inventory'] = float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = serializer_data["purchase_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['warning'] = '待设置'
                    else:
                        size_name = serializer_data['size']
                        if serializer_data["supplier"] not in size_list[size_name]['supplier']:
                            size_list[size_name]['supplier'] += '; '+serializer_data["supplier"]
                        size_list[size_name]['inventory'] += float(serializer_data["amount"])
                        if serializer_data["purchase_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["purchase_date"]


                '''
                出库
                '''
                selected_source_table = storage_source_out_model.objects.filter(b_display = '1')
                selected_source_table = selected_source_table.filter(category = source_dictionary[category])
                for i in range(0, len(selected_source_table)):
                    serializer=storage_source_out_serializers(selected_source_table[i])
                    serializer_data = serializer.data
                    serializer_data['item']=serializer_data['item'].strip()
                    if (';'+serializer_data['item']+';') not in size_name_str:
                        size_name = serializer_data['item']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['supplier'] = '暂无'
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['warning'] = '待设置'
                    else:
                        size_name = serializer_data['item']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                #return HttpResponse(size_name_str)
                threshold_model_data_all = warning_threshold_model.objects.all()
                i = 0
                for sizes in size_list.keys():
                    threshold_model_data = threshold_model_data_all.filter(size=sizes)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                        warning_color = 0
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                        try:
                            if size_list[sizes]['inventory'] > float(warning):
                                warning_color = 1
                            else:
                                warning_color = 0
                        except:
                            warning_color = 0
                    else:
                        warning = '多条同名信息，请核实'
                        warning_color = 0
                    iter_data = {'No': i+1,
                                 'name': sizes,
                                 'supplier': size_list[sizes]['supplier'],
                                 'inventory': size_list[sizes]['inventory'],
                                 'last_buy_date': size_list[sizes]['last_buy_date'],
                                 'late_use_date': size_list[sizes]['late_use_date'],
                                 'warning': warning,
                                 'warning_color': warning_color,
                                 #'warning': size_list[sizes]['warning'],
                                 }
                    data_to_render.append(iter_data)
                    i += 1

                return render_to_response('storage_source.html', {'data':data_to_render, 'source_name':category}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_source_name(request, category=None, target_size=None):
    try:
        if request.user.has_perm("main.is_storage") or  request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                if 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_in':
                    #return HttpResponse(request.GET['uuid'])
                    selected_table = purchase_model.objects.filter(purchase_id = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=purchase_model_serializers(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_out':
                    selected_table = storage_source_out_model.objects.filter(delivery_id = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=storage_source_out_serializers(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)


                source_dictionary = {u'母合金':1, u'耐火材料':2, u'辅助材料':3, u'护盒':4, u'五金电器':5}
                selected_source_table = purchase_model.objects.filter(b_display = 1)
                selected_source_table = selected_source_table.filter(is_stored=1)
                selected_source_table = selected_source_table.filter(purchase_category = source_dictionary[category])
                selected_source_table = selected_source_table.filter(size = target_size)
                data_to_render_pendai = []
                amount = 0
                total_price = 0
                for i in range(0, len(selected_source_table)):
                    serializer=purchase_model_serializers(selected_source_table[i])
                    serializer_data = serializer.data
                    iter_data = {'index': i+1,
                                 'item_id': serializer_data['purchase_id'],
                                 'category': category,
                                 'size': serializer_data['size'],
                                 'item_size': serializer_data['purchase_name'],
                                 'date': serializer_data['purchase_date'],
                                 'buyNo': serializer_data['storage_no'],
                                 'supplier': serializer_data["supplier"],
                                 'price': serializer_data["unit_price"],
                                 'number': serializer_data["amount"],
                                 'total_price': serializer_data["total_price"],
                                  'uuid': serializer_data["purchase_id"],
                                 }
                    amount += float(serializer_data["amount"])
                    total_price += float(serializer_data["total_price"])
                    data_to_render_pendai.append(iter_data)
                sum_data = {'index':'总计采购','category':'总计采购','number':amount,'total_price':total_price}
                data_to_render_pendai.append(sum_data)
                '''
                出库
                '''
                product_out_model_data = storage_source_out_model.objects.filter(b_display='1')
                product_out_model_data = product_out_model_data.filter(item = target_size)
                data_out_to_render = []
                amount = 0
                product_out_model_data = product_out_model_data.filter(category = source_dictionary[category])
                for i in range(0, len(product_out_model_data)):
                     serializer=storage_source_out_serializers(product_out_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'index': i+1,
                                  'category': category,
                                 'size': serializer_data['item'],
                                  'item_size': serializer_data['item_size'],
                                 'date': serializer_data['update_date'],
                                 'outNo': serializer_data['No'],
                                 'reason': serializer_data['reason'],
                                 'department': serializer_data['department'],
                                 'user': serializer_data['user'],
                                  'amount': serializer_data['amount'],
                                 'comment': serializer_data['comment'],
                                  'uuid': serializer_data['delivery_id'],
                                 }
                     amount += float(serializer_data['amount'])
                     data_out_to_render.append(iter_data)
                sum_data = {'index':'总计出库','category':'总计出库','amount':amount}
                data_out_to_render.append(sum_data)
                return render_to_response('storage_source_name.html', {'data':data_to_render_pendai, 'data_out':data_out_to_render, 'item_category':category, 'item_class':target_size}, context_instance=RequestContext(request))


    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_mudai(request):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '1')
                data_to_render_pendai = []
                size_name_str = ''
                size_list = {}
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['item_size']+';') not in size_name_str:
                        size_name = serializer_data['item_size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = float(serializer_data["item_weight"])
                        size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['category'] = '母带'
                    else:
                        size_name = serializer_data['item_size']
                        size_list[size_name]['inventory'] += float(serializer_data["item_weight"])
                        if serializer_data["produce_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                '''
                出库
                '''
                selected_pendai_table = storage_product_out_model.objects.filter(b_display = '1')
                selected_pendai_table = selected_pendai_table.filter(category = '1')
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=storage_product_out_serializers(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['category'] = '母带'
                    else:
                        size_name = serializer_data['size']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                i = 0
                threshold_model_data_all = warning_threshold_model.objects.all()
                for sizes in size_list.keys():
                    fullname=size_list[sizes]['category'].decode('utf-8')+sizes
                    threshold_model_data = threshold_model_data_all.filter(size=fullname)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                        warning_color = 0
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                        try:
                            if size_list[sizes]['inventory'] > float(warning):
                                warning_color = 1
                            else:
                                warning_color = 0
                        except:
                            warning_color = 0
                    else:
                        warning = '多条同名信息，请核实'
                        warning_color = 0
                    iter_data = {'No': i+1,
                                 'name': sizes,
                                 'inventory': size_list[sizes]['inventory'],
                                 'last_buy_date': size_list[sizes]['last_buy_date'],
                                 'late_use_date': size_list[sizes]['late_use_date'],
                                 'warning': warning,
                                 'warning_color': warning_color,
                                 }
                    data_to_render_pendai.append(iter_data)
                    i += 1

                return render_to_response('storage_item.html', {'data':data_to_render_pendai, 'item_name':u"母带", 'url':'mudai'}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_gunjian(request):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '3')
                data_to_render_pendai = []
                size_name_str = ''
                size_list = {}
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['item_size']+';') not in size_name_str:
                        size_name = serializer_data['item_size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = float(serializer_data["item_weight"])
                        size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['category'] = '辊剪'
                    else:
                        size_name = serializer_data['item_size']
                        size_list[size_name]['inventory'] += float(serializer_data["item_weight"])
                        if serializer_data["produce_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                '''
                出库
                '''
                selected_pendai_table = storage_product_out_model.objects.filter(b_display = '1')
                selected_pendai_table = selected_pendai_table.filter(category = '3')
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=storage_product_out_serializers(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['category'] = '辊剪'
                    else:
                        size_name = serializer_data['size']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                i = 0
                threshold_model_data_all = warning_threshold_model.objects.all()
                for sizes in size_list.keys():
                    fullname=size_list[sizes]['category'].decode('utf-8')+sizes
                    threshold_model_data = threshold_model_data_all.filter(size=fullname)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                        warning_color = 0
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                        try:
                            if size_list[sizes]['inventory'] > float(warning):
                                warning_color = 1
                            else:
                                warning_color = 0
                        except:
                            warning_color = 0
                    else:
                        warning = '多条同名信息，请核实'
                        warning_color = 0
                    iter_data = {'No': i+1,
                                 'name': sizes,
                                 'inventory': size_list[sizes]['inventory'],
                                 'last_buy_date': size_list[sizes]['last_buy_date'],
                                 'late_use_date': size_list[sizes]['late_use_date'],
                                 'warning': warning,
                                 'warning_color': warning_color,
                                 }
                    data_to_render_pendai.append(iter_data)
                    i += 1

                return render_to_response('storage_item.html', {'data':data_to_render_pendai, 'item_name':u"辊剪", 'url':'gunjian'}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_tiexin(request):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or   request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '2')
                data_to_render_pendai = []
                size_name_str = ''
                size_list = {}
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['item_size']+';') not in size_name_str:
                        size_name = serializer_data['item_size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = float(serializer_data["item_weight"])
                        size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['category'] = '铁芯'
                    else:
                        size_name = serializer_data['item_size']
                        size_list[size_name]['inventory'] += float(serializer_data["item_weight"])
                        if serializer_data["produce_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                '''
                出库
                '''
                selected_pendai_table = storage_product_out_model.objects.filter(b_display = '1')
                selected_pendai_table = selected_pendai_table.filter(category = '2')
                data_to_render_pendai = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=storage_product_out_serializers(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['category'] = '铁芯'
                    else:
                        size_name = serializer_data['size']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                i = 0
                threshold_model_data_all = warning_threshold_model.objects.all()
                for sizes in size_list.keys():
                    fullname=size_list[sizes]['category'].decode('utf-8')+sizes
                    threshold_model_data = threshold_model_data_all.filter(size=fullname)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                        warning_color = 0
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                        try:
                            if size_list[sizes]['inventory'] > float(warning):
                                warning_color = 1
                            else:
                                warning_color = 0
                        except:
                            warning_color = 0
                    else:
                        warning = '多条同名信息，请核实'
                        warning_color = 0
                    iter_data = {'No': i+1,
                                 'name': sizes,
                                 'inventory': size_list[sizes]['inventory'],
                                 'last_buy_date': size_list[sizes]['last_buy_date'],
                                 'late_use_date': size_list[sizes]['late_use_date'],
                                 'warning': warning,
                                 'warning_color': warning_color,
                                 }
                    data_to_render_pendai.append(iter_data)
                    i += 1

                return render_to_response('storage_item.html', {'data':data_to_render_pendai, 'item_name':u"铁芯", 'url':'tiexin'}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_name_mudai(request, target_size=None):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':
                if 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_in':
                    #return HttpResponse(request.GET['uuid'])
                    selected_table = item_model.objects.filter(uuid = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=item_model_serializer(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_out':
                    selected_table = storage_product_out_model.objects.filter(delivery_id = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=storage_product_out_serializers(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '1')
                selected_pendai_table = selected_pendai_table.filter(item_size = target_size)
                data_to_render_pendai = []
                amount = 0
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    selected_sample_form_sql = sample_form_model.objects.filter(index = serializer_data["item_buyNo"])
                    if len(selected_sample_form_sql) == 0:
                        itembuyNo = "未找到源生产单号"
                        target_user = "None"
                        produce_uuid = "None"
                    else:
                        sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                        content = sample_form_serializer.data
                        itembuyNo = serializer_data["item_buyNo"]
                        target_user = content['belong_to']
                        produce_uuid = content['message_id']
                    iter_data = {'No': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'category': category_dictionary[serializer_data['item_category']],
                                 'size': serializer_data['item_size'],
                                 'date': serializer_data['produce_date'],
                                 'buyNo': itembuyNo,
                                 'produceNo': serializer_data["item_id"],
                                 'class': serializer_data["item_class"],
                                 'container': serializer_data["item_container"],
                                 'weight': serializer_data["item_weight"],
                                 'comment': serializer_data["item_comment"],
                                 'target_user': target_user,
                                 'produce_uuid': produce_uuid,
                                 'uuid':  serializer_data["uuid"],
                                 }
                    amount += float(serializer_data["item_weight"])
                    data_to_render_pendai.append(iter_data)
                sum_data = {'No':'总计生产','item_id':'-','category':'-','size':'-','date':'-','buyNo':'-','class':'-',
                             'container':'-','weight':amount,'comment':'-','target_user':'-','produce_uuid':'-'}
                data_to_render_pendai.append(sum_data)
                '''
                出库
                '''
                product_out_model_data = storage_product_out_model.objects.filter(b_display='1')
                product_out_model_data = product_out_model_data.filter(size = target_size)
                data_out_to_render = []
                amount = 0
                product_out_model_data = product_out_model_data.filter(category = 1)
                for i in range(0, len(product_out_model_data)):
                     serializer=storage_product_out_serializers(product_out_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'No': i+1,
                                  'category': category_dictionary[serializer_data['category']],
                                 'uuid': serializer_data['delivery_id'],
                                 'update_date': serializer_data['update_date'],
                                 'contract_No': serializer_data['contract_No'],
                                 'size': serializer_data['size'],
                                 'customer': serializer_data['customer'],
                                 'amount': serializer_data['amount'],
                                 'comment': serializer_data['comment'],
                                 }
                     amount += float(serializer_data['amount'])
                     data_out_to_render.append(iter_data)
                sum_data = {'No':'总计出库','category':'-', 'delivery_id':'-','update_date':'-','contract_No':'-','size':'-',
                             'customer':'-','amount':amount,'comment':'-'}
                data_out_to_render.append(sum_data)
                return render_to_response('storage_item_name.html', {'data':data_to_render_pendai, 'data_out':data_out_to_render, 'item_category_cn':u"母带", 'item_category':"mudai",  'item_class':target_size}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_name_gunjian(request, target_size=None):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':

                if 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_in':
                    #return HttpResponse(request.GET['uuid'])
                    selected_table = item_model.objects.filter(uuid = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=item_model_serializer(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_out':
                    selected_table = storage_product_out_model.objects.filter(delivery_id = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=storage_product_out_serializers(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '3')
                selected_pendai_table = selected_pendai_table.filter(item_size = target_size)
                data_to_render_pendai = []
                amount = 0
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    selected_sample_form_sql = sample_form_model.objects.filter(index = serializer_data["item_buyNo"])
                    if len(selected_sample_form_sql) == 0:
                        itembuyNo = "未找到源生产单号"
                        target_user = "None"
                        produce_uuid = "None"
                    else:
                        sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                        content = sample_form_serializer.data
                        itembuyNo = serializer_data["item_buyNo"]
                        target_user = content['belong_to']
                        produce_uuid = content['message_id']
                    iter_data = {'No': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'category': category_dictionary[serializer_data['item_category']],
                                 'size': serializer_data['item_size'],
                                 'date': serializer_data['produce_date'],
                                 'buyNo': itembuyNo,
                                 'produceNo': serializer_data["item_id"],
                                 'class': serializer_data["item_class"],
                                 'container': serializer_data["item_container"],
                                 'weight': serializer_data["item_weight"],
                                 'comment': serializer_data["item_comment"],
                                 'target_user': target_user,
                                 'produce_uuid': produce_uuid,
                                 'uuid': serializer_data["uuid"],
                                 }
                    amount += float(serializer_data["item_weight"])
                    data_to_render_pendai.append(iter_data)
                sum_data = {'No':'总计生产','item_id':'-','category':'-','size':'-','date':'-','buyNo':'-','class':'-',
                             'container':'-','weight':amount,'comment':'-','target_user':'-','produce_uuid':'-'}
                data_to_render_pendai.append(sum_data)
                '''
                出库
                '''
                product_out_model_data = storage_product_out_model.objects.filter(b_display='1')
                product_out_model_data = product_out_model_data.filter(size = target_size)
                data_out_to_render = []
                amount = 0
                product_out_model_data = product_out_model_data.filter(category = 3)
                for i in range(0, len(product_out_model_data)):
                     serializer=storage_product_out_serializers(product_out_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'No': i+1,
                                  'category': category_dictionary[serializer_data['category']],
                                 'uuid': serializer_data['delivery_id'],
                                 'update_date': serializer_data['update_date'],
                                 'contract_No': serializer_data['contract_No'],
                                 'size': serializer_data['size'],
                                 'customer': serializer_data['customer'],
                                 'amount': serializer_data['amount'],
                                 'comment': serializer_data['comment'],
                                 }
                     amount += float(serializer_data['amount'])
                     data_out_to_render.append(iter_data)
                sum_data = {'No':'总计出库','category':'-', 'delivery_id':'-','update_date':'-','contract_No':'-','size':'-',
                             'customer':'-','amount':amount,'comment':'-'}
                data_out_to_render.append(sum_data)
                return render_to_response('storage_item_name.html', {'data':data_to_render_pendai,'data_out':data_out_to_render,  'item_category_cn':u"辊剪", 'item_category':"gunjian",  'item_class':target_size}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_item_name_tiexin(request, target_size=None):
    try:
        if request.user.has_perm("main.is_storage") or request.user.has_perm("main.is_producer") or request.user.has_perm("main.is_produce_manager") or  request.user.has_perm("main.is_storage_manager"):
            if request.method == 'GET':

                if 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_in':
                    #return HttpResponse(request.GET['uuid'])
                    selected_table = item_model.objects.filter(uuid = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=item_model_serializer(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                elif 'operation' in request.GET.keys() and request.GET['operation'] == 'delete_out':
                    selected_table = storage_product_out_model.objects.filter(delivery_id = request.GET['uuid'])
                    if len(selected_table) > 1:
                        return HttpResponse("uuid conflict!")
                    elif len(selected_table) < 1:
                        return HttpResponse("uuid not found!")
                    serializer=storage_product_out_serializers(selected_table[0])
                    content = serializer.data
                    content['b_display'] = '0'
                    serializer.update(selected_table[0],content)
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                selected_pendai_table = selected_pendai_table.filter(b_display=1)
                selected_pendai_table = selected_pendai_table.filter(item_category = '2')
                selected_pendai_table = selected_pendai_table.filter(item_size = target_size)
                data_to_render_pendai = []
                amount = 0
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    selected_sample_form_sql = sample_form_model.objects.filter(index = serializer_data["item_buyNo"])
                    if len(selected_sample_form_sql) == 0:
                        itembuyNo = "未找到源生产单号"
                        target_user = "None"
                        produce_uuid = "None"
                    else:
                        sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                        content = sample_form_serializer.data
                        itembuyNo = serializer_data["item_buyNo"]
                        target_user = content['belong_to']
                        produce_uuid = content['message_id']
                    iter_data = {'No': i+1,
                                 'item_id': serializer_data['produce_uuid'],
                                 'category': category_dictionary[serializer_data['item_category']],
                                 'size': serializer_data['item_size'],
                                 'date': serializer_data['produce_date'],
                                 'buyNo': itembuyNo,
                                 'produceNo': serializer_data["item_id"],
                                 'class': serializer_data["item_class"],
                                 'container': serializer_data["item_container"],
                                 'weight': serializer_data["item_weight"],
                                 'comment': serializer_data["item_comment"],
                                 'target_user': target_user,
                                 'produce_uuid': produce_uuid,
                                 'uuid': serializer_data["uuid"],
                                 }
                    amount += float(serializer_data["item_weight"])
                    data_to_render_pendai.append(iter_data)
                sum_data = {'No':'总计生产','item_id':'-','category':'-','size':'-','date':'-','buyNo':'-','class':'-',
                             'container':'-','weight':amount,'comment':'-','target_user':'-','produce_uuid':'-'}
                data_to_render_pendai.append(sum_data)
                '''
                出库
                '''
                product_out_model_data = storage_product_out_model.objects.filter(b_display='1')
                product_out_model_data = product_out_model_data.filter(size = target_size)
                data_out_to_render = []
                amount = 0
                product_out_model_data = product_out_model_data.filter(category = 2)
                for i in range(0, len(product_out_model_data)):
                     serializer=storage_product_out_serializers(product_out_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'No': i+1,
                                  'category': category_dictionary[serializer_data['category']],
                                 'uuid': serializer_data['delivery_id'],
                                 'update_date': serializer_data['update_date'],
                                 'contract_No': serializer_data['contract_No'],
                                 'size': serializer_data['size'],
                                 'customer': serializer_data['customer'],
                                 'amount': serializer_data['amount'],
                                 'comment': serializer_data['comment'],
                                 }
                     amount += float(serializer_data['amount'])
                     data_out_to_render.append(iter_data)
                sum_data = {'No':'总计出库','category':'-', 'delivery_id':'-','update_date':'-','contract_No':'-','size':'-',
                             'customer':'-','amount':amount,'comment':'-'}
                data_out_to_render.append(sum_data)

                return render_to_response('storage_item_name.html', {'data':data_to_render_pendai, 'data_out':data_out_to_render,  'item_category_cn':u"铁芯", 'item_category':"tiexin",  'item_class':target_size}, context_instance=RequestContext(request))
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def storage_captial(request, target_user=None, uuid=None):
   try:
       if request.user.has_perm('main.edit_capital_info'):
           if request.method== 'GET':
                capital_model_data = capital_model.objects.filter(b_display='1')
                data_to_render = []
                for i in range(0, len(capital_model_data)):
                     serializer=capital_model_serializer(capital_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'No': i+1,
                                 'uuid': serializer_data['uuid'],
                                 'category': serializer_data['category'],
                                 'size': serializer_data["size"],
                                 'amount':serializer_data["amount"],
                                 'price': serializer_data["amount"],
                                 'total_price':serializer_data["total_price"],
                                 'last_update_time': serializer_data["last_update_time"],
                                 'place': serializer_data["place"],
                                 'comment': serializer_data["comment"]
                                 }
                     data_to_render.append(iter_data)

                return render_to_response('storage_capital_main.html', {'data':data_to_render, 'target_user':target_user}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if request.POST["operation"] == 'update' :
                    capital_model_data = capital_model.objects.filter(b_display='1', uuid=request.POST["uuid"])
                    if len(capital_model_data) != 1:
                        return HttpResponse("item not unique or not exists! please contact lybroman@hotmail.com")
                    serializer=capital_model_serializer(capital_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]

                    serializer.update(capital_model_data[0], serializer_data)
                    return HttpResponse(json.dumps({'SUCCESS':"update the capital form!"}))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    iter_data = {
                                 'uuid': str(UUID.uuid1()),
                                 'category': request.POST['category'],
                                 'size': request.POST["size"],
                                 'amount': request.POST["amount"],
                                 'price': request.POST["amount"],
                                 'total_price': request.POST["total_price"],
                                 'last_update_time': request.POST["last_update_time"],
                                 'place': request.POST["place"],
                                 'comment': request.POST["comment"],
                                 'b_display' : '1',
                                 }
                    capital_model_serializer_ser = capital_model_serializer(data=iter_data)
                    if capital_model_serializer_ser.is_valid():
                        capital_model_serializer_ser.create(iter_data)
                        return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                    else:
                        return HttpResponse(json.dumps({'Error':capital_model_serializer_ser.errors}))
       else:
           return HttpResponse("You don't have permission!")

   except:
       return HttpResponse(traceback.format_exc())


def storage_check(request, target_user=None, uuid=None):
    try:
       if request.user.has_perm('main.edit_check_info'):
           if request.method== 'GET':
                check_model_data = check_model.objects.filter(b_display='1')
                data_to_render = []
                for i in range(0, len(check_model_data)):
                     serializer=check_model_serializer(check_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'No': i+1,
                                 'uuid': serializer_data['uuid'],
                                 'staff': serializer_data['staff'],
                                 'last_update_time': serializer_data["last_update_time"],
                                 'comment': serializer_data["comment"]
                                 }
                     data_to_render.append(iter_data)
                auto_now = str(datetime.datetime.now())
                auto_now = auto_now[0:10]
                return render_to_response('storage_check_main.html', {'data':data_to_render, 'target_user':target_user, 'auto_now':auto_now}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if request.POST["operation"] == 'update' :
                    check_model_data = check_model.objects.filter(b_display='1', uuid=request.POST["uuid"])
                    if len(check_model_data) != 1:
                        return HttpResponse("item not unique or not exists! please contact lybroman@hotmail.com")
                    serializer=check_model_serializer(check_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]

                    serializer.update(check_model_data[0], serializer_data)
                    return HttpResponse(json.dumps({'SUCCESS':"update the capital form!"}))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    iter_data = {
                                'uuid': str(UUID.uuid1()),
                                 'staff': request.POST['staff'],
                                 'last_update_time':  request.POST["last_update_time"],
                                 'comment':  request.POST["comment"],
                                 'b_display' : '1',
                                 }
                    check_model_serializer_ser =check_model_serializer(data=iter_data)
                    if check_model_serializer_ser.is_valid():
                        check_model_serializer_ser.create(iter_data)
                        return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                    else:
                        return HttpResponse(json.dumps({'Error':check_model_serializer_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def storage_source_threshold(request, target_user=None):
    try:
       if request.user.has_perm('main.edit_threshold'):
           if request.method== 'GET':
                '''
                pass
                首先读取原材料页面的需要设置的数据
                '''
                selected_source_table = purchase_model.objects.filter(b_display = 1)
                selected_source_table = selected_source_table.filter(is_stored=1)
                #selected_source_table = selected_source_table.filter(purchase_category = source_dictionary[category])
                size_name_str = ''
                size_list = {}
                data_to_render = []
                for i in range(0, len(selected_source_table)):
                    serializer=purchase_model_serializers(selected_source_table[i])
                    serializer_data = serializer.data
                    serializer_data['size']=serializer_data['size'].strip()
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['supplier'] = serializer_data["supplier"]
                        size_list[size_name]['inventory'] = float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = serializer_data["purchase_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['warning'] = '待设置'
                    else:
                        size_name = serializer_data['size']
                        if serializer_data["supplier"] not in size_list[size_name]['supplier']:
                            size_list[size_name]['supplier'] += '; '+serializer_data["supplier"]
                        size_list[size_name]['inventory'] += float(serializer_data["amount"])
                        if serializer_data["purchase_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["purchase_date"]


                '''
                出库
                '''
                selected_source_table = storage_source_out_model.objects.filter(b_display = '1')
                #selected_source_table = selected_source_table.filter(category = source_dictionary[category])
                for i in range(0, len(selected_source_table)):
                    serializer=storage_source_out_serializers(selected_source_table[i])
                    serializer_data = serializer.data
                    serializer_data['item']=serializer_data['item'].strip()
                    if (';'+serializer_data['item']+';') not in size_name_str:
                        size_name = serializer_data['item']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['supplier'] = '暂无'
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['warning'] = '待设置'
                    else:
                        size_name = serializer_data['item']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                #return HttpResponse(size_name_str)
                i = 0
                threshold_model_data_all = warning_threshold_model.objects.all()
                strr=''
                for sizes in size_list.keys():
                    threshold_model_data = threshold_model_data_all.filter(size=sizes)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                    else:
                        warning = '多条同名信息，请核实'
                    iter_data = {'No': i+1,
                                 'name': sizes,
                                 'supplier': size_list[sizes]['supplier'],
                                 'inventory': size_list[sizes]['inventory'],
                                 'threshold': warning,
                                 }
                    data_to_render.append(iter_data)
                    i += 1
                '''
                显示出来并设置
                '''
                auto_now = str(datetime.datetime.now())
                auto_now = auto_now[0:10]
                return render_to_response('storage_source_threshold.html', {'data':data_to_render, 'target_user':target_user, 'auto_now':auto_now}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if request.POST["operation"] == 'update' :
                    threshold_model_data = warning_threshold_model.objects.filter(size=request.POST["name"])
                    if len(threshold_model_data) > 1:
                        return HttpResponse("多条同名信息，请核实")
                    elif len(threshold_model_data) == 1:
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        serializer_data['warning_threshold'] =  request.POST['threshold']
                        serializer.update(threshold_model_data[0], serializer_data)
                        return HttpResponseRedirect('/ERP/storage_source_threshold/{}/'.format(target_user))
                        #return HttpResponse(json.dumps({'SUCCESS':"update the capital form!"}))
                    else:
                        iter_data = {
                                    #'id': uuid.uuid1(),
                                     'size': request.POST['name'],
                                     'warning_threshold':  request.POST["threshold"],
                                     'comment': '',
                                     }
                        warning_threshold_model_serializer_ser = warning_threshold_model_serializer(data=iter_data)
                        #return HttpResponse(json.dumps(iter_data))
                        if warning_threshold_model_serializer_ser.is_valid():
                            warning_threshold_model_serializer_ser.create(iter_data)
                            return HttpResponseRedirect('/ERP/storage_source_threshold/{}/'.format(target_user))
                            #return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                        else:
                            return HttpResponse(json.dumps({'Error':warning_threshold_model_serializer_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())


def storage_item_threshold(request, target_user=None):
    try:
       if request.user.has_perm('main.edit_threshold'):
           if request.method== 'GET':
                '''
                pass
                首先读取原材料页面的需要设置的数据
                '''
                category_dict={'1':'母带','2':'铁芯','3':'辊剪'}
                selected_pendai_table = item_model.objects.filter(isLatest = 1)
                selected_pendai_table = selected_pendai_table.filter(is_stored=1)
                #selected_pendai_table = selected_pendai_table.filter(item_category = '1')
                data_to_render = []
                size_name_str = ''
                size_list = {}
                for i in range(0, len(selected_pendai_table)):
                    serializer=item_model_serializer(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['item_size']+';') not in size_name_str:
                        size_name = serializer_data['item_size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = float(serializer_data["item_weight"])
                        size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                        size_list[size_name]['late_use_date'] = '-'
                        size_list[size_name]['category'] = category_dict[serializer_data["item_category"]]
                    else:
                        size_name = serializer_data['item_size']
                        size_list[size_name]['inventory'] += float(serializer_data["item_weight"])
                        if serializer_data["produce_date"]>size_list[size_name]['last_buy_date']:
                            size_list[size_name]['last_buy_date'] = serializer_data["produce_date"]
                '''
                出库
                '''
                selected_pendai_table = storage_product_out_model.objects.filter(b_display = '1')
                #selected_pendai_table = selected_pendai_table.filter(category = '1')
                data_to_render = []
                for i in range(0, len(selected_pendai_table)):
                    serializer=storage_product_out_serializers(selected_pendai_table[i])
                    serializer_data = serializer.data
                    if (';'+serializer_data['size']+';') not in size_name_str:
                        size_name = serializer_data['size']
                        size_name_str = size_name_str + ';' + size_name + ';'
                        size_list[size_name] = {}
                        size_list[size_name]['inventory'] = -float(serializer_data["amount"])
                        size_list[size_name]['last_buy_date'] = '-'
                        size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        size_list[size_name]['category'] = category_dict[serializer_data["category"]]
                    else:
                        size_name = serializer_data['size']
                        size_list[size_name]['inventory'] -= float(serializer_data["amount"])
                        if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        if size_list[size_name]['late_use_date'] == '-':
                            size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                        else:
                            if serializer_data["update_date"]>size_list[size_name]['late_use_date']:
                                size_list[size_name]['late_use_date'] = serializer_data["update_date"]
                i = 0
                threshold_model_data_all = warning_threshold_model.objects.all()
                for sizes in size_list.keys():
                    fullname=size_list[sizes]['category'].decode('utf-8')+sizes
                    threshold_model_data = threshold_model_data_all.filter(size=fullname)
                    if(len(threshold_model_data)<1):
                        warning = 'None'
                    elif(len(threshold_model_data)==1):
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        warning = serializer_data['warning_threshold']
                    else:
                        warning = '多条同名信息，请核实'
                    iter_data = {'No': i+1,
                                 'category': size_list[sizes]['category'],
                                 'name': sizes,
                                 'inventory': size_list[sizes]['inventory'],
                                 'threshold': warning,
                                 }
                    data_to_render.append(iter_data)
                    i += 1

                auto_now = str(datetime.datetime.now())
                auto_now = auto_now[0:10]
                return render_to_response('storage_item_threshold.html', {'data':data_to_render, 'target_user':target_user, 'auto_now':auto_now}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                #return HttpResponse(json.dumps(request.POST))
                if request.POST["operation"] == 'update' :
                    threshold_model_data = warning_threshold_model.objects.filter(size=(request.POST["category"]+request.POST["name"]))
                    if len(threshold_model_data) > 1:
                        return HttpResponse("多条同名信息，请核实")
                    elif len(threshold_model_data) == 1:
                        serializer=warning_threshold_model_serializer(threshold_model_data[0])
                        serializer_data = serializer.data
                        serializer_data['warning_threshold'] =  request.POST['threshold']
                        serializer.update(threshold_model_data[0], serializer_data)
                        return HttpResponseRedirect('/ERP/storage_item_threshold/{}/'.format(target_user))
                        #return HttpResponse(json.dumps({'SUCCESS':"update the capital form!"}))
                    else:
                        iter_data = {
                                    #'id': uuid.uuid1(),
                                     'size': request.POST['category']+request.POST['name'],
                                     'warning_threshold':  request.POST["threshold"],
                                     'comment': '',
                                     }
                        warning_threshold_model_serializer_ser = warning_threshold_model_serializer(data=iter_data)
                        #return HttpResponse(json.dumps(iter_data))
                        if warning_threshold_model_serializer_ser.is_valid():
                            warning_threshold_model_serializer_ser.create(iter_data)
                            return HttpResponseRedirect('/ERP/storage_item_threshold/{}/'.format(target_user))
                            #return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                        else:
                            return HttpResponse(json.dumps({'Error':warning_threshold_model_serializer_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())


def storage_delivery(request, category=None, size=None, customer=None, target_user=None):
    try:
       if request.user.has_perm('main.add_delivery_model'):
           if request.method== 'GET':
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                delivery_model_data = storage_delivery_model.objects.filter(b_display='1')
                if size != None:
                    delivery_model_data = delivery_model_data.filter(size = size)
                if customer != None:
                    delivery_model_data = delivery_model_data.filter(customer = customer)
                data_to_render = []
                setting_size_sql = setting_size_model.objects.all()
                setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                if category == u'母带':
                    delivery_model_data = delivery_model_data.filter(category = '1')
                    for i in range(0, len(delivery_model_data)):
                         serializer=storageDeliverySerializers(delivery_model_data[i])
                         serializer_data = serializer.data
                         sales_No_uuid = ''
                         sales_statistics_form_sql = salesStatisticstable.objects.filter( No = serializer_data['sales_No'])
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(isLatest='1')
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(b_display='1')
                         if(len(sales_statistics_form_sql)==1):
                             sales_statistics_form_serializer = salesStatisticstableSerializer(sales_statistics_form_sql[0])
                             sales_No_uuid = sales_statistics_form_serializer.data['uuid']
                         elif(len(sales_statistics_form_sql)==0):
                             sales_No_uuid = 'no-such-uuid'
                         else:
                             sales_No_uuid = 'no-unique-uuid'

                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'sales_No': serializer_data['sales_No'],
                                     'sales_No_uuid': sales_No_uuid,
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'delivery_No': serializer_data['delivery_No'],
                                     'delivery_amount': serializer_data['delivery_amount'],
                                     'delivery_status': serializer_data['delivery_status'],
                                     'delivery_track_No': serializer_data['delivery_track_No'],
                                     'delivery_comment': serializer_data['delivery_comment'],
                                     }
                         data_to_render.append(iter_data)
                elif category == u'铁芯':
                    delivery_model_data = delivery_model_data.filter(category = '2')
                    for i in range(0, len(delivery_model_data)):
                         serializer=storageDeliverySerializers(delivery_model_data[i])
                         serializer_data = serializer.data
                         sales_No_uuid = ''
                         sales_statistics_form_sql = salesStatisticstable.objects.filter( No = serializer_data['sales_No'])
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(isLatest='1')
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(b_display='1')
                         if(len(sales_statistics_form_sql)==1):
                             sales_statistics_form_serializer = salesStatisticstableSerializer(sales_statistics_form_sql[0])
                             sales_No_uuid = sales_statistics_form_serializer.data['uuid']
                         elif(len(sales_statistics_form_sql)==0):
                             sales_No_uuid = 'no-such-uuid'
                         else:
                             sales_No_uuid = 'no-unique-uuid'
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'sales_No': serializer_data['sales_No'],
                                     'sales_No_uuid': sales_No_uuid,
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'delivery_No': serializer_data['delivery_No'],
                                     'delivery_amount': serializer_data['delivery_amount'],
                                     'delivery_status': serializer_data['delivery_status'],
                                     'delivery_track_No': serializer_data['delivery_track_No'],
                                     'delivery_comment': serializer_data['delivery_comment'],
                                     }
                         data_to_render.append(iter_data)
                elif category == u'辊剪':
                    delivery_model_data = delivery_model_data.filter(category = '3')
                    for i in range(0, len(delivery_model_data)):
                         serializer=storageDeliverySerializers(delivery_model_data[i])
                         serializer_data = serializer.data
                         sales_No_uuid = ''
                         sales_statistics_form_sql = salesStatisticstable.objects.filter( No = serializer_data['sales_No'])
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(isLatest='1')
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(b_display='1')
                         if(len(sales_statistics_form_sql)==1):
                             sales_statistics_form_serializer = salesStatisticstableSerializer(sales_statistics_form_sql[0])
                             sales_No_uuid = sales_statistics_form_serializer.data['uuid']
                         elif(len(sales_statistics_form_sql)==0):
                             sales_No_uuid = 'no-such-uuid'
                         else:
                             sales_No_uuid = 'no-unique-uuid'
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'sales_No': serializer_data['sales_No'],
                                     'sales_No_uuid': sales_No_uuid,
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'delivery_No': serializer_data['delivery_No'],
                                     'delivery_amount': serializer_data['delivery_amount'],
                                     'delivery_status': serializer_data['delivery_status'],
                                     'delivery_track_No': serializer_data['delivery_track_No'],
                                     'delivery_comment': serializer_data['delivery_comment'],
                                     }
                         data_to_render.append(iter_data)
                elif category == u'全部':
                    #delivery_model_data = delivery_model_data.filter(category = '1')
                    for i in range(0, len(delivery_model_data)):
                         serializer=storageDeliverySerializers(delivery_model_data[i])
                         serializer_data = serializer.data
                         sales_No_uuid = ''
                         sales_statistics_form_sql = salesStatisticstable.objects.filter( No = serializer_data['sales_No'])
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(isLatest='1')
                         sales_statistics_form_sql = sales_statistics_form_sql.filter(b_display='1')
                         if(len(sales_statistics_form_sql)==1):
                             sales_statistics_form_serializer = salesStatisticstableSerializer(sales_statistics_form_sql[0])
                             sales_No_uuid = sales_statistics_form_serializer.data['uuid']
                         elif(len(sales_statistics_form_sql)==0):
                             sales_No_uuid = 'no-such-uuid'
                         else:
                             sales_No_uuid = 'no-unique-uuid'
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'sales_No': serializer_data['sales_No'],
                                     'sales_No_uuid': sales_No_uuid,
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'delivery_No': serializer_data['delivery_No'],
                                     'delivery_amount': serializer_data['delivery_amount'],
                                     'delivery_status': serializer_data['delivery_status'],
                                     'delivery_track_No': serializer_data['delivery_track_No'],
                                     'delivery_comment': serializer_data['delivery_comment'],
                                     }
                         data_to_render.append(iter_data)
                return render_to_response('storage_delivery_main.html', {'data':data_to_render, 'target_user':target_user, 'category':category, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                productDictionary = {u"母带":1, u"铁芯":2, u"辊剪":3}
                if request.POST["operation"] == 'update' :
                    delivery_model_data = storage_delivery_model.objects.filter(b_display='1', delivery_id=request.POST["delivery_id"])
                    if len(delivery_model_data) != 1:
                        return HttpResponse("更新失败！请求条目不存在！")
                    serializer=storageDeliverySerializers(delivery_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]
                    serializer_data['category'] = productDictionary[serializer_data['category']]
                    serializer.update(delivery_model_data[0], serializer_data)
                    return HttpResponseRedirect('/ERP/storage/delivery/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    iter_data = {
                                'delivery_id': str(UUID.uuid1()),
                                'category': productDictionary[request.POST['category']],
                                'sales_No': request.POST['sales_No'],
                                 'contract_No': request.POST['contract_No'],
                                 'update_date': request.POST['update_date'],
                                 'size':  request.POST['size'],
                                 'customer':  request.POST['customer'],
                                 'delivery_No':  request.POST['delivery_No'],
                                 'delivery_amount':  request.POST['delivery_amount'],
                                 'delivery_status':  request.POST['delivery_status'],
                                 'delivery_track_No':  request.POST['delivery_track_No'],
                                 'delivery_comment':  request.POST['delivery_comment'],
                                 'b_display' : '1',
                                 }
                    storageDeliverySerializers_ser =storageDeliverySerializers(data=iter_data)
                    if storageDeliverySerializers_ser.is_valid():
                        storageDeliverySerializers_ser.create(iter_data)
                        return HttpResponseRedirect('/ERP/storage/delivery/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
                    else:
                        return HttpResponse(json.dumps({'Error':storageDeliverySerializers_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def storage_product_out(request, category=None, target_user=None, uuid=None):
    try:
       if request.user.has_perm('main.edit_product_out_model') or request.user.has_perm('main.is_special_user'):
           if request.method== 'GET':
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                product_out_model_data = storage_product_out_model.objects.filter(b_display='1')
                setting_size_sql = setting_size_model.objects.all()
                setting_size_unit_list = [''] + [i.size_name for i in setting_size_sql]
                data_to_render = []
                data_to_render_today =[]
                amount = 0
                amount_today = 0
                if category == u'母带':
                    product_out_model_data = product_out_model_data.filter(category = 1)
                    product_out_model_data = product_out_model_data.order_by('-update_date')
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount += float(serializer_data['amount'])
                         data_to_render.append(iter_data)
                    product_out_model_data = product_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount_today += float(serializer_data['amount'])
                         data_to_render_today.append(iter_data)
                elif category == u'铁芯':
                    product_out_model_data = product_out_model_data.filter(category = 2)
                    product_out_model_data = product_out_model_data.order_by('-update_date')
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount += float(serializer_data['amount'])
                         data_to_render.append(iter_data)
                    product_out_model_data = product_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount_today += float(serializer_data['amount'])
                         data_to_render_today.append(iter_data)
                elif category == u'辊剪':
                    product_out_model_data = product_out_model_data.filter(category = 3)
                    product_out_model_data = product_out_model_data.order_by('-update_date')
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount += float(serializer_data['amount'])
                         data_to_render.append(iter_data)
                    product_out_model_data = product_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount_today += float(serializer_data['amount'])
                         data_to_render_today.append(iter_data)
                elif category == u'全部':
                    product_out_model_data = product_out_model_data.order_by('-update_date')
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount += float(serializer_data['amount'])
                         data_to_render.append(iter_data)
                    product_out_model_data = product_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(product_out_model_data)):
                         serializer=storage_product_out_serializers(product_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'No': i+1,
                                      'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'contract_No': serializer_data['contract_No'],
                                     'size': serializer_data['size'],
                                     'customer': serializer_data['customer'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         amount_today += float(serializer_data['amount'])
                         data_to_render_today.append(iter_data)
                sum_data = {'No':'总计','category':category, 'delivery_id':'-','update_date':'-','contract_No':'-','size':'-',
                             'customer':'-','amount':amount,'comment':'-'}
                data_to_render.append(sum_data)
                sum_data_today = {'No':'总计','category':category, 'delivery_id':'-','update_date':'-','contract_No':'-','size':'-',
                             'customer':'-','amount':amount_today,'comment':'-'}
                data_to_render_today.append(sum_data_today)
                return render_to_response('storage_product_out_main.html', {'data':data_to_render,'data_today':data_to_render_today, 'target_user':target_user, 'category':category, 'setting_size_unit_list':setting_size_unit_list}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                productDictionary = {u"母带":1, u"铁芯":2, u"辊剪":3}
                if request.POST["operation"] == 'update' :
                    product_out_model_data = storage_product_out_model.objects.filter(b_display='1', delivery_id=request.POST["delivery_id"])
                    if len(product_out_model_data) != 1:
                        return HttpResponse("更新失败！请求条目不存在！")
                    serializer=storage_product_out_serializers(product_out_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]
                    serializer_data['category'] = productDictionary[serializer_data['category']]
                    serializer.update(product_out_model_data[0], serializer_data)
                    return HttpResponse(json.dumps({'SUCCESS':"update the product out form!"}))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    iter_data = {
                                'delivery_id': str(UUID.uuid1()),
                                'category': productDictionary[request.POST['category']],
                                 'contract_No': request.POST['contract_No'],
                                 'update_date': request.POST['update_date'],
                                 'size':  request.POST['size'],
                                 'customer':  request.POST['customer'],
                                 'amount':  request.POST['amount'],
                                 'comment':  request.POST['comment'],
                                 'b_display' : '1',
                                 }
                    storage_product_out_serializers_ser =storage_product_out_serializers(data=iter_data)
                    if storage_product_out_serializers_ser.is_valid():
                        storage_product_out_serializers_ser.create(iter_data)
                        return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                    else:
                        return HttpResponse(json.dumps({'Error':storage_product_out_serializers_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def storage_source_out(request, category=None, target_user=None, uuid=None):
    try:
       if request.user.has_perm('main.edit_source_out_model'):
           if request.method== 'GET':
                category_dictionary = {'1':u'母合金', '2':u'耐火材料', '3':u'辅助材料', '4':u'护盒', '5':u'五金电器'}
                category_dictionary_reverse = {u'母合金':1, u'耐火材料':2, u'辅助材料':3, u'护盒':4, u'五金电器':5}
                source_out_model_data = storage_source_out_model.objects.filter(b_display='1')
                data_to_render = []
                data_to_render_today = []
                if category == u'母合金' or category == u'耐火材料' or category == u'辅助材料' or category == u'护盒' or category == u'五金电器':
                    source_out_model_data = source_out_model_data.filter(category = category_dictionary_reverse[category])
                    source_out_model_data = source_out_model_data.order_by('-update_date')
                    for i in range(0, len(source_out_model_data)):
                         serializer=storage_source_out_serializers(source_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'item': serializer_data['item'],
                                      'item_size': serializer_data['item_size'],
                                     'No': serializer_data['No'],
                                     'reason': serializer_data['reason'],
                                     'department': serializer_data['department'],
                                     'user': serializer_data['user'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         data_to_render.append(iter_data)
                    source_out_model_data = source_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(source_out_model_data)):
                         serializer=storage_source_out_serializers(source_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'item': serializer_data['item'],
                                      'item_size': serializer_data['item_size'],
                                     'No': serializer_data['No'],
                                     'reason': serializer_data['reason'],
                                     'department': serializer_data['department'],
                                     'user': serializer_data['user'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         data_to_render_today.append(iter_data)

                elif category == u'全部':
                    #source_out_model_data = source_out_model_data.filter(category = '4')
                    source_out_model_data = source_out_model_data.order_by('-update_date')
                    for i in range(0, len(source_out_model_data)):
                         serializer=storage_source_out_serializers(source_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'item': serializer_data['item'],
                                      'item_size': serializer_data['item_size'],
                                     'No': serializer_data['No'],
                                     'reason': serializer_data['reason'],
                                     'department': serializer_data['department'],
                                     'user': serializer_data['user'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         data_to_render.append(iter_data)
                    source_out_model_data = source_out_model_data.filter(update_date = datetime.date.today())
                    for i in range(0, len(source_out_model_data)):
                         serializer=storage_source_out_serializers(source_out_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['category']],
                                     'delivery_id': serializer_data['delivery_id'],
                                     'update_date': serializer_data['update_date'],
                                     'item': serializer_data['item'],
                                      'item_size': serializer_data['item_size'],
                                     'No': serializer_data['No'],
                                     'reason': serializer_data['reason'],
                                     'department': serializer_data['department'],
                                     'user': serializer_data['user'],
                                     'amount': serializer_data['amount'],
                                     'comment': serializer_data['comment'],
                                     }
                         data_to_render_today.append(iter_data)
                return render_to_response('storage_source_out_main.html', {'data':data_to_render, 'data_today':data_to_render_today, 'target_user':target_user, 'category':category}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                productDictionary = {u'母合金':1, u'耐火材料':2, u'辅助材料':3, u'护盒':4, u'五金电器':5}
                if request.POST["operation"] == 'update' :
                    source_out_model_data = storage_source_out_model.objects.filter(b_display='1', delivery_id=request.POST["delivery_id"])
                    if len(source_out_model_data) != 1:
                        return HttpResponse("更新失败！请求条目不存在！")
                    serializer=storage_source_out_serializers(source_out_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]
                    serializer_data['category'] = productDictionary[serializer_data['category']]
                    serializer.update(source_out_model_data[0], serializer_data)
                    return HttpResponse(json.dumps({'SUCCESS':"update the source out  form!"}))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    iter_data = {
                                'delivery_id': str(UUID.uuid1()),
                                'category': productDictionary[request.POST['category']],
                                 'update_date': request.POST['update_date'],
                                 'item': request.POST['item'],
                                 'item_size': request.POST['item_size'],
                                 'No': request.POST['No'],
                                 'reason': request.POST['reason'],
                                 'department': request.POST['department'],
                                 'user': request.POST['user'],
                                 'amount': request.POST['amount'],
                                 'comment': request.POST['comment'],
                                 'b_display' : '1',
                                 }
                    storage_source_out_serializers_ser =storage_source_out_serializers(data=iter_data)
                    if storage_source_out_serializers_ser.is_valid():
                        storage_source_out_serializers_ser.create(iter_data)
                        return HttpResponse(json.dumps({'SUCCESS':iter_data}))
                    else:
                        return HttpResponse(json.dumps({'Error':storage_source_out_serializers_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())


def storage_product_in(request, category=None, target_user=None, uuid=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            if request.method== 'GET':
                category_dictionary = {'1':u'母带', '2':u'铁芯', '3':u'辊剪'}
                category_dictionary_revise = {u'母带':1, u'铁芯':2, u'辊剪':3}
                product_in_sql = item_model.objects.filter(isLatest = 1)
                data_to_render = []
                amount = 0
                if category == u'母带' or category == u'铁芯' or category == u'辊剪':
                    product_in_sql = product_in_sql.filter(item_category = category_dictionary_revise[category])
                    product_in_sql = product_in_sql.filter(b_display=1)
                    product_in_sql = product_in_sql.order_by('is_stored', '-produce_date')
                    for i in range(0, len(product_in_sql)):
                         serializer=item_model_serializer(product_in_sql[i])
                         serializer_data = serializer.data
                         if serializer_data['is_stored'] != '1':
                            is_stored = '是'
                            is_stored2 = '否'
                         else:
                             is_stored = ''
                             is_stored2 = ''
                             amount += float(serializer_data['item_weight'])
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['item_category']],
                                     'update_date': serializer_data['produce_date'],
                                     'produce_No': serializer_data['item_id'],
                                     'size': serializer_data['item_size'],
                                     'class': serializer_data['item_class'],
                                     'container': serializer_data['item_container'],
                                     'is_stored': is_stored,
                                      'is_stored2': is_stored2,
                                     'No': serializer_data['item_weight'],
                                      'uuid': serializer_data['uuid'],
                                     }
                         data_to_render.append(iter_data)
                elif category == u'全部':
                    product_in_sql = product_in_sql.filter(b_display=1)
                    product_in_sql = product_in_sql.order_by('is_stored', '-produce_date')
                    for i in range(0, len(product_in_sql)):
                         serializer=item_model_serializer(product_in_sql[i])
                         serializer_data = serializer.data
                         if serializer_data['is_stored'] != '1':
                            is_stored = '是'
                            is_stored2 = '否'
                         else:
                             is_stored = ''
                             is_stored2 = ''
                             amount += float(serializer_data['item_weight'])
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['item_category']],
                                     'update_date': serializer_data['produce_date'],
                                     'produce_No': serializer_data['item_id'],
                                     'size': serializer_data['item_size'],
                                     'class': serializer_data['item_class'],
                                     'container': serializer_data['item_container'],
                                      'is_stored': is_stored,
                                      'is_stored2': is_stored2,
                                     'No': serializer_data['item_weight'],
                                       'uuid': serializer_data['uuid'],
                                     }
                         data_to_render.append(iter_data)
                #sum_data = {'index':'总计','category':category, 'update_date':'-','produce_No':'-','size':'-',
                #             'class':'-','container':'-','No':amount}
                #data_to_render.append(sum_data)
                return render_to_response('storage_product_in_main.html', {'data':data_to_render, 'target_user':target_user, 'category':category}, context_instance=RequestContext(request))
            else: # POST method
                pass
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_source_in(request, category=None, target_user=None, uuid=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            if request.method== 'GET':
                category_dictionary = {'1':u'母合金', '2':u'耐火材料', '3':u'辅助材料', '4':u'护盒', '5':u'五金电器'}
                category_dictionary_reverse = {u'母合金':1, u'耐火材料':2, u'辅助材料':3, u'护盒':4, u'五金电器':5}
                product_in_sql = purchase_model.objects.filter(b_display = 1)
                data_to_render = []
                amount = 0
                total_price = 0
                if category == u'母合金' or category == u'耐火材料' or category == u'辅助材料' or category == u'护盒' or category == u'五金电器':
                    product_in_sql = product_in_sql.filter(purchase_category = category_dictionary_reverse[category])
                    product_in_sql = product_in_sql.order_by('is_stored', '-purchase_date')
                    for i in range(0, len(product_in_sql)):
                         serializer=purchase_model_serializers(product_in_sql[i])
                         serializer_data = serializer.data
                         if serializer_data['is_stored'] != '1':
                            is_stored = '是'
                            is_stored2 = '否'
                         else:
                             is_stored = ''
                             is_stored2 = ''
                             amount += float(serializer_data['amount'])
                             total_price += float(serializer_data['total_price'])

                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['purchase_category']],
                                     'update_date': serializer_data['purchase_date'],
                                     'No': serializer_data['storage_no'],
                                     'item': serializer_data['size'],
                                      'item_size': serializer_data['purchase_name'],
                                     'supplier': serializer_data['supplier'],
                                     'price': serializer_data['unit_price'],
                                     'amount': serializer_data['amount'],
                                      'total_price': round(float(serializer_data['total_price']),4),
                                      'is_stored': is_stored,
                                      'is_stored2': is_stored2,
                                      'purchase_id': serializer_data['purchase_id'],
                                     }
                         data_to_render.append(iter_data)
                elif category == u'全部':
                    product_in_sql = product_in_sql.order_by('is_stored', '-purchase_date')
                    for i in range(0, len(product_in_sql)):
                         serializer=purchase_model_serializers(product_in_sql[i])
                         serializer_data = serializer.data
                         if serializer_data['is_stored'] != '1':
                            is_stored = '是'
                            is_stored2 = '否'
                         else:
                             is_stored = ''
                             is_stored2 = ''
                             amount += float(serializer_data['amount'])
                             total_price += float(serializer_data['total_price'])
                         iter_data = {'index': i+1,
                                     'category': category_dictionary[serializer_data['purchase_category']],
                                     'update_date': serializer_data['purchase_date'],
                                     'No': serializer_data['storage_no'],
                                     'item': serializer_data['size'],
                                      'item_size': serializer_data['purchase_name'],
                                     'supplier': serializer_data['supplier'],
                                     'price': serializer_data['unit_price'],
                                     'amount': serializer_data['amount'],
                                      'total_price':  round(float(serializer_data['total_price']),4),
                                      'is_stored': is_stored,
                                      'is_stored2': is_stored2,
                                      'purchase_id': serializer_data['purchase_id'],
                                     }
                         data_to_render.append(iter_data)
                sum_data = {'index':'总计','category':category,'amount':amount,'total_price':total_price}
                data_to_render.append(sum_data)
                return render_to_response('storage_source_in_main.html', {'data':data_to_render, 'target_user':target_user, 'category':category}, context_instance=RequestContext(request))
            else: # POST method
                pass
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def storage_source_jn_stored_confirm(request, category=None, uuid=None, target_user=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            purchase_model_sql = purchase_model.objects.filter(purchase_id=uuid)
            if(len(purchase_model_sql)!=1):
                return HttpResponse('未找到该uuid，或有多个uuid，请联系管理员')
            else:
                serializer=purchase_model_serializers(purchase_model_sql[0])
                serializer_data = serializer.data
                serializer_data['is_stored'] = '1'
                serializer.update(purchase_model_sql[0],serializer_data)
                return HttpResponseRedirect('/ERP/storage/source_in/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_source_jn_stored_cancel(request, category=None, uuid=None, target_user=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            purchase_model_sql = purchase_model.objects.filter(purchase_id=uuid)
            if(len(purchase_model_sql)!=1):
                return HttpResponse('未找到该uuid，或有多个uuid，请联系管理员')
            else:
                serializer=purchase_model_serializers(purchase_model_sql[0])
                serializer_data = serializer.data
                serializer_data['b_display'] = '0'
                serializer.update(purchase_model_sql[0],serializer_data)
                return HttpResponseRedirect('/ERP/storage/source_in/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))


def storage_product_jn_stored_confirm(request, category=None, uuid=None, target_user=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            item_model_sql = item_model.objects.filter(isLatest=1)
            item_model_sql = item_model_sql.filter(uuid=uuid)
            if(len(item_model_sql)!=1):
                return HttpResponse('未找到该uuid，或有多个uuid，请联系管理员')
            else:
                serializer=item_model_serializer(item_model_sql[0])
                serializer_data = serializer.data
                serializer_data['is_stored'] = '1'
                serializer.update(item_model_sql[0],serializer_data)
                return HttpResponseRedirect('/ERP/storage/product_in/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))

def storage_product_jn_stored_cancel(request, category=None, uuid=None, target_user=None):
    try:
        if request.user.has_perm('main.is_storage') or request.user.has_perm('main.is_storage_manager'):
            item_model_sql = item_model.objects.filter(isLatest=1)
            item_model_sql = item_model_sql.filter(uuid=uuid)
            if(len(item_model_sql)!=1):
                return HttpResponse('未找到该uuid，或有多个uuid，请联系管理员')
            else:
                serializer=item_model_serializer(item_model_sql[0])
                serializer_data = serializer.data
                serializer_data['isLatest'] = '0'
                serializer.update(item_model_sql[0],serializer_data)
                return HttpResponseRedirect('/ERP/storage/product_in/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
        else:
            return  HttpResponse('No permission!')
    except:
        return HttpResponse(json.dumps({'Error':traceback.format_exc()}))




