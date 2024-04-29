from django.db import models
from django.db.models.query import QuerySet
from core import choices
from django.db.models.signals import post_delete
from django.utils.text import slugify
import uuid
# Create your models here.

class Institute(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)

class Student(models.Model):
    institute=models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='students')
    name=models.CharField(max_length=200,null=True,blank=True)

class SoftDeletionQueryset(QuerySet):
    def delete(self):
        return super(SoftDeletionQueryset,self).update(object_status=choices.ObjectStatus.DELETED)
    
    def hard_delete(self):
        return super(SoftDeletionQueryset,self).delete()
    
class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return SoftDeletionQueryset(self.model).filter(object_status=choices.ObjectStatus.ACTIVE)
    def complete(self):
        return super().get_queryset()
    
class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    object_status=models.SmallIntegerField(choices=choices.ObjectStatus.CHOICES,default=choices.ObjectStatus.ACTIVE)
    objects=SoftDeletionManager()
    class Meta:
        abstract=True

    def delete(self,hard_delete=False):
        if not hard_delete:
            self.object_status=choices.ObjectStatus.DELETED
            self.save()
        else:
            super().delete()
        post_delete.send(sender=self.__class__,instance=self)



class SlugModel(models.Model):
    slug=models.SlugField(max_length=255,unique=True,blank=True)

    def get_slug_field(self):
        return 'name'
    
    def save(self,*args,**kwargs):
        if self.slug=="" or self.slug is None:
            self.slug=slugify(getattr(self,self.get_slug_field()))
            existing_slug_count=self.__class__.objects.filter(slug__icontains=self.slug).count()
            if existing_slug_count>0 and self.id is None:
                self.slug+="-{}".format(existing_slug_count+1)
        super(SlugModel,self).save(*args,**kwargs)

    class Meta:
        abstract=True

    def __str__(self):
        return "{}".format(getattr(self,self.get_slug_field()))
    
class School(BaseModel,SlugModel):
    name=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=500,null=True,blank=True)

class SchoolProxy(School):
    class Meta:
        proxy=True
        verbose_name_plural = "school pro"