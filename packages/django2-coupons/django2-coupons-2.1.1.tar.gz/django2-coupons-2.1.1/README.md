# django-coupons

![build status](https://travis-ci.org/byteweaver/django-coupons.png)

A reuseable Django application for coupon gereration and handling

The project is inherited from [byteweaver/django-coupons](https://github.com/byteweaver/django-coupons/). But the origin project doesn't support the django 2.0 version. There are many django2.0 PR in origin [project](https://github.com/byteweaver/django-coupons/pulls), but none of them are merged. 

So I create a new repository and upload it to pypi as `django2-coupons`.

## Setup instructions

1. Install `django-coupons` via pip:
   ```
   $ pip install django2-coupons
   ```

2. Add `'coupons'` to `INSTALLED_APPS` in `settings.py`.

3. Migrate database:

   ```
   $ python manage.py migrate
   ```

## How to UpGrade
Since the django require `on_delete` parameter for ForeignKey, The previous migrations
is nolong usable.  If you are upgrading the django-coupons, please fake the first migrations. Then you can migrate the rest migrations. If there is any problem, maybe you will have to manually modify the django migrations table.
```
python3 manage.py migrate --fake coupons 0001
python3 manage.py migrate coupons
```

## Supported use cases of coupons

This application supports different kind of coupons in the way how they can be redeemed.
The difference is defined by the number of possible redeems and if they are bound to a specific user (may even be a list of users) or not.

    1) single time (default), coupon can be used one time without being bound to an user.
    2) user limited, coupon can be used one time but only by a specific user.
    3) limit number, coupon can be used a limited number of times, by any user once.
    4) users list, coupon can be used by a defined list of users, each once.
    5) unlimited, coupon can be used unlimited times, but only once by the same user.

## More example can been seen in the tests
