
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config import settings

class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

router = APIRouter()

@router.post("/email")
async def send_email(email: EmailSchema):
    html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 25px; border-radius: 8px; border: 1px solid #e0e0e0; background-color: #ffffff;">
        <h2 style="color: #333333; text-align: left; margin-bottom: 20px;">Thank You for Utilizing Our Service</h2>
        <p style="font-size: 16px; line-height: 1.6; color: #555555;">
            Dear Valued User,
        </p>
        <p style="font-size: 16px; line-height: 1.6; color: #555555;">
            We extend our sincere gratitude for choosing and utilizing our service. Your engagement is highly valued, 
            and we are committed to providing you with the best possible experience.
        </p>
        <p style="font-size: 16px; line-height: 1.6; color: #555555;">
            Should you have any inquiries or require assistance, please do not hesitate to contact our support team. We are here to help.
        </p>
        <p style="font-size: 16px; line-height: 1.6; color: #555555; margin-top: 30px;">
            Sincerely, <br> The [Poogle/Baaler] Team
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 25px 0;">
        <p style="font-size: 10px; color: #aaaaaa; text-align: center;">
            <em>This message was generated with AI assistance. Ref: <h5>This is from the Batman</h5></em>
        </p>
    </div>
    """

    message = MessageSchema(
        subject="Thanks for using our service",
        recipients=[email.email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    # background_tasks.add_task(fm.send_message, message)
    await fm.send_message(message)
    return {"message": "email has been sent"}
