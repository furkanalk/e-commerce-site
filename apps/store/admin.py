from django.contrib import admin
from .models import Category, Product, Comments, Order, OrderItem, QuestionAnswer

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'product', 'user', 'status']
    list_filter = ['status', 'reported']

class QnAAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'product', 'user']
    list_filter = ['status']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'status']
    list_filter = ['status']

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(QuestionAnswer, QnAAdmin)
