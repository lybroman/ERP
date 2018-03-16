#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yuboli
#
# Created:     07/04/2016
# Copyright:   (c) yuboli 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from rest_framework import serializers
from produce_model import item_model, source_model, size_model, item_name_model, source_name_model, product_name_model
from models import produce_statistics_pendai_model, produce_statistics_gunjian_model, produce_statistics_tiexin_model, sample_statistics_pendai_model, sample_statistics_gunjian_model, sample_statistics_tiexin_model
class size_model_serializer(serializers.Serializer):
    size_id = serializers.CharField(max_length=255, default='', allow_null=True)
    size_name = serializers.CharField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `size_model` instance, given the validated data.
        """
        return size_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `size_model` instance, given the validated data.
        """
        # briefInfo
        instance.size_id = validated_data.get('size_id', instance.size_id)
        instance.size_name =  validated_data.get('size_name', instance.size_name)
        instance.save()
        return instance

class item_name_model_serializer(serializers.Serializer):
    item_name_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_name_str = serializers.CharField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `item_name_model` instance, given the validated data.
        """
        return item_name_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `item_name_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_name_id = validated_data.get('item_name_id', instance.item_name_id)
        instance.item_name_str =  validated_data.get('item_name_str', instance.item_name_str)
        instance.save()
        return instance

class source_name_model_serializer(serializers.Serializer):
    source_name_id = serializers.CharField(max_length=255, default='', allow_null=True)
    source_name_str = serializers.CharField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_name_model` instance, given the validated data.
        """
        return source_name_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_name_model` instance, given the validated data.
        """
        # briefInfo
        instance.source_name_id = validated_data.get('source_name_id', instance.source_name_id)
        instance.source_name_str =  validated_data.get('source_name_str', instance.source_name_str)
        instance.save()
        return instance

class item_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_category = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    item_level = serializers.CharField(max_length=255, default='', allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_class = serializers.CharField(max_length=255, default='', allow_null=True)
    item_weight = serializers.CharField(max_length=255, default='', allow_null=True)
    item_sale_weight = serializers.CharField(max_length=255, default='', allow_null=True)
    item_inventory = serializers.CharField(max_length=255, default='', allow_null=True)
    item_sale_link = serializers.CharField(max_length=255, default='', allow_null=True)
    is_stored = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    item_container = serializers.CharField(max_length=255, default='', allow_null=True)

    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    produce_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `item_model` instance, given the validated data.
        """
        return item_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `item_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_category = validated_data.get('item_category', instance.item_category)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_buyNo =  validated_data.get('item_buyNo', instance.item_buyNo)
        instance.item_level =  validated_data.get('item_level', instance.item_level)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_class =  validated_data.get('item_class', instance.item_class)
        instance.item_weight =  validated_data.get('item_weight', instance.item_weight)
        instance.item_sale_weight =  validated_data.get('item_sale_weight', instance.item_sale_weight)
        instance.item_inventory =  validated_data.get('item_inventory', instance.item_inventory)
        instance.item_sale_link =  validated_data.get('item_sale_link', instance.item_sale_link)
        instance.is_stored =  validated_data.get('is_stored', instance.is_stored)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.item_container =  validated_data.get('item_container', instance.item_container)

        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.produce_uuid =  validated_data.get('produce_uuid', instance.produce_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class source_model_serializer(serializers.Serializer):
    source_id = serializers.CharField(max_length=255, default='', allow_null=True)
    source_name = serializers.CharField(max_length=255, default='', allow_null=True)
    source_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    source_update_date = serializers.DateField(default=None, allow_null=True)
    source_size = serializers.CharField(max_length=255, default='', allow_null=True)

    source_amount = serializers.CharField(max_length=255, default='', allow_null=True)
    source_supplier = serializers.CharField(max_length=255, default='', allow_null=True)

    source_usage_date = serializers.DateField(default=None, allow_null=True)
    source_alert = serializers.CharField(max_length=255, default='', allow_null=True)

    source_storage_index = serializers.CharField(max_length=255, default='', allow_null=True)
    source_unit = serializers.CharField(max_length=255, default='', allow_null=True)
    source_total_price = serializers.CharField(max_length=255, default='', allow_null=True)
    source_quality = serializers.CharField(max_length=255, default='', allow_null=True)
    source_class = serializers.CharField(max_length=255, default='', allow_null=True)
    source_track_no = serializers.CharField(max_length=255, default='', allow_null=True)
    source_usage = serializers.CharField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return source_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.source_id = validated_data.get('source_id', instance.source_id)
        instance.source_name =  validated_data.get('source_name', instance.source_name)
        instance.source_comment =  validated_data.get('source_comment', instance.source_comment)
        instance.source_update_date =  validated_data.get('source_update_date', instance.source_update_date)
        instance.source_size =  validated_data.get('source_size', instance.source_size)

        instance.source_amount =  validated_data.get('source_amount', instance.source_amount)
        instance.source_supplier =  validated_data.get('source_supplier', instance.source_supplier)

        instance.source_usage_date =  validated_data.get('source_usage_date', instance.source_usage_date)
        instance.source_alert =  validated_data.get('source_alert', instance.source_alert)

        instance.source_storage_index =  validated_data.get('source_storage_index', instance.source_storage_index)
        instance.source_unit =  validated_data.get('source_unit', instance.source_unit)
        instance.source_total_price =  validated_data.get('source_total_price', instance.source_total_price)
        instance.source_quality =  validated_data.get('source_alert', instance.source_quality)
        instance.source_class =  validated_data.get('source_class', instance.source_class)
        instance.source_track_no =  validated_data.get('source_track_no', instance.source_track_no)
        instance.source_usage =  validated_data.get('source_usage', instance.source_usage)

        instance.save()
        return instance

class produce_statistics_pendai_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_class = serializers.CharField(max_length=255, default='', allow_null=True)
    item_container = serializers.CharField(max_length=255, default='', allow_null=True)
    item_A = serializers.CharField(max_length=255, default='', allow_null=True)
    item_B = serializers.CharField(max_length=255, default='', allow_null=True)
    item_C = serializers.CharField(max_length=255, default='', allow_null=True)
    item_D = serializers.CharField(max_length=255, default='', allow_null=True)
    item_weight = serializers.CharField(max_length=255, default='', allow_null=True)
    item_usage = serializers.CharField(max_length=255, default='', allow_null=True)

    item_new_usage = serializers.CharField(max_length=255, default='0', allow_null=True)
    item_goback_usage = serializers.CharField(max_length=255, default='0', allow_null=True)
    item_londerful_usage = serializers.CharField(max_length=255, default='0', allow_null=True)

    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=555, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return produce_statistics_pendai_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_class =  validated_data.get('item_class', instance.item_class)
        instance.item_container =  validated_data.get('item_container', instance.item_container)
        instance.item_A =  validated_data.get('item_A', instance.item_A)
        instance.item_B =  validated_data.get('item_B', instance.item_B)
        instance.item_C =  validated_data.get('item_C', instance.item_C)
        instance.item_D =  validated_data.get('item_D', instance.item_D)
        instance.item_weight =  validated_data.get('item_weight', instance.item_weight)
        instance.item_usage =  validated_data.get('item_usage', instance.item_usage)

        instance.item_new_usage =  validated_data.get('item_new_usage', instance.item_new_usage)
        instance.item_goback_usage =  validated_data.get('item_goback_usage', instance.item_goback_usage)
        instance.item_londerful_usage =  validated_data.get('item_londerful_usage', instance.item_londerful_usage)

        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class produce_statistics_gunjian_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_staff = serializers.CharField(max_length=255, default='', allow_null=True)
    item_machine = serializers.CharField(max_length=255, default='', allow_null=True)
    item_pass = serializers.CharField(max_length=255, default='', allow_null=True)
    item_fail = serializers.CharField(max_length=255, default='', allow_null=True)
    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return produce_statistics_gunjian_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_staff =  validated_data.get('item_staff', instance.item_staff)
        instance.item_machine =  validated_data.get('item_machine', instance.item_machine)
        instance.item_pass =  validated_data.get('item_pass', instance.item_pass)
        instance.item_fail =  validated_data.get('item_fail', instance.item_fail)
        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class produce_statistics_tiexin_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_staff = serializers.CharField(max_length=255, default='', allow_null=True)
    item_material = serializers.CharField(max_length=255, default='', allow_null=True)
    item_amount = serializers.CharField(max_length=255, default='', allow_null=True)
    item_pass = serializers.CharField(max_length=255, default='', allow_null=True)
    item_fail = serializers.CharField(max_length=255, default='', allow_null=True)
    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return produce_statistics_tiexin_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_staff =  validated_data.get('item_staff', instance.item_staff)
        instance.item_material =  validated_data.get('item_material', instance.item_material)
        instance.item_amount =  validated_data.get('item_amount', instance.item_amount)
        instance.item_pass =  validated_data.get('item_pass', instance.item_pass)
        instance.item_fail =  validated_data.get('item_fail', instance.item_fail)
        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class sample_statistics_pendai_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_class = serializers.CharField(max_length=255, default='', allow_null=True)
    item_container = serializers.CharField(max_length=255, default='', allow_null=True)
    item_A = serializers.CharField(max_length=255, default='', allow_null=True)
    item_B = serializers.CharField(max_length=255, default='', allow_null=True)
    item_C = serializers.CharField(max_length=255, default='', allow_null=True)
    item_D = serializers.CharField(max_length=255, default='', allow_null=True)
    item_weight = serializers.CharField(max_length=255, default='', allow_null=True)
    item_usage = serializers.CharField(max_length=255, default='', allow_null=True)
    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=555, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return sample_statistics_pendai_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_class =  validated_data.get('item_class', instance.item_class)
        instance.item_container =  validated_data.get('item_container', instance.item_container)
        instance.item_A =  validated_data.get('item_A', instance.item_A)
        instance.item_B =  validated_data.get('item_B', instance.item_B)
        instance.item_C =  validated_data.get('item_C', instance.item_C)
        instance.item_D =  validated_data.get('item_D', instance.item_D)
        instance.item_weight =  validated_data.get('item_weight', instance.item_weight)
        instance.item_usage =  validated_data.get('item_usage', instance.item_usage)
        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class sample_statistics_gunjian_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_staff = serializers.CharField(max_length=255, default='', allow_null=True)
    item_machine = serializers.CharField(max_length=255, default='', allow_null=True)
    item_pass = serializers.CharField(max_length=255, default='', allow_null=True)
    item_fail = serializers.CharField(max_length=255, default='', allow_null=True)
    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return sample_statistics_gunjian_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_staff =  validated_data.get('item_staff', instance.item_staff)
        instance.item_machine =  validated_data.get('item_machine', instance.item_machine)
        instance.item_pass =  validated_data.get('item_pass', instance.item_pass)
        instance.item_fail =  validated_data.get('item_fail', instance.item_fail)
        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class sample_statistics_tiexin_model_serializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255, default='', allow_null=True)
    item_buyNo = serializers.CharField(max_length=255, default='', allow_null=True)
    produce_date = serializers.DateField(default=None, allow_null=True)
    item_size = serializers.CharField(max_length=255, default='', allow_null=True)
    item_staff = serializers.CharField(max_length=255, default='', allow_null=True)
    item_material = serializers.CharField(max_length=255, default='', allow_null=True)
    item_amount = serializers.CharField(max_length=255, default='', allow_null=True)
    item_pass = serializers.CharField(max_length=255, default='', allow_null=True)
    item_fail = serializers.CharField(max_length=255, default='', allow_null=True)
    item_rate = serializers.CharField(max_length=255, default='', allow_null=True)
    item_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_Nos = serializers.CharField(max_length=555, default='', allow_null=True)
    #
    uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    isLatest = serializers.IntegerField(default=1, allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    storage_item_uuid = serializers.CharField(max_length=100, default='', allow_null=True)
    b_display = serializers.CharField(max_length=100, default='1', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `source_model` instance, given the validated data.
        """
        return sample_statistics_tiexin_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `source_model` instance, given the validated data.
        """
        # briefInfo
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.item_buyNo = validated_data.get('item_buyNo', instance.item_buyNo)
        instance.produce_date =  validated_data.get('produce_date', instance.produce_date)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.item_staff =  validated_data.get('item_staff', instance.item_staff)
        instance.item_material =  validated_data.get('item_material', instance.item_material)
        instance.item_amount =  validated_data.get('item_amount', instance.item_amount)
        instance.item_pass =  validated_data.get('item_pass', instance.item_pass)
        instance.item_fail =  validated_data.get('item_fail', instance.item_fail)
        instance.item_rate =  validated_data.get('item_rate', instance.item_rate)
        instance.item_comment =  validated_data.get('item_comment', instance.item_comment)
        instance.purchase_Nos =  validated_data.get('purchase_Nos', instance.purchase_Nos)
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.isLatest =  validated_data.get('isLatest', instance.isLatest)
        instance.last_revise_date =  validated_data.get('last_revise_date', instance.last_revise_date)
        instance.storage_item_uuid =  validated_data.get('storage_item_uuid', instance.storage_item_uuid)
        instance.b_display =  validated_data.get('b_display', instance.b_display)

        instance.save()
        return instance

class product_name_model_serializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255, default='', allow_null=True)
    product_size = serializers.CharField(max_length=255, default='', allow_null=True)
    product_comment = serializers.CharField(max_length=255, default='', allow_null=True)
    product_unit = serializers.CharField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `product_name_model` instance, given the validated data.
        """
        return product_name_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `product_name_model` instance, given the validated data.
        """
        # briefInfo
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_size =  validated_data.get('product_size', instance.product_size)
        instance.product_comment =  validated_data.get('product_comment', instance.product_comment)
        instance.product_unit =  validated_data.get('product_unit', instance.product_unit)
        instance.save()
        return instance
