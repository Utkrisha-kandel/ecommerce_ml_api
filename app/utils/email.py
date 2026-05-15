from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)
async def send_order_confirmation(email: str, order_id: str, total_price: float):
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=[email],
        body=f"""
        Hi there!

        Your order has been placed successfully.

        Order ID: {order_id}
        Total Price: ${total_price}

        Thank you for shopping with us!
        """,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
