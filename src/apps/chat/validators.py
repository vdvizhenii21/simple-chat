from django.core.exceptions import ValidationError


class ThreadValidators:
    @staticmethod
    def validate_participants_count(value):
        if len(value) > 2:
            raise ValidationError("Thread can only have 2 participants.")
