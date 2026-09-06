from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/cancel/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('buy-now/<int:pk>/', views.buy_now, name='buy_now'),
    path('orders/track/<int:pk>/', views.order_tracking, name='order_tracking'),
    path('products/<int:pk>/review/', views.add_review, name='add_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/products/add/', views.admin_product_add, name='admin_product_add'),
    path('dashboard/products/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('dashboard/products/delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('dashboard/orders/<int:pk>/status/', views.admin_order_status, name='admin_order_status'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/users/<int:pk>/toggle/', views.admin_user_toggle, name='admin_user_toggle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
