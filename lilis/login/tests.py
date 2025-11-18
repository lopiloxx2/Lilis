from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .forms import RegistroForm
from .models import validar_rut, PerfilUsuario


class RegistroFormTests(TestCase):
	def test_password_mismatch(self):
		form_data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password1': 'secret1',
			'password2': 'secret2',
			'rut': '12.345.678-5',
			'telefono': '12345678',
			'empresa': 'ACME'
		}
		form = RegistroForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertIn('password2', form.errors)

	def test_valid_form(self):
		form_data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password1': 'secret',
			'password2': 'secret',
			'rut': '12.345.678-5',
			'telefono': '12345678',
			'empresa': 'ACME'
		}
		form = RegistroForm(data=form_data)
		self.assertTrue(form.is_valid())


class ValidarRutTests(TestCase):
	def test_valid_rut(self):
		# Known valid RUT: 12.345.678-5 (calculated DV = 5)
		try:
			validar_rut('12.345.678-5')
		except ValidationError:
			self.fail('validar_rut raised ValidationError for a valid RUT')

	def test_invalid_rut(self):
		with self.assertRaises(ValidationError):
			validar_rut('12.345.678-0')


class PerfilUsuarioModelTests(TestCase):
	def test_perfil_str(self):
		user = User.objects.create_user(username='u1', password='p')
		perfil = PerfilUsuario.objects.create(user=user, rut='12.345.678-5')
		self.assertEqual(str(perfil), 'u1 (12.345.678-5)')

