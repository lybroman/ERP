# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib import admin
import django

class user_control_model(models.Model):

    """
    user_contorl models:

    user_id: char(auto added)
    user_name: char
    user_password: char(1 spec charater + 1 number + 1 uppper chacter)
    user_email: char
    user_permisson_level: char
    user_title: char (optional)
    user_next_level_manager char (valid user_id; optional)
    """
    user_id = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)
    user_permission_level = models.CharField(max_length=100, blank=True, null=True)
    user_title = models.CharField(max_length=100, blank=True, null=True)
    user_next_level_manager = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('user_id','user_name', 'user_password')

class salesExetable(models.Model):
    # briefInfo
    No = models.CharField(max_length=200, blank=True, null=True)
    companyName = models.CharField(max_length=100, blank=True, null=True)
    salesman = models.CharField(max_length=100, blank=True, null=True)
    companyInfo = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    productType = models.CharField(max_length=100, blank=True, null=True)

    # contactInfo
    date = models.DateField(blank=True, null=True)
    productCode = models.CharField(max_length=200, blank=True, null=True)
    mag = models.CharField(max_length=100, blank=True, null=True)
    specification = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    quantityDemand = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, blank=True, null=True)
    quantityActual = models.CharField(max_length=100, blank=True, null=True)
    assessment = models.CharField(max_length=100, blank=True, null=True)
    priceUnit = models.CharField(max_length=100, blank=True, null=True)
    priceTotal = models.CharField(max_length=100, blank=True, null=True)
    payment = models.CharField(max_length=100, blank=True, null=True)

    # progressPlanning
    supplierP = models.CharField(max_length=100, blank=True, null=True)
    inquiryP = models.CharField(max_length=100, blank=True, null=True)
    quoteP = models.CharField(max_length=100, blank=True, null=True)
    sampleP = models.CharField(max_length=100, blank=True, null=True)
    testP = models.CharField(max_length=100, blank=True, null=True)
    smallOrderP = models.CharField(max_length=100, blank=True, null=True)

    # progressActual
    supplier = models.CharField(max_length=100, blank=True, null=True)
    dateDeliver = models.DateField(blank=True, null=True)
    sampleNum = models.CharField(max_length=100, blank=True, null=True)
    sampleNo = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    test = models.CharField(max_length=100, blank=True, null=True)
    smallOrder = models.FileField(upload_to='uploadFiles/',blank=True, null=True)

    # quote
    dateQuote = models.DateField(blank=True, null=True)
    quoteApply = models.CharField(max_length=100, blank=True, null=True)
    quoteOrder = models.FileField(upload_to='uploadFiles/',blank=True, null=True)

    # order
    dateOrder = models.DateField(blank=True, null=True)
    orderNo = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    orderInfo = models.CharField(max_length=100, blank=True, null=True)

    # contract
    dateContract = models.DateField(blank=True, null=True)
    contractNo = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    contractInfo = models.CharField(max_length=100, blank=True, null=True)

    # sample
    contractReviewNoS = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    salesNoS = models.FileField(upload_to='uploadFiles/',blank=True, null=True)

    # product
    contractReviewNoP = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    salesNoP = models.FileField(upload_to='uploadFiles/',blank=True, null=True)

    # produce
    produceNo = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    produceStatus = models.CharField(max_length=100, blank=True, null=True)
    transNo = models.CharField(max_length=100, blank=True, null=True)

    # others
    comments = models.CharField(max_length=1000, blank=True, null=True)
    personCharge = models.CharField(max_length=100, blank=True, null=True)
    personSupervise = models.CharField(max_length=100, blank=True, null=True)
    conclusion = models.CharField(max_length=1000, blank=True, null=True)

    # func-related
    uuid = models.CharField(max_length=100, blank=True, null=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    sample_form_uuid = models.CharField(max_length=100, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)

    message_id = models.CharField(max_length=100, blank=True, null=True)
    approver = models.CharField(max_length=100, blank=True, null=True)

    """
    models for currenncy and amount
    """
    currency_unit = models.CharField(max_length=100, default='CNY',blank=True, null=True)
    amount_unit = models.CharField(max_length=100, default='kg',blank=True, null=True)
    currency_rate = models.CharField(max_length=100, default='1.0', blank=True, null=True)

    b_display =  models.CharField(default='1', max_length=100)

    class Meta:
        #ordering = ('user_id','user_name', 'user_password')
        permissions = (
            ("view_a_form", "可以查看 销售表单"),
            ("create_a_form", "可以新建 销售表单"),
            ("edit_a_form", "可以修改 销售表单"),
            ("is_a_salesman", "销售员工"),
            ("is_sales_manager", "销售经理"),
        )

class salesStatisticstable(models.Model):
    # briefInfo
    No = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    companyName = models.CharField(max_length=100, blank=True, null=True)
    contractNo = models.FileField(upload_to='uploadFiles/',blank=True, null=True)
    productType = models.CharField(max_length=100, blank=True, null=True)
    salesman = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    #
    Size = models.CharField(max_length=100, blank=True, null=True)
    orderAmount = models.CharField(max_length=100, blank=True, null=True)
    confirmDate = models.CharField(max_length=100, blank=True, null=True)
    productDue = models.CharField(max_length=100, blank=True, null=True)
    remainStorage = models.CharField(max_length=100, blank=True, null=True)

    #
    priceUnit = models.CharField(max_length=100, blank=True, null=True)
    orderPrice = models.CharField(max_length=100, blank=True, null=True)
    paymentMethod = models.CharField(max_length=100, blank=True, null=True)
    paymentDate = models.DateField(blank=True, null=True)

    """
    models for currenncy and amount
    """
    currency_unit = models.CharField(max_length=100, default='CNY', blank=True, null=True)
    amount_unit = models.CharField(max_length=100, default='kg',blank=True, null=True)
    currency_rate = models.CharField(max_length=100, default='1.0',blank=True, null=True)

    #
    shippingAmount = models.TextField(blank=True, null=True)
    shippingAmountActual = models.TextField(blank=True, null=True)
    shippingAmountDue = models.TextField(blank=True, null=True)

    #
    taxStatus = models.CharField(max_length=100, blank=True, null=True)
    deliveryStatus = models.CharField(max_length=100, blank=True, null=True)
    moneyStatus = models.CharField(max_length=100, blank=True, null=True)

    #
    comments = models.CharField(max_length=1000, blank=True, null=True)

    # func-related
    uuid = models.CharField(max_length=100, blank=True, null=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)

    b_display = models.CharField(default='1', max_length=100)


class message_model(models.Model):

    """
    key filed of message_model models:

    message_id: char(auto add an uuid)
    receiver_name: char
    requester_name: char(1 spec charater + 1 number + 1 uppper chacter)
    request_date: char
    status: choice ('new', 'read', 'completed')
    content: can be blank
    url: can be blank
    """

    message_id = models.CharField(max_length=255, primary_key=True)
    receiver_name = models.CharField(max_length=255)
    requester_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='NE')
    request_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)

    category = models.CharField(max_length=255, default='PR')
    size = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    order_amount = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    approver_name = models.CharField(max_length=255, blank=True, null=True)
    index = models.CharField(max_length=255, blank=True, null=True)

    producer_name = models.CharField(max_length=255, blank=True, null=True)

    requester_display =models.BooleanField(default=True)
    approver_display =models.BooleanField(default=True)
    buyer_display =models.BooleanField(default=True)
    receiver_display =models.BooleanField(default=True)
    producer_display =models.BooleanField(default=True)

    update_date = models.DateTimeField(blank=True, null=True)

    render_content = models.TextField(default=True,blank=True, null=True)

    """
    a new state machine for purchase 待打款 -> 物流单号 -> 采购完成
    """
    purchase_state = models.CharField(max_length=255,default=True,blank=True, null=True)

    class Meta:
        permissions = (
            ('is_approver', 'Approver,可以通过request请求'),
            ('is_buyer', '采购员工'),
            ('is_producer', '生产员工'),
            ('is_producer_manager', '生产经理'),
            ('is_quality', '质检部门权限'),
            ('is_special_user', '特殊观察权限'),
        )

class sample_form_model(models.Model):
    """
    a modoel for sample form
    """
    message_id = models.CharField(max_length=255, primary_key=True)
    index = models.CharField(max_length=255, blank=True, null=True)
    sale_index = models.CharField(max_length=255, default='', blank=True, null=True)
    create_date = models.CharField(max_length=255, blank=True, null=True)
    belong_to = models.CharField(max_length=255, blank=True, null=True)
    produce_status = models.CharField(max_length=255, blank=True, null=True)

    statement = models.CharField(max_length=255, blank=True, null=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    submit_date = models.DateField(blank=True, null=True)
    contact_person = models.CharField(max_length=255,blank=True, null=True)
    contact_person_phone = models.CharField(max_length=255,blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=255,blank=True, null=True)
    size = models.CharField(max_length=255,blank=True, null=True)
    amount = models.CharField(max_length=255,blank=True, null=True)
    requirement_0 = models.TextField(blank=True, null=True)
    requirement_1 = models.TextField(blank=True, null=True)
    requirement_2 = models.TextField(blank=True, null=True)
    sales_comment = models.TextField(blank=True, null=True)

    producer = models.CharField(max_length=255,blank=True, null=True)
    producer_date =  models.DateField(blank=True, null=True)
    approver = models.CharField(max_length=255,blank=True, null=True)
    approver_date =  models.DateField(blank=True, null=True)

    technical_comment = models.TextField(blank=True, null=True)
    technician = models.CharField(max_length=255,blank=True, null=True)
    technician_date =  models.DateField(blank=True, null=True)

    sales_editable = models.BooleanField(default=False)
    technical_editable = models.BooleanField(default=False)
    produce_editable = models.BooleanField(default=False)
    delivery_editable = models.BooleanField(default=False)

    producer_step_date_0 =  models.DateField(blank=True, null=True)
    producer_step_date_1 =  models.DateField(blank=True, null=True)
    producer_step_date_2 =  models.DateField(blank=True, null=True)
    producer_step_date_3 =  models.DateField(blank=True, null=True)
    producer_step_date_4 =  models.DateField(blank=True, null=True)
    producer_step_date_5 =  models.DateField(blank=True, null=True)

    planner = models.CharField(max_length=255,blank=True, null=True)
    planner_date =  models.DateField(blank=True, null=True)
    planner_comment = models.TextField(blank=True, null=True)

    produce_Nos = models.CharField(max_length=555,blank=True, null=True)
    produce_comment = models.TextField(blank=True, null=True)
    producian = models.CharField(max_length=256,blank=True, null=True)
    producian_date =  models.DateField(blank=True, null=True)

    deliver = models.CharField(max_length=245,blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    track_number = models.CharField(max_length=255,blank=True, null=True)
    delivery_date =  models.DateField(blank=True, null=True)

    manager = models.CharField(max_length=255,blank=True, null=True)
    manager_date =  models.DateField(blank=True, null=True)

    is_sample_form = models.BooleanField(default=True)
    sales_form_uuid = models.CharField(max_length=100, blank=True, null=True)
    """
    new field added to support reorder
    """
    is_display =  models.BooleanField(default=True)
    isnot_completed =  models.BooleanField(default=True)

    sequence = models.IntegerField(default=True)
    reorder = models.IntegerField(default=True)

    class Meta:
        permissions = (
            ('is_sample_producer', '样品生产员工'),
        )


class produce_statistics_pendai_model(models.Model):
    item_id = models.CharField(max_length=255, blank=True, null=True )
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_class =  models.CharField(max_length=255, blank=True, null=True)
    item_container =  models.CharField(max_length=255, blank=True, null=True)
    item_A =  models.CharField(max_length=255, blank=True, null=True)
    item_B =  models.CharField(max_length=255, blank=True, null=True)
    item_C =  models.CharField(max_length=255, blank=True, null=True)
    item_D =  models.CharField(max_length=255, blank=True, null=True)
    item_weight =  models.CharField(max_length=255, blank=True, null=True)
    item_usage =  models.CharField(max_length=255, blank=True, null=True)
    '''
    add new field
    '''
    item_new_usage = models.CharField(max_length=255, blank=True, null=True)
    item_goback_usage = models.CharField(max_length=255, blank=True, null=True)
    item_londerful_usage = models.CharField(max_length=255, blank=True, null=True)


    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=555, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100, primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)
    class Meta:
        permissions = (
            ('add_pendai_data', u"可以添加 喷带统计表数据"),
        )
class produce_statistics_gunjian_model(models.Model):
    item_id = models.CharField(max_length=255,  blank=True, null=True )
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_staff =  models.CharField(max_length=255, blank=True, null=True)
    item_machine =  models.CharField(max_length=255, blank=True, null=True)
    item_pass =  models.CharField(max_length=255, blank=True, null=True)
    item_fail =  models.CharField(max_length=255, blank=True, null=True)
    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=255, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100,primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)
    class Meta:
        permissions = (
            ('add_gunjian_data', u"可以添加 辊剪统计表数据"),
        )
class produce_statistics_tiexin_model(models.Model):
    item_id = models.CharField(max_length=255,  blank=True, null=True)
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_staff =  models.CharField(max_length=255, blank=True, null=True)
    item_material =  models.CharField(max_length=255, blank=True, null=True)
    item_amount =  models.CharField(max_length=255, blank=True, null=True)
    item_pass =  models.CharField(max_length=255, blank=True, null=True)
    item_fail =  models.CharField(max_length=255, blank=True, null=True)
    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=255, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100, primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)
    class Meta:
        permissions = (
            ('add_tiexin_data', u"可以添加 铁芯统计表数据"),
        )


class sample_statistics_pendai_model(models.Model):
    item_id = models.CharField(max_length=255, blank=True, null=True )
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_class =  models.CharField(max_length=255, blank=True, null=True)
    item_container =  models.CharField(max_length=255, blank=True, null=True)
    item_A =  models.CharField(max_length=255, blank=True, null=True)
    item_B =  models.CharField(max_length=255, blank=True, null=True)
    item_C =  models.CharField(max_length=255, blank=True, null=True)
    item_D =  models.CharField(max_length=255, blank=True, null=True)
    item_weight =  models.CharField(max_length=255, blank=True, null=True)
    item_usage =  models.CharField(max_length=255, blank=True, null=True)
    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=555, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100, primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)

class sample_statistics_gunjian_model(models.Model):
    item_id = models.CharField(max_length=255,  blank=True, null=True )
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_staff =  models.CharField(max_length=255, blank=True, null=True)
    item_machine =  models.CharField(max_length=255, blank=True, null=True)
    item_pass =  models.CharField(max_length=255, blank=True, null=True)
    item_fail =  models.CharField(max_length=255, blank=True, null=True)
    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=255, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100,primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)

class sample_statistics_tiexin_model(models.Model):
    item_id = models.CharField(max_length=255,  blank=True, null=True)
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_staff =  models.CharField(max_length=255, blank=True, null=True)
    item_material =  models.CharField(max_length=255, blank=True, null=True)
    item_amount =  models.CharField(max_length=255, blank=True, null=True)
    item_pass =  models.CharField(max_length=255, blank=True, null=True)
    item_fail =  models.CharField(max_length=255, blank=True, null=True)
    item_rate =  models.CharField(max_length=255, blank=True, null=True)
    item_comment =  models.CharField(max_length=255, blank=True, null=True)
    purchase_Nos =  models.CharField(max_length=555, blank=True, null=True)
    # func-related
    uuid = models.CharField(max_length=100, primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    storage_item_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)


class capital_model(models.Model):
    """
    分类	品名规格	价格	数量	总值	最后录入时间	地点	备注
    """
    uuid =  models.CharField(max_length=355,  blank=True, null=True)
    category =  models.CharField(max_length=255,  blank=True, null=True)
    size =  models.CharField(max_length=555,  blank=True, null=True)
    price =  models.CharField(max_length=255,  blank=True, null=True)
    amount =  models.CharField(max_length=255,  blank=True, null=True)
    total_price =  models.CharField(max_length=255,  blank=True, null=True)
    last_update_time =   models.DateField(auto_now=True, null=True)
    place =  models.CharField(max_length=255,  blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)
    comment =  models.TextField( blank=True, null=True)
    class Meta:
        permissions = (
                ('edit_capital_info', u"可以编辑固定资产表"),
            )

class check_model(models.Model):
    """
    日期	盘点人员	盘点说明
    """
    uuid =  models.CharField(max_length=255,  blank=True, null=True)
    last_update_time =   models.DateField(auto_now=True, null=True)
    staff =  models.CharField(max_length=255,  blank=True, null=True)
    b_display =  models.CharField(default='1',max_length=255,  blank=True, null=True)
    comment =  models.TextField( blank=True, null=True)
    class Meta:
        permissions = (
                ('edit_check_info', u"可以编辑盘点表"),
            )

class storage_delivery_model(models.Model):
    delivery_id = models.CharField(max_length=255, primary_key=True)
    sales_No = models.CharField(default='N/A', max_length=255)
    contract_No = models.CharField(max_length=255)
    update_date = models.DateField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    customer =  models.CharField(max_length=255, blank=True, null=True)
    delivery_No =  models.CharField(max_length=255, blank=True, null=True)
    delivery_amount =  models.CharField(max_length=255, blank=True, null=True)
    delivery_status =  models.CharField(max_length=255, blank=True, null=True)
    delivery_track_No =  models.CharField(max_length=255, blank=True, null=True)
    delivery_comment =  models.CharField(max_length=254, blank=True, null=True)
    b_display =  models.CharField(default='1',max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
            ('add_delivery_model', u"添加物流信息"),
        )

class storage_product_out_model(models.Model):
    delivery_id = models.CharField(max_length=255, primary_key=True)
    contract_No = models.CharField(max_length=255)
    update_date = models.DateField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    customer =  models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    b_display =  models.CharField(default='1',max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
            ('edit_product_out_model', u"编辑成品出库信息"),
        )

class storage_source_out_model(models.Model):
    delivery_id = models.CharField(max_length=255, primary_key=True)
    update_date = models.DateField(blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_size = models.CharField(max_length=355, blank=True, null=True)
    No =  models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    user  = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
            ('edit_source_out_model', u"编辑原料出库信息"),
        )

import datetime
class user_model_extend(models.Model):
    """
    using username as primary key, an extension for user model
    """
    username = models.CharField(max_length=255, primary_key=True)
    profile_image = models.ImageField(blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    backup_email = models.CharField(max_length=255, blank=True, null=True)
    backup_mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    manager = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(max_length=255, blank=True, null=True)
    identity = models.CharField(max_length=255, blank=True, null=True)
    """
    hr extension
    """
    londerful_id = models.CharField(max_length=255, default='' ,blank=True, null=True)
    fullname = models.CharField(max_length=255, default='' ,blank=True, null=True)
    department = models.CharField(max_length=255, default='' ,blank=True, null=True)
    job = models.CharField(max_length=255, default='' ,blank=True, null=True)
    gender = models.CharField(max_length=255, default='' ,blank=True, null=True)
    nationality = models.CharField(max_length=255, default='' ,blank=True, null=True)
    birth_place = models.CharField(max_length=255, default='' ,blank=True, null=True)
    on_board_time = models.CharField(max_length=255, default='' ,blank=True, null=True)
    contract_start_time = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    contract_end_time = models.DateField(default=django.utils.timezone.now,blank=True, null=True)
    first_level_manager = models.CharField(max_length=255, default='' ,blank=True, null=True)
    second_level_manager = models.CharField(max_length=255, default='' ,blank=True, null=True)
    direct_report = models.CharField(max_length=255, default='' ,blank=True, null=True)
    identity_address = models.CharField(max_length=255, default='' ,blank=True, null=True)
    insurance = models.CharField(max_length=255, default='' ,blank=True, null=True)
    insurance_date = models.DateField(default=django.utils.timezone.now,blank=True, null=True)
    education = models.CharField(max_length=255, default='' ,blank=True, null=True)
    level = models.CharField(max_length=255, default='' ,blank=True, null=True)
    college = models.CharField(max_length=255, default='' ,blank=True, null=True)
    major = models.CharField(max_length=255, default='' ,blank=True, null=True)
    score = models.CharField(max_length=255, default='' ,blank=True, null=True)
    computer_skill = models.CharField(max_length=255, default='' ,blank=True, null=True)
    foreign_language = models.CharField(max_length=255, default='' ,blank=True, null=True)
    foreign_language_level = models.CharField(max_length=255, default='' ,blank=True, null=True)
    train_record = models.TextField(default='' ,blank=True, null=True)
    assessment_record = models.TextField(default='' ,blank=True, null=True)
    comment = models.TextField(default='' ,blank=True, null=True)
    time =  models.TextField(default='' ,blank=True, null=True)
    tutor =  models.TextField(default='' ,blank=True, null=True)
    topic =  models.TextField(default='' ,blank=True, null=True)
    result =  models.TextField(default='' ,blank=True, null=True)


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_address','customer_contact', 'customer_mobile', 'customer_rank')

class customer_model(models.Model):
    customer_name = models.CharField(max_length=255, default='N/A',primary_key=True)
    customer_rank = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_address = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_contact = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_mobile = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_comment = models.TextField(default='N/A',blank=True, null=True)
    customer_backup = models.TextField(default='N/A',blank=True, null=True)
    customer_email = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_fax = models.CharField(max_length=255, default='N/A', blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=100)
    customer_mobile2 = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_contact2 = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_email2 = models.CharField(max_length=255, default='N/A',blank=True, null=True)
    customer_fax2 = models.CharField(max_length=255, default='N/A', blank=True, null=True)

    class Meta:
        verbose_name = u"客户"
        verbose_name_plural  = u"客户"
        permissions = (
                ('modify_rank_customer', u"调整客户等级"),
            )


"""
Models for currency and amount
"""
class CurrencyModelAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_comment')

class currency_model(models.Model):
    currency_uuid = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    currency_comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = u"货币单位"
        verbose_name_plural  = u"货币单位"
        permissions = (
                ('modify_archive', u"可以编辑档案信息"),
            )

class AmountModelAdmin(admin.ModelAdmin):
    list_display = ('amount_name', 'amount_comment')

class amount_model(models.Model):
    amount_uuid = models.CharField(max_length=255, blank=True, null=True)
    amount_name = models.CharField(max_length=255, blank=True, null=True)
    amount_comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = u"物件计量单位"
        verbose_name_plural  = u"物件计量单位"


class warning_threshold_model(models.Model):
    size = models.CharField(max_length=255, blank=True, null=True)
    warning_threshold = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        permissions = (
            ('edit_threshold', u"编辑预警值信息"),
        )

class SettingSizeModelAdmin(admin.ModelAdmin):
    list_display = ('size_name', 'size_comment')
    list_filter = ('size_comment',)
    search_fields=('size_name',)

class setting_size_model(models.Model):
    size_uuid = models.CharField(max_length=255, blank=True, null=True)
    size_name = models.CharField(max_length=255, blank=True, null=True)
    size_comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = u"全部规格"
        verbose_name_plural  = u"全部规格"
        permissions = (
                ('modify_size', u"可以编辑规格信息"),
            )