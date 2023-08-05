#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-29 11:38:43


from rest_framework import mixins, viewsets, pagination, permissions
from . import models, filters, serializers


class PaginationClass(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class CouponUserViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = models.CouponUser.objects.all()
    filter_class = filters.CouponUserFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializer_name = "CouponUser{}Serializer".format(
            self.action.capitalize())
        return getattr(serializers, serializer_name)

    def get_queryset(self):
        return models.CouponUser.objects.filter(user=self.request.user)
