from rest_framework import routers
from django.urls import path, include
from original_message import views
from original_message.views import OriginalMessageListView #ProductListView, OrderSuccessView, CreateOrder
from .api import OriginalMessageViewSet, OriginalMessagesApi
#from .api_g import OriginalMessagesApi

router = routers.DefaultRouter()
router.register('original_message', OriginalMessageViewSet, 'original_messages')
# urlpatterns = router.urls

original_message_urlspatterns = ([
    path('', OriginalMessageListView.as_view(), name='original_message_list'),
    #path('order_success/', OrderSuccessView.as_view(), name='order_success'),
    #path('detail_order/', views.detail_order , name='detail_order'),
    #path('create_order/', CreateOrder.as_view() , name='create_order'),
    path('api/', include(router.urls)),
    path('apiProducts/', OriginalMessagesApi.as_view()),
], 'original_message')


