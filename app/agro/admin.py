from django.contrib import admin

from .models import Crop, CropType, Farm, Farmer

admin.site.register(Crop)
admin.site.register(CropType)
admin.site.register(Farm)
admin.site.register(Farmer)
