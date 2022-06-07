from . import views as v
from django.urls import path


urlpatterns = [
    path('', v.index, name='index'),
    path('new-transaction', v.trans_page, name='transaction'),
    path('confirm-transaction', v.trans_details, name='details'),

    path('login', v.login_page, name='login'),
    path('sign-up', v.register, name='register'),
]
