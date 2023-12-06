from mailjet_rest import Client
from app_models.cv_models import CvCreation
from app_models.job_ads_models import Job_ad
from private_details import mailjet_public_api_key as api_key, mailjet_secret_api_key as api_secret, skill_sync_address
from private_details import mailjet_sender_email as sender
from services import job_seeker_services, company_services

mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def password_reset_activation_email(user, activation_token):
    activation_link: str = skill_sync_address + 'profile/password/reset?activation_token=' + activation_token
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


def company_match_request_notification(cv: CvCreation, job_ad: Job_ad, job_ad_id, mini_cv_id):
        receiver_email, receiver_username = company_services.find_company_email_username_by_job_ad(job_ad_id)
        sender_email, sender_username = job_seeker_services.get_email_username_by_cv(mini_cv_id)
        pending_matches: str = skill_sync_address + f'companies_match/requests'
        match_request = {
            'Messages': [
                {
                    "From": {
                        "Email": f"{sender}",
                        "Name": "Skill-Sync"
                    },
                    "To": [
                        {
                            "Email": f"{receiver_email}",
                            "Name": f"{receiver_username}"
                        }
                    ],
                    "Subject": "Match Request at Skill-Sync",
                    "TextPart": "You were matched in our platform.",
                    "HTMLPart": f"<h3>Hello, {receiver_username}!</h3><br/>"
                                f'<p>You received a new match request from {sender_username} for your Job Ad#{job_ad_id}.'
                                f'<p>Job Ad Description: {job_ad.description}'
                                f'<p>Job Ad Date Posted: {job_ad.date_posted}'
                                f'<p>Job Ad Date City: {job_ad.location_name}'
                                f'<p>Job Ad Remote: {job_ad.remote_status}'
                                f'<p>Job Ad Min Salary: {job_ad.min_salary}'
                                f'<p>Job Ad Max Salary: {job_ad.max_salary}'
                                f'<p><strong>CV</strong></p>'
                                f'<p><strong> Description:</strong> {cv.description}</p>'
                                f'<p><strong> Date Posted:</strong> {cv.date_posted}</p>'
                                f'<p><strong> City:</strong> {cv.location_name}</p>'
                                f'<p><strong> Remote:</strong> {cv.remote_status}</p>'
                                f'<p><strong> Min Salary:</strong> {cv.min_salary}</p>'
                                f'<p><strong> Max Salary:</strong> {cv.max_salary}</p>'
                                f'<p></p>'
                                f"<p>You can view your pending matches <a href='{pending_matches}'>HERE!</a></p>"
                                f'Contact the professional at: {sender_email}'
                                '<p>Congratulations!</p>' +
                                '<p></p>' +
                                '<p><em>Skill, Sync, Match!</em></p>'
                }

            ]
        }

        result = mailjet.send.create(data=match_request)
        return result


# This is also one of the points that needs to be refactored heavily, but needs
# refactoring at models, services, and routers, so it's left for a future point.
def job_seeker_match_request_notification(job_ad: Job_ad, job_ad_id, mini_cv_id):
    sender_email, sender_username = company_services.find_company_email_username_by_job_ad(job_ad_id)
    receiver_email, receiver_username = job_seeker_services.get_email_username_by_cv(mini_cv_id)
    pending_matches: str = skill_sync_address + f'job_seekers_match/pending_list'
    match_request = {
        'Messages': [
            {
                "From": {
                    "Email": f"{sender}",
                    "Name": "Skill-Sync"
                },
                "To": [
                    {
                        "Email": f"{receiver_email}",
                        "Name": f"{receiver_username}"
                    }
                ],
                "Subject": "Match Request at Skill-Sync",
                "TextPart": "You were matched in our platform.",
                "HTMLPart": f"<h3>Hello, {receiver_username}!</h3><br/>"
                            f'<p>You received a new match request from {sender_username} for your main CV. '
                            f'<p></p>'
                            f'<p><strong> Description:</strong> {job_ad.description}</p>'
                            f'<p><strong> Date Posted:</strong> {job_ad.date_posted}</p>'
                            f'<p><strong> City:</strong> {job_ad.location_name}</p>'
                            f'<p><strong> Remote:</strong> {job_ad.remote_status}</p>'
                            f'<p><strong> Min Salary:</strong> {job_ad.min_salary}</p>'
                            f'<p><strong> Max Salary:</strong> {job_ad.max_salary}</p>'
                            f'<p></p>'
                            f"<p>You can view your pending matches <a href='{pending_matches}'>HERE!</a></p>"
                            f'Contact the company at: {sender_email}'
                            '<p>Congratulations!</p>' +
                            '<p></p>' +
                            '<p><em>Skill, Sync, Match!</em></p>'
            }

        ]
    }

    result = mailjet.send.create(data=match_request)
    return result
