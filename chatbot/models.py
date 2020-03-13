# Create your models here.
import i18n
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from chatbot import response as r
# Create your models here.
from chatbot.facebook_settings import APP_URL


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SenderMsg(BaseModel):
    sender_id = models.ForeignKey("FbUserDetails", on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name="sender id")


class Conversation(BaseModel):
    conv_body = models.TextField(null=True, blank=True, verbose_name="grammaire")
    sendingmsg = models.ForeignKey(SenderMsg, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='sendingmsg')

    def __str__(self):
        return u'%s %s' % (self.sendingmsg, self.conv_body)


class FbUserDetails(BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="User first name")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="User last name")
    profile_pic = models.CharField(max_length=255, null=True, blank=True, verbose_name="User url image")
    conv = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True, related_name='coversations')

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_user_details(self, user_dic=None):
        return user_dic


class TypeMessage(BaseModel):  # dict messerie return
    nom = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True, verbose_name="grammaire")

    class Meta:
        verbose_name_plural = "TypeMessage"
        ordering = ["id"]

    def __str__(self):
        return u'%s ' % self.nom


class Field(BaseModel):
    typemessage = models.ForeignKey(TypeMessage, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="TypeMessage")
    title = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    payload = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return u'%s ' % self.typemessage

    class Meta:
        ordering = ('title',)


class Message(BaseModel):
    fields = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="type_message_fields", blank=True,
                               null=True)
    bloc = models.ForeignKey("Bloc", on_delete=models.CASCADE, related_name="bloc", blank=True, null=True)
    typemsg = models.ForeignKey("TypeMessage", on_delete=models.CASCADE, related_name="type_msg", blank=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return u'%s ' % self.fields

    def _process_to_send(self, msgid):
        model_dict_msg = {}

        return dict


class InputMsg(BaseModel):  # ??

    msg = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Message id")
    text = models.TextField(max_length=255, null=True, blank=True, verbose_name="data rdy to send")

    def __str__(self):
        return u'%s ' % self.msg


class IncommingMsg(BaseModel):
    senderid = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sender id")
    text = models.CharField(max_length=255, null=True, blank=True, verbose_name="Action choisie")
    timestamp = models.CharField(max_length=255, null=True, blank=True, verbose_name="TimeStamp")

    def __str__(self):
        return u'%s %s' % (self.senderid, self.timestamp)


class Bloc(MPTTModel, BaseModel):
    ROOTNODE = 1
    BRANCHNODE = 2
    LEAFNODE = 3

    TYPE_CHOICES = (
        (ROOTNODE, 'rootnode'),
        (BRANCHNODE, 'branchnode'),
        (LEAFNODE, 'leafnode'),
    )

    entery_point = models.CharField(max_length=200, null=True, blank=True)
    type_bloc = models.IntegerField(choices=TYPE_CHOICES, default=BRANCHNODE)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='master')
    structure = models.CharField(max_length=200, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return u'%s ' % self.name

    def get_master_name(self):
        if self.parent:
            return self.parent.name
        else:
            return "root bloc"


class Curation:
    def __init__(self, user, webhookEvent):
        self.user = user
        self.webhookEvent = webhookEvent

    @classmethod
    def handle_payload(cls, payload):
        pass

    class Meta:
        abstract = True


class Order:
    @staticmethod
    def handle_payload(payload):
        response = dict()
        if payload == 'TRACK_ORDER':
            response = r.gen_quick_reply(i18n.t("order.prompt"), [
                {
                    "title": i18n.t("order.account"),
                    payload: "LINK_ORDER"
                },
                {
                    "title": i18n.t("order.search"),
                    payload: "SEARCH_ORDER"
                },
                {
                    "title": i18n.t("menu.help"),
                    payload: "CARE_ORDER"
                }
            ])
        elif payload == "SEARCH_ORDER":
            response = r.gen_text(i18n.t("order.number"))
        elif payload == "LINK_ORDER":
            response = [
                r.gen_text(i18n.t("order.dialog")),
                r.gen_text(i18n.t("order.searching")),
                r.gen_image_template(
                    APP_URL + '/order.png',
                    i18n.t("order.status")
                )
            ]
        return response

    class Meta:
        abstract = True


class Survey:
    def handle_payload(self, payload):
        pass

    class Meta:
        abstract = True
