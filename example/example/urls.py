"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import PaymentSetupView, PaymentList, create_new_payment, PaymentDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('django_coinpayments.urls', namespace='django_coinpayments')),
    url(r'^$', PaymentSetupView.as_view(), name='payment_setup'),
    url(r'^payments/$', PaymentList.as_view(), name='payment_list'),
    url(r'^payment/(?P<pk>[0-9a-f-]+)$', PaymentDetail.as_view(), name='payment_detail'),
    url(r'^payment/new/(?P<pk>[0-9a-f-]+)$', create_new_payment, name='payment_new'),

]
