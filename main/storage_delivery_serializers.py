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
from main.models import storage_delivery_model

class storageDeliverySerializers(serializers.Serializer):
    delivery_id = serializers.CharField(max_length=100, default='', allow_null=True)
    sales_No = serializers.CharField(max_length=100, default='', allow_null=True)
    contract_No = serializers.CharField(max_length=100, default='', allow_null=True)
    update_date = serializers.DateField(default='', allow_null=True)
    size = serializers.CharField(max_length=100, default='', allow_null=True)
    customer =  serializers.CharField(max_length=100, default='', allow_null=True)
    delivery_No = serializers.CharField(max_length=100, default='', allow_null=True)
    delivery_amount = serializers.CharField(max_length=100, default='', allow_null=True)
    delivery_status =  serializers.CharField(max_length=100, default='', allow_null=True)
    delivery_track_No =  serializers.CharField(max_length=100, default='', allow_null=True)
    delivery_comment =  serializers.CharField(default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)
    category =  serializers.CharField(max_length=100, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `storage_delivery_model` instance, given the validated data.
        """
        return storage_delivery_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `storage_delivery_model` instance, given the validated data.
        """
        instance.delivery_id =  validated_data.get('delivery_id', instance.delivery_id)
        instance.sales_No =  validated_data.get('sales_No', instance.sales_No)
        instance.contract_No =  validated_data.get('contract_No', instance.contract_No)
        instance.update_date =  validated_data.get('update_date', instance.update_date)
        instance.size =  validated_data.get('size', instance.size)
        instance.customer =  validated_data.get('customer', instance.customer)
        instance.delivery_No =  validated_data.get('delivery_No', instance.delivery_No)
        instance.delivery_amount =  validated_data.get('delivery_amount', instance.delivery_amount)
        instance.delivery_status =  validated_data.get('delivery_status', instance.delivery_status)
        instance.delivery_track_No =  validated_data.get('delivery_track_No', instance.delivery_track_No)
        instance.delivery_comment =  validated_data.get('delivery_comment', instance.delivery_comment)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.category =  validated_data.get('category', instance.category)
        instance.save()
        return instance
