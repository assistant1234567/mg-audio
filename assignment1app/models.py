from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_past(value):
    if value < timezone.now():
        raise ValidationError("Uploaded time cannot be in the past.")

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    uploaded_time = models.DateTimeField(validators=[validate_not_past])
    audio_file = models.FileField(upload_to='audio_files/', null=False)
    

    def __str__(self):
        return self.name
