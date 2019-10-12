from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class LoanApplication(models.Model):
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    REJECTED = "rejected"
    TYPE_CHOICES = (
        (UNDER_REVIEW, "under_review"),
        (APPROVED, "approved"),
        (DISBURSED, "disbursed"),
        (REJECTED, "rejected"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=100000)
    tenure = models.PositiveIntegerField(default=12)
    status = models.CharField(max_length=20, default=UNDER_REVIEW, choices=TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s - %s" % (self.user.first_name, self.amount, self.tenure)
