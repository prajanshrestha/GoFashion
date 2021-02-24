from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View

from store.models.customer import Customer


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        post_data = request.POST
        first_name = post_data.get('firstname')
        last_name = post_data.get('lastname')
        phone = post_data.get('phone')
        email = post_data.get('email')
        password = post_data.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None

        # creating customer object
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validate_customer(customer)

        # saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    # customer validation
    def validate_customer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = 'First Name is required!'
        elif len(customer.first_name) < 3:
            error_message = 'First Name is too short. It must be at least 3 characters long!'
        elif not customer.last_name:
            error_message = 'Last Name is required!'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name is too short. It must be at least 3 characters long!'
        elif not customer.phone:
            error_message = 'Phone number is required!'
        elif len(customer.phone) < 10:
            error_message = 'Phone number must be 10 characters long!'
        elif len(customer.phone) > 10:
            error_message = "Phone number can't be more than 10 characters!"
        elif not customer.email:
            error_message = 'Email field is empty!'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 characters long!'
        elif not customer.password:
            error_message = 'Password field is empty!'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 characters long!'
        elif customer.is_exists():
            error_message = 'Email address already exists!'

        return error_message
