import random
import string

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from store.models.customer import Customer


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # one time password
        letters = string.ascii_lowercase
        letters += string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        print(result_str)

        # verify
        customer = Customer.objects.get(email=email)

        # send email with one time password
        # this is remaining

        customer.password = make_password(result_str)
        customer.save()
        return redirect('login')
    else:
        return render(request, 'password_reset.html')
