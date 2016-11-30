from django import forms
from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.forms import ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CompetitionGroup
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)
    # username = forms.CharField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit = False)
        user.username = self.cleaned_data['username'].lower()
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name'].capitalize()
        user.last_name = self.cleaned_data['last_name'].capitalize()

        if commit:
            user.save()
        return user

class UserModelMultipleChoiceField(ModelMultipleChoiceField):

        def label_from_instance(self, obj):
            return "%s %s" % (obj.first_name, obj.last_name)

class CompetitionGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompetitionGroupForm, self).__init__(*args, **kwargs)
        # change default labels for the form
        self.fields['users'] = UserModelMultipleChoiceField(queryset = User.objects.exclude(profile__role='instructor').all().order_by('first_name', 'last_name'), widget=forms.widgets.SelectMultiple)
        self.fields['users'].label = "Participants"

    class Meta:
        model = CompetitionGroup
        fields = ('name', 'description', 'reward', 'users')
        