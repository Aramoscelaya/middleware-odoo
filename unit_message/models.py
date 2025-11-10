from django.db import models

# Create your models here.
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class unit_message(models.Model):
    message = models.JSONField(null=True, blank=True, default=None, verbose_name='Mensaje unitario')
    original_message_id = models.IntegerField(verbose_name='ID Mensaje Original')   
    entity = models.CharField(max_length=50, verbose_name='Entidad')
    status = models.CharField(max_length=5, verbose_name='Estatus')
    active = models.IntegerField(verbose_name='Activo')
    response = CKEditor5Field('Response', config_name='Response')
    run_at = models.IntegerField(verbose_name='Run at')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Unit Message'
        verbose_name_plural = 'Unit Message'
        ordering = ['-updated_at']
        permissions = [
            ('can_edit_unit_message', 'Puede hacer todo en unit message'),
        ]
    
    def __str__(self):
        return self.entity