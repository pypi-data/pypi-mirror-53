# coding: utf-8
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
import json
import time
import requests
import utils
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_yzj
from .forms import YZJOptionsForm


class YZJPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to YunZhiJia.
    """
    author = 'edison'
    author_url = 'https://github.com/slowwalkerlcr/sentry-yzj'
    version = sentry_yzj.VERSION
    description = 'Send error counts to YunZhiJia.'
    resource_links = [
        ('Source', 'https://github.com/slowwalkerlcr/sentry-yzj'),
        ('Bug Tracker', 'https://github.com/slowwalkerlcr/sentry-yzj/issues'),
        ('README', 'https://github.com/slowwalkerlcr/sentry-yzj/blob/master/README.md'),
    ]

    slug = 'YunZhiJia'
    title = 'YunZhiJia'
    conf_key = slug
    conf_title = title
    project_conf_form = YZJOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('yzj_url', project)) and bool(self.get_option('yzj_no', project)) and bool(self.get_option('yzj_pub', project)) and bool(self.get_option('yzj_notify', project)) and bool(self.get_option('yzj_pubsercet', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        yzj_notify = self.get_option('yzj_notify', group.project)
        notifyArray = yzj_notify.split(",")
        send_url = self.get_option('yzj_url', group.project)
        noStr =  self.get_option('yzj_no', group.project)
        pubStr = self.get_option('yzj_pub', group.project)
        t = time.time()
        timeStr = str(int(t))
        pubsercet = self.get_option('yzj_pubsercet', group.project)
        nonceStr = "abcd1234"
        pubtokenBody=[noStr,pubStr,pubsercet,nonceStr,timeStr];
        pubtokenBody.sort();
        pubtokenStr=utils.str_encrypt("".join(pubtokenBody));
        title = u"New alert from {}".format(event.project.slug)

        data = {
            "from": {
                "no": noStr,
                "pub": pubStr,
                "pubtoken": pubtokenStr,
                "nonce": nonceStr,
                "time": timeStr
            },
            "to": [
                {
                    "no": noStr,
                    "user":notifyArray
                }
            ],
            "type": 2,
            "msg": {
                "text": u"#### {title} \n > {message} [href]({url})".format(
                    title=title,
                    message=event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
