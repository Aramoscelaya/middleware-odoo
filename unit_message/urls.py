from rest_framework import routers
from django.urls import path, include
from unit_message import views
from unit_message.views import UnitMessageListView #ProductListView, OrderSuccessView, CreateOrder
from .api import UnitMessageViewSet, UnitMessagesApi
#from .api_g import UnitMessagesApi

router = routers.DefaultRouter()
router.register('unit_message', UnitMessageViewSet, 'unit_messages')
# urlpatterns = router.urls

unit_message_urlspatterns = ([
    path('', UnitMessageListView.as_view(), name='unit_message_list'),
    #path('order_success/', OrderSuccessView.as_view(), name='order_success'),
    #path('detail_order/', views.detail_order , name='detail_order'),
    #path('create_order/', CreateOrder.as_view() , name='create_order'),
    path('api/', include(router.urls)),
    path('apiProducts/', UnitMessagesApi.as_view()),
], 'unit_message')


