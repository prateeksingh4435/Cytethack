from django.contrib import admin

# Register your models here.
from .models import Host,Process


admin.site.register([Host,Process])