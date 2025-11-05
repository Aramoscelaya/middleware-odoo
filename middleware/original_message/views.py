from typing import Any, Dict
from django.shortcuts import render, HttpResponseRedirect
from .models import original_message
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
#from .forms import OrderForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

# Create your views here.
@method_decorator(permission_required('original_message.can_edit_original_message', login_url='/accounts/login/'), name='dispatch')
class OriginalMessageListView(ListView):
    model = original_message
    #queryset = original_message.objects.filter(~Q(quantity=0))
    template_name = 'original_message/original_message_list.html'
    paginate_by = 2
