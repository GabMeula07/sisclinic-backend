import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")

def send_reset_email(email: str, token: str):
    """
    Envia um e-mail de recuperação de senha usando SendGrid.
    """
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=email,
        subject="Redefinição de Senha",
        html_content=f"""
        <p>Você solicitou a redefinição de senha.</p>
        <p>Use o link abaixo para criar uma nova senha:</p>
        <a href="{reset_link}">{reset_link}</a>
        <p>Se você não solicitou essa ação, ignore este e-mail.</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}") 