import threading

import resend
from flask import current_app


def enviar_correo(destinatario, asunto, html):
    """Envía un correo usando Resend API de forma asíncrona (no bloquea el request)."""
    app = current_app._get_current_object()
    threading.Thread(
        target=lambda: _enviar(app, destinatario, asunto, html)
    ).start()


def _enviar(app, destinatario, asunto, html):
    try:
        with app.app_context():
            resend.api_key = app.config["RESEND_API_KEY"]
            resend.Emails.send(
                {
                    "from": app.config["MAIL_DEFAULT_SENDER"],
                    "to": [destinatario],
                    "subject": asunto,
                    "html": html,
                }
            )
    except Exception:
        pass
