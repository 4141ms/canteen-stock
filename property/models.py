from django.db import models

# 供货商
class Supplier(models.Model):
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

