
from rest_framework import serializers
from purchase_models import purchase_model, supplier_model

class purchase_model_serializers(serializers.Serializer):
    purchase_id = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_category = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_name = serializers.CharField(max_length=255, default='N/A', allow_null=True)
    last_revise_date = serializers.DateField(default='', allow_null=True)
    purchase_index = serializers.CharField(max_length=255, default='CGXXXXXX', allow_null=True)
    supplier = serializers.CharField(max_length=255, default='', allow_null=True)
    amount = serializers.CharField(max_length=255, default='', allow_null=True)
    size = serializers.CharField(max_length=255, default='', allow_null=True)
    purchase_date = serializers.DateField(allow_null=True)
    is_stored = serializers.CharField(max_length=255, default='', allow_null=True)
    storage_no = serializers.CharField(max_length=255, default='', allow_null=True)
    unit_price = serializers.CharField(max_length=255, default='', allow_null=True)
    total_price = serializers.CharField(max_length=255, default='', allow_null=True)
    quality = serializers.CharField(max_length=255, default='', allow_null=True)
    comment = serializers.CharField(max_length=255, default='', allow_null=True)
    buyer_name = serializers.CharField(max_length=255, default='', allow_null=True)
    b_display = serializers.CharField(max_length=255, default='1', allow_null=True)


    def create(self, validated_data):
        """
        Create and return a new `purchase_model` instance, given the validated data.
        """
        return purchase_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `purchase_model` instance, given the validated data.
        """
        # briefInfo
        instance.purchase_id = validated_data.get('purchase_id', instance.purchase_id)
        instance.purchase_category =  validated_data.get('purchase_category', instance.purchase_category)
        instance.supplier =  validated_data.get('supplier', instance.supplier)
        instance.amount =  validated_data.get('amount', instance.amount)
        instance.size =  validated_data.get('size', instance.size)
        instance.purchase_date =  validated_data.get('purchase_date', instance.purchase_date)
        instance.is_stored =  validated_data.get('is_stored', instance.is_stored)
        instance.storage_no =  validated_data.get('storage_no', instance.storage_no)
        instance.unit_price =  validated_data.get('unit_price', instance.unit_price)
        instance.total_price =  validated_data.get('total_price', instance.total_price)
        instance.quality =  validated_data.get('quality', instance.quality)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.buyer_name =  validated_data.get('buyer_name', instance.buyer_name)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.purchase_name = validated_data.get('purchase_name', instance.purchase_name)
        instance.purchase_index = validated_data.get('purchase_index', instance.purchase_index)
        instance.save()
        return instance

class supplier_model_serializers(serializers.Serializer):
    supplier_id = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_name = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_contact = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_rank = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_address = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_phone = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_product = serializers.CharField(max_length=255, default='', allow_null=True)
    unit_price = serializers.CharField(max_length=255, default='', allow_null=True)
    amount = serializers.CharField(max_length=255, default='', allow_null=True)
    total_price = serializers.CharField(max_length=255, default='', allow_null=True)
    comment = serializers.CharField(max_length=255, default='', allow_null=True)
    b_display = serializers.CharField(max_length=255, default='', allow_null=True)
    return_list = serializers.CharField(max_length=255, default='', allow_null=True)
    supplier_table = serializers.FileField(max_length=255, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `supplier_model` instance, given the validated data.
        """
        return supplier_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `supplier_model` instance, given the validated data.
        """
        # briefInfo
        instance.supplier_id = validated_data.get('supplier_id', instance.supplier_id)
        instance.supplier_name = validated_data.get('supplier_name', instance.supplier_name)
        instance.supplier_contact = validated_data.get('supplier_contact', instance.supplier_contact)
        instance.supplier_address = validated_data.get('supplier_address', instance.supplier_address)
        instance.supplier_phone = validated_data.get('supplier_phone', instance.supplier_phone)
        instance.supplier_rank = validated_data.get('supplier_rank', instance.supplier_rank)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.supplier_product = validated_data.get('supplier_product', instance.supplier_product)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.b_display = validated_data.get('b_display', instance.b_display)
        instance.return_list = validated_data.get('return_list', instance.return_list)
        instance.supplier_table = validated_data.get('supplier_table', instance.supplier_table)

        instance.save()
        return instance
