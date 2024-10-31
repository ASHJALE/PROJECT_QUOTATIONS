from django.db import models
from django.contrib.auth.models import User


class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Add total cost field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class Pricing(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField for monetary values
    date = models.DateTimeField(auto_now_add=True)
    materials = models.ManyToManyField(Material, through='PricingMaterial')  # Add through model
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pricing for {self.project.name}"


class PricingMaterial(models.Model):
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)  # Price when added to pricing

    def __str__(self):
        return f"{self.material.name} x {self.quantity} for {self.pricing.project.name}"


class ProjectElement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Unnamed Element")  # Add a default
    # or
    # name = models.CharField(max_length=100, null=True, blank=True)  # Make it nullable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ElementMaterial(models.Model):
    element = models.ForeignKey(ProjectElement, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.material.name} x {self.quantity} for {self.element.name}"


class QuoteRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)  # This is the renamed field
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)