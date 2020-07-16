from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 5)]
PRODUCT_SIZE_CHOICES = [
    ('0-3', '0-3'), ('3-6', '3-6'), ('6-12', '6-12'), 
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), 
    ('5', '5'),
]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                            choices=PRODUCT_QUANTITY_CHOICES,
                            coerce=int,
                            label=(''))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartAddSizeProductForm(forms.Form):
    size = forms.TypedChoiceField(
                        choices=PRODUCT_SIZE_CHOICES,
                        coerce=str,
                        label=(''))
    quantity = forms.TypedChoiceField(
                            choices=PRODUCT_QUANTITY_CHOICES,
                            coerce=int,
                            label=(''))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


# class SizeForm(forms.Form):
#     size = forms.TypedChoiceField(
#                         choices=PRODUCT_SIZE_CHOICES,
#                         coerce=str,
#                         label=(''))
    
