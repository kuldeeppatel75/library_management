from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class MemberRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=10,unique=True)
    photo = models.ImageField(upload_to='member_photos/')
    membership_plan = models.CharField(max_length=20) # 4_hours, 8_hours, etc.
    amount = models.IntegerField() # 500, 800, 1000, 1600
    utr_number = models.CharField(max_length=50, default="PENDING_UTR")
    password = models.CharField(max_length=128, blank=True, null=True)
    is_approved = models.BooleanField(default=False) # Admin approve karega tab True hoga
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.photo:
            try:
                img = Image.open(self.photo)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.thumbnail((1024, 1024))
                output = BytesIO()
                img.save(output, format='JPEG', quality=70)
                output.seek(0)
                file_name = self.photo.name.split('.')[0] + '.jpg'
                self.photo.save(file_name, ContentFile(output.read()), save=False)
            except Exception as e:
                print("Image compression error:", e)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.membership_plan}"
    
class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General Inquiry'),
        ('Membership', 'Membership Issue'),
        ('Payment', 'Payment/UTR Problem'),
        ('Complaint', 'Complaint / Feedback'),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)  # Admin track karne ke liye ki complaint solve hui ya nahi

    def __str__(self):
        return f"{self.name} - {self.category} - {self.subject}"
