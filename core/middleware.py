from django.http import HttpResponse
def my_middleware(get_response):
    print("initialize--",get_response)
    def my_function(request):
        print("--request-before_view--",request)
        print("-authentication-",request.user.is_authenticated)
        print("-authentication-",request.GET)
        response=get_response(request)
        print("--response after view--",response)
        # print("--response after view--",response.context_data)
        return response
    return my_function


class MyMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("-class initializer-",self.get_response)
    def __call__(self,request):
        print('-class before view-',request)
        response=self.get_response(request)
        print('-class after view-',response)
        
        return response
    
    def process_view(self,request,*args,**kwargs):
        print("--class process middleware--")
        # return HttpResponse('hello middleware')
        return None

    def process_exception(self,request,exception):
        print("--class exception--",exception)
        return HttpResponse(exception)
    
    def process_template_response(self,request,reponse):
        print("--class response context--",reponse.context_data)
        reponse.context_data['hello']="yes"
        print("--class response context--",reponse.context_data)
        return reponse