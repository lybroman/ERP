from rest_framework import serializers
from models import capital_model, check_model, storage_delivery_model, storage_product_out_model, storage_source_out_model


class capital_model_serializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=255, default='', allow_null=True)
    category = serializers.CharField(max_length=255, default='', allow_null=True)
    size = serializers.CharField(max_length=255, default='', allow_null=True)
    price = serializers.CharField(max_length=255, default='', allow_null=True)
    amount = serializers.CharField(max_length=255, default='', allow_null=True)
    total_price = serializers.CharField(max_length=255, default='', allow_null=True)
    last_update_time = serializers.DateField(default='', allow_null=True)
    place = serializers.CharField(max_length=255, default='', allow_null=True)
    comment = serializers.CharField(default='', allow_null=True)
    b_display = serializers.CharField(default='1')

    def create(self, validated_data):
        return capital_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.category =  validated_data.get('category', instance.category)
        instance.size =  validated_data.get('size', instance.size)
        instance.price =  validated_data.get('price', instance.price)
        instance.amount =  validated_data.get('amount', instance.amount)
        instance.total_price =  validated_data.get('total_price', instance.total_price)
        instance.last_update_time =  validated_data.get('last_update_time', instance.last_update_time)
        instance.place =  validated_data.get('place', instance.place)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.save()


class check_model_serializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=255, default='', allow_null=True)
    last_update_time = serializers.DateField(default='', allow_null=True)
    staff = serializers.CharField(max_length=255, default='', allow_null=True)
    comment = serializers.CharField(default='', allow_null=True)
    b_display = serializers.CharField(default='1')
    def create(self, validated_data):
        return check_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid =  validated_data.get('uuid', instance.uuid)
        instance.last_update_time =  validated_data.get('last_update_time', instance.last_update_time)
        instance.staff =  validated_data.get('staff', instance.staff)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.save()

class storage_product_out_serializers(serializers.Serializer):
    delivery_id = serializers.CharField(max_length=100, default='', allow_null=True)
    contract_No = serializers.CharField(max_length=100, default='', allow_null=True)
    update_date = serializers.DateField(default='', allow_null=True)
    size = serializers.CharField(max_length=100, default='', allow_null=True)
    customer =  serializers.CharField(max_length=100, default='', allow_null=True)
    amount = serializers.CharField(max_length=100, default='', allow_null=True)
    comment =serializers.CharField(default='', allow_null=True)
    b_display =  serializers.CharField(max_length=100, default=1, allow_null=True)
    category =  serializers.CharField(max_length=100, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `storage_product_out_model` instance, given the validated data.
        """
        return storage_product_out_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `storage_product_out_model` instance, given the validated data.
        """
        instance.delivery_id =  validated_data.get('delivery_id', instance.delivery_id)
        instance.contract_No =  validated_data.get('contract_No', instance.contract_No)
        instance.update_date =  validated_data.get('update_date', instance.update_date)
        instance.size =  validated_data.get('size', instance.size)
        instance.customer =  validated_data.get('customer', instance.customer)
        instance.amount =  validated_data.get('amount', instance.amount)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.category =  validated_data.get('category', instance.category)
        instance.save()
        return instance

class storage_source_out_serializers(serializers.Serializer):
    delivery_id = serializers.CharField(max_length=100, default='', allow_null=True)
    update_date = serializers.DateField(default='', allow_null=True)
    item = serializers.CharField(max_length=100, default='', allow_null=True)
    item_size = serializers.CharField(max_length=100, default='', allow_null=True)
    No =  serializers.CharField(max_length=100, default='', allow_null=True)
    reason = serializers.CharField(max_length=100, default='', allow_null=True)
    department = serializers.CharField(max_length=100, default='', allow_null=True)
    user  = serializers.CharField(max_length=100, default='', allow_null=True)
    amount = serializers.CharField(max_length=100, default='', allow_null=True)
    comment = serializers.CharField( default='', allow_null=True)
    b_display =  serializers.CharField(max_length=100, default='', allow_null=True)
    category =  serializers.CharField(max_length=100, default='', allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `storage_source_out_model` instance, given the validated data.
        """
        return storage_source_out_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `storage_source_out_model` instance, given the validated data.
        """
        instance.delivery_id =  validated_data.get('delivery_id', instance.delivery_id)
        instance.item =  validated_data.get('item', instance.item)
        instance.item_size =  validated_data.get('item_size', instance.item_size)
        instance.update_date =  validated_data.get('update_date', instance.update_date)
        instance.No =  validated_data.get('No', instance.No)
        instance.reason =  validated_data.get('reason', instance.reason)
        instance.department =  validated_data.get('department', instance.department)
        instance.user =  validated_data.get('user', instance.user)
        instance.amount =  validated_data.get('amount', instance.amount)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.category =  validated_data.get('category', instance.category)
        instance.save()
        return instance