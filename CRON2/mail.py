from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

env_config = ConnectionConfig(
   MAIL_USERNAME='livingstonemaxwell971@gmail.com',
    MAIL_PASSWORD='',
    MAIL_FROM='livingstonemaxwell971@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='CRON2.0',
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER='templates',
 )

async def send_error_email(recepient,status_code):


    message=MessageSchema(
        subject=f'Cron Job Failed',
        recipients=[recepient,],
        template_body={'status_code':status_code},
        subtype='html'

    )
    f=FastMail(env_config)
    try:
       return  await f.send_message(message, template_name='error_mail.html')

    except Exception as e:
        return e
