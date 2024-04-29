from django.contrib import admin
from core.models import Institute,Student,School,SchoolProxy
# Register your models here.
class InstituteAdmin(admin.ModelAdmin):
    list_display=['name']

class StudentAdmin(admin.ModelAdmin):
    list_display=['institute','name']

class SchoolAdmin(admin.ModelAdmin):
    list_display=['id','name','location','created','modified']
    readonly_fields=['slug','created','modified']

class SchoolProxyAdmin(admin.ModelAdmin):
    list_display=['id','name','location','created','modified']
    readonly_fields=['slug','created','modified']

admin.site.register(Institute,InstituteAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(SchoolProxy,SchoolProxyAdmin)