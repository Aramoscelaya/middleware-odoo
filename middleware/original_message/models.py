from django.db import models

# Create your models here.
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class original_message(models.Model):
    file = models.CharField(max_length=350, verbose_name='Archivo')    
    entity = models.CharField(max_length=50, verbose_name='Entidad')    
    status = models.CharField(max_length=2, verbose_name='Estado')
    request = CKEditor5Field('Request', config_name='Request')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Original Message'
        verbose_name_plural = 'Original Message'
        ordering = ['-updated_at']
        permissions = [
            ('can_edit_original_message', 'Puede hacer todo en original message'),
        ]
    
    def __str__(self):
        return self.entity