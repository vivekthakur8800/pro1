from django.shortcuts import render
from django.views import View
# from django.http import response
from core.models import Institute
# Create your views here.

class HomeView(View):
    def get(self,request,*args,**kwargs):
        context={}
        context['institutes']=Institute.objects.all()
        return render(request,"core/home.html",context)