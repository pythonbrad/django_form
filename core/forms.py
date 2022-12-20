from django import forms
from crispy_bulma.widgets import FileUploadInput
from .models import Form as MForm, Entry, Record


class Form(forms.ModelForm):
    class Meta:
        model = MForm
        fields = ['name', 'description', 'banner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banner'].widget = FileUploadInput()


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'label', 'help_text', 'type', 'metadata']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = []

    def __init__(self, entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.entry = entry
        if entry.type == 'number':
            field = forms.fields.IntegerField(min_value=0)
        elif entry.type == 'integer':
            field = forms.fields.IntegerField()
        elif entry.type == 'text':
            field = forms.fields.CharField(max_length=255)
        elif entry.type == 'date':
            field = forms.fields.DateField(
                widget=forms.TextInput(attrs={'type': 'date'})
            )
        elif entry.type == 'time':
            field = forms.fields.TimeField(
                widget=forms.TextInput(attrs={'type': 'time'})
            )
        elif entry.type == 'decimal':
            field = forms.fields.DecimalField()
        elif entry.type == 'email':
            field = forms.fields.EmailField()
        elif entry.type == 'url':
            field = forms.fields.URLField()
        elif entry.type == 'bool':
            field = forms.fields.BooleanField(required=False)
        elif entry.type == 'ipv4':
            field = forms.fields.GenericIPAddressField(protocol='ipv4')
        elif entry.type == 'ipv6':
            field = forms.fields.GenericIPAddressField(protocol='ipv6')
        elif entry.type == 'ipv46':
            field = forms.fields.GenericIPAddressField(protocol='both')
        elif entry.type == 'choice':
            field = forms.fields.ChoiceField(
                choices=enumerate(entry.metadata.split(','))
            )
        elif entry.type == 'choices':
            field = forms.fields.MultipleChoiceField(
                choices=enumerate(entry.metadata.split(','))
            )
        else:
            raise Exception('Entry type "%s" not supported' % entry.type)
        self.fields[entry.name] = field
        self.fields[entry.name].help_text = entry.help_text
        self.fields[entry.name].label = entry.label

    def save(self, *args, **kwargs):
        self.instance.value = self.cleaned_data[self.instance.entry.name]
        return self.instance.save(*args, **kwargs)
