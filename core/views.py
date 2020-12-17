from django.shortcuts import render


def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler403(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 403
    return response


def handler500(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 500
    return response
