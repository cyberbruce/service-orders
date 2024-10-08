from django.contrib import admin
from . import models


admin.site.site_header = 'California Computer Technologies'

admin.site.register(models.User)
