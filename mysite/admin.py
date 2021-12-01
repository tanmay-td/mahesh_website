from django.contrib import admin
from mysite.models import agent,farmer,transaction

# Register your models here.

admin.site.register(agent)
admin.site.register(farmer)
admin.site.register(transaction)