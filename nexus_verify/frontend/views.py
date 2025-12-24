from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from api.models import Property, User

# Forms can be defined here or in a separate forms.py, inline for simplicity now
from django import forms

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'location', 'property_id', 'owner_name', 'zoning_status', 'fraud_risk_level', 'document', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_id': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'zoning_status': forms.TextInput(attrs={'class': 'form-control'}),
            'fraud_risk_level': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

# Auth Views
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('property_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('property_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Property CRUD Views
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'frontend/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            from django.db.models import Q
            qs = qs.filter(Q(location__icontains=q) | Q(title__icontains=q))
        return qs

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'frontend/property_form.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'frontend/property_form.html'
    success_url = reverse_lazy('property_list')

    def test_func(self):
        # Allow edit if user is the registrar or an auditor? 
        # For simplicity, let's say only the creator for now, or Auditor.
        obj = self.get_object()
        return obj.registered_by == self.request.user or self.request.user.role == 'AUDITOR'

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'frontend/property_confirm_delete.html'
    success_url = reverse_lazy('property_list')

    def test_func(self):
        obj = self.get_object()
        return obj.registered_by == self.request.user
