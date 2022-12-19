from django.contrib import admin
from .models import Payment, Order, OrderProduct

# แสดงแถวย่อยใต้แถวแม่
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price', 'ordered']
    extra = 0 # ปิด 3 แถวว่างสุดท้าย 

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'cust_name', 'payment', 'phone', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search__field = ['order_number', 'cust_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
