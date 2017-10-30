import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("sender_email@gmail.com")
to_email = Email("destination_email@gmail.com")
subject = "Email subject"
content = Content("text/plain", "Here Mail text")
mail = Mail(from_email, subject, to_email, content)
print mail.get()
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)