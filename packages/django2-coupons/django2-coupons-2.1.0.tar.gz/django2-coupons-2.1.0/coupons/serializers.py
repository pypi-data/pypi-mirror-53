#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-29 12:48:05


from . import models
from rest_framework import serializers


class CouponUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CouponUser
        fields = ["id", "redeemed_at", ]
