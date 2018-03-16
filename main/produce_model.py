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

class size_model(models.Model):
    size_id = models.CharField(max_length=255,  primary_key=True)
    size_name = models.CharField(max_length=255, blank=True, null=True)

class item_name_model(models.Model):
    item_name_id = models.CharField(max_length=255, primary_key=True)
    item_name_str = models.CharField(max_length=255, blank=True, null=True)

class source_name_model(models.Model):
    source_name_id = models.CharField(max_length=255, primary_key=True)
    source_name_str = models.CharField(max_length=255, blank=True, null=True)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_size','product_comment')

class product_name_model(models.Model):
    PRODUCT_CHOICES = (
       ("DC", u"带材"),
       ("CX", u"铁芯"),
       ("QJ", u"器件")
    )
    product_name = models.CharField(max_length=255, blank=True, null=True, choices=PRODUCT_CHOICES)
    product_size = models.CharField(max_length=255, blank=True, null=True)
    product_comment = models.CharField(max_length=255, blank=True, null=True)
    product_unit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u"产品"
        verbose_name_plural  = u"产品"
        permissions = (
                ('modify_product_list', u"编辑公司产品信息"),
            )

class item_model(models.Model):
    item_id = models.CharField(max_length=255, blank=True, null=True)
    item_category = models.CharField(max_length=255, blank=True, null=True)
    produce_date = models.DateField(blank=True, null=True)
    item_buyNo = models.CharField(max_length=255, blank=True, null=True)
    item_level = models.CharField(max_length=255, blank=True, null=True)
    item_size = models.CharField(max_length=255, blank=True, null=True)
    item_class = models.CharField(max_length=255, blank=True, null=True)
    item_weight = models.CharField(max_length=255, blank=True, null=True)
    item_sale_weight = models.CharField(max_length=255, blank=True, null=True)
    item_inventory = models.CharField(max_length=255, blank=True, null=True)
    item_sale_link = models.CharField(max_length=255, blank=True, null=True)
    is_stored = models.CharField(max_length=255, blank=True, null=True)
    item_comment = models.CharField(max_length=255, blank=True, null=True)
    item_container = models.CharField(max_length=255, blank=True, null=True)

    uuid = models.CharField(max_length=100, primary_key=True)
    isLatest = models.IntegerField(default=1, blank=True, null=True)
    last_revise_date = models.DateField(auto_now=True, null=True)
    produce_uuid = models.CharField(max_length=100, blank=True, null=True)
    b_display =  models.CharField(default='1', max_length=255,  blank=True, null=True)

class source_model(models.Model):
    source_id = models.CharField(max_length=255, primary_key=True)
    source_name = models.CharField(max_length=255, blank=True, null=True)
    source_comment = models.CharField(max_length=255, blank=True, null=True)
    source_update_date = models.DateField(blank=True, null=True)
    source_size = models.CharField(max_length=255, blank=True, null=True)
    """
    amount = kucun
    """
    source_amount = models.CharField(max_length=255, blank=True, null=True)
    source_supplier = models.CharField(max_length=255, blank=True, null=True)
    """
    add for storage
    """
    source_usage_date = models.DateField(blank=True, null=True)
    source_alert = models.CharField(max_length=255, blank=True, null=True)

    """
    detail info
    """
    source_storage_index = models.CharField(max_length=255, blank=True, null=True)
    source_unit = models.CharField(max_length=255, blank=True, null=True)
    source_total_price = models.CharField(max_length=255, blank=True, null=True)
    source_quality = models.CharField(max_length=255, blank=True, null=True)
    source_class = models.CharField(max_length=255, blank=True, null=True)
    source_track_no = models.CharField(max_length=255, blank=True, null=True)
    source_usage = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        permissions = (
                ('is_storage', u"库存员工"),
                ('is_storage_manager', u"库存经理"),
                ('storage_can_see_sample_form', u"库存员工 可以查看生产单"),
            )

