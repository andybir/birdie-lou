import braintree
import weasyprint
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
from cart.cart import Cart
from weasyprint import HTML
from weasyprint.pdf import PDFFile, pdf_format


def payment_process(request):
    # cart = Cart(request)
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark order as paid
            order.paid = True
            # store unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # create invoice e-mail
            subject = 'birdie lou - invoice no. {}'.format(order.id)
            message = 'Thank you for ordering from birdie lou! Please see attached for your invoice.\n\nIf you have any questions about your order please contact us at hello@birdie-lou.com.'
            email = EmailMessage(subject,
                                 message,
                                 'hello@birdie-lou.com',
                                 [order.email])
            # generate PDF
            html = render_to_string('orders/order/pdf.html', 
                                    {'order': order})
            out = BytesIO()
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out,
                                    stylesheets=stylesheets)
            # attach PDF file
            email.attach('order_{}.pdf'.format(order.id),
                         out.getvalue(),
                         'application/pdf')
            # send e-mail
            email.send()

            # clear the cart
            # cart.clear()
            
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

# Edit WeasyPrint PDF
# html = HTML('http://weasyprint.org/')
# content = BytesIO(html.write_pdf())
# pdf_file = PDFFile(content)
# params = pdf_format('/OpenAction [0 /FitV null]')
# pdf_file.extend_dict(pdf_file.catalog, params)
# pdf_file.finish()
# pdf = pdf_file.fileobj.getvalue()
# open('/tmp/weasyprint.pdf', 'wb').write(pdf)