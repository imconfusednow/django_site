from django.db import models

class Emails(models.Model):
    Email = models.EmailField()
    Subject = models.CharField(max_length=50)
    Message = models.TextField()
    DateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Email


class site_contents(models.Model):
    result = models.TextField()
    link = models.CharField(max_length=50)
    number = models.IntegerField()
    tag = models.CharField(max_length=5)
    name = models.CharField(max_length=50)