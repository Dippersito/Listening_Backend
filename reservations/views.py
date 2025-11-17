# reservations/views.py

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer
from .email_service import send_confirmation_email

# Obtenemos el total de la configuración
TOTAL_CAPACITY = settings.TOTAL_EVENT_CAPACITY

@api_view(['GET'])
def get_reservation_count(request):
    """
    Endpoint para obtener los cupos restantes.
    GET /api/reservations/count
    """
    try:
        count = Reservation.objects.count()
        remaining = TOTAL_CAPACITY - count
        
        # Asegurarnos de que no sea negativo
        if remaining < 0:
            remaining = 0 
            
        return Response({"remaining": remaining}, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Fallback por si la BD falla (como en tu React)
        return Response({"remaining": TOTAL_CAPACITY}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_reservation(request):
    """
    Endpoint para crear una nueva reserva.
    POST /api/reservations/create
    """
    
    # --- Chequeo de Cupos ---
    if Reservation.objects.count() >= TOTAL_CAPACITY:
        return Response(
            {"error": "¡Lo sentimos! Las pulseras están agotadas, comunicate al 940183490."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # --- Serialización y Validación ---
    serializer = ReservationSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Guardamos la reserva en la BD
            reservation = serializer.save()
            
            # --- Envío de Email ---
            # Envolvemos el envío de email en un try/except
            # La reserva es exitosa aunque el email falle (es mejor)
            try:
                send_confirmation_email(reservation.name, reservation.email)
            except Exception as e:
                # En un proyecto real, aquí registraríamos el error (logging)
                print(f"¡Alerta! Reserva {reservation.id} guardada, pero email falló: {e}")

            # --- Respuesta Exitosa ---
            # Calculamos el nuevo restante
            remaining = TOTAL_CAPACITY - Reservation.objects.count()
            
            # Devolvemos la data que el frontend espera
            return Response(
                {
                    "newRemaining": remaining,
                    "name": reservation.name,
                    "email": reservation.email
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            # Esto puede pasar si hay un error de BD inesperado
            return Response(
                {"error": "Ocurrió un error interno al guardar."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    else:
        # --- Respuesta de Error de Validación ---
        # Si el serializer no es válido (ej. email duplicado, formato incorrecto)
        # DRF automáticamente devuelve un JSON como:
        # {"email": ["El correo ya está registrado."]}
        # Tu frontend ya sabe cómo manejar esto (errorData.email)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)