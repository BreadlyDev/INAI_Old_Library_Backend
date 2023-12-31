from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.exceptions import ValidationError

ROLES = (
    ("Admin", "Admin"),
    ("Librarian", "Librarian"),
    ("Student", "Student")
)


def validate_phone(phone):
    if not phone.isdigit():
        raise ValidationError("Номер телефона должен состоять из цифр")


def set_password_exist(self, password):
    if not password:
        self.set_password(password)


class Group(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "groups"
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"{self.name} группа"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязательное поле")

        email = self.normalize_email(email)
        role = extra_fields.get("role", ROLES[2][1])

        if role not in dict(ROLES).keys():
            raise ValueError("Неверная роль пользователя")

        user = self.model(email=email, **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = ROLES[0][1]

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[validate_phone])
    role = models.CharField(max_length=150, choices=ROLES, default=ROLES[2][1])
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              null=True, blank=True, unique=False)

    username = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.role} {self.firstname} {self.lastname}"

    def save(self, *args, **kwargs):
        if self.group is None and self.role == ROLES[2][1]:
            raise ValidationError({"Сообщение": "У студентов обязательно должна быть указана группа"})
        if self.password and not self.password.startswith(("pbkdf2_sha256$", "bcrypt")):
            self.set_password(self.password)
        super().save(*args, **kwargs)
