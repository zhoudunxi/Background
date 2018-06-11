#!/usr/bin/python
#encoding=utf8
__author__ = 'wch96'
from django import template

register = template.Library()



@register.filter(name="splitt")
def splitt(tool_cfgs):
    return tool_cfgs.strip().split(",")
