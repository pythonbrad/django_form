from django import forms
from .models import Form as MForm, Entry, Record


class Form(forms.ModelForm):
    class Meta:
        model = MForm
        fields = ['name', 'description']


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['form']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['value']

    def __init__(self, entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.entry = entry
        self.fields['value'] = {
            'number': forms.fields.IntegerField(min_value=0),
            'integer': forms.fields.IntegerField(),
            'text': forms.fields.CharField(max_length=255),
            'date': forms.fields.DateField(),
            'time': forms.fields.TimeField(),
            'decimal': forms.fields.DecimalField(),
            'email': forms.fields.EmailField(),
            'url': forms.fields.URLField(),
            'bool': forms.fields.BooleanField(),
            'ipv4': forms.fields.GenericIPAddressField(protocol='ipv4'),
            'ipv6': forms.fields.GenericIPAddressField(protocol='ipv6'),
            'ipv46': forms.fields.GenericIPAddressField(protocol='both'),
        }[entry.type]
