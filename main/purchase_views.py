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
from purchase_models import purchase_model, supplier_model
from purchase_serilaizers import purchase_model_serializers, supplier_model_serializers
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from urllib import unquote

def purchase_main(request, target_user=None):
    try:
        if request.user.is_anonymous() or not request.user.is_authenticated():
            return HttpResponseRedirect(r'/ERP/login/')
        else:
            if request.method == 'GET':
                data_to_render = {'target_user' : target_user}
                return render_to_response('purchase_main.html', {'data': data_to_render} , context_instance=RequestContext(request))
                #return render_to_response('sales_main.html', context_instance=RequestContext(request))
            elif request.method == 'POST':
                pass
    except:
        return HttpResponse(json.dumps({"ERROR" : traceback.format_exc()}))

def purchase_category(request, category=None, target_user=None):
    '''
    puchase_name和size颠倒：purch_name是规格，size是名称
    '''
    try:
       if request.user.has_perm('main.is_buyer'):
           if request.method== 'GET':
                purchase_model_data = purchase_model.objects.filter(b_display='1')
                data_to_render = []
                productDictionary = {u"母合金":'1', u"耐火材料":'2', u"辅助材料":'3', u"护盒":'4', u"五金电气":'5'}
                purchase_model_data = purchase_model_data.filter(purchase_category= productDictionary[category])
                '''
                #显示所有条目
                for i in range(0, len(purchase_model_data)):
                     serializer=purchase_model_serializers(purchase_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'index': i+1,
                                 'purchase_id': serializer_data['purchase_id'],
                                 'size': serializer_data['size'],
                                 'supplier': serializer_data['supplier'],
                                 'amount': serializer_data['amount'],
                                 'purchase_date': serializer_data['purchase_date'],
                                 'comment': serializer_data['comment'],
                                 'alert': serializer_data['alert'],
                                 }
                     data_to_render.append(iter_data)
                 '''
                size=[]
                size_supplier = {}
                for i in range(0, len(purchase_model_data)):
                    serializer=purchase_model_serializers(purchase_model_data[i])
                    serializer_data = serializer.data
                    if serializer_data['size'] not in size:
                        size.append(serializer_data['size'])
                        size_supplier[serializer_data['size']] = {}
                        size_supplier[serializer_data['size']][serializer_data['supplier']] = {}
                        size_supplier[serializer_data['size']][serializer_data['supplier']]['amount'] = float(serializer_data['amount'])
                        size_supplier[serializer_data['size']][serializer_data['supplier']]['last_purchase_date'] = serializer_data['purchase_date']
                    else:
                        if serializer_data['supplier'] not in size_supplier[serializer_data['size']].keys():
                            size_supplier[serializer_data['size']][serializer_data['supplier']] = {}
                            size_supplier[serializer_data['size']][serializer_data['supplier']]['amount'] = float(serializer_data['amount'])
                            size_supplier[serializer_data['size']][serializer_data['supplier']]['last_purchase_date'] = serializer_data['purchase_date']
                        else:
                            size_supplier[serializer_data['size']][serializer_data['supplier']]['amount'] += float(serializer_data['amount'])
                            if size_supplier[serializer_data['size']][serializer_data['supplier']]['last_purchase_date'] < serializer_data['purchase_date']:
                                size_supplier[serializer_data['size']][serializer_data['supplier']]['last_purchase_date'] = serializer_data['purchase_date']


                i=0

                for sizes in size_supplier.keys():
                    for suppliers in size_supplier[sizes].keys():
                        iter_data = {'index': i+1,
                                 'size': sizes,
                                 'supplier': suppliers,
                                 'amount': size_supplier[sizes][suppliers]['amount'],
                                 'purchase_date': size_supplier[sizes][suppliers]['last_purchase_date'],
                                 'comment': '',
                                 'alert': '',
                                 }
                        i += 1
                        data_to_render.append(iter_data)

                """
                query supplier model
                """
                supplier_sql = supplier_model.objects.values("supplier_name").distinct()

                supplier_list = [i["supplier_name"] for i in supplier_sql]

                return render_to_response('purchase_category.html', {'data':data_to_render, 'target_user':target_user, 'category':category, 'supplier_list':supplier_list}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                productDictionary = {u"母合金":'1', u"耐火材料":'2', u"辅助材料":'3', u"护盒":'4', u"五金电气":'5'}
                if request.POST["operation"] == 'add':
                    # add a new item
                    """
                    update purchase_index
                    """
                    purchase_model_data = purchase_model.objects.filter(last_revise_date__year = str(datetime.datetime.now().year))
                    year = str(int(datetime.datetime.now().year) % 100)
                    count = len(purchase_model_data) + 1
                    index = 'CG{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)
                    # add a new item
                    iter_data = {
                                 'purchase_id': str(uuid.uuid1()),
                                 'purchase_index':index,
                                 'purchase_name' : request.POST['purchase_name'],
                                 'purchase_category': productDictionary[category],
                                 'supplier': request.POST['supplier'],
                                 'amount': request.POST['amount'],
                                 'purchase_date': request.POST['purchase_date'],
                                 'storage_no': request.POST['storage_no'],
                                 'unit_price': request.POST['unit_price'],
                                 'total_price': request.POST['total_price'],
                                 'comment': request.POST['comment'],
                                 'quality': request.POST['quality'],
                                 'size': request.POST['size'],
                                 'buyer_name': request.user.username,
                                 'b_display' : '1',

                                 }
                    purchase_model_serializers_ser =purchase_model_serializers(data=iter_data)
                    if purchase_model_serializers_ser.is_valid():
                        purchase_model_serializers_ser.create(iter_data)
                        return HttpResponseRedirect('/ERP/purchase/category/'+unquote(category).encode('utf-8')+'/{}'.format(target_user))
                    else:
                        return HttpResponse(json.dumps({'Error':purchase_model_serializers_ser.errors}))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def purchase_detail(request, category=None, size=None, target_user=None):
    try:
       if request.user.has_perm('main.is_buyer'):
           if request.method== 'GET':
                purchase_model_data = purchase_model.objects.filter(b_display='1')
                data_to_render = []
                sumdata_to_render = []
                productDictionary = {u"母合金":'1', u"耐火材料":'2', u"辅助材料":'3', u"护盒":'4', u"五金电气":'5'}
                purchase_model_data = purchase_model_data.filter(purchase_category= productDictionary[category])
                purchase_model_data = purchase_model_data.filter(size = size)
                purchase_model_data = purchase_model_data.order_by('-purchase_date')
                amount = 0
                for i in range(0, len(purchase_model_data)):
                     serializer=purchase_model_serializers(purchase_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'index': i+1,
                                 'purchase_index' : serializer_data['purchase_index'],
                                 'purchase_name' : serializer_data['purchase_name'],
                                 'purchase_id': serializer_data['purchase_id'],
                                 'purchase_date': serializer_data['purchase_date'],
                                 'storage_no': serializer_data['storage_no'],
                                 'supplier': serializer_data['supplier'],
                                 'unit_price': serializer_data['unit_price'],
                                 'amount': round(float(serializer_data['amount']),4),
                                 'total_price': round(float(serializer_data['total_price']),4),
                                 'comment': serializer_data['comment'],
                                 'quality': serializer_data['quality'],
                                 }
                     amount += float(serializer_data['total_price'])
                     data_to_render.append(iter_data)
                sum_data = {'index': '总计', 'total_price':amount}
                sumdata_to_render.append(sum_data)

                """
                query supplier model
                """
                supplier_sql = supplier_model.objects.values("supplier_name").distinct()
                supplier_list = [i["supplier_name"] for i in supplier_sql]
                return render_to_response('purchase_detail.html', {'data':data_to_render,'sum':sumdata_to_render, 'target_user':target_user, 'category':category, 'size':size, 'supplier_list': supplier_list}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                productDictionary = {u"母合金":'1', u"耐火材料":'2', u"辅助材料":'3', u"护盒":'4', u"五金电气":'5'}
                if request.POST["operation"] == 'add':
                    # add a new item
                    """
                    update purchase_index
                    """
                    purchase_model_data = purchase_model.objects.filter(last_revise_date__year = str(datetime.datetime.now().year))
                    year = str(int(datetime.datetime.now().year) % 100)
                    count = len(purchase_model_data) + 1
                    index = 'CG{}{}{}{}{}'.format(year, count/1000 % 10, count/100 % 10, count/10 % 10, count/1 % 10)

                    iter_data = {
                                 'purchase_id': str(uuid.uuid1()),
                                 'purchase_index' : index,
                                 'purchase_name' : request.POST['purchase_name'],
                                 'purchase_category': productDictionary[category],
                                 'supplier': request.POST['supplier'],
                                 'amount': request.POST['amount'],
                                 'purchase_date': request.POST['purchase_date'],
                                 'storage_no': request.POST['storage_no'],
                                 'unit_price': request.POST['unit_price'],
                                 'total_price': request.POST['total_price'],
                                 'comment': request.POST['comment'],
                                 'quality': request.POST['quality'],
                                 'size': request.POST['size'],
                                 'buyer_name': request.user.username,
                                 'b_display' : '1',
                                 }

                    purchase_model_serializers_ser =purchase_model_serializers(data=iter_data)
                    if purchase_model_serializers_ser.is_valid():
                        purchase_model_serializers_ser.create(iter_data)
                        return HttpResponseRedirect('/ERP/purchase/detail/'+unquote(category).encode('utf-8')+'/'+unquote(size).encode('utf-8')+'/{}'.format(target_user))
                    else:
                        return HttpResponse(json.dumps({'Error':purchase_model_serializers_ser.errors}))
                elif request.POST["operation"] == 'update' :
                    purchase_model_data = purchase_model.objects.filter(b_display='1', purchase_id=request.POST["purchase_id"])
                    if len(purchase_model_data) != 1:
                        return HttpResponse("更新失败！请求条目不存在！")
                    serializer=purchase_model_serializers(purchase_model_data[0])
                    serializer_data = serializer.data
                    for key in serializer_data:
                        if key in request.POST:
                            serializer_data[key] =  request.POST[key]
                    serializer_data['purchase_category'] = productDictionary[category]
                    serializer.update(purchase_model_data[0], serializer_data)
                    return HttpResponseRedirect('/ERP/purchase/detail/'+unquote(category).encode('utf-8')+'/'+unquote(size).encode('utf-8')+'/{}'.format(target_user))
                elif request.POST["operation"] == 'delete' :
                    purchase_model_data = purchase_model.objects.filter(b_display='1', purchase_id=request.POST["purchase_id"])
                    if len(purchase_model_data) != 1:
                        return HttpResponse("更新失败！请求条目不存在！")
                    serializer=purchase_model_serializers(purchase_model_data[0])
                    serializer_data = serializer.data
                    serializer_data['b_display'] = '0'
                    serializer.update(purchase_model_data[0], serializer_data)
                    return HttpResponseRedirect('/ERP/purchase/detail/'+unquote(category).encode('utf-8')+'/'+unquote(size).encode('utf-8')+'/{}'.format(target_user))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def purchase_detail_uuid(request,uuid=None):
    try:
       if request.user.has_perm('main.is_buyer') or request.user.has_perm('main.is_producer') or request.user.has_perm("main.is_produce_manager"):
           if request.method== 'GET':
                purchase_model_data = purchase_model.objects.filter(b_display='1')
                data_to_render = []
                purchase_model_data = purchase_model_data.filter(purchase_id = uuid)
                for i in range(0, len(purchase_model_data)):
                     serializer=purchase_model_serializers(purchase_model_data[i])
                     serializer_data = serializer.data
                     iter_data = {'index': i+1,
                                 'purchase_index' : serializer_data['purchase_index'],
                                  'size' : serializer_data['size'],
                                 'purchase_name' : serializer_data['purchase_name'],
                                 'purchase_id': serializer_data['purchase_id'],
                                 'purchase_date': serializer_data['purchase_date'],
                                 'storage_no': serializer_data['storage_no'],
                                 'supplier': serializer_data['supplier'],
                                 'unit_price': serializer_data['unit_price'],
                                 'amount': serializer_data['amount'],
                                 'total_price': serializer_data['total_price'],
                                 'comment': serializer_data['comment'],
                                 'quality': serializer_data['quality'],
                                 }
                     data_to_render.append(iter_data)
                """
                query supplier model
                """
                supplier_sql = supplier_model.objects.values("supplier_name").distinct()
                supplier_list = [i["supplier_name"] for i in supplier_sql]
                return render_to_response('purchase_detail_uuid.html', {'data':data_to_render, 'supplier_list': supplier_list}, context_instance=RequestContext(request))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def purchase_supplier(request, target_user=None):
    try:
       if request.user.has_perm('main.is_buyer'):
           if request.method== 'GET':
                productDictionary = {'1':u"母合金", '2':u"耐火材料", '3' : u"辅助材料", '4': u"护盒", '5': u"五金电气"}
                purchase_model_data = purchase_model.objects.filter(b_display='1')
                purchase_model_data = purchase_model_data.order_by('purchase_category')
                data_to_render = []
                count = 0
                product_dict = {}
                for i in range(0, len(purchase_model_data)):
                    bAdd = False
                    serializer=purchase_model_serializers(purchase_model_data[i])
                    serializer_data = serializer.data
                    product_name = productDictionary[serializer_data['purchase_category']]
                    #return HttpResponse(product_name)
                    tmp = u"{}-{}".format(product_name, serializer_data['size'])
                    if serializer_data['supplier'] in product_dict.keys():
                        if tmp in product_dict[serializer_data['supplier']]:
                            pass
                        else:
                            bAdd = True
                            product_dict[serializer_data['supplier']].append(tmp)
                    else:

                        product_dict[serializer_data['supplier']] = [tmp]
                        bAdd = True

                    if bAdd:
                        supplier_sql = supplier_model.objects.filter(b_display=1, supplier_name=serializer_data['supplier'])
                        if len(supplier_sql)<1:
                            supplier_rank = 'N/A'
                            comment = 'N/A'
                        elif len(supplier_sql)>1:
                            supplier_rank = '信息有误'
                            comment = '信息有误'
                        else:
                            supplier_sql_serializer=supplier_model_serializers(supplier_sql[0])
                            supplier_sql_serializer_data = supplier_sql_serializer.data
                            supplier_rank = supplier_sql_serializer_data['supplier_rank']
                            comment = supplier_sql_serializer_data['comment']
                        iter_data = {'index': count + 1,
                                 'purchase_id': serializer_data['purchase_id'],
                                 'supplier_name': serializer_data['supplier'],
                                 'supplier_rank': supplier_rank,
                                 'supplier_product':  product_name,
                                 'size': serializer_data['size'],
                                 'purchase_name': serializer_data['purchase_name'],
                                 'unit_price': serializer_data['unit_price'],
                                 'comment': comment,
                                 }
                        data_to_render.append(iter_data)
                        count += 1
                return render_to_response('supplier_common.html', {'data':data_to_render, 'target_user':target_user}, context_instance=RequestContext(request))
       else:
            return HttpResponse("您没有对应的权限！请联系管理员！")
    except:
         return HttpResponse(traceback.format_exc())


def purchase_supplier_detail(request, supplier_name=None, target_user=None):
    try:
       if request.user.has_perm('main.is_buyer'):
           if request.method== 'GET':
                productDictionary = {'1':u"母合金", '2':u"耐火材料", '3' : u"辅助材料", '4': u"护盒", '5': u"五金电气"}
                purchase_model_data = purchase_model.objects.filter(b_display='1', supplier=supplier_name)
                data_to_render = []
                for i in range(0, len(purchase_model_data)):
                    serializer=purchase_model_serializers(purchase_model_data[i])
                    serializer_data = serializer.data
                    iter_data = {
                             'index': i + 1,
                             'supplier_product': productDictionary[serializer_data['purchase_category']],
                             'size': serializer_data['size'],
                             'purchase_name': serializer_data['purchase_name'],
                             'purchase_date': serializer_data['purchase_date'],
                             'unit_price': serializer_data['unit_price'],
                             'amount': serializer_data['amount'],
                             'total_price': serializer_data['total_price'],
                             'comment': serializer_data['comment'],
                             }
                    data_to_render.append(iter_data)
                supplier_model_data = supplier_model.objects.filter(b_display='1', supplier_name=supplier_name)
                supplier_data_to_render = []
                if len(supplier_model_data)>0:
                    serializer=supplier_model_serializers(supplier_model_data[0])
                    serializer_data = serializer.data
                    supplier_table = None
                    if serializer_data['supplier_table'] != None:
                        supplier_table = unquote(serializer_data['supplier_table'])
                        supplier_table = supplier_table[23:len(supplier_table)]

                    iter_data = {
                             'supplier_id': serializer_data['supplier_id'],
                             'supplier_name': serializer_data['supplier_name'],
                             'supplier_contact': serializer_data['supplier_contact'],
                             'supplier_address': serializer_data['supplier_address'],
                             'supplier_phone': serializer_data['supplier_phone'],
                             'supplier_product': serializer_data['supplier_product'],
                             'supplier_table': supplier_table,
                             'return_list': serializer_data['return_list'],
                             'supplier_rank': serializer_data['supplier_rank'],
                             'comment': serializer_data['comment'],
                             }
                    supplier_data_to_render.append(iter_data)
                else:
                    iter_data = {
                             'supplier_name': supplier_name,
                             }
                    supplier_data_to_render.append(iter_data)
                return render_to_response('supplier_detail_common.html', {'data':data_to_render,'supplier_data':supplier_data_to_render, 'target_user':target_user, 'supplier_name':supplier_name}, context_instance=RequestContext(request))
           elif request.method == 'POST':
                if request.POST.has_key('operation') and request.POST["operation"] != 'update' :
                    data = json.loads(str(request.POST["operation"]))
                    if "download" in data["operation"]:
                        if "supplier_table" in data["target"]:
                            supplier_model_sql = supplier_model.objects.filter(b_display='1', supplier_name=supplier_name)
                            if len(supplier_model_sql)!=1:
                                return HttpResponse("所选择供应商信息有误！请联系管理员")
                            else:
                                serializer=supplier_model_serializers(supplier_model_sql[0])
                                data_to_render = serializer.data
                                filename = data_to_render['supplier_table']
                                if filename == None:
                                    return HttpResponse("没有可以下载的文件，请后退！")
                                else:
                                    filename1 = unquote(filename).decode('utf-8')
                                    filename1 = 'C:'+ filename1
                                    #return HttpResponse(filename1)
                                    response = HttpResponse(readFile(filename1))
                                    response['Content-Type'] = 'application/octet-stream'
                                    response['Content-Disposition'] = 'attachment;filename=%s' % filename[23:len(filename)]
                                    return response # download request data
                        else:
                            return HttpResponse(repr('No supplier_table in "target" feature...'))
                    else:
                        return HttpResponse(repr('No download in "operation" feature...'))
                if request.POST["operation"] == 'update' :
                    supplier_model_data = supplier_model.objects.filter(b_display='1', supplier_name=request.POST["supplier_name"])
                    if len(supplier_model_data) == 0:
                        '''
                        new supplier
                        '''
                        new_uuid = str(uuid.uuid1())
                        iter_data = {
                                 'supplier_id': new_uuid,
                                 'supplier_name': request.POST['supplier_name'],
                                 'supplier_contact': request.POST['supplier_contact'],
                                 'supplier_address': request.POST['supplier_address'],
                                 'supplier_phone': request.POST['supplier_phone'],
                                 'supplier_product': request.POST['supplier_product'],
                                 'return_list': request.POST['return_list'],
                                 'supplier_rank': request.POST['supplier_rank'],
                                 'comment': request.POST['comment'],
                                 'supplier_table': request.FILES.get('supplier_table'),
                                 #'buyer_name': request.user.username,
                                 'b_display' : '1',
                                 }

                        supplier_model_serializers_ser = supplier_model_serializers(data=iter_data)

                        if supplier_model_serializers_ser.is_valid():
                            supplier_model_serializers_ser.create(iter_data)
                            supplier_model_sql = supplier_model.objects.filter(b_display='1', supplier_name=request.POST["supplier_name"])
                            supplier_model_sql[0].supplier_table = request.FILES.get('supplier_table')
                            supplier_model_sql[0].save()
                            return HttpResponseRedirect('/ERP/purchase/supplier_detail/'+unquote(request.POST["supplier_name"]).encode('utf-8')+'/{}'.format(target_user))
                        else:
                            return HttpResponse(json.dumps({'Error':supplier_model_serializers_ser.errors}))
                    elif len(supplier_model_data) >1:
                        return HttpResponse("请求供应商信息有误！多条供应商记录，请联系管理员！")
                    else:
                        serializer=supplier_model_serializers(supplier_model_data[0])
                        serializer_data = serializer.data
                        supplier_table = serializer_data['supplier_table']
                        for key in serializer_data:
                            if key in request.POST:
                                serializer_data[key] =  request.POST[key]

                        serializer.update(supplier_model_data[0], serializer_data)

                        if request.FILES.get('supplier_table') != None:
                            supplier_model_data[0].supplier_table = request.FILES.get('supplier_table')
                        else:
                            if supplier_table != None:
                                supplier_model_data[0].supplier_table  = unquote(supplier_table)
                        supplier_model_data[0].save()
                        return HttpResponseRedirect('/ERP/purchase/supplier_detail/'+unquote(request.POST["supplier_name"]).encode('utf-8')+'/{}'.format(target_user))
       else:
            return HttpResponse("You don't have permission!")
    except:
         return HttpResponse(traceback.format_exc())

def readFile(fn, buf_size=262120):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()



def purchase_supplier_archive(request):
    if request.user.has_perm('main.is_buyer'):
        try:
            if request.method== 'GET':
                    supplier_model_data = supplier_model.objects.filter(b_display='1')
                    data_to_render = []
                    for i in range(0, len(supplier_model_data)):
                         serializer=supplier_model_serializers(supplier_model_data[i])
                         serializer_data = serializer.data
                         iter_data = {'index': i+1,
                                     'supplier_id': serializer_data['supplier_id'],
                                     'supplier_name': serializer_data['supplier_name'],
                                     'supplier_address': serializer_data['supplier_address'],
                                     'supplier_contact': serializer_data["supplier_contact"],
                                     'supplier_phone': serializer_data["supplier_phone"],
                                     'supplier_rank': serializer_data["supplier_rank"],
                                     }
                         data_to_render.append(iter_data)
                    return render_to_response('purchase_supplier_archive.html', {'data':data_to_render, 'target_user':request.GET["target_user"]}, context_instance=RequestContext(request))
            else:
                if request.POST["operation"] == 'update' :
                        supplier_model_data = supplier_model.objects.filter(b_display='1', supplier_name=request.POST["supplier_name"], supplier_id=request.POST["supplier_id"])
                        if len(supplier_model_data) != 1:
                            return HttpResponse("item not unique or not exists! please contact lybroman@hotmail.com")
                        serializer=supplier_model_serializers(supplier_model_data[0])
                        serializer_data = serializer.data
                        if serializer_data['supplier_name'] != request.POST['supplier_name']:
                            return HttpResponse("Supplier name cannot be changed!")
                        for key in serializer_data:
                            if key in request.POST:
                                serializer_data[key] =  request.POST[key]

                        serializer.update(supplier_model_data[0], serializer_data)
                        return HttpResponseRedirect('/ERP/purchase/purchase_supplier_archive?target_user={}'.format(request.POST["target_user"]))
                elif request.POST["operation"] == 'add':
                    # add a new item
                    supplier_model_data = supplier_model.objects.filter(supplier_name=request.POST["supplier_name"])
                    if len(supplier_model_data) != 0:
                        return HttpResponse("供应商信息已存在!")
                    iter_data = {
                                'supplier_id': uuid.uuid1(),
                                 'supplier_name': request.POST['supplier_name'],
                                 'supplier_address': request.POST["supplier_address"],
                                 'supplier_contact': request.POST["supplier_contact"],
                                 'supplier_phone': request.POST["supplier_phone"],
                                 'supplier_rank': request.POST["supplier_rank"],
                                 'b_display' : '1',
                                 }
                    supplier_model_serializers_ser =supplier_model_serializers(data=iter_data)
                    if supplier_model_serializers_ser.is_valid():
                        supplier_model_serializers_ser.create(iter_data)
                        return HttpResponseRedirect('/ERP/purchase/purchase_supplier_archive?target_user={}'.format(request.POST["target_user"]))
                    else:
                        return HttpResponse(json.dumps({'Error':supplier_model_serializers_ser.errors}))
        except:
            return HttpResponse(traceback.format_exc())
    else:
        return HttpResponse('Permission Denied')