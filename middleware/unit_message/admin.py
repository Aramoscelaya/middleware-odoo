from django.contrib import admin
from . import models

# Register your models here.


class UnitMessageAdmin(admin.ModelAdmin):
    # Campos de solo lectura
    readonly_fields = ('created_at', 'updated_at')
    # Columnas a mostrar en la tabla
    list_display = ('entity', 'status', 'active', 'created_at')
    # Orden jerárquico de las columnas en la tabla. Usar '-' para invertir el orden.
    ordering = ('-updated_at',)
    # Campo para crear una jerarquía de fechas de filtro rápido (por mes y luego por día)
    date_hierarchy = 'created_at'
    # Campos de filtros
    list_filter = ('entity', 'status', 'active', 'updated_at')


admin.site.register(models.unit_message, UnitMessageAdmin)