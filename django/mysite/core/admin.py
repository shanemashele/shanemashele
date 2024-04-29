

from django.contrib import admin 
from . models import Category, Customer,Cloth,Cart,Measurement,CustomerAddress,Order,CartItem,OrderItem,Payment
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Category)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id']
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cloth', 'quantity', 'cloth_image']

    def cloth_image(self, obj):
        return mark_safe('<img src="{}" height="100" />'.format(obj.cloth.image.url))

    cloth_image.short_description = 'Cloth Image'

admin.site.register(CartItem, CartItemAdmin)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['order','transaction_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ['id']
    




@admin.register(Cloth)
class ClothModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','category','quantity']
    
@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['address_type','street_address','city','state','postal_code','country','default','is_active']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','image','quantity','price']



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'email', 'address', 'country', 'city', 'zipcode', 'phone')
    readonly_fields = ['password']


admin.site.register(Measurement)
# Register your models here.
