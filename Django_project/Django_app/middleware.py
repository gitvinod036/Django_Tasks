from django.http import HttpResponse

class SampleMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        print("Before request")
        response=self.get_response(request)
        print("After request")
        return response
    

class LastMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("initiated")
    def __call__(self,request):
        # response=self.get_response(request)
        # return response
    
        try:
            cookie=request.COOKIES.get("first_cookie")
            if cookie:
                request["name"]="New_User"
                response=self.get_response(request)
                return response
        except:
            return HttpResponse("Invalid")
        