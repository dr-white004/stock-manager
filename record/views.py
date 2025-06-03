from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

from .models import ClockType, Stock, Sale, Return
from .forms import ClockTypeForm, StockForm, SaleForm, ReturnForm


# ========== USER AUTHENTICATION VIEWS ==========

from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)   # Use custom form here
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('summary')
    else:
        form = UserRegisterForm()   # And here
    return render(request, 'register.html', {'form': form})



# ========== DATA VIEWS ==========

class ClockTypeListView(LoginRequiredMixin, ListView):
    model = ClockType
    template_name = 'clocktype_list.html'
    context_object_name = 'clock_types'

    def get_queryset(self):
        return ClockType.objects.filter(user=self.request.user)


class ClockTypeCreateView(LoginRequiredMixin, CreateView):
    model = ClockType
    form_class = ClockTypeForm
    template_name = 'clocktype_form.html'
    success_url = reverse_lazy('clocktype_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'stock_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        return Stock.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clock_types'] = ClockType.objects.filter(user=self.request.user)
        return context


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale_form.html'
    success_url = reverse_lazy('sale_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sale_list.html'
    context_object_name = 'sales'

    def get_queryset(self):
        return Sale.objects.filter(user=self.request.user)


class ReturnCreateView(LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnForm
    template_name = 'return_form.html'
    success_url = reverse_lazy('return_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReturnListView(LoginRequiredMixin, ListView):
    model = Return
    template_name = 'return_list.html'
    context_object_name = 'returns'

    def get_queryset(self):
        return Return.objects.filter(user=self.request.user)



@login_required
def inventory_summary(request):
    clock_types = ClockType.objects.filter(user=request.user)
    summary = []

    for clock in clock_types:
        total_received = sum(stock.quantity_received for stock in clock.stock_set.filter(user=request.user))
        total_defective = sum(stock.defective_quantity for stock in clock.stock_set.filter(user=request.user))
        total_sold = sum(sale.quantity for sale in clock.sale_set.filter(user=request.user))
        total_returned = sum(ret.quantity for ret in clock.return_set.filter(user=request.user))

        current_stock = total_received  - total_sold - total_returned

        summary.append({
            'clock': clock,
            'total_received': total_received,
            'total_defective': total_defective,
            'total_sold': total_sold,
            'total_returned': total_returned,
            'current_stock': current_stock,
        })

    return render(request, 'summary.html', {'summary': summary})
