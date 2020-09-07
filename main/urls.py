from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('store', views.store, name='store'),
    path('about', views.about, name='about'),
    url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

]
