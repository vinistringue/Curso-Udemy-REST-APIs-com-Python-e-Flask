import requests
from flask import current_app

def enviar_email_confirmacao(usuario):
    # Link de confirmação (ajuste URL base se for produção)
    link = f"http://localhost:5000/confirmacao/{usuario.user_id}"

    # Corpo do email em HTML
    corpo_email = f"""
    <html>
        <body>
            <h2>Bem-vindo ao sistema!</h2>
            <p>Para ativar sua conta, clique no link abaixo:</p>
            <a href="{link}">Confirmar meu email</a>
        </body>
    </html>
    """

    # Envio via API Mailgun
    return requests.post(
        f"https://api.mailgun.net/v3/{current_app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={
            "from": current_app.config['EMAIL_FROM'],
            "to": usuario.login,
            "subject": "Confirme seu cadastro",
            "html": corpo_email
        }
    )
