from efl import elementary as elm

from efl.elementary.actionslider import *
from efl.elementary.background import *
from efl.elementary.box import *
from efl.elementary.bubble import *
from efl.elementary.button import *
from efl.elementary.calendar_elm import *
from efl.elementary.check import *
from efl.elementary.clock import *
from efl.elementary.colorselector import *
from efl.elementary.configuration import *
from efl.elementary.conformant import *
from efl.elementary.ctxpopup import *
from efl.elementary.datetime_elm import *
from efl.elementary.dayselector import *
from efl.elementary.diskselector import *
from efl.elementary.entry import *
from efl.elementary.fileselector import *
from efl.elementary.fileselector_button import *
from efl.elementary.fileselector_entry import *
from efl.elementary.flip import *
from efl.elementary.flipselector import *
from efl.elementary.frame import *
from efl.elementary.general import *
from efl.elementary.gengrid import *
from efl.elementary.genlist import *
from efl.elementary.gesture_layer import *
from efl.elementary.grid import *
from efl.elementary.hover import *
from efl.elementary.hoversel import *
from efl.elementary.icon import *
from efl.elementary.image import *
from efl.elementary.index import *
from efl.elementary.innerwindow import *
from efl.elementary.label import *
from efl.elementary.layout import *
from efl.elementary.list import *
from efl.elementary.map import *
from efl.elementary.mapbuf import *
from efl.elementary.menu import *
from efl.elementary.multibuttonentry import *
from efl.elementary.naviframe import *
from efl.elementary.need import *
from efl.elementary.notify import *
from efl.elementary.object import *
from efl.elementary.panel import *
from efl.elementary.panes import *
from efl.elementary.photo import *
from efl.elementary.photocam import *
from efl.elementary.plug import *
from efl.elementary.popup import *
from efl.elementary.progressbar import *
from efl.elementary.radio import *
from efl.elementary.scroller import *
from efl.elementary.segment_control import *
from efl.elementary.separator import *
from efl.elementary.slider import *
from efl.elementary.slideshow import *
from efl.elementary.spinner import *
from efl.elementary.systray import *
from efl.elementary.table import *
from efl.elementary.theme import *
from efl.elementary.thumb import *
from efl.elementary.toolbar import *
from efl.elementary.transit import *
from efl.elementary.video import *
from efl.elementary.web import *
from efl.elementary.window import *


elm.init()
win = StandardWindow("test", "test", size=(320, 320))
win.callback_delete_request_add(lambda x: elm.exit())
win.show()
elm.run()
elm.shutdown()
