class PruebaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # (Opcional) Código antes de la vista
        print("Antes de la vista")

        response = self.get_response(request)

        # (Opcional) Código después de la vista
        print("Después de la vista")

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass