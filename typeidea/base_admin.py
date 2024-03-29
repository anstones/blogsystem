#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import admin

class BaseOwnerAdmin:
    """
    1. 用来自动补充文章，分类，标签，侧边栏，友链这些model的owner字段
    2. 用来针对queyset 过滤当前用户
    """
    #只显示当前用户自己创建的文章
    exclude = ('owner', )

    def get__list_queryset(self):
        request = self.request
        queryset = super().get__list_queryset()
        return queryset.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()
