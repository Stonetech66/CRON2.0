from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s") 
load_dotenv()

password=os.getenv("MAIL_PASSWORD")
username=os.getenv("MAIL_USERNAME")
mail_from=os.getenv("MAIL_FROM")

STATUS_CODES={
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
}

env_config = ConnectionConfig(
   MAIL_USERNAME=username,
    MAIL_PASSWORD=password,
    MAIL_FROM=mail_from,
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='CRON2.0',
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER='templates',
 )

async def send_error_email(data):


    message=MessageSchema(
        subject=f'CronJob Failed 😞',
        recipients=[data['email'],],
        template_body={'status_code':data['code'], 'cron':data['cron'], 'message':STATUS_CODES[int(data['code'])] },
        subtype='html'

    )
    f=FastMail(env_config)
    try:
       await f.send_message(message, template_name='error_mail.html') 
       logger.info("Email sent") 
    except Exception as e:
        logger.error(f"Email failed to send {e} ") 
