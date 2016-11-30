from django import forms
from .models import *
from django.forms import ModelForm, Textarea, ModelChoiceField, DateInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
        
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

class CompetitionGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompetitionGroupForm, self).__init__(*args, **kwargs)
        # change default labels for the form
        self.fields['users'].label = "Participants"

    users = forms.ModelMultipleChoiceField(queryset = User.objects.exclude(profile__role='instructor').all())

    class Meta:
        model = CompetitionGroup
        fields = ('name', 'description', 'reward', 'users')
        widgets = {
            'users': forms.CheckboxSelectMultiple()
        }

class ClassTypeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(CompetitionGroupForm, self).__init__(*args, **kwargs)
    #     # change default labels for the form
    #     self.fields['users'].label = "Participants"

    # users = forms.ModelMultipleChoiceField(queryset = User.objects.exclude(profile__role='instructor').all())

    class Meta:
        model = ClassType
        fields = ('name', 'description', 'start_date','end_date')
        widgets = {
            'start_date': DateInput(attrs={'class':'datepicker'}),
            'end_date': DateInput(attrs={'class':'datepicker'}),
            'description': Textarea()
        }

class ClassScheduleForm(forms.ModelForm):

    DAYS = (
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    )
    day_of_week = forms.ChoiceField(choices=DAYS, required=True)
    instructor = forms.ModelChoiceField(queryset = Profile.objects.filter(role='instructor'))
    instructor.label_from_instance = lambda obj: "%s %s" % (obj.user.first_name, obj.user.last_name)
    class Meta:
        model = ClassSchedule
        fields = ('instructor', 'day_of_week', 'location', 'start_time', 'end_time', 'points')
        widgets = {
            'start_time': DateInput(attrs={'class':'timepicker'}),
            'end_time': DateInput(attrs={'class':'timepicker'}),
        }