#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-29 12:36:19


import django_filters

from . import models


class CouponUserFilter(django_filters.rest_framework.FilterSet):
    coupon_compagin_name = django_filters.CharFilter(
        field_name="coupon__campaign__name")
    not_redeemed = django_filters.BooleanFilter(
        field_name="redeemed_at",
        lookup_expr="isnull")

    class Meta:
        model = models.CouponUser
        fields = ["coupon", "coupon_compagin_name", "not_redeemed"]
