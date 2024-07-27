from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False)
    active = models.BooleanField(default=True)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(upload_to='freelancerIcon/', null=True, blank=True)  


    def __str__(self):
        return f"{self.pk} {self.user}, {self.stars}"
    
class Skills(models.Model):
    fkFler = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.pk} {self.fkFler} {self.name}"

class ProjectOffer(models.Model):
    fkFler = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=20)
    desc = models.TextField(blank=False, max_length=300)
    price = models.FloatField(blank=False, validators=[MinValueValidator(5.00)])
    time_in_days = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    revisions = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='project_images/', null=False, blank=False)

    def __str__(self):
        return f"{self.pk} {self.fkFler} {self.title}"
