import threading
from django.core.mail import send_mail

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            'from@example.com',
            self.recipient_list,
            fail_silently=False,
        )

def send_email_thread(subject, message, recipient_list):
    EmailThread(subject, message, recipient_list).start()
