from django import forms
from ..models import Employee
from django.forms import ModelForm


#generic form
#model form

class EmpForm(forms.ModelForm):
    class Meta:
      model=Employee
      fields="__all__"
