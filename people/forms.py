import taggit

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = (
            'user',
            'first_name',
            'last_name',
            'password',
            'last_login',
            'username',
            'is_staff',
            'is_superuser',
            'is_active')