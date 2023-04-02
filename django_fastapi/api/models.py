from django.db import models
from django.contrib.auth.models import AbstractUser

from safedelete.models import (HARD_DELETE_NOCASCADE, SOFT_DELETE_CASCADE, SafeDeleteModel)

class Persona(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    edad = models.IntegerField()

    def data(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad
        }

    class Meta:
        db_table = 'persona'
        verbose_name = 'persona'
        verbose_name_plural = 'Persona'
        ordering = ['-id']

class User(AbstractUser, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']

class Token(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    # history = HistoricalRecords()
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,  related_name='+', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        db_table = "cs_token"
        ordering = ['-id']  # Orders by Id ("-" means descending)
