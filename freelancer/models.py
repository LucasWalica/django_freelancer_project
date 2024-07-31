from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum


class workingSectors(Enum):
    IT = 'IT'
    FINANCE = 'Finance'
    HEALTHCARE = 'Healthcare'
    EDUCATION = 'Education'
    MARKETING = 'Marketing'
    DESIGN = 'Design'
    ENGINEERING = 'Engineering'
    CUSTOMER_SERVICE = 'Customer Service'
    LEGAL = 'Legal'
    SALES = 'Sales'
    HR = 'Human Resources'
    WRITING_EDITING = 'Writing and Editing'
    DATA_SCIENCE = 'Data Science and Analytics'
    PROJECT_MANAGEMENT = 'Project Management'
    CONSULTING = 'Consulting'
    OPERATIONS = 'Operations'
    RESEARCH_DEVELOPMENT = 'Research and Development'
    ADMIN_SUPPORT = 'Administrative Support'
    CONSTRUCTION = 'Construction'
    REAL_ESTATE = 'Real Estate'
    ENTERTAINMENT_MEDIA = 'Entertainment and Media'
    OTHER = 'Other'


# Create your models here.
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False)
    active = models.BooleanField(default=True)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(upload_to='freelancerIcon/', null=True, blank=True)  

    def __str__(self):
        return f"{self.pk} - {self.user}"
    
class Skills(models.Model):
    fkFler = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.pk} - {self.fkFler} - {self.name}"

class ProjectOffer(models.Model):
    fkFler = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=20)
    desc = models.TextField(blank=False, max_length=300)
    price = models.FloatField(blank=False, validators=[MinValueValidator(5.00)])
    time_in_days = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    revisions = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='project_images/', null=True, blank=False)
    catOne = models.CharField(max_length=30,
                        choices=[(c.value, c.name) for c in workingSectors],
                        blank=False, null=False, 
                        default=workingSectors.OTHER.name)
    catTwo = models.CharField(max_length=30,
                        choices=[(c.value, c.name) for c in workingSectors],
                        blank=True, null=True, 
                        default=workingSectors.OTHER.name)

    def __str__(self):
        return f"{self.pk} - {self.fkFler} - {self.title}"
    

#only active when project sent
class CommetsOnFreelancer(models.Model):
    fkFler = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content =models.TextField(max_length=100, blank=False)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __Str__(self):
        return f"{self.pk} - {self.fkName}"
