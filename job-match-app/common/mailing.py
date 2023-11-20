from mailjet_rest import Client
from private_details import mailjet_public_api_key as api_key, mailjet_secret_api_key as api_secret, skill_sync_address
from private_details import mailjet_sender_email as sender

mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def password_reset_activation_email(user, activation_token):
    data_password_reset_activation = {
        'Messages': [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Skill Sync"
                },
                "To": [
                    {
                        "Email": f"{user.email}",
                    }
                ],
                "Subject": "Password Reset Request at SkillSync",
                "TextPart": "You requested a password reset for your SkillSync account.",
                "HTMLPart": f'<h3>Hello!</h3><br/>' +
                            f'<p>You have requested a password request at our website.</strong></p>' +
                            f'If you haven\'t requested a password request please ignore this email.' +
                            f"If you would like to proceed resetting your password please click below:"
                            f"<p><a href='''{skill_sync_address + 'profile/password/reset/' +activation_token}'''>RESET PASSWORD!</a></p>" +
                            '<p>May the secure connection be with you!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=data_password_reset_activation)
    return result


def password_reset_email(user, generated_password):
    data_password_reset = {
        'Messages': [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Skill Sync"
                },
                "To": [
                    {
                        "Email": f"{user.email}",
                        "Name": f"{user.username}"
                    }
                ],
                "Subject": "Password Reset Confirmation at SkillSync",
                "TextPart": "You requested a password reset for your SkillSync account.",
                "HTMLPart": f'<h3>{user.username}!</h3><br/>' +
                            f'<p>Your password has been successfully reset. For the following account type: {user.group}. ' +
                            f'Your new password is: <strong>{generated_password}</strong></p>' +
                            '<p>May the secure connection be with you!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=data_password_reset)
    return result
