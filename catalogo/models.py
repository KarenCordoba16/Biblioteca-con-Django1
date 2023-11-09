from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
import uuid 
from biblioteca import settings
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    email = models.EmailField(_('email adress'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        
        return '{}{}'.format(settings.STATIC_URL, 'img/user-default.png')

class Genero(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del género (por ej: PRogramación, DB, SO, etc.)")

    def __str__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaNac = models.DateField(null=True, blank=True)
    fechaDeceso = models.DateField('Fallecido',null=True, blank=True)

    def get_absolute_url(self):
        return reverse('autorInfo', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.nombre}, {self.apellido}'
    
class Idioma(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del idioma, por ej: Inglés, etc.")

    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=1000, help_text="Ingrese un resumen del libro")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn/10">ISBN numero</a>')
    imagen = models.ImageField(upload_to='catalogo/upload/img', null=True, blank=True)
    genero = models.ManyToManyField(Genero, help_text="Seleccione un genero (o varios) para el libro.")
    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('LibroInfo', args=[str(self.id)])
    
    def __str__(self):
        return self.titulo
    


class Ejemplar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    fechaDevolucion = models.DateField(null=True, blank=True)

    ESTADO_EJEMPLAR = (
        ('m', 'en mantenimiento'),
        ('p', 'prestado'),
        ('d', 'disponible'),
        ('r', 'reservado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_EJEMPLAR, blank=True, default='d', help_text='Disponibilidad del ejemplar')
    # Foreign keys
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["fechaDevolucion"]

    def __str__(self):
        return f"{self.id} ({self.libro.titulo})"
    
