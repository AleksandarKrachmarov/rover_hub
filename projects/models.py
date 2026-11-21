from django.conf import settings
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    class Category(models.TextChoices):
        CONTROLLER = 'controller', 'Controller'
        SENSOR = 'sensor', 'Sensor'
        MOTOR = 'motor', 'Motor'
        POWER = 'power', 'Power'
        CHASSIS = 'chassis', 'Chassis'
        OTHER = 'other', 'Other'


    name = models.CharField(max_length=100)
    category = models.CharField(choices=Category.choices, max_length=20)

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'planning', 'Planning'
        IN_PROGRESS = 'in_progress', 'In Progress'
        TESTING = 'testing', 'Testing'
        COMPLETED = 'completed', 'Completed'

    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PLANNING)
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,  blank=True)
    components = models.ManyToManyField(
        Component,
        through='ProjectComponent',
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

class ProjectComponent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.project.name} - {self.component.name} | qty: {self.quantity}'
