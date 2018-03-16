from django.contrib import admin

# Register your models here.
from purchase_models import supplier_model, SupplierModelAdmin
from models import SettingSizeModelAdmin, setting_size_model, customer_model, CustomerModelAdmin, currency_model, CurrencyModelAdmin, AmountModelAdmin, amount_model
from produce_model import product_name_model, ProductModelAdmin

admin.site.register(supplier_model, SupplierModelAdmin)
admin.site.register(customer_model, CustomerModelAdmin)
admin.site.register(product_name_model, ProductModelAdmin)

admin.site.register(currency_model, CurrencyModelAdmin)
admin.site.register(amount_model, AmountModelAdmin)
admin.site.register(setting_size_model, SettingSizeModelAdmin)