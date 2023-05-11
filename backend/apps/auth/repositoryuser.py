from backend.apps.user.models import UserModel
from sqlalchemy.orm import Session

import smtplib  # https://docs.python.org/3/library/smtplib.html
from email.message import EmailMessage


class UserRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def create_user(self, signup: UserModel) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except:
            return False
        return True

    def get_user(self):
        return self.sess.query(UserModel).all()

    # Схожость имен в базе
    def get_user_by_username(self, username: str):
        return self.sess.query(UserModel).filter(UserModel.username == username).first()


class SendEmailVerify:
    def sendVerify(token):    # https://myaccount.google.com/apppasswords
        email_address = "ermekoffdastan@gmail.com"
        email_password = "cpxuhepswnflagsa"

        msg = EmailMessage()
        msg['Subject'] = "Email subject"
        msg['Form'] = email_address
        msg['To'] = "ermekoffdastan@yandex.ru"
        msg.set_content(
            f"""\
            verify account
            http://localhost:8080/user/verify/{token}
            """
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
