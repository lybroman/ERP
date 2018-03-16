from rest_framework import serializers
from hr_models import hr_rank_model

class hr_rank_model_serializer(serializers.Serializer):
    rank_uuid = serializers.CharField(max_length=255, default='', allow_null=True)
    target_user = serializers.CharField(max_length=255, default='', allow_null=True)
    date_for =  serializers.DateField(default=None, allow_null=True)
    update_date =serializers.DateField(default=None, allow_null=True)
    comment = serializers.CharField(max_length=255, default='', allow_null=True)
    score = serializers.CharField(max_length=255, default='', allow_null=True)
    ranker = serializers.CharField(max_length=255, default='', allow_null=True)
    b_display = serializers.CharField(max_length=255, default='1', allow_null=True)


    def create(self, validated_data):
        """
        Create and return a new `hr_rank_model` instance, given the validated data.
        """
        return hr_rank_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `hr_rank_model` instance, given the validated data.
        """
        # briefInfo
        instance.rank_uuid = validated_data.get('rank_uuid', instance.rank_uuid)
        instance.target_user =  validated_data.get('target_user', instance.target_user)
        instance.date_for =  validated_data.get('date_for', instance.date_for)
        instance.update_date =  validated_data.get('update_date', instance.update_date)
        instance.comment =  validated_data.get('comment', instance.comment)
        instance.ranker =  validated_data.get('ranker', instance.ranker)
        instance.score =  validated_data.get('score', instance.score)
        instance.b_display =  validated_data.get('b_display', instance.b_display)
        instance.save()
        return instance