# app/migrations/0002_create_superuser.py
from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='p@123eq!y6'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),  # <- fresh clone er last migration
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]