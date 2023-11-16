from mailjet_rest import Client
from private_details import mailjet_public_api_key as api_key, mailjet_secret_api_key as api_secret
from private_details import mailjet_sender_email as sender

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def password_reset_email(user, generated_password):
    data_password_reset = {
        'Messages' : [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Skill Sync"
                },
                "To": [
                    {
                        "Email": f"{user.email}",
                        "Name": {user.username}
                    }
                ],
                "Subject": "Password Reset at SkillSync",
                "TextPart": "You requested a password reset for your SkillSync account.",
                "HTMLPart": f'<h3>{user.username}., !</h3><br/>'
                            '<p>Your password has been successfully reset.'
                            f'Your new password is: <strong>[{generated_password}]</strong></p>'
                            '<p>May the secure connection be with you!</p>'
                            '<p></p>'
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=data_password_reset)

    return result