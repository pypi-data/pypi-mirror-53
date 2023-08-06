from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class ProfileForm(forms.Form):

    role = forms.ChoiceField(
        label=_('Role'),
        choices=settings.DJANGO_SSO_PROFILE_ROLE_CHOICES,
        initial=0)

    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(
        attrs={'type': 'text',
               'placeholder': _('First name')}))

    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(
        attrs={'type': 'text',
               'placeholder': _('Last name')}))

    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(
        attrs={'placeholder': _('Description')}))

    picture = forms.ImageField(
        label=_('Picture'),
    )

    birthdate = forms.DateField(
        label=_('Birthdate'),
        widget=forms.TextInput(
        attrs={ 'type': 'date',
                'placeholder': _('Birthdate')}))

    latitude = forms.FloatField(
        label=_('Latitude'))

    longitude = forms.FloatField(
        label=_('Longitude'))

    country = forms.CharField(
        label=_('Country'),
        widget=forms.TextInput(
        attrs={ 'type': 'text',
                'placeholder': _('Country')}))

    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(
        attrs={'placeholder': _('Address')}))

    language = forms.CharField(
        label=_('Language'),
        widget=forms.TextInput(
        attrs={'type': 'text',
             'placeholder': _('Language')}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if settings.DJANGO_SSO_USER_CREATE_PROFILE_ON_SIGNUP:
            for field in settings.DJANGO_SSO_PROFILE_FIELDS:
                self.fields[field].required = field in settings.DJANGO_SSO_REQUIRED_PROFILE_FIELDS
