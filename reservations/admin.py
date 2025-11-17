# reservations/admin.py

from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el admin de Reservas.
    Esto hace que el panel sea mucho más útil.
    """
    
    # Muestra estas columnas en la lista de reservas
    list_display = ('name', 'email', 'instagram', 'created_at')
    
    # Añade filtros en el panel derecho (ej. por fecha)
    list_filter = ('created_at',)
    
    # Añade una barra de búsqueda
    search_fields = ('name', 'email', 'instagram')
    
    # Hacemos que la data sea de solo-lectura en el admin
    # Es más seguro, ya que solo queremos 'monitorear', no editar.
    
    def has_add_permission(self, request):
        # Deshabilita el botón de "Añadir reserva"
        return False

    def has_change_permission(self, request, obj=None):
        # Deshabilita la edición
        return False

    def has_delete_permission(self, request, obj=None):
        # Deshabilita el borrado
        return False