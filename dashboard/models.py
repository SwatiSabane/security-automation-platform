from django.db import models


class Vulnerability(models.Model):

    severity = models.CharField(max_length=20)

    package_name = models.CharField(max_length=200)

    cve_id = models.CharField(max_length=100,unique=True)

    description = models.TextField()

    STATUS_CHOICES = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
]
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='Open'
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.cve_id