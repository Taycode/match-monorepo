from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField


class Talent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    parsed_role = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    parsed_years_of_experience = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    resume_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'talents'

    def __str__(self):
        return f'{self.first_name} {self.last_name} -> {self.email}'
