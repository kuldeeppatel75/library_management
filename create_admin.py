import os
import django

# Django environment setup
# (Agar tumhare project ka folder naam 'library_management' nahi hai, toh neeche settings wali line mein apne project ka naam likh dena)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_core.settings')
django.setup()

from django.contrib.auth.models import User

# Render ke environment variables se details uthayega
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'kuldeep_admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@codebykuldeep.site')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# Check karo ki admin pehle se exist karta hai ya nahi
if not User.objects.filter(username=username).exists():
    if password:
        User.objects.create_superuser(username=username, email=email, password=password)
        print("SUCCESS: Superuser created successfully!")
    else:
        print("ERROR: DJANGO_SUPERUSER_PASSWORD environment variable is missing!")
else:
    print("INFO: Superuser already exists. Skipping creation.")