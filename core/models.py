from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils import timezone
import random
import string


User = get_user_model()


def generate_code():
    s = string.ascii_uppercase
    code = ''.join([s[random.randint(0, len(s)-1)] for i in range(6)])
    return code


# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=255)
    banner = models.ImageField(blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='forms'
    )
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=8, default=generate_code)

    def __str__(self):
        return 'Form %s' % self.name


class Entry(models.Model):
    ENTRY_CHOICES = (
        ('number', 'Number'),
        ('integer', 'Integer'),
        ('text', 'Text'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('decimal', 'Decimal'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('bool', 'Boolean'),
        ('ipv4', 'IPV4 Adress'),
        ('ipv6', 'IPV6 Adress'),
        ('ipv46', 'IPV4 or IPV6 Adress'),
    )
    form = models.ForeignKey(
        'Form', on_delete=models.CASCADE, related_name='entries'
    )
    name = models.CharField(max_length=8)
    label = models.CharField(max_length=64)
    help_text = models.CharField(max_length=255, default="", blank=True)
    max_length = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(255)],
        default=255
    )
    type = models.CharField(
        max_length=10, choices=ENTRY_CHOICES, default='text'
    )

    def __str__(self):
        return "Entry %s" % self.name


class Record(models.Model):
    entry = models.ForeignKey(
        'Entry', on_delete=models.CASCADE, related_name='records'
    )
    value = models.CharField(max_length=255)
    date_submitted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+',
        blank=True, null=True
    )
