from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Product
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         category=item['category'],
                                         available=item['available'])
                '''
                if vintage, make unavailable for purchase
                '''
                # if item['category'] == 'vintage accessories':
                #     item['available'] = False
                # current_order = OrderItem.objects.filter(order_id=order.id)
                # vintage = current_order.filter(category__startswith='vintage')
                # vint_id = vintage.values_list('product', flat=True)
                #     for id in vint_id:
                #         Product.objects.filter(id=id).update(available=False)

                # vintage = OrderItem.objects.filter(category__contains='vintage')
                # vintage_id = vintage.values('product_id')
                # first_id = vintage_id[:1]
                # Product.objects.filter(id=first_id).update(available=False)
                # vintage.update(available=False)
                    # vintage = OrderItem.objects.get(category__contains='vintage')
                    # vintage.update(available=False)

            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response