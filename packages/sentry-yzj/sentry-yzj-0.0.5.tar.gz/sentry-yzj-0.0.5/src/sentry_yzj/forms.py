# coding: utf-8
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from django import forms


class YZJOptionsForm(forms.Form):

    yzj_url = forms.CharField(
        max_length=255,
        help_text='云之家发送消息请求URL'
    )
    yzj_no = forms.CharField(
        max_length=255,
        help_text='发送方企业的企业注册号(eid)'
    )
    yzj_pub = forms.CharField(
        max_length=255,
        help_text='发送使用的公共号ID'
    )
    yzj_pubsercet= forms.CharField(
        max_length=255,
        help_text='公共号密钥'
    )
    yzj_notify = forms.CharField(
        max_length=255,
        help_text='公共号接受人的OpenId,多个用户以“,”分开'
    )

