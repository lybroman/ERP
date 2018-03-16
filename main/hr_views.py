from rest_framework import generics
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import sys, os, time, copy, json
import datetime
import traceback
import uuid
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
import datetime
from hr_models import *
from hr_serializers import *
from models import user_model_extend
from serializers import user_model_extend_serializer
from django.contrib.auth.models import User


def hr_rank_overview(request, target_user=None, rank_uuid=None):
    if request.user.has_perm('main.is_ranker'):
        if request.method == 'GET':
            if target_user and rank_uuid:
                if rank_uuid == 'new_form':
                    rank_uuid = uuid.uuid1()
                    update_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    return render_to_response('hr_rank_detail.html', {'target_user' : target_user, 'rank_uuid':rank_uuid, 'update_date':update_date}, context_instance=RequestContext(request))
                else:
                    rank_tu_sql = hr_rank_model.objects.filter(target_user=target_user, rank_uuid=rank_uuid, b_display='1')
                    if len(rank_tu_sql) == 1:
                        serializer=hr_rank_model_serializer(rank_tu_sql[0])
                        serializer_data = serializer.data
                        iter_data = {
                             'rank_uuid': serializer_data['rank_uuid'],
                             'target_user': serializer_data['target_user'],
                             'date_for': serializer_data['date_for'],
                             'update_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                             'comment': serializer_data["comment"],
                             'score':  serializer_data["score"],
                             #'ranker':  serializer_data["ranker"],
                             'b_display' : '1',
                             }
                        return render_to_response('hr_rank_detail.html', iter_data, context_instance=RequestContext(request))
                    else:
                        return HttpResponse('Bad Request: No such record!')
            elif target_user:
                rank_tu_sql = hr_rank_model.objects.filter(target_user=target_user, b_display='1')
                data_to_render = []
                for i in range(0, len(rank_tu_sql)):
                    serializer=hr_rank_model_serializer(rank_tu_sql[i])
                    serializer_data = serializer.data
                    it = {\
                    'no' : i + 1,
                    'rank_uuid': serializer_data['rank_uuid'],
                    'date_for' : serializer_data['date_for'],
                    'update_date' : serializer_data['update_date'],
                    'score':serializer_data['score'],
                    'ranker':serializer_data['ranker'],}
                    data_to_render.append(it)
                return render_to_response('hr_rank_overview.html', {'data':data_to_render, 'target_user':target_user}, context_instance=RequestContext(request))

        elif request.method == 'POST':
            rank_tu_sql = hr_rank_model.objects.filter(target_user=target_user, b_display='1', rank_uuid=rank_uuid)
            if len(rank_tu_sql) == 1:
                serializer=hr_rank_model_serializer(rank_tu_sql[0])
                serializer_data = serializer.data
                for key in serializer_data:
                    if key in request.POST:
                        serializer_data[key] =  request.POST[key]
                serializer.update(rank_tu_sql[0], serializer_data)
                return HttpResponseRedirect('/ERP/hr_rank_overview/{}/'.format(target_user))
            elif len(rank_tu_sql) == 0:
                iter_data = {
                             'rank_uuid': request.POST['rank_uuid'],
                             'target_user': request.POST['target_user'],
                             'date_for': request.POST['date_for'],
                             'update_date':  request.POST["update_date"],
                             'comment':  request.POST["comment"],
                             'score':  request.POST["score"],
                             'ranker':  request.POST["ranker"],
                             'b_display' : '1',
                             }
                hr_rank_model_serializer_ser =hr_rank_model_serializer(data=iter_data)
                if hr_rank_model_serializer_ser.is_valid():
                    hr_rank_model_serializer_ser.create(iter_data)
                    return HttpResponseRedirect('/ERP/hr_rank_overview/{}/'.format(target_user))
                else:
                    return HttpResponse(json.dumps({'ERROR':hr_rank_model_serializer_ser.errors}))
            else:
                return HttpResponse('Bad Request!')

        return render_to_response('hr_rank_overview.html', {}, context_instance=RequestContext(request))
    else:
        return 'Permission Denied!'

def employee_profile(request, target_user=None):
    if request.method == 'GET':
        user_profile_sql = user_model_extend.objects.filter(username=target_user)
        if len(user_profile_sql) == 0:
            # current target user do not have an extention, auto create one
            user_model = User.objects.filter(username=target_user)
            if len(user_model) == 1:
                data_to_save = {'username':target_user, 'profile_image':None}
                user_profile_sql_ser = user_model_extend_serializer(data=data_to_save)
                if user_profile_sql_ser.is_valid():
                    user_profile_sql_ser.create(data_to_save)
                    return render_to_response('employee_profile.html', {'target_user':target_user}, context_instance=RequestContext(request))
                else:
                    return HttpResponse(user_profile_sql_ser.errors)
            else:
                return HttpResponse('No Such User!')
        else:
            user_profile_sql_serializer = user_model_extend_serializer(user_profile_sql[0])
            user_profile_data = user_profile_sql_serializer.data
            data_to_render = {}
            for key in user_profile_data.keys():
                data_to_render[key] = user_profile_data[key]
            data_to_render['target_user'] = target_user
            return render_to_response('employee_profile.html', data_to_render, context_instance=RequestContext(request))
    elif request.method == 'POST':
        user_profile_sql = user_model_extend.objects.filter(username=target_user)
        if len(user_profile_sql) == 0:
            return HttpResponse('No Such User!')
        else:
            data = request.POST
            serializer=user_model_extend_serializer(user_profile_sql[0])
            serializer_data = serializer.data
            #return HttpResponse(data.keys())
            for key in data.keys():
                serializer_data[key] =  data[key]
            serializer.update(user_profile_sql[0], serializer_data)
            return HttpResponseRedirect('/ERP/employee_profile/{}/'.format(request.POST["target_user"]))



