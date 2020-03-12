# vim: set fileencoding=utf-8 :
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


class SenderMsgAdmin(admin.ModelAdmin):

    list_display = ('id', 'created_at', 'updated_at', 'sender_id')
    list_filter = (
        'created_at',
        'updated_at',
        'sender_id',
        'id',
        'created_at',
        'updated_at',
        'sender_id',
    )
    date_hierarchy = 'created_at'


class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'conv_body',
        'sendingmsg',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'sendingmsg',
        'id',
        'created_at',
        'updated_at',
        'conv_body',
        'sendingmsg',
    )
    date_hierarchy = 'created_at'


class FbUserDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'first_name',
        'last_name',
        'profile_pic',
        'conv',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'conv',
        'id',
        'created_at',
        'updated_at',
        'first_name',
        'last_name',
        'profile_pic',
        'conv',
    )
    date_hierarchy = 'created_at'


class TypeMessageAdmin(admin.ModelAdmin):

    list_display = ('id', 'created_at', 'updated_at', 'nom', 'body')
    list_filter = (
        'created_at',
        'updated_at',
        'id',
        'created_at',
        'updated_at',
        'nom',
        'body',
    )
    date_hierarchy = 'created_at'


class FieldAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'typemessage',
        'title',
        'image_url',
        'text',
        'subtitle',
        'url',
        'payload',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'typemessage',
        'id',
        'created_at',
        'updated_at',
        'typemessage',
        'title',
        'image_url',
        'text',
        'subtitle',
        'url',
        'payload',
    )
    date_hierarchy = 'created_at'


class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'fields',
        'bloc',
        'typemsg',
        'description',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'fields',
        'bloc',
        'typemsg',
        'id',
        'created_at',
        'updated_at',
        'fields',
        'bloc',
        'typemsg',
        'description',
    )
    date_hierarchy = 'created_at'


class InputMsgAdmin(admin.ModelAdmin):

    list_display = ('id', 'created_at', 'updated_at', 'msg', 'text')
    list_filter = (
        'created_at',
        'updated_at',
        'msg',
        'id',
        'created_at',
        'updated_at',
        'msg',
        'text',
    )
    date_hierarchy = 'created_at'


class IncommingMsgAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'senderid',
        'text',
        'timestamp',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'id',
        'created_at',
        'updated_at',
        'senderid',
        'text',
        'timestamp',
    )
    date_hierarchy = 'created_at'

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_indent_field = ""


class BlocAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'created_at',
        'updated_at',
        'entery_point',
        'type_bloc',
        'name',
        'parent',
        'structure',
        'lft',
        'rght',
        'tree_id',
        'level',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'parent',
        'id',
        'created_at',
        'updated_at',
        'entery_point',
        'type_bloc',
        'name',
        'parent',
        'structure',
        'lft',
        'rght',
        'tree_id',
        'level',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.SenderMsg, SenderMsgAdmin)
_register(models.Conversation, ConversationAdmin)
_register(models.FbUserDetails, FbUserDetailsAdmin)
_register(models.TypeMessage, TypeMessageAdmin)
_register(models.Field, FieldAdmin)
_register(models.Message, MessageAdmin)
_register(models.InputMsg, InputMsgAdmin)
_register(models.IncommingMsg, IncommingMsgAdmin)
_register(models.Bloc, BlocAdmin)
