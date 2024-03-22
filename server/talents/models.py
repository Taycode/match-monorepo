from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField


class Talent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    skills = ArrayField(models.CharField(max_length=50))
    resume = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'talents'
