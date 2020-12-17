from extuser.models import ExtUser
from sales_and_clients.cart import Cart


def fullname(request):
    username = request.user.username
    if username:
        user = ExtUser.objects.get(username=username)
        return {'fullname': user}
    else:
        return {'fullname': 'incognito'}


def cart(request):
    return {'cart': Cart(request)}

