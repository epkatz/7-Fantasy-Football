from django.core.mail import send_mail



def registration_email(username, email, team_name):
    message = "Welcome to the Team7 Fantasy League!\nYour team is called " + team_name
    send_mail('Welcome ' + username, message, 'no-response@team7.com', [email], fail_silently=False)
    
