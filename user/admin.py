from django.contrib import admin
from django import forms
from user.models import User
# Register your models here.
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),required=False)
    class Meta:
        model=User
        fields='__all__'

    def save(self,commit=True):
        user=super(UserForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class UserAdmin(admin.ModelAdmin):
    form=UserForm
    list_display=['id','email','name','is_superuser','created','modified']
    list_filter=['is_active','last_login']
    search_fields=['id','name','email']

admin.site.register(User,UserAdmin)