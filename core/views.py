from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from core.models import Student
# from django.http import response
from core.models import Institute
from django.urls import reverse
from django.template.response import TemplateResponse
# Create your views here.

class HomeView(View):
    def get(self,request,*args,**kwargs):
        context={}
        context['institutes']=Institute.objects.all()
        # print("-reverse-",reverse('core:home'))
        # context['cal']=1/0
        # return render(request,"core/home.html",context)
        return TemplateResponse(request,"core/home.html",context)
    
class StudentList(ListView):
    model=Student
    template_name="core/students.html"
    # template_name_suffix="_get"
    context_object_name="students"

    def get_queryset(self):
        # return super().get_queryset()
        return self.model.objects.all()
    
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context["test"]="test_success"
        return context
    
    def get_template_names(self):
        # return super().get_template_names()
        return [self.template_name]
    
class StudentDetail(DetailView):
    model=Student
    template_name="core/student.html"
    # pk_url_kwarg="pk"
    context_object_name="stu"