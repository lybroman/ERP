# -*- coding: utf-8 -*-
from rest_framework import generics
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import sys, os, time, copy, json
import traceback
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from models import user_model_extend
from serializers import user_model_extend_serializer
from django.contrib.auth.models import User

from models import produce_statistics_pendai_model,produce_statistics_gunjian_model, sample_form_model, produce_statistics_tiexin_model
from produce_model import item_model
from produce_serializers import  item_model_serializer
from serializers import sample_form_model_serializer
from produce_serializers import  produce_statistics_pendai_model_serializer, produce_statistics_gunjian_model_serializer, produce_statistics_tiexin_model_serializer

def MHJ_track(request, track_id=None):
    if request.user.has_perm('main.is_quality'):
        if request.method == 'GET':
            return render_to_response('MHJ_track.html',{'target_user': request.user.username}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            try:
                data = request.POST
                if data.has_key("search_id"):
                     track_id = data["search_id"]
                     culprit_lists_sql = produce_statistics_pendai_model.objects.filter(item_id__icontains = track_id, isLatest=1)
                     data_to_render = []
                     for index in range(0, len(culprit_lists_sql)):
                        clt_serializer = produce_statistics_pendai_model_serializer(culprit_lists_sql[index])
                        clt_serializer_data = clt_serializer.data
                        item = {'index' : index + 1,
                                'item_id':clt_serializer_data['item_id'] ,
                                'item_uuid':clt_serializer_data['uuid'] ,
                                'produce_date':clt_serializer_data['produce_date'] ,
                                'item_size':clt_serializer_data['item_size'] ,
                                'item_class':clt_serializer_data['item_class'] ,
                                'item_weight':clt_serializer_data['item_weight'] ,
                                'item_buyNo':clt_serializer_data['item_buyNo']
                                }

                        purchase_Nos = clt_serializer_data['purchase_Nos']
                        if purchase_Nos == '' or purchase_Nos == None:
                            item['supplier'] = []
                        elif ';' in purchase_Nos:
                            purchase_list = purchase_Nos.split(';')
                            item['supplier'] = []
                            for pn in purchase_Nos:
                                if pn == '':
                                    pass
                                else:
                                    item['supplier'].append(pn)
                        else:
                            item['supplier'] = [purchase_Nos]
                        data_to_render.append(item)

                     return render_to_response('MHJ_track.html', {"items":data_to_render, "search_id":track_id, 'target_user':request.user.username}, context_instance=RequestContext(request))
                else:
                    return HttpResponse(json.dumps({"error":request.POST.keys()}))
            except:
                return HttpResponse(json.dumps({"error":traceback.format_exc()}))
    else:
        return HttpResponse(u"您没有质检权限！")

def DC_track(request, track_id=None):
    if request.user.has_perm('main.is_quality'):
        if request.method == 'GET':
            return render_to_response('DC_track.html',{'target_user': request.user.username}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            try:
                data = request.POST
                if data.has_key("search_id"):
                     track_id = data["search_id"]
                     culprit_lists_sql = produce_statistics_gunjian_model.objects.filter(item_id__icontains = track_id, isLatest=1)
                     data_to_render = []
                     for index in range(0, len(culprit_lists_sql)):
                        clt_serializer = produce_statistics_gunjian_model_serializer(culprit_lists_sql[index])
                        clt_serializer_data = clt_serializer.data
                        item = {'index' : index + 1,
                                'item_id':clt_serializer_data['item_id'] ,
                                'item_uuid':clt_serializer_data['uuid'] ,
                                'produce_date':clt_serializer_data['produce_date'] ,
                                'item_size':clt_serializer_data['item_size'] ,
                                'item_staff':clt_serializer_data['item_staff'] ,
                                'item_pass':clt_serializer_data['item_pass'] ,
                                'item_fail':clt_serializer_data['item_fail'] ,
                                'item_buyNo':clt_serializer_data['item_buyNo']
                                }

                        selected_sample_form_sql = sample_form_model.objects.filter(index = clt_serializer_data['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            item['sales_uuid'] = '#'
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            item['sales_uuid'] = content['message_id']

                        selected_item_sql = item_model.objects.filter(uuid = clt_serializer_data['storage_item_uuid'])
                        if len(selected_item_sql) != 1:
                            item['storage_size'] = 'N/A'
                        else:
                            serializer=item_model_serializer(selected_item_sql[0])
                            content = serializer.data
                            item['storage_size'] = content['item_size']

                        data_to_render.append(item)
                     return render_to_response('DC_track.html', {"items":data_to_render, "search_id":track_id, 'target_user':request.user.username}, context_instance=RequestContext(request))
                else:
                    return HttpResponse(json.dumps({"error":request.POST.keys()}))
            except:
                return HttpResponse(json.dumps({"error":traceback.format_exc()}))
    else:
        return HttpResponse(u"您没有质检权限！")


def CX_track(request, track_id=None):
    if request.user.has_perm('main.is_quality'):
        if request.method == 'GET':
            return render_to_response('CX_track.html',{'target_user': request.user.username}, context_instance=RequestContext(request))
        elif request.method == 'POST':
            try:
                data = request.POST
                if data.has_key("search_id"):
                     track_id = data["search_id"]
                     culprit_lists_sql = produce_statistics_tiexin_model.objects.filter(item_id__icontains = track_id, isLatest=1)
                     data_to_render = []
                     for index in range(0, len(culprit_lists_sql)):
                        clt_serializer = produce_statistics_tiexin_model_serializer(culprit_lists_sql[index])
                        clt_serializer_data = clt_serializer.data
                        item = {'index' : index + 1,
                                'item_id':clt_serializer_data['item_id'] ,
                                'item_uuid':clt_serializer_data['uuid'] ,
                                'produce_date':clt_serializer_data['produce_date'] ,
                                'item_amount':clt_serializer_data['item_amount'] ,
                                'item_buyNo':clt_serializer_data['item_buyNo']
                                }

                        selected_sample_form_sql = sample_form_model.objects.filter(index = clt_serializer_data['item_buyNo'])
                        if len(selected_sample_form_sql) == 0:
                            item['sales_uuid'] = 'N/A'
                        else:
                            sample_form_serializer = sample_form_model_serializer(selected_sample_form_sql[0])
                            content = sample_form_serializer.data
                            item['sales_uuid'] = content['message_id']

                        selected_item_sql = item_model.objects.filter(uuid = clt_serializer_data['storage_item_uuid'])
                        if len(selected_item_sql) != 1:
                            item['storage_size'] = 'N/A'
                        else:
                            serializer=item_model_serializer(selected_item_sql[0])
                            content = serializer.data
                            item['storage_size'] = content['item_size']

                        data_to_render.append(item)
                     return render_to_response('CX_track.html', {"items":data_to_render, "search_id":track_id, 'target_user':request.user.username}, context_instance=RequestContext(request))
                else:
                    return HttpResponse(json.dumps({"error":request.POST.keys()}))
            except:
                return HttpResponse(json.dumps({"error":traceback.format_exc()}))
    else:
        return HttpResponse(u"您没有质检权限！")

