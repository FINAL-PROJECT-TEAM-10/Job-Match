from pydantic import BaseModel

from app_models.validation_models import ALLOWED_PASSWORD


class PasswordUpdater(BaseModel):
    old_password: ALLOWED_PASSWORD
    new_password: ALLOWED_PASSWORD