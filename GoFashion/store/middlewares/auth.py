from django.shortcuts import redirect


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request, *args, **kwargs):
        return_url = request.META['PATH_INFO']
        if not request.session.get('customer'):
            return redirect(f'/login?return_url={return_url}')

        response = get_response(request, *args, **kwargs)

        return response

    return middleware
