from mailjet_rest import Client
from private_details import mailjet_public_api_key as api_key, mailjet_secret_api_key as api_secret, skill_sync_address
from private_details import mailjet_sender_email as sender
from services import job_seeker_services

mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def password_reset_activation_email(user, activation_token):
    activation_link: str =skill_sync_address + 'profile/password/reset?activation_token=' + activation_token
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
                        "Name": f"{user.username}"
                    }
                ],
                "Subject": "Password Reset Request at Skill-Sync",
                "TextPart": "You requested a password reset for your Skill-Sync account.",
                "HTMLPart": f'<h3>Hello, {user.username}!</h3><br/>' +
                            f'<p>You have requested a password request at our website.</strong></p>' +
                            f'If you haven\'t requested a password request please ignore this email.' +
                            f"If you would like to proceed resetting your password please click below:"
                            f"<p><a href='{activation_link}'>RESET PASSWORD!</a></p>" +
                            '<p>May the secure connection be with you!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=data_password_reset_activation)
    return result


def password_reset_email(payload, generated_password):
    data_password_reset = {
        'Messages': [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Skill Sync"
                },
                "To": [
                    {
                        "Email": f"{payload['email']}",
                        "Name": f"{payload['username']}"
                    }
                ],
                "Subject": "Password Reset Confirmation at Skill-Sync",
                "TextPart": "You requested a password reset for your Skill-Sync account.",
                "HTMLPart": f"<h3>Hello, {payload['username']}!</h3><br/>" +
                            f'<p>Your password has been successfully reset. For the following account type: {payload["group"]}. ' +
                            f'Your new password is: <strong>{generated_password}</strong></p>' +
                            '<p>May the secure connection be with you!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=data_password_reset)
    return result

def company_match_request_notification():
    pass

def seeker_match_request_notification(payload, mini_cv_id):
    receiver, receiver_username = job_seeker_services.get_email_username_by_cv(mini_cv_id)
    pending_matches: str = skill_sync_address + f'job_seekers_match/pending_list'
    match_request = {
        'Messages': [
            {
                "From": {
                    "Email": f"{payload['email']}",
                    "Name": "Skill Sync"
                },
                "To": [
                    {
                        "Email": f"{receiver}",
                        "Name": f"{receiver_username}"
                    }
                ],
                "Subject": "Password Reset Confirmation at Skill-Sync",
                "TextPart": "You requested a password reset for your Skill-Sync account.",
                "HTMLPart": f"<h3>Hello, {receiver_username}!</h3><br/>" +
                            f'<p>You received a new match request for your main CV. ' +
                            f"<p>You can view your pending matches <a href='{pending_matches}'>HERE!</a></p>" +
                            '<p>Congratulations!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=match_request)
    return result
