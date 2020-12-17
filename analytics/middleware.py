from .models import CountForIP, BlackIP


def count_page(get_response):
    import time
    import datetime
    def middleware(request):
        url_address = request.get_full_path()
        ip_address = request.META['REMOTE_ADDR']
        CountForIP.objects.create(page_url=url_address, ip_address=ip_address)

        response = get_response(request)
        visits = CountForIP.objects.filter(ip_address=ip_address)[:5]
        timer = visits[0].time - visits[4].time
        if timer.seconds < 1:
            BlackIP.objects.create(black_address=ip_address)

        return response

    return middleware
