from django.test import TestCase
from .models import User, Form, Entry, Record
from .forms import RecordForm


# Create your tests here.
class FormModelTest(TestCase):
    def test_create_form(self):
        user = User.objects.create(
            username='brad'
        )
        return Form.objects.get_or_create(
            author=user,
            defaults={
                'name': 'Python Survey 2022',
                'description': 'A survey to get feedback about the usage of python as main language.',
            }
        )[0]


class EntryModelTest(FormModelTest):
    def test_create_entry(self):
        form = self.test_create_form()
        for _ in Entry.ENTRY_CHOICES:
            Entry.objects.get_or_create(
                form=form,
                name=_[0],
                defaults={
                    'label': _[1],
                    'help_text': '',
                    'max_length': 64,
                    'type': _[0]
                }
            )


class RecordModelTest(EntryModelTest):
    def test_create_record(self):
        self.test_create_entry()
        data = {
            'number': '123',
            'integer': '-123',
            'text': 'Hello',
            'date': '2022-05-23',
            'time': '10:00',
            'decimal': '3.5',
            'email': 'example@example.com',
            'url': 'http://example.com',
            'bool': 'true',
            'ipv4': '127.0.0.1',
            'ipv6': '::1',
            'ipv46': '::1',
        }
        for entry in Entry.objects.filter():
            Record.objects.create(
                entry=entry,
                value=data[entry.type]
            )


class RecordFormTest(EntryModelTest):
    def test_create_record(self):
        self.test_create_entry()
        data = {
            'number': '123',
            'integer': '-123',
            'text': 'Hello',
            'date': '2022-05-23',
            'time': '10:00',
            'decimal': '3.5',
            'email': 'example@example.com',
            'url': 'http://example.com',
            'bool': 'true',
            'ipv4': '127.0.0.1',
            'ipv6': '::1',
            'ipv46': '::1',
        }
        for entry in Entry.objects.filter():
            form = RecordForm(entry, {
                'value': data[entry.type]
            })
            self.assertTrue(form.is_valid())
            form.save()
