#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-29 11:37:10

from rest_framework import routers
from . import views


app_name = "coupons"
router = routers.SimpleRouter()
router.register("couponuser", views.CouponUserViewSet)
urlpatterns = router.urls + [

]
