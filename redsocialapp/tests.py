from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Perfil
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class IngresoViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        #se crea una simulacion de una imagen para el perfil
        imagen_perfil = SimpleUploadedFile(
            name='test_profile.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        
        self.perfil = Perfil.objects.create(
            user=self.user,
            email='test@example.com', 
            nombre='Test',
            imagen=imagen_perfil,    
            confirmado=True,
            creado=True
        )

    def test_ingreso_get(self): #este test verifica que si se accede por GET a la vista, se muestra el template.
        response = self.client.get(reverse('ingreso'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ingreso.html')

    def test_ingreso_redirect_si_autenticado(self): #este test simula que un usuario autenticado entra a la página de login.
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('ingreso'))
        self.assertRedirects(response, reverse('inicio'))

    def test_ingreso_post_credenciales_invalidas(self): #este test verifica el comportamiento cuando las credenciales son inválidas.
        response = self.client.post(reverse('ingreso'), {
            'username': 'noexiste',
            'password': 'algo'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña no válidos.')

    def test_ingreso_post_credenciales_validas_redirige_inicio(self):
        response = self.client.post(reverse('ingreso'), {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)  # Añade follow=True
        self.assertRedirects(response, reverse('inicio'))
        self.assertTrue(response.context['user'].is_authenticated)  #verifica autenticación