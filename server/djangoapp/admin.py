from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'dealer_id', 'types', 'year']
    list_filter = ['types', 'car_make', 'dealer_id', 'year']
    search_fields = ['car_make', 'name']

# Register models here
if not admin.site.is_registered(CarMake):
    admin.site.register(CarMake, CarMakeAdmin)

if not admin.site.is_registered(CarModel):
    admin.site.register(CarModel)

