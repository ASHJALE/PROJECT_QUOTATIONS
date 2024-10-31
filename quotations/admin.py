from django.contrib import admin
from .models import Material, Project, Pricing, ProjectElement, QuoteRequest

admin.site.register(Material)
admin.site.register(Project)
admin.site.register(Pricing)
admin.site.register(ProjectElement)
admin.site.register(QuoteRequest)