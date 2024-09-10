from django.db import models


class Booking(models.Model):
    sector = models.CharField(max_length=50)
    time_slot = models.CharField(max_length=100)
    client_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sector} - {self.client_email}"
