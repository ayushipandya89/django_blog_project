from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, MinLengthValidator, \
    FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from users.constants import UNIQUE_USERNAME, FIRSTNAME_ERROR, LASTNAME_ERROR, USERNAME_HELPTEXT


# Create your models here.
class User(AbstractUser):
    """
    model to store user's personal information
    """
    genders = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            USERNAME_HELPTEXT
        ),
        validators=[username_validator, MinLengthValidator(2)],
        error_messages={
            "unique": UNIQUE_USERNAME,
        },
    )

    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message=FIRSTNAME_ERROR,
        code='first_name'
    )])

    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message=LASTNAME_ERROR,
        code='last_name'
    )])

    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=genders)

    class Meta:
        db_table = 'AuthUsers'
        verbose_name = "Personal details"
        permissions = [
            ("list_user", "Can list user"),

        ]

    def __str__(self):
        return f"{self.username}-{self.id}"

