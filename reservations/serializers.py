# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'instagram']

    def validate_instagram(self, value):
        """
        Validación extra para asegurar que el instagram empiece con @
        (Tu frontend ya lo hace, pero es buena práctica validar en ambos lados)
        """
        if not value.startswith('@'):
            raise serializers.ValidationError("El usuario de Instagram debe comenzar con @.")
        
        # Re-usamos la regex de tu frontend (ligeramente adaptada para Python)
        import re
        if not re.match(r"^@[a-zA-Z0-9._]{3,30}$", value):
             raise serializers.ValidationError("Formato de Instagram inválido.")
        
        return value