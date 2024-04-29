"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
     path('', views.homep, name='welcome'), 
     path('signup/', views.SignupPage, name='signup'),
      path('login/', views.loginpage, name='login'),
       path('Category/', views.homepage, name='category'),
       path('Woman/', views.woman, name='woman'),
       path('Man/', views.man, name='man'),
       path('Children/', views.children, name='children'),
        path('Desired/', views.Desired, name='desired'),
        path('Couples/', views.Couples, name='couples'),
         path("accounts/", include("django.contrib.auth.urls")),
          path('logout/', views.logoutnow, name='logout'),
          path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
           path('add-to-cart/<int:cloth_id>/', views.add_to_cart, name='add_to_cart'),
           path('cloth/<int:cloth_id>/', views.cloth_detail, name='cloth_detail'),
            path('cart/', views.view_cart, name='cart'),
            path('remove-from-cart/<int:cloth_id>/', views.remove_from_cart, name='remove_from_cart'),
              path('increment-quantity/<int:cloth_id>/', views.increment_quantity, name='increment_quantity'),
               path('decrement-quantity/<int:cloth_id>/', views.decrement_quantity, name='decrement_quantity'),
                 path('size/', views.Size, name='size'),
                  path('enter/', views.Enter, name='enter'),
                   path('profile/', views.customer_profile, name='customer_profile'),
                     path('measurement_list/', views.measurement_list, name='measurement_list'),
                    path('checkout/', views.checkout, name='checkout'),
                      path('paypal-ipn/', include('paypal.standard.ipn.urls')),
                      path('payment-complete/', views.payment_complete, name='payment_complete'),
                      path('receive_measurements/', views.receive_measurements, name='receive_measurements'),
                      path('order-success/<str:order_number>/<str:total_price>/', views.order_success, name='order_success'),
                     path('view-orders/', views.view_orders, name='view_orders'),
                     path('track-order/', views.track_order, name='track_order'),
                      path('aboutus/', views.about_us, name='aboutus'),
                       path('terms/', views.terms, name='terms'),
                       path('shopnow/', views.shopnow, name='shopnow'),
                    path('payment-success/', views.PaymentSuccessful, name='payment-success'),
                      path('add_address/', views.add_address, name='add_address'),
                      path('listaddress/', views.address_list, name='listaddress'),
                       
                  
                    

      
    
   
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
