import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("teodorstefu@gmail.com")
to_email = Email("ilinca.olte@gmail.com")
subject = "Monkeeeeey"
content = Content("text/plain", "Acesta este un mail formal de la Monkey catre iub.")
mail = Mail(from_email, subject, to_email, content)
print mail.get()
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)