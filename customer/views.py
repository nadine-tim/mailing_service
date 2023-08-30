from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from customer.forms import CustomerForms
from customer.models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customer_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForms
    success_url = reverse_lazy('customer:list')

    def form_valid(self, form):
        new_customer = form.save()
        if new_customer.user is None:
            new_customer.user = self.request.user
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForms
    success_url = reverse_lazy('customer:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customer:list')