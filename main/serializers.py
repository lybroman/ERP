#-------------------------------------------------------------------------------
# Name:        serializers
# Purpose:
#
# Author:      yuboli
#
# Created:     22/12/2015
# Copyright:   (c) yuboli 2015
# Licence:     yubo.li@intel.com
#-------------------------------------------------------------------------------
from rest_framework import serializers
import django
from main.models import user_control_model
from main.models import salesExetable, salesStatisticstable, message_model, sample_form_model, user_model_extend, customer_model, warning_threshold_model

'''
class user_control_model_serializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, blank=True, default='')
    user_name = serializers.CharField(max_length=100, blank=True, default='')
    user_password = serializers.CharField(max_length=100, blank=True, default='')
    user_email = serializers.CharField(max_length=100, blank=True, default='')
    user_permission_level = serializers.CharField(max_length=100, blank=True, default='')
    user_title = serializers.CharField(max_length=100, blank=True, default='')
    user_next_level_manager = serializers.CharField(max_length=100, blank=True, default='')

    def create(self, validated_data):
        """
        Create and return a new `user_control_model` instance, given the validated data.
        """
        return user_control_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `user_control_model` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.user_password = validated_data.get('user_password', instance.user_password)
        instance.user_email = validated_data.get('user_email', instance.user_email)
        instance.user_permission_level = validated_data.get('user_permisson_level', instance.user_permisson_level)
        instance.user_title = validated_data.get('user_title', instance.user_title)
        instance.user_next_level_manager = validated_data.get('user_next_level_manager', instance.user_next_level_manager)
        instance.save()
        return instance
'''

class salesExetableSerializer(serializers.Serializer):
    # briefInfo
    No = serializers.CharField(max_length=100, default='', allow_null=True)
    companyName = serializers.CharField(max_length=100, default='', allow_null=True)
    salesman = serializers.CharField(max_length=100, default='', allow_null=True)
    companyInfo = serializers.CharField(max_length=100, default='', allow_null=True)
    country = serializers.CharField(max_length=100, default='', allow_null=True)
    productType = serializers.CharField(max_length=100, default='', allow_null=True)

    # contactInfo
    date = serializers.DateField(default='', allow_null=True)
    productCode = serializers.CharField(max_length=100, default='', allow_null=True)
    mag = serializers.CharField(max_length=100, default='', allow_null=True)
    specification = serializers.FileField(max_length=100, default='', allow_null=True)
    quantityDemand = serializers.CharField(max_length=100, default='', allow_null=True)
    opponent = serializers.CharField(max_length=100, default='', allow_null=True)
    quantityActual = serializers.CharField(max_length=100, default='', allow_null=True)
    assessment = serializers.CharField(max_length=100, default='', allow_null=True)
    priceUnit = serializers.CharField(max_length=100, default='', allow_null=True)
    priceTotal = serializers.CharField(max_length=100, default='', allow_null=True)
    payment = serializers.CharField(max_length=100, default='', allow_null=True)

    # progressPlanning
    supplierP = serializers.CharField(max_length=100, default='', allow_null=True)
    inquiryP = serializers.CharField(max_length=100, default='', allow_null=True)
    quoteP = serializers.CharField(max_length=100, default='', allow_null=True)
    sampleP = serializers.CharField(max_length=100, default='', allow_null=True)
    testP = serializers.CharField(max_length=100, default='', allow_null=True)
    smallOrderP = serializers.CharField(max_length=100, default='', allow_null=True)

    # progressActual
    supplier = serializers.CharField(max_length=100, default='', allow_null=True)
    dateDeliver = serializers.DateField(default='', allow_null=True)
    sampleNum = serializers.CharField(max_length=100, default='', allow_null=True)
    sampleNo = serializers.FileField(max_length=100, default='', allow_null=True)
    test = serializers.CharField(max_length=100, default='', allow_null=True)
    smallOrder = serializers.FileField(max_length=100, default='', allow_null=True)

    # quote
    dateQuote = serializers.DateField(default='', allow_null=True)
    quoteApply = serializers.CharField(max_length=100, default='', allow_null=True)
    quoteOrder = serializers.FileField(max_length=100, default='', allow_null=True)

    # order
    dateOrder = serializers.DateField(default='', allow_null=True)
    orderNo = serializers.FileField(max_length=100, default='', allow_null=True)
    orderInfo = serializers.CharField(max_length=100, default='', allow_null=True)

    # contract
    dateContract = serializers.DateField(default='', allow_null=True)
    contractNo = serializers.FileField(max_length=100, default='', allow_null=True)
    contractInfo = serializers.CharField(max_length=100, default='', allow_null=True)

    # sample
    contractReviewNoS = serializers.FileField(max_length=100, default='', allow_null=True)
    salesNoS = serializers.FileField(max_length=100, default='', allow_null=True)

    # product
    contractReviewNoP = serializers.FileField(max_length=100, default='', allow_null=True)
    salesNoP = serializers.FileField(max_length=100, default='', allow_null=True)

    # produce
    produceNo = serializers.FileField(max_length=100, default='', allow_null=True)
    produceStatus = serializers.CharField(max_length=100, default='', allow_null=True)
    transNo = serializers.CharField(max_length=100, default='', allow_null=True)

    # others
    comments = serializers.CharField(max_length=1000, default='', allow_null=True)
    personCharge = serializers.CharField(max_length=100, default='', allow_null=True)
    personSupervise = serializers.CharField(max_length=100, default='', allow_null=True)
    conclusion = serializers.CharField(max_length=1000, default='', allow_null=True)

    # func-related
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    sample_form_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)

    currency_unit = serializers.CharField(max_length=100, default='CNY', allow_null=True)
    amount_unit = serializers.CharField(max_length=100, default='KG', allow_null=True)
    currency_rate = serializers.CharField(max_length=100, default='1.0', allow_null=True)

    message_id = serializers.CharField(max_length=100, default='', allow_null=True)
    approver = serializers.CharField(max_length=100, default='', allow_null=True)

    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `salesExetable` instance, given the validated data.
        """
        return salesExetable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `salesExetable` instance, given the validated data.
        """
        # briefInfo
        instance.No = validated_data.get('No', instance.No)
        instance.companyName =  validated_data.get('companyName', instance.companyName)
        instance.salesman =  validated_data.get('salesman', instance.salesman)
        instance.companyInfo =  validated_data.get('companyInfo', instance.companyInfo)
        instance.country =  validated_data.get('country', instance.country)
        instance.productType =  validated_data.get('productType', instance.productType)
        # contactInfo
        instance.date =  validated_data.get('date', instance.date)
        instance.productCode =  validated_data.get('productCode', instance.productCode)
        instance.mag =  validated_data.get('mag', instance.mag)
        instance.specification =  validated_data.get('specification', instance.specification)
        instance.quantityDemand =  validated_data.get('quantityDemand', instance.quantityDemand)
        instance.opponent =  validated_data.get('opponent', instance.opponent)
        instance.quantityActual =  validated_data.get('quantityActual', instance.quantityActual)
        instance.assessment =  validated_data.get('assessment', instance.assessment)
        instance.priceUnit =  validated_data.get('priceUnit', instance.priceUnit)
        instance.priceTotal =  validated_data.get('priceTotal', instance.priceTotal)
        instance.payment =  validated_data.get('payment', instance.payment)
        # progressPlanning
        instance.supplierP =  validated_data.get('supplierP', instance.supplierP)
        instance.inquiryP =  validated_data.get('inquiryP', instance.inquiryP)
        instance.quoteP =  validated_data.get('quoteP', instance.quoteP)
        instance.sampleP =  validated_data.get('sampleP', instance.sampleP)
        instance.testP =  validated_data.get('testP', instance.testP)
        instance.smallOrderP =  validated_data.get('smallOrderP', instance.smallOrderP)
        # progressActual
        instance.supplier =  validated_data.get('supplier', instance.supplier)
        instance.dateDeliver =  validated_data.get('dateDeliver', instance.dateDeliver)
        instance.sampleNum =  validated_data.get('sampleNum', instance.sampleNum)
        instance.sampleNo =  validated_data.get('sampleNo', instance.sampleNo)
        instance.test =  validated_data.get('test', instance.test)
        instance.smallOrder =  validated_data.get('smallOrder', instance.smallOrder)
        # quote
        instance.dateQuote =  validated_data.get('dateQuote', instance.dateQuote)
        instance.quoteApply =  validated_data.get('quoteApply', instance.quoteApply)
        instance.quoteOrder =  validated_data.get('quoteOrder', instance.quoteOrder)
        # orders
        instance.dateOrder =  validated_data.get('dateOrder', instance.dateOrder)
        instance.orderNo =  validated_data.get('orderNo', instance.orderNo)
        instance.orderInfo =  validated_data.get('orderInfo', instance.orderInfo)
        # contract
        instance.dateContract =  validated_data.get('dateContract', instance.dateContract)
        instance.contractNo =  validated_data.get('contractNo', instance.contractNo)
        instance.contractInfo =  validated_data.get('contractInfo', instance.contractInfo)
        # sample
        instance.contractReviewNoS =  validated_data.get('contractReviewNoS', instance.contractReviewNoS)
        instance.salesNoS =  validated_data.get('salesNoS', instance.salesNoS)
        # product
        instance.contractReviewNoP =  validated_data.get('contractReviewNoP', instance.contractReviewNoP)
        instance.salesNoP =  validated_data.get('salesNoP', instance.salesNoP)
        # produce
        instance.produceNo =  validated_data.get('produceNo', instance.produceNo)
        instance.produceStatus =  validated_data.get('produceStatus', instance.produceStatus)
        instance.transNo =  validated_data.get('transNo', instance.transNo)
        # others
        instance.comments =  validated_data.get('comments', instance.comments)
        instance.personCharge =  validated_data.get('personCharge', instance.personCharge)
        instance.personSupervise =  validated_data.get('personSupervise', instance.personSupervise)
        instance.conclusion =  validated_data.get('conclusion', instance.conclusion)
        # func-related
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.sample_form_uuid =  validated_data.get('sample_form_uuid', instance.sample_form_uuid)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)

        instance.message_id =  validated_data.get('message_id', instance.message_id)
        instance.approver =  validated_data.get('approver', instance.approver)

        instance.currency_unit =  validated_data.get('currency_unit', instance.currency_unit)
        instance.currency_rate =  validated_data.get('currency_rate', instance.currency_rate)
        instance.amount_unit =  validated_data.get('amount_unit', instance.amount_unit)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance


class salesStatisticstableSerializer(serializers.Serializer):
    # briefInfo
    No = serializers.CharField(max_length=100, default='', allow_null=True)
    date = serializers.DateField(default='', allow_null=True)
    companyName = serializers.CharField(max_length=100, default='', allow_null=True)
    contractNo = serializers.FileField(max_length=100, default='', allow_null=True)
    productType = serializers.CharField(max_length=100, default='', allow_null=True)
    salesman = serializers.CharField(max_length=100, default='', allow_null=True)
    country = serializers.CharField(max_length=100, default='', allow_null=True)

    #
    Size = serializers.CharField(max_length=100, default='', allow_null=True)
    orderAmount = serializers.CharField(max_length=100, default='', allow_null=True)
    confirmDate = serializers.CharField(max_length=100, default='', allow_null=True)
    productDue = serializers.CharField(max_length=100, default='', allow_null=True)
    remainStorage = serializers.CharField(max_length=100, default='', allow_null=True)

    #
    priceUnit = serializers.CharField(max_length=100, default='', allow_null=True)
    orderPrice = serializers.CharField(max_length=100, default='', allow_null=True)
    paymentMethod = serializers.CharField(max_length=100, default='', allow_null=True)
    paymentDate = serializers.DateField(default='', allow_null=True)

    currency_unit = serializers.CharField(max_length=100, default='CNY', allow_null=True)
    amount_unit = serializers.CharField(max_length=100, default='KG', allow_null=True)
    currency_rate = serializers.CharField(max_length=100, default='1.0', allow_null=True)

    #
    shippingAmount = serializers.CharField(default='', allow_null=True)
    shippingAmountActual = serializers.CharField(default='', allow_null=True)
    shippingAmountDue = serializers.CharField(default='', allow_null=True)

    #
    taxStatus = serializers.CharField(max_length=100, default='', allow_null=True)
    deliveryStatus = serializers.CharField(max_length=100, default='', allow_null=True)
    moneyStatus = serializers.CharField(max_length=100, default='', allow_null=True)

    #
    comments = serializers.CharField(max_length=100, default='', allow_null=True)

    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `dut_management_model` instance, given the validated data.
        """
        return salesStatisticstable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `dut_management_model` instance, given the validated data.
        """
        # briefInfo
        instance.No = validated_data.get('No', instance.No)
        instance.date =  validated_data.get('date', instance.date)
        instance.companyName =  validated_data.get('companyName', instance.companyName)
        instance.contractNo =  validated_data.get('contractNo', instance.contractNo)
        instance.productType =  validated_data.get('productType', instance.productType)
        instance.salesman =  validated_data.get('salesman', instance.salesman)
        instance.country =  validated_data.get('country', instance.country)
        #
        instance.Size =  validated_data.get('Size', instance.Size)
        instance.orderAmount =  validated_data.get('orderAmount', instance.orderAmount)
        instance.confirmDate =  validated_data.get('confirmDate', instance.confirmDate)
        instance.productDue =  validated_data.get('productDue', instance.productDue)
        instance.remainStorage =  validated_data.get('remainStorage', instance.remainStorage)

        instance.priceUnit =  validated_data.get('priceUnit', instance.priceUnit)
        instance.orderPrice =  validated_data.get('orderPrice', instance.orderPrice)
        instance.paymentMethod =  validated_data.get('paymentMethod', instance.paymentMethod)
        instance.paymentDate =  validated_data.get('paymentDate', instance.paymentDate)

        instance.shippingAmount =  validated_data.get('shippingAmount', instance.shippingAmount)
        instance.shippingAmountActual =  validated_data.get('shippingAmountActual', instance.shippingAmountActual)
        instance.shippingAmountDue =  validated_data.get('shippingAmountDue', instance.shippingAmountDue)

        instance.taxStatus =  validated_data.get('taxStatus', instance.taxStatus)
        instance.deliveryStatus =  validated_data.get('deliveryStatus', instance.deliveryStatus)
        instance.moneyStatus =  validated_data.get('moneyStatus', instance.moneyStatus)

        instance.comments =  validated_data.get('comments', instance.comments)
        # func-related
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)

        instance.currency_unit =  validated_data.get('currency_unit', instance.currency_unit)
        instance.currency_rate =  validated_data.get('currency_rate', instance.currency_rate)
        instance.amount_unit =  validated_data.get('amount_unit', instance.amount_unit)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance


class message_model_serializer(serializers.Serializer):
    """
    message_id = models.CharField(primary_key=True)
    receiver_name = models.CharField()
    requester_name = models.CharField()
    request_date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)
    """
    message_id = serializers.CharField()
    receiver_name = serializers.CharField()
    requester_name = serializers.CharField()
    status = serializers.CharField(default='NE')
    request_date = serializers.DateTimeField()
    content = serializers.CharField(allow_blank=True, default='')
    url = serializers.CharField(allow_blank=True, default='')

    title = serializers.CharField()

    category = serializers.CharField(allow_blank=True, default='')
    size = serializers.CharField(allow_blank=True, default='')
    unit = serializers.CharField(allow_blank=True, default='')
    order_amount = serializers.CharField(allow_blank=True, default='')
    total_price = serializers.CharField(allow_blank=True, default='')
    due_date = serializers.DateTimeField()
    buyer_name = serializers.CharField(allow_blank=True, default='')
    approver_name = serializers.CharField(allow_blank=True, default='')
    index = serializers.CharField(default='')
    producer_name = serializers.CharField(allow_blank=True, default='')

    requester_display = serializers.BooleanField(default=True)
    approver_display = serializers.BooleanField(default=True)
    buyer_display = serializers.BooleanField(default=True)
    receiver_display = serializers.BooleanField(default=True)
    producer_display = serializers.BooleanField(default=True)

    update_date = serializers.DateTimeField()

    render_content = serializers.CharField(default='')

    purchase_state = serializers.CharField(default='N/A')

    def create(self, validated_data):
        """
        Create and return a new `message_model` instance, given the validated data.
        """
        return message_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `message_model` instance, given the validated data.
        """
        instance.message_id = validated_data.get('message_id', instance.message_id)
        instance.receiver_name = validated_data.get('receiver_name', instance.receiver_name)
        instance.requester_name = validated_data.get('requester_name', instance.requester_name)
        instance.status = validated_data.get('status', instance.status)
        instance.request_date = validated_data.get('request_date', instance.request_date)
        instance.content = validated_data.get('content', instance.content)
        instance.url = validated_data.get('url', instance.url)
        instance.message_title = validated_data.get('title', instance.title)

        instance.category = validated_data.get('category', instance.category)
        instance.size = validated_data.get('size', instance.size)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.order_amount = validated_data.get('order_amount', instance.order_amount)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.buyer_name = validated_data.get('buyer_name', instance.buyer_name)
        instance.approver_name = validated_data.get('approver_name', instance.buyer_name)
        instance.index = validated_data.get('index', instance.index)

        instance.requester_display = validated_data.get('requester_display', instance.requester_display)
        instance.approver_display = validated_data.get('approver_display', instance.approver_display)
        instance.buyer_display = validated_data.get('buyer_display', instance.buyer_display)
        instance.receiver_display = validated_data.get('receiver_display', instance.receiver_display)

        instance.update_date = validated_data.get('update_date', instance.update_date)
        instance.producer_name = validated_data.get('producer_name', instance.producer_name)
        instance.render_content = validated_data.get('render_content', instance.render_content)
        instance.purchase_state = validated_data.get('purchase_state', instance.purchase_state)
        instance.save()
        return instance

class sample_form_model_serializer(serializers.Serializer):
    message_id = serializers.CharField(max_length=255)
    index = serializers.CharField(max_length=255)
    sale_index = serializers.CharField(max_length=255,default='')
    create_date = serializers.CharField(max_length=255)
    belong_to = serializers.CharField(max_length=255, allow_blank=True, default='')
    produce_status = serializers.CharField(max_length=255, allow_blank=True, default='')

    statement = serializers.CharField()
    customer = serializers.CharField()
    submit_date = serializers.DateField(default=None, allow_null=True)
    contact_person = serializers.CharField(max_length=255, allow_blank=True)
    contact_person_phone = serializers.CharField(max_length=255, allow_blank=True)
    due_date = serializers.DateField(default=None, allow_null=True)
    category = serializers.CharField()
    size = serializers.CharField()
    amount = serializers.CharField()
    requirement_0 = serializers.CharField(allow_blank=True, default='')
    requirement_1 = serializers.CharField(allow_blank=True, default='')
    requirement_2 = serializers.CharField(allow_blank=True, default='')
    sales_comment = serializers.CharField(allow_blank=True, default='')

    producer = serializers.CharField(allow_blank=True, default='')
    producer_date =  serializers.DateField(default=None, allow_null=True)
    approver = serializers.CharField(allow_blank=True, default='')
    approver_date =  serializers.DateField(default=None, allow_null=True)

    technical_comment = serializers.CharField(allow_blank=True, default='')
    technician = serializers.CharField(allow_blank=True, default='')
    technician_date =  serializers.DateField(default=None, allow_null=True)

    sales_editable = serializers.BooleanField(default=False)
    technical_editable = serializers.BooleanField(default=False)
    produce_editable = serializers.BooleanField(default=False)
    delivery_editable = serializers.BooleanField(default=False)

    producer_step_date_0 =  serializers.DateField(default=None, allow_null=True)
    producer_step_date_1 =  serializers.DateField(default=None, allow_null=True)
    producer_step_date_2 =  serializers.DateField(default=None, allow_null=True)
    producer_step_date_3 =  serializers.DateField(default=None, allow_null=True)
    producer_step_date_4 =  serializers.DateField(default=None, allow_null=True)
    producer_step_date_5 =  serializers.DateField(default=None, allow_null=True)

    planner = serializers.CharField(allow_blank=True, default='')
    planner_date =  serializers.DateField(default=None, allow_null=True)
    planner_comment = serializers.CharField(allow_blank=True, default='')

    produce_Nos = serializers.CharField(allow_blank=True, default='')
    produce_comment = serializers.CharField(allow_blank=True, default='')
    producian = serializers.CharField(allow_blank=True, default='')
    producian_date =  serializers.DateField(default=None, allow_null=True)

    deliver = serializers.CharField(allow_blank=True, default='')
    delivery_address = serializers.CharField(allow_blank=True, default='')
    track_number = serializers.CharField(allow_blank=True, default='')
    delivery_date =  serializers.DateField(default=None, allow_null=True)

    manager = serializers.CharField(allow_blank=True, default='')
    manager_date =  serializers.DateField(default=None, allow_null=True)

    is_sample_form = serializers.BooleanField(default=True)

    is_display =  serializers.BooleanField(default=True)
    isnot_completed =  serializers.BooleanField(default=False)
    sequence = serializers.IntegerField(allow_null=True, default=-1)
    reorder = serializers.IntegerField(allow_null=True, default=-1)
    sales_form_uuid = serializers.CharField(max_length=100, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `sample_form_model_` instance, given the validated data.
        """
        return sample_form_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `sample_form_model_` instance, given the validated data.
        """
        instance.message_id = validated_data.get('message_id', instance.message_id)
        instance.index = validated_data.get('index', instance.index)
        instance.sale_index = validated_data.get('sale_index', instance.sale_index)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.belong_to = validated_data.get('belong_to', instance.belong_to)
        instance.produce_status = validated_data.get('produce_status', instance.produce_status)

        instance.statement = validated_data.get('statement', instance.statement)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.submit_date = validated_data.get('submit_date', instance.submit_date)
        instance.contact_person = validated_data.get('contact_person', instance.contact_person)
        instance.contact_person_phone = validated_data.get('contact_person_phone', instance.contact_person_phone)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.size = validated_data.get('size', instance.size)
        instance.category = validated_data.get('category', instance.category)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.requirement_0 = validated_data.get('requirement_0', instance.requirement_0)
        instance.requirement_1 = validated_data.get('requirement_1', instance.requirement_1)
        instance.requirement_2 = validated_data.get('requirement_2', instance.requirement_2)
        instance.sales_comment = validated_data.get('sales_comment', instance.sales_comment)

        instance.producer = validated_data.get('producer', instance.producer)
        instance.producer_date =  validated_data.get('producer_date', instance.producer_date)
        instance.approver = validated_data.get('approver', instance.approver)
        instance.approver_date =  validated_data.get('approver_date', instance.approver_date)

        instance.technical_comment = validated_data.get('technical_comment', instance.technical_comment)
        instance.technician = validated_data.get('technician', instance.technician)
        instance.technician_date =  validated_data.get('technician_date', instance.technician_date)

        instance.sales_editable = validated_data.get('sales_editable', instance.sales_editable)
        instance.technical_editable = validated_data.get('technical_editable', instance.technical_editable)
        instance.produce_editable = validated_data.get('produce_editable', instance.produce_editable)
        instance.delivery_editable = validated_data.get('delivery_editable', instance.delivery_editable)

        instance.producer_step_date_0 =  validated_data.get('producer_step_date_0', instance.producer_step_date_0)
        instance.producer_step_date_1 =  validated_data.get('producer_step_date_1', instance.producer_step_date_1)
        instance.producer_step_date_2 =  validated_data.get('producer_step_date_2', instance.producer_step_date_2)
        instance.producer_step_date_3 =  validated_data.get('producer_step_date_3', instance.producer_step_date_3)
        instance.producer_step_date_4 =  validated_data.get('producer_step_date_4', instance.producer_step_date_4)
        instance.producer_step_date_5 =  validated_data.get('producer_step_date_5', instance.producer_step_date_5)

        instance.planner = validated_data.get('planner', instance.planner)
        instance.planner_date =  validated_data.get('planner_date', instance.planner_date)
        instance.planner_comment = validated_data.get('planner_comment', instance.planner_comment)

        instance.produce_Nos = validated_data.get('produce_Nos', instance.produce_Nos)
        instance.produce_comment = validated_data.get('produce_comment', instance.produce_comment)
        instance.producian = validated_data.get('producian', instance.producian)
        instance.producian_date =  validated_data.get('producian_date', instance.producian_date)

        instance.deliver = validated_data.get('deliver', instance.deliver)
        instance.delivery_address = validated_data.get('delivery_address', instance.delivery_address)
        instance.track_number = validated_data.get('track_number', instance.track_number)
        instance.delivery_date =  validated_data.get('delivery_date', instance.delivery_date)

        instance.manager = validated_data.get('manager', instance.manager)
        instance.manager_date =  validated_data.get('manager_date', instance.manager_date)

        instance.is_sample_form =  validated_data.get('is_sample_form', instance.is_sample_form)
        instance.is_display =  validated_data.get('is_display', instance.is_display)
        instance.isnot_completed =  validated_data.get('isnot_completed', instance.isnot_completed)
        instance.sequence =  validated_data.get('sequence', instance.sequence)
        instance.reorder =  validated_data.get('reorder', instance.reorder)
        instance.sales_form_uuid =  validated_data.get('sales_form_uuid', instance.sales_form_uuid)

        instance.save()
        return instance

import datetime
class user_model_extend_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    profile_image = serializers.ImageField(allow_null=True)
    mobile = serializers.CharField(max_length=255, allow_blank=True, default='')
    email = serializers.CharField(max_length=255, allow_blank=True, default='')
    backup_email = serializers.CharField(max_length=255, allow_blank=True, default='')
    backup_mobile = serializers.CharField(max_length=255, allow_blank=True, default='')
    address = serializers.CharField(max_length=255, allow_blank=True, default='')
    comment = serializers.CharField(max_length=255, allow_blank=True, default='')
    manager = serializers.CharField(max_length=255, allow_blank=True, default='')
    birthday = serializers.DateField(default=None, allow_null=True)
    identity = serializers.CharField(max_length=255, allow_blank=True, default='')

    """
    hr
    """
    londerful_id = serializers.CharField(max_length=255, allow_blank=True, default='')
    fullname = serializers.CharField(max_length=255, allow_blank=True, default='')
    department = serializers.CharField(max_length=255, allow_blank=True, default='')
    job = serializers.CharField(max_length=255, allow_blank=True, default='')
    gender = serializers.CharField(max_length=255, allow_blank=True, default='')
    nationality = serializers.CharField(max_length=255, allow_blank=True, default='')
    birth_place = serializers.CharField(max_length=255, allow_blank=True, default='')
    on_board_time = serializers.CharField(max_length=255, allow_blank=True, default='')
    contract_start_time = serializers.DateField(default=django.utils.timezone.now, allow_null=True)
    contract_end_time = serializers.DateField(default=django.utils.timezone.now,allow_null=True)
    first_level_manager = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    second_level_manager = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    direct_report = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    identity_address = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    insurance = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    insurance_date = serializers.DateField(default=django.utils.timezone.now,allow_null=True)
    education = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    level = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    college = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    major = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    score = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    computer_skill = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    foreign_language = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    foreign_language_level = serializers.CharField(max_length=255, default='' ,allow_blank=True)
    train_record = serializers.CharField(default='' ,allow_blank=True)
    assessment_record = serializers.CharField(default='' ,allow_blank=True)
    comment = serializers.CharField(default='' ,allow_blank=True)
    time =  serializers.CharField(default='' ,allow_blank=True)
    tutor = serializers.CharField(default='' ,allow_blank=True)
    topic =  serializers.CharField(default='' ,allow_blank=True)
    result = serializers.CharField(default='' ,allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `user_model_extend` instance, given the validated data.
        """
        return user_model_extend.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `user_model_extend` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.backup_email = validated_data.get('backup_email', instance.backup_email)
        instance.backup_mobile = validated_data.get('backup_mobile', instance.backup_mobile)
        instance.address = validated_data.get('address', instance.address)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.identity = validated_data.get('identity', instance.identity)
        """
        hr
        """
        instance.londerful_id = validated_data.get('londerful_id', instance.londerful_id)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.department = validated_data.get('department', instance.department)
        instance.job = validated_data.get('job', instance.job)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.birth_place = validated_data.get('birth_place', instance.birth_place)
        instance.on_board_time = validated_data.get('on_board_time', instance.on_board_time)
        instance.contract_start_time = validated_data.get('contract_start_time', instance.contract_start_time)
        instance.contract_end_time = validated_data.get('contract_end_time', instance.contract_end_time)
        instance.first_level_manager = validated_data.get('first_level_manager', instance.first_level_manager)
        instance.second_level_manager = validated_data.get('second_level_manager', instance.second_level_manager)
        instance.direct_report = validated_data.get('direct_report', instance.direct_report)
        instance.identity_address = validated_data.get('identity_address', instance.identity_address)
        instance.insurance = validated_data.get('insurance', instance.insurance)
        instance.insurance_date = validated_data.get('insurance_date', instance.insurance_date)
        instance.education = validated_data.get('education', instance.education)
        instance.level = validated_data.get('level', instance.level)
        instance.college = validated_data.get('college', instance.college)
        instance.major = validated_data.get('major', instance.major)
        instance.score = validated_data.get('score', instance.score)
        instance.computer_skill = validated_data.get('computer_skill', instance.computer_skill)
        instance.foreign_language = validated_data.get('foreign_language', instance.foreign_language)
        instance.foreign_language_level = validated_data.get('foreign_language_level', instance.foreign_language_level)
        instance.train_record = validated_data.get('train_record', instance.train_record)
        instance.assessment_record = validated_data.get('assessment_record', instance.assessment_record)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.time = validated_data.get('time', instance.time)
        instance.tutor = validated_data.get('tutor', instance.tutor)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.result = validated_data.get('result', instance.result)

        instance.save()
        return instance

class customer_model_serializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_rank = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_address = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_contact = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_mobile = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_comment = serializers.CharField(allow_blank=True, default='N/A')
    customer_backup = serializers.CharField(allow_blank=True, default='N/A')
    customer_email = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_fax = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    b_display = serializers.CharField(max_length=255, allow_blank=True, default='1')
    customer_mobile2 = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_contact2 = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_email2 = serializers.CharField(max_length=255, allow_blank=True, default='N/A')
    customer_fax2 = serializers.CharField(max_length=255, allow_blank=True, default='N/A')

    def create(self, validated_data):
        """
        Create and return a new `customer_model` instance, given the validated data.
        """
        return customer_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `customer_model` instance, given the validated data.
        """
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_rank = validated_data.get('customer_rank', instance.customer_rank)
        instance.customer_address = validated_data.get('customer_address', instance.customer_address)
        instance.customer_contact = validated_data.get('customer_contact', instance.customer_contact)
        instance.customer_mobile = validated_data.get('customer_mobile', instance.customer_mobile)
        instance.customer_comment = validated_data.get('customer_comment', instance.customer_comment)
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        instance.customer_fax = validated_data.get('customer_fax', instance.customer_fax)
        instance.customer_backup = validated_data.get('customer_backup', instance.customer_backup)
        instance.b_display = validated_data.get('b_display', instance.b_display)
        instance.customer_mobile2 = validated_data.get('customer_mobile2', instance.customer_mobile2)
        instance.customer_contact2 = validated_data.get('customer_contact2', instance.customer_contact2)
        instance.customer_email2 = validated_data.get('customer_email2', instance.customer_email2)
        instance.customer_fax2 = validated_data.get('customer_fax2', instance.customer_fax2)
        instance.save()
        return instance


"""
Serializers for currecny and ammount
"""
from models import currency_model, amount_model

class currency_model_serializer(serializers.Serializer):
    currency_uuid = serializers.CharField(max_length=255, allow_blank=True)
    currency_name = serializers.CharField(max_length=255, allow_blank=True, default='')
    currency_comment = serializers.CharField( allow_blank=True, default='')

    def create(self, validated_data):
        """
        Create and return a new `currency_model` instance, given the validated data.
        """
        return currency_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `currency_model` instance, given the validated data.
        """
        instance.currency_uuid = validated_data.get('currency_uuid', instance.currency_uuid)
        instance.currency_name = validated_data.get('currency_name', instance.currency_name)
        instance.currency_comment = validated_data.get('currency_comment', instance.currency_comment)
        instance.save()
        return instance

class amount_model_serializer(serializers.Serializer):
    amount_uuid = serializers.CharField(max_length=255, allow_blank=True)
    amount_name = serializers.CharField(max_length=255, allow_blank=True, default='')
    amount_comment = serializers.CharField( allow_blank=True, default='')

    def create(self, validated_data):
        """
        Create and return a new `amount_model` instance, given the validated data.
        """
        return amount_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `amount_model` instance, given the validated data.
        """
        instance.amount_uuid = validated_data.get('amount_uuid', instance.amount_uuid)
        instance.amount_name = validated_data.get('amount_name', instance.amount_name)
        instance.amount_comment = validated_data.get('amount_comment', instance.amount_comment)
        instance.save()
        return instance


class warning_threshold_model_serializer(serializers.Serializer):
    size = serializers.CharField(max_length=255, allow_blank=True)
    warning_threshold = serializers.CharField(max_length=255, allow_blank=True)
    comment = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `amount_model` instance, given the validated data.
        """
        return warning_threshold_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `amount_model` instance, given the validated data.
        """
        instance.size = validated_data.get('size', instance.size)
        instance.warning_threshold = validated_data.get('warning_threshold', instance.warning_threshold)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
