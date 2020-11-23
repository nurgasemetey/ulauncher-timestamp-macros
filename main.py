import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import datetime

logger = logging.getLogger(__name__)


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        logger.info('preferences %s' % json.dumps(extension.preferences))

        print('{0:%Y-%m-%d}'.format(datetime.datetime.now()))
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='YYYY-MM-DD',
                                         description='{0:%Y-%m-%d}'.format(datetime.datetime.now()),
                                         on_enter=CopyToClipboardAction('{0:%Y-%m-%d}'.format(datetime.datetime.now()))))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='HH:mm',
                                         description='{0:%H:%M}'.format(datetime.datetime.now()),
                                         on_enter=CopyToClipboardAction(
                                             '{0:%H:%M}'.format(datetime.datetime.now()))))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='YYYY-MM-DD HH:mm',
                                         description='{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()),
                                         on_enter=CopyToClipboardAction(
                                             '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.now()))))

        now = datetime.datetime.now()
        time_intervals = [
            (0, 3), (3, 6), (6, 9), (9, 12), (12, 15), (15, 18), (18, 21), (21,)
        ]
        current_time_interval = ''
        for i in time_intervals:
            if i[0] == 21:
                current_time_interval = '21-24'
                break
            if i[0] <= now.hour and now.hour < i[1]:
                current_time_interval = '{}-{}'.format(i[0], i[1])
                break
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='HH1-HH2',
                                         description=current_time_interval,
                                         on_enter=CopyToClipboardAction(
                                             current_time_interval)))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='HH1-HH2: HH:mm',
                                         description='%s: %s' % (current_time_interval,'{0:%H:%M}'.format(datetime.datetime.now())),
                                         on_enter=CopyToClipboardAction(
                                             '%s: %s' % (current_time_interval,'{0:%H:%M}'.format(datetime.datetime.now())))))
        
        
        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
