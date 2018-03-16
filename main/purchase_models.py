# -*- coding: utf-8 -*-
################################################################################
##
##   PRODUCE
##
##
################################################################################
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib import admin

class purchase_model(models.Model):
    purchase_id = models.CharField(max_length=255,  primary_key=True)
    """
    母合金 耐火材料 护盒 包装物 五金零件
    """
    purchase_category = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    purchase_index = models.CharField(default='CGXXXXXX', max_length=255)
    purchase_name = models.CharField(default='N/A', max_length=255)
    size = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    is_stored = models.CharField(max_length=255, blank=True, null=True)
    storage_no = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.CharField(max_length=255, blank=True, null=True)
    quality = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    b_display = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
                ('is_buyer', u"采购员"),
                ('is_buyer_manager', u"采购经理"),
            )


class SupplierModelAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'supplier_address','supplier_contact', 'supplier_phone', 'supplier_rank')

class supplier_model(models.Model):
    supplier_id = models.CharField(max_length=255,  primary_key=True)
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_contact = models.CharField(max_length=255, blank=True, null=True)
    supplier_address = models.CharField(max_length=255, blank=True, null=True)
    supplier_phone = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.CharField(max_length=255, blank=True, null=True)
    supplier_product = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.CharField(max_length=255, blank=True, null=True)
    supplier_rank = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    b_display = models.CharField(max_length=255, blank=True, null=True)
    return_list = models.CharField(max_length=255, blank=True, null=True)
    supplier_table = models.FileField(upload_to='uploadFiles/',blank=True, null=True)

    class Meta:
        verbose_name = u"供应商"
        verbose_name_plural  = u"供应商"
        permissions = (
                ('modify_rank', u"调整供应商等级"),
            )
