from typing import Any, Dict
from django.shortcuts import render, HttpResponseRedirect
from .models import unit_message
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
@method_decorator(permission_required('unit_message.can_edit_unit_message', login_url='/accounts/login/'), name='dispatch')
class UnitMessageListView(ListView):
    model = unit_message
    #queryset = original_message.objects.filter(~Q(quantity=0))
    template_name = 'unit_message/unit_message_list.html'
    paginate_by = 2
