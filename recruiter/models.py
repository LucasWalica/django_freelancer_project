from django.db import models
from django.contrib.auth.models import User, Permission
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

# maybe it would be a good idea to add a enum that contains all the 
# working positions for recruiter projects (python dev, dev, java dev....)
# this could be a little bit strange but it could help people 
# find what they want (or make it harder, dont know )

# Create your models here.
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False)
    active = models.BooleanField(default=True)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(upload_to='recruiterIcon/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user}"


# add ACTIVE attribute
class RecruiterProject(models.Model):
    fkRec = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=40)
    desc = models.TextField(blank=False, max_length=1000)
    catOne = models.CharField(max_length=30, choices=[(c.value, c.name) for c in workingSectors], blank=False, null=False)
    catTwo = models.CharField(max_length=30, choices=[(c.value, c.name) for c in workingSectors], blank=True, null=True)
    vacancies = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.fkRec} - {self.title}"
    

#recruiter can show or hide commets 
class CommentOnRecruiter(models.Model):
    fkRec = models.OneToOneField(RecruiterProfile, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=100, blank=False)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __Str__(self):
        return f"{self.pk} - {self.fkName}"
