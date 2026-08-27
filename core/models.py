from django.db import models

class MemberRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='member_photos/')
    membership_plan = models.CharField(max_length=20) # 4_hours, 8_hours, etc.
    amount = models.IntegerField() # 500, 800, 1000, 1600
    utr_number = models.CharField(max_length=50, default="PENDING_UTR")
    password = models.CharField(max_length=128, blank=True, null=True)
    is_approved = models.BooleanField(default=False) # Admin approve karega tab True hoga
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.membership_plan}"
