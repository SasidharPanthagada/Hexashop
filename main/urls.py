from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('contact/',views.contact ,name="contact"),
    
    path('cart/', views.cart ,name="cart"),
    path('checkout/', views.checkout ,name="checkout"),
    path('update_item/', views.updateitem ,name="update_item"),
    path('process_order/', views.processorder ,name="process_order"),
    path('products/<slug:category_slug>',views.products ,name="products"),
    path('single-product/<slug:product_slug>/', views.singleproduct , name='single-product'),
    path('about/',views.about ,name='about'),

]