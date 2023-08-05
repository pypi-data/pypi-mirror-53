# coding: utf-8

from django import forms


class YZJOptionsForm(forms.Form):
    yzj_url = forms.CharField(
        max_length=255,
        help_text='YunZhiJia URL'
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
        help_text='公共号接受人的OpenIds,多个用户以\',\'分开'
    )

