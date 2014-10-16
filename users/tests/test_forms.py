from unittest import TestCase
import pytest
from django.core.exceptions import ValidationError

from .. import forms
from ..models import User


class UserCreationFormTest(TestCase):

    def test_passwords_match(self):
        test_password = "test valid password"
        form = forms.UserCreationForm(data={
            'password1': test_password,
            'password2': test_password,
        })
        form.is_valid()  # populates cleaned_data
        form.clean()

    def test_passwords_differ(self):
        form = forms.UserCreationForm(data={
            'password1': "passwords",
            'password2': "differ",
        })
        form.is_valid()
        with pytest.raises(ValidationError) as excinfo:
            form.clean()
        assert form.PASSWORDS_DONT_MATCH in str(excinfo.value)

    @pytest.mark.django_db
    def test_committed_saving(self):
        test_password = "test valid password"
        form = forms.UserCreationForm(data={
            'name': "Joe",
            'email': "joe@example.com",
            'password1': test_password,
            'password2': test_password,
        })
        saved = form.save()
        retrieved = User.objects.get(pk=saved.pk)
        assert saved == retrieved

    def test_uncommitted_saving(self):
        test_password = "test valid password"
        form = forms.UserCreationForm(data={
            'name': "Joe",
            'email': "joe@example.com",
            'password1': test_password,
            'password2': test_password,
        })
        assert form.save(commit=False).pk is None
