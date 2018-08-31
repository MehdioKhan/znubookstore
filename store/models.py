from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    translator = models.CharField(max_length=100, blank=True, null=True)
    publish_year = models.DateField()
    publish_date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField('Category')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='pics/')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(max_length=60, blank=True, null=True)
    telegram_id = models.CharField(max_length=30, blank=True, null=True)
    tel_no = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
