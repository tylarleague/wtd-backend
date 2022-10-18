from django.db import models

# Create your models here.
class Discount(models.Model):
    code = models.CharField(max_length=500, unique=True)
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return str(self.code) + " - " + str(self.percentage) + "%"