from django.urls import path
from . import views
from .consumers import ChatConsumer


#HTTP response to be sent

urlpatterns = [
    path('',views.index,name='index'),
    path('message/',views.message_view, name='message'),
]