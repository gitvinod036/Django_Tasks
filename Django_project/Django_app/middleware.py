class SampleMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        print("Before request")
        response=self.get_response(request)
        print("After")
        return response
    

class LastMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("initiated")
    def __call__(self,request):
        response=self.get_response(request)
        return response
        