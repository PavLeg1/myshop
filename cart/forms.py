from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):

    # Позволяет выбрать количество от 1 до 20
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    
    # Позволяет указывать, должно ли quantity быть прибавлено к количеству в корзине
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)