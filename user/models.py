from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,Group,Permission
from core.models import SoftDeletionQueryset
from core import choices
from django.utils.translation import gettext_lazy as _
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from core.models import BaseModel,SlugModel
import random
import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
# Create your models here.


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, name, password=None,**extra_kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None,**extra_kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        extra_kwargs.setdefault('is_staff',False)
        extra_kwargs.setdefault('is_superuser',False)

        return self._create_user(email,name,password,**extra_kwargs)

    def create_superuser(self, email, name, password=None,**extra_kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        extra_kwargs.setdefault('is_staff',True)
        extra_kwargs.setdefault('is_superuser',True)
        extra_kwargs.setdefault('is_active',True)

        if extra_kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be True')
        if extra_kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff True')
        if extra_kwargs.get('is_active') is not True:
            raise ValueError('Superuser must have is_active True')
        
        return self._create_user(email,name,password,**extra_kwargs)
    
    def get_queryset(self):
        return SoftDeletionQueryset(self.model).filter(object_status=choices.ObjectStatus.ACTIVE)
    def complete(self):
        return super().get_queryset()
    
class PermissionMixins(models.Model):
    is_superuser=models.BooleanField(_('superuser status'),default=False,help_text=_('Designates get all the permissions without explicitly assigning them.'))
    groups=models.ManyToManyField(Group,verbose_name=_("groups"),blank=True,help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),related_name='user_groups_set',related_query_name='goognu_user')
    user_permissions=models.ManyToManyField(Permission,verbose_name=_('user permissions'),blank=True,help_text=_("Specific permissions for this user."),related_name="user_permissions_set",related_query_name="goognu_user")

    class Meta:
        abstract=True
    
    def get_groups_permissions(self,obj=None):
        permissions=set()
        for backend in auth.get_backends():
            if hasattr(backend,'get_groups_permissions'):
                permissions.update(backend.get_group_permissions(self,obj))
        return permissions
    
    def get_all_permissions(self,obj=None):
        return _user_get_all_permissions(self,obj)
    
    def has_perm(self,perm,obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self,perm,obj)
    
    def has_perms(self,perm_list,obj=None):
        for perm in perm_list:
            if not self.has_perm(perm,obj):
                return False
        return True
    
    def has_module_perms(self,app_label):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_perms(self,app_label)
        
    
def _user_get_all_permissions(user,obj):
    permissions=set()
    for backend in auth.get_backends():
        if hasattr(backend,'get_all_permissions'):
            permissions.update(backend.get_all_permissions(user,obj))
    return permissions
    
def _user_has_perm(user,perm,obj):
    for backend in auth.get_backends():
        if not hasattr(backend,'has_perm'):
            continue
        try:
            if backend.has_perm(user,perm,obj):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_perms(user,app_label):
    for backend in auth.get_backends():
        if not hasattr(backend,"has_module_perms"):
            continue
        try:
            if backend.has_module_perms(user,app_label):
                return True
        except PermissionDenied:
            return False
    return False

def user_image_directory(instance,filename):
    return "upload/users/user_{0}/{1}".format(instance.id,filename)

class User(AbstractBaseUser,BaseModel,PermissionMixins,SlugModel):
    name=models.CharField(max_length=240,null=True,blank=True)
    email=models.EmailField(verbose_name='email address',max_length=255,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    image=models.ImageField(upload_to=user_image_directory,null=True,blank=True,max_length=250)

    objects=CustomUserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['name']

    @property
    def username(self):
        return self.email.replace('@','')
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if not self.image:
            self._grab_avator()

    def _grab_avator(self):
        colors_lst = [
            "00AA55",
            "1BA39C",
            "03A678",
            "00AA00",
            "26A65B",
            "00A566",
            "4183D7",
            "3477DB",
            "007FAA",
            "3455DB",
            "0000E0",
            "0000B5",
            "E26A6A",
            "B381B3",
            "E26A6A",
            "BF6EE0",
            "FF00FF",
            "BF55EC",
            "D252B2",
            "9370DB",
            "D25299",
            "D25852",
            "D2527F",
            "E73C70",
            "F62459",
            "E000E0",
            "AA8F00",
            "AA8F00",
            "D47500",
            "FF4500",
            "E63022",
            "E76E3C",
            "EF4836",
            "FF0000",
            "DC143C",
        ]
        url = "https://ui-avatars.com/api/?name={}&background={}&color=FFF&font-size=0.55&bold=True&size=256".format(
            self.name, random.choice(colors_lst)
        )
        r=requests.get(url,timeout=5)
        img_temp=NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        self.image.save("user_{}.jpg".format(self.id),File(img_temp),save=True)
        