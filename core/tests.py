from django.test import TestCase
from .models import User, Form, Entry, Record
from .forms import RecordForm


# Create your tests here.
class FormModelTest(TestCase):
    def test_create_form(self):
        user = User.objects.get_or_create(
            username='brad'
        )[0]
        return Form.objects.get_or_create(
            author=user,
            defaults={
                'name': 'Python Survey 2022',
                'description': 'A survey to get feedback about'
                ' the usage of python as main language.',
            }
        )[0]


class EntryModelTest(FormModelTest):
    def test_create_entry(self):
        form = self.test_create_form()
        data = {
            'choice': 'A,B,C,D',
            'choices': 'A,B,C,D',
        }
        for _ in Entry.ENTRY_CHOICES:
            Entry.objects.get_or_create(
                form=form,
                name=_[0],
                defaults={
                    'label': _[1],
                    'help_text': '',
                    'max_length': 255,
                    'type': _[0],
                    'metadata': data.get(_[0], ''),
                }
            )
        Entry.objects.get_or_create(
            form=form,
            name='optional',
            defaults={
                'label': 'optional',
                'type': _[0],
                'optional': True
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
            'choice': '0',
            'choices': '0,1',
        }
        for entry in Entry.objects.filter():
            Record.objects.create(
                entry=entry,
                value=data[entry.type],
                author=User.objects.get_or_create(
                    username='luck'
                )[0]
            )


class RecordFormTest(EntryModelTest):
    def test_create_fill_form(self):
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
            'choice': '0',
            'choices': [0, 1],
        }
        for entry in Entry.objects.filter():
            form = RecordForm(entry, {
                entry.name: data[entry.type]
                if entry.name != 'optional' else None
            })
            self.assertTrue(form.is_valid())
            form.instance.author = User.objects.get_or_create(
                username='joseph'
            )[0]
            form.save()
