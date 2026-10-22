# Python.DjangoInputValidation.json -> "Django Input Validation Python" [InputValidation]
# Expected: method django is_valid (form validation in a Django view)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ShippingAddressForm


@login_required
def shipping_address(request):
    form = ShippingAddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        request.session["shipping_address"] = form.cleaned_data
        return redirect("checkout-payment")
    return render(request, "orders/shipping_address.html", {"form": form})
