#-------------------------------------------------------------------------------
# Name:        urls
# Purpose:
#
# Author:      yuboli
#
# Created:     16/03/2016
# Copyright:   (c) yuboli 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from django.conf.urls import url
from main import views, request_views, produce_views, storage_views, purchase_views, hr_views, quality_views
urlpatterns = [
     url(r'login/$', views.log_in),
     url(r'logout/$', views.log_out),

     url(r'sales_customer_archive', views.sales_customer_archive),
     url(r'sales_form/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', views.sales_form),
     url(r'sales_form/$', views.sales_form),
     url(r'sales_main/(?P<target_user>\S+)/$', views.sales_main),
     url(r'produce_main/(?P<target_user>\S+)/$', produce_views.produce_main),
     url(r'produce_main/$', produce_views.produce_main),
     url(r'sales_list/(?P<target_user>\S+)/$', views.sales_list),
     url(r'sales_statistics_list/(?P<target_user>\S+)/$', views.sales_statistics_list),
     url(r'sales_statistics_form/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', views.sales_statistics_form),
     url(r'sales_statistics_form/(?P<form_uuid>\S+)/$', views.sales_statistics_form),
     url(r'sales_statistics_form/$', views.sales_statistics_form),
     url(r'sales_statistics_customer/(?P<customer>[^/]+)/(?P<target_size>[^/]+)/(?P<person>\S+)/$', views.sales_statistics_customer),
     url(r'sales_statistics_customer/(?P<customer>[^/]+)/(?P<person>\S+)/$', views.sales_statistics_customer),
     url(r'sales_statistics_customer/(?P<customer>\S+)/$', views.sales_statistics_customer),
     url(r'sales_statistics_nation/(?P<nation>[^/]+)/(?P<person>\S+)/$', views.sales_statistics_nation),
     url(r'sales_statistics_nation/(?P<nation>\S+)/$', views.sales_statistics_nation),
     url(r'sales_statistics_agent/(?P<agent>\S+)/$', views.sales_statistics_agent),
     url(r'request/$', request_views.requests),
     url(r'request/(?P<request_id>\S+)/$', request_views.requests),
     url(r'request/(?P<request_id>[^/]+)/(?P<url>\S+)/$', request_views.requests),
     url(r'adjust_sequence/$', request_views.adjust_sequence),

     url(r'message/$', request_views.messages),
     url(r'register/$', views.registration),
     url(r'sample_form/(?P<form_uuid>[^/]+)/(?P<sample_form_uuid>[^/]+)/(?P<target_user>\S+)/$', views.sample_form),
     url(r'sample_form/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', views.sample_form),
     url(r'sales_producer_request_list/(?P<target_user>\S+)/$', views.sales_producer_request_list),
     url(r'produce_request_form/(?P<target_user>[^/]+)/(?P<form_uuid>\S+)/$', views.produce_request_form),
     url(r'produce_request_form/(?P<target_user>[^/]+)/$', views.produce_request_form),
     url(r'sample_request_form/(?P<target_user>[^/]+)/(?P<form_uuid>\S+)/$', views.sample_request_form),
     url(r'sample_request_form/(?P<target_user>[^/]+)/$', views.sample_request_form),
     url(r'produce_executive_list/(?P<target_user>[^/]+)/$', produce_views.produce_executive_list),
     url(r'produce_executive_list/$', produce_views.produce_executive_list),
     url(r'sample_executive_list/(?P<target_user>[^/]+)/$', produce_views.sample_executive_list),
     url(r'sample_executive_list/$', produce_views.sample_executive_list),
     url(r'produce_statistics_list/(?P<target_user>[^/]+)/$', produce_views.produce_statistics_list),
     url(r'produce_statistics_list/$', produce_views.produce_statistics_list),
     url(r'sample_statistics_list/(?P<target_user>[^/]+)/$', produce_views.sample_statistics_list),
     url(r'sample_statistics_list/$', produce_views.sample_statistics_list),

     url(r'produce_statistics_pendai/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.produce_statistics_pendai),
     url(r'produce_statistics_pendai/(?P<target_user>\S+)/$', produce_views.produce_statistics_pendai),
     url(r'produce_statistics_pendai/$', produce_views.produce_statistics_pendai),
     url(r'produce_statistics_gunjian/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.produce_statistics_gunjian),
     url(r'produce_statistics_gunjian/(?P<target_user>\S+)/$', produce_views.produce_statistics_gunjian),
     url(r'produce_statistics_gunjian/$', produce_views.produce_statistics_gunjian),
     url(r'produce_statistics_tiexin/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.produce_statistics_tiexin),
     url(r'produce_statistics_tiexin/(?P<target_user>\S+)/$', produce_views.produce_statistics_tiexin),
     url(r'produce_statistics_tiexin/$', produce_views.produce_statistics_tiexin),

     url(r'sample_statistics_pendai/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.sample_statistics_pendai),
     url(r'sample_statistics_pendai/(?P<target_user>\S+)/$', produce_views.sample_statistics_pendai),
     url(r'sample_statistics_pendai/$', produce_views.sample_statistics_pendai),
     url(r'sample_statistics_gunjian/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.sample_statistics_gunjian),
     url(r'sample_statistics_gunjian/(?P<target_user>\S+)/$', produce_views.sample_statistics_gunjian),
     url(r'sample_statistics_gunjian/$', produce_views.sample_statistics_gunjian),
     url(r'sample_statistics_tiexin/(?P<form_uuid>[^/]+)/(?P<target_user>\S+)/$', produce_views.sample_statistics_tiexin),
     url(r'sample_statistics_tiexin/(?P<target_user>\S+)/$', produce_views.sample_statistics_tiexin),
     url(r'sample_statistics_tiexin/$', produce_views.sample_statistics_tiexin),

    url(r'produce_storage_mudai/$', produce_views.produce_storage_mudai),
    url(r'produce_storage_chengpin/$', produce_views.produce_storage_chengpin),
    url(r'produce_storage_texin/$', produce_views.produce_storage_texin),
    url(r'produce_storage_mudai_hejin/$', produce_views.produce_storage_mudai_hejin),
    url(r'produce_storage_huhe/$', produce_views.produce_storage_huhe),

    url(r'storage_main/(?P<target_user>\S+)/$', storage_views.storage_main),
    url(r'storage_main/$', storage_views.storage_main),
    url(r'storage_item_mudai/$',storage_views.storage_item_mudai),
    url(r'storage_item_gunjian/$',storage_views.storage_item_gunjian),
    url(r'storage_item_tiexin/$',storage_views.storage_item_tiexin),
    url(r'storage_item_name/mudai/(?P<target_size>\S+)/$',storage_views.storage_item_name_mudai),
    url(r'storage_item_name/gunjian/(?P<target_size>\S+)/$',storage_views.storage_item_name_gunjian),
    url(r'storage_item_name/tiexin/(?P<target_size>\S+)/$',storage_views.storage_item_name_tiexin),
    url(r'storage_source/(?P<category>\S+)/$',storage_views.storage_source),
    url(r'storage_source_name/(?P<category>[^/]+)/(?P<target_size>\S+)/$',storage_views.storage_source_name),
    url(r'storage_source_threshold/(?P<target_user>\S+)/$',storage_views.storage_source_threshold),
    url(r'storage_item_threshold/(?P<target_user>\S+)/$',storage_views.storage_item_threshold),
    # standalone tables
    url(r'storage/capital/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_captial),
    url(r'storage/check/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_check),
    url(r'storage/capital/(?P<target_user>\S+)/$',storage_views.storage_captial),
    url(r'storage/check/(?P<target_user>\S+)/$',storage_views.storage_check),

    # update the storage form
    url(r'storage/delivery/(?P<category>[^/]+)/size=(?P<size>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_delivery),
    url(r'storage/delivery/(?P<category>[^/]+)/customer=(?P<customer>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_delivery),
    url(r'storage/delivery/(?P<category>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_delivery),
    url(r'storage/source_out/(?P<category>[^/]+)/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_source_out),
    url(r'storage/source_out/(?P<category>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_source_out),
    url(r'storage/source_in/(?P<category>[^/]+)/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_source_in),
    url(r'storage/source_in/(?P<category>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_source_in),
    url(r'storage/source_in_stored_confirm/(?P<category>[^/]+)/(?P<uuid>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_source_jn_stored_confirm),
    url(r'storage/source_in_stored_cancel/(?P<category>[^/]+)/(?P<uuid>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_source_jn_stored_cancel),
    url(r'storage/product_in_stored_confirm/(?P<category>[^/]+)/(?P<uuid>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_product_jn_stored_confirm),
    url(r'storage/product_in_stored_cancel/(?P<category>[^/]+)/(?P<uuid>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_product_jn_stored_cancel),
    url(r'storage/product_in/(?P<category>[^/]+)/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_product_in),
    url(r'storage/product_in/(?P<category>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_product_in),
    url(r'storage/product_out/(?P<category>[^/]+)/(?P<target_user>[^/]+)/(?P<uuid>\S+)/$',storage_views.storage_product_out),
    url(r'storage/product_out/(?P<category>[^/]+)/(?P<target_user>\S+)/$',storage_views.storage_product_out),

	#hr_form
    url(r'hr_main/(?P<target_user>\S+)/$', views.hr_main),

	# purchase
    url(r'purchase_main/(?P<target_user>\S+)/$', purchase_views.purchase_main),
    # source purchase
    url(r'purchase/category/(?P<category>[^/]+)/(?P<target_user>\S+)/$', purchase_views.purchase_category),
    url(r'purchase/detail/(?P<category>[^/]+)/(?P<size>[^/]+)/(?P<target_user>\S+)/$', purchase_views.purchase_detail),
    url(r'purchase/detail_uuid/(?P<uuid>\S+)/$', purchase_views.purchase_detail_uuid),
    url(r'purchase/purchase_supplier_archive', purchase_views.purchase_supplier_archive),
    url(r'purchase/supplier/(?P<target_user>\S+)/$', purchase_views.purchase_supplier),
    url(r'purchase/supplier_detail/(?P<supplier_name>[^/]+)/(?P<target_user>\S+)/$', purchase_views.purchase_supplier_detail),
    # superuser_age
    url(r'sales_manager/(?P<target_user>\S+)/$', views.sales_manager),
    url(r'superuser/(?P<target_user>\S+)/$', views.superuser),
    # produce chart
    url(r'produce/chart/(?P<category>\S+)/$', produce_views.produce_chart),
	url(r'hr_rank_overview/(?P<target_user>[^/]+)/(?P<rank_uuid>\S+)/$', hr_views.hr_rank_overview),
    url(r'hr_rank_overview/(?P<target_user>[^/]+)/$', hr_views.hr_rank_overview),
    url(r'employee_profile/(?P<target_user>[^/]+)/$', hr_views.employee_profile),
	
    url(r'produce/chart_day/(?P<category>\S+)/$', produce_views.produce_chart_day),
    # quality
    url(r'quality_main/(?P<target_user>\S+)/$', views.quality_main),
    url(r'quality_main/$', views.quality_main),
    url(r'MHJ_track/(?P<track_id>\S+)/$', quality_views.MHJ_track),
    url(r'MHJ_track/$', quality_views.MHJ_track),
    url(r'DC_track/(?P<track_id>\S+)/$', quality_views.DC_track),
    url(r'DC_track/$', quality_views.DC_track),
    url(r'CX_track/(?P<track_id>\S+)/$', quality_views.CX_track),
    url(r'CX_track/$', quality_views.CX_track),
    # special user main
    url(r'special_user_main/(?P<target_user>\S+)/$', views.special_user_main),
]
