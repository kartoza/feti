from django.core.validators import RegexValidator


UsernameValidator = [
    RegexValidator(r"^[\w.]+$")
]
