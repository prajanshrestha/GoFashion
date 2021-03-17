from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View

from store.models.customer import Customer


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')  # this is done to hold the return_url
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                request.session['first_name'] = customer.first_name
                request.session['last_name'] = customer.last_name
                request.session['phone'] = customer.phone
                request.session['email'] = customer.email

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Email or Password is invalid!'
        else:
            error_message = 'Email or Password is invalid!'

        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')


def edit_profile(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == 'GET':
        data = {
            'customer': customer
        }
        return render(request, 'edit_profile.html', data)
    else:
        customer.first_name = request.POST['first_name']
        customer.last_name = request.POST['last_name']
        customer.phone = request.POST['phone']
        customer.email = request.POST['email']
        customer.save()

        request.session.clear()

        request.session['customer'] = customer.id
        request.session['first_name'] = customer.first_name
        request.session['last_name'] = customer.last_name
        request.session['phone'] = customer.phone
        request.session['email'] = customer.email

        return redirect('profile')
