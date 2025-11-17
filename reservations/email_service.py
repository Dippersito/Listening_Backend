# reservations/email_service.py

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

# --- Constantes del Email ---
# (Las sacamos de tu prompt)
IMAGE_URL = 'https://i.imgur.com/wrhMggB.jpeg'
LOCATION_URL = 'https://maps.app.goo.gl/dcHkQ1RAbjMp7p6B8'
# Usamos la fecha de la imagen (28 de Nov)
EVENT_DATE = '28 de Noviembre, 8:00 pm' 
EVENT_NAME = 'PERDIDO EN EL FINDE - LISTENING PARTY'
EVENT_PLACE = 'Residencial los Olmos E1 - JLByR'


def create_html_content(user_name):
    """
    Genera el HTML para el correo de confirmación.
    Usamos CSS inline para máxima compatibilidad con clientes de correo.
    """
    
    # Aquí adaptamos el HTML de la imagen que subiste
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-R">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ margin: 0; padding: 0; background-color: #121212; }}
            .container {{
                width: 90%; max-width: 600px; margin: 20px auto; 
                background-color: #1c1c1c; color: #ffffff; 
                font-family: Arial, sans-serif; border-radius: 8px; overflow: hidden;
            }}
            .header-img {{ width: 100%; max-width: 250px; height: auto; margin: 20px auto; display: block; }}
            .content {{ padding: 30px; text-align: center; }}
            h1 {{ font-size: 28px; color: #ffffff; margin-top: 0; }}
            p {{ font-size: 16px; line-height: 1.5; color: #c0c0c0; }}
            .details-box {{ 
                background-color: #252525; border-radius: 8px; 
                padding: 20px; text-align: left; margin: 25px 0;
            }}
            .details-box p {{ color: #ffffff; margin: 10px 0; }}
            .details-box span {{ font-weight: bold; color: #c0c0c0; }}
            .button {{
                display: inline-block;
                background-color: #e900fe; /* Rosa fucsia */
                color: #ffffff;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #121212;">
        <div class="container" style="width: 90%; max-width: 600px; margin: 20px auto; background-color: #1c1c1c; color: #ffffff; font-family: Arial, sans-serif; border-radius: 8px; overflow: hidden;">
            <div class="content" style="padding: 30px; text-align: center;">
                
                <img src="{IMAGE_URL}" alt="Perdido en el Finde" class="header-img" style="width: 100%; max-width: 250px; height: auto; margin: 20px auto; display: block;">

                <h1 style="font-size: 28px; color: #ffffff; margin-top: 0;">¡Reserva Confirmada!</h1>
                
                <p style="font-size: 16px; line-height: 1.5; color: #c0c0c0;">
                    ¡Hola, {user_name}!
                </p>
                <p style="font-size: 16px; line-height: 1.5; color: #c0c0c0;">
                    No te vas a quedar 'PERDIDO EN EL FINDE'. Tu lugar para el LISTENING PARTY está oficialmente reservado.
                </p>

                <div class="details-box" style="background-color: #252525; border-radius: 8px; padding: 20px; text-align: left; margin: 25px 0;">
                    <p style="color: #ffffff; margin: 10px 0;"><span style="font-weight: bold; color: #c0c0c0;">Evento:</span> {EVENT_NAME}</p>
                    <p style="color: #ffffff; margin: 10px 0;"><span style="font-weight: bold; color: #c0c0c0;">Fecha:</span> {EVENT_DATE}</p>
                    <p style="color: #ffffff; margin: 10px 0;"><span style="font-weight: bold; color: #c0c0c0;">Lugar:</span> {EVENT_PLACE}</p>
                </div>

                <a href="{LOCATION_URL}" target="_blank" class="button" style="display: inline-block; background-color: #e900fe; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; margin-top: 20px;">
                    VER UBICACIÓN EN MAPS
                </a>

            </div>
        </div>
    </body>
    </html>
    """

def send_confirmation_email(name, email):
    """
    Configura y envía el email transaccional usando Brevo.
    """
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    subject = "¡Reserva Confirmada! 🧭 PERDIDO EN EL FINDE - LISTENING PARTY"
    html_content = create_html_content(name)
    
    # --- Quién envía ---
    # IMPORTANTE: Este email debe estar validado como "Sender" en tu cuenta de Brevo.
    sender = {"name": "PERDIDO EN EL FINDE", "email": "no-reply@tu-dominio.com"} 
    
    # --- Quién recibe ---
    to = [{"email": email, "name": name}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, 
        sender=sender, 
        subject=subject, 
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email enviado a {email}: {api_response}")
        return True
    except ApiException as e:
        print(f"Error al enviar email a {email} usando Brevo: {e}")
        return False