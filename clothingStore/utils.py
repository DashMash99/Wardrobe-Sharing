import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print ('Cart: ', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["days"]

            product = Product.objects.get(id=i)
            total = (product.pricePerDay * cart[i]["days"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["days"]

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'pricePerDay': product.pricePerDay,
                    'imageURL':product.imageURL,
                    },
                'days': cart[i]["days"],
                'get_total': total
            }
            items.append(item)
        except:
            pass

    return{'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return{'cartItems':cartItems, 'order':order, 'items':items}


def guestOrder(request, data):
    
    print('User is not logged in')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            days=item['days']
        )

    return customer, order
