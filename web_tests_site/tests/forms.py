from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User_Info

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class UserAddForm(forms.ModelForm):

    class Meta:
        model = User_Info
        fields = ('university', 'specialty', 'info',)