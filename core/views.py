from django.shortcuts import render
from django.views import View
# from django.http import response
from core.models import Institute
from django.template.response import TemplateResponse
# Create your views here.

class HomeView(View):
    def get(self,request,*args,**kwargs):
        context={}
        context['institutes']=Institute.objects.all()
        # context['cal']=1/0
        # return render(request,"core/home.html",context)
        return TemplateResponse(request,"core/home.html",context)