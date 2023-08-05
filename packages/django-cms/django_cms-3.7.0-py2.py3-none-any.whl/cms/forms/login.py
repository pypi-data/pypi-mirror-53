from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CMSToolbarLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CMSToolbarLoginForm, self).__init__(*args, **kwargs)
        kwargs['prefix'] = kwargs.get('prefix', 'cms')
        self.fields['username'].widget = forms.TextInput(
            attrs = { 'required': 'required' })
        self.fields['password'].widget = forms.PasswordInput(
            attrs = { 'required': 'required' })
