from django.db import models

class Tag(models.Model):
  # Must specify 'max_length' on CharFields.
  name = models.CharField(max_length = 255, unique = True)
  
  def __str__(self):
    return self.name