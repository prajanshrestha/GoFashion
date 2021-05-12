from django.db import models


class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=20, null= True)
    street = models.CharField(max_length=50, null= True)

    def register(self):
        self.save()

    # this is done so that customer with the same email can't be registered
    def is_exists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')
