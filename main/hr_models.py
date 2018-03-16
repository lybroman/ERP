# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib import admin

class hr_rank_model(models.Model):
    rank_uuid = models.CharField(primary_key=True, max_length=255, blank=True, null=True)
    target_user = models.CharField(max_length=255, blank=True, null=True)
    date_for =  models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    comment = models.TextField(default='N/A', blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    ranker = models.CharField(max_length=255, blank=True, null=True)
    b_display = models.CharField(max_length=255, default='1', blank=True, null=True)
    class Meta:
        permissions = (
            ('is_ranker', '可以进行评级'),
        )

