# reservations/models.py

from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    
    # 'unique=True' es clave. 
    # Si alguien intenta registrar el mismo email, la BD lo bloqueará.
    email = models.EmailField(unique=True) 
    
    # Hacemos el instagram único también, como pide el frontend
    instagram = models.CharField(max_length=50, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"