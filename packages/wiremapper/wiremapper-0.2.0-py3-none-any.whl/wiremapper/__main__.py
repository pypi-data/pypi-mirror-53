import threading

import gi
import pockethernet
import logging

from pockethernet import WiremapResult, LinkResult, PoEResult

import wiremapper.discover
import wiremapper.wiremap

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Gio, GdkPixbuf

gi.require_version('Handy', '0.0')
from gi.repository import Handy

logging.basicConfig(level=logging.DEBUG)


class DeviceFinder(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
        devices = list(wiremapper.discover.get_paired_devices())
        GLib.idle_add(self.callback, devices)


class Quicktest(threading.Thread):
    def __init__(self, callback, mac):
        threading.Thread.__init__(self)
        self.callback = callback
        self.mac = mac
        self.cancelled = threading.Event()

    def all_none(self, data):
        return all(x is None for x in data)

    def cancel(self):
        self.cancelled.set()
        GLib.idle_add(self.callback, True, "Stopping tests...", [])

    def run(self):
        GLib.idle_add(self.callback, True, "Connecting to the Pockethernet")
        client = pockethernet.Pockethernet()
        client.connect(self.mac)
        GLib.idle_add(self.callback, True, "Running wiremap")

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        wiremap = client.get_wiremap()

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        logging.debug('Wiremap connections: {}'.format(wiremap.connections))
        logging.debug('Wiremap shorts     : {}'.format(wiremap.shorts))

        # Check the situations that guarantee a wiremap adapter is connected first because it's very fast and
        # guarantees the other tests will fail anyway
        if wiremap.connections == [None, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Straight cable, unshielded", [wiremap])
            return

        if wiremap.connections == [0, 1, 2, 3, 4, 5, 6, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Straight cable, shielded", [wiremap])
            return

        if wiremap.connections == [None, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "2-pair cable, unshielded", [wiremap])
            return

        if wiremap.connections == [0, 1, 2, 3, None, None, 6, None, None] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "2-pair cable, shielded", [wiremap])
            return

        if wiremap.connections == [None, 8, 7, 6, 5, 4, 3, 2, 1] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Rollover cable (for serial console)", [wiremap])
            return

        if wiremap.connections == [None, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Crossover cable, unshielded", [wiremap])
            return

        if wiremap.connections == [0, 3, 6, 1, 4, 5, 2, 7, 8] and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Crossover cable, shielded", [wiremap])
            return

        if wiremap.shorts == [None, 3, 6, None, 7, 8, None, None, None] and self.all_none(wiremap.connections):
            GLib.idle_add(self.callback, False, "Found loopback adapter", [wiremap])
            return

        if self.all_none(wiremap.connections) and self.all_none(wiremap.shorts):
            GLib.idle_add(self.callback, False, "Open", [wiremap])
            return

        # Test a link because weird wiremap reading might just be an ethernet port
        GLib.idle_add(self.callback, True, "Running link test")
        link = client.get_link()

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        if link.up:
            GLib.idle_add(self.callback, True, "Running PoE test")
            poe = client.get_poe()

            if self.cancelled.is_set():
                GLib.idle_add(self.callback, False, "Stopped", [])
                return

            poe_status = "no PoE"
            if poe.poe_a_volt + poe.poe_b_volt > 3:
                if poe.poe_a_volt > poe.poe_b_volt:
                    poe_status = "PoE 802.3af mode A ({}V)".format(poe.poe_a_volt)
                else:
                    poe_status = "PoE 802.3af mode B ({}V)".format(poe.poe_b_volt)
            elif sum(poe.pair_volts) > 3:
                poe_status = "passive PoE ({}v)".format(max(poe.pair_volts))

            GLib.idle_add(self.callback, False, "{} link established, {}".format(link.speed, poe_status), [link, poe])
            return

        # Running PoE test after failed link because it might be a PoE injector without upstream
        GLib.idle_add(self.callback, True, "Running PoE test")
        poe = client.get_poe()

        if self.cancelled.is_set():
            GLib.idle_add(self.callback, False, "Stopped", [])
            return

        # Assume the cable is messed up and my software works for now :)
        GLib.idle_add(self.callback, False, "Miswire", [wiremap, link, poe])
        return


class WiremapperApplication(Gtk.Application):
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        AppWindow(self)


class AppWindow:
    def __init__(self, application):
        self.application = application
        builder = Gtk.Builder()
        with pkg_resources.path('wiremapper', 'wiremapper.glade') as ui_file:
            builder.add_from_file(str(ui_file))
        builder.connect_signals(Handler(builder))

        window = builder.get_object("main_window")
        window.set_application(self.application)
        window.show_all()

        Gtk.main()


class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.window = builder.get_object('main_window')
        self.mobile_stackswitcher = builder.get_object('mobile_stackswitcher')
        self.quicktest_spinner = builder.get_object('quicktest_spinner')
        self.quicktest_start = builder.get_object('quicktest_start')
        self.quicktest_status = builder.get_object('quicktest_status')
        self.device_list = builder.get_object('device_list')
        self.quicktest_result = builder.get_object('quicktest_result')

        self.mac = None

        self.quicktest_running = False
        self.quicktest_thread = None

    def on_quit(self, *args):
        Gtk.main_quit()

    def on_headerbar_squeezer_notify(self, squeezer, event):
        """
        This handler gets called when the squeezer in the headerbar changes the visible control.
        If the window is wide enough the visible control is a GtkStackSwitcher. if it is too small
        to show that control it will display an empty GtkBox.

        If the stackswitcher is hidden it shows the mobile stackswitcher at the bottom instead
        """
        child = str(squeezer.get_visible_child())
        self.mobile_stackswitcher.set_reveal(child.startswith('<Gtk.Box'))

    def on_start(self, *args):
        thread = DeviceFinder(self.devicefinder_update)
        thread.start()

    def devicefinder_update(self, devices):
        logging.debug('Got devicefinder callback with {} devices'.format(len(devices)))

        # model.clear()
        amount = len(devices)
        i = 0

        if amount == 1:
            self.mac = devices[0][0]

        for address, label in devices:
            i += 1
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            label_mac = Gtk.Label(label=address, xalign=0)
            label_name = Gtk.Label(label=label, xalign=0)
            label_name.set_markup('<b>{}</b>'.format(label))
            box.pack_start(label_name, False, False, True)
            box.pack_start(label_mac, False, False, True)
            if i != amount:
                box.pack_start(Gtk.Separator(), False, False, True)

            checkmark = Gtk.Image()
            if i == 1:
                checkmark.set_from_icon_name('object-select-symbolic', Gtk.IconSize.BUTTON)

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            hbox.pack_start(box, False, False, True)
            hbox.pack_start(checkmark, False, False, True)

            self.device_list.pack_start(hbox, False, False, True)
        self.device_list.show_all()
        # if len(devices) == 1:
        #    self.device_selector.set_active(0)

    def on_device_change(self, combobox):
        tree_iter = combobox.get_active()
        if tree_iter is not None and tree_iter > -1:
            model = combobox.get_model()
            self.mac = model[tree_iter][1]
            logging.debug('Changing device to {}'.format(self.mac))

    def on_quicktest_start_clicked(self, button):
        if self.quicktest_running:
            self.quicktest_thread.cancel()
            button.set_sensitive(False)
        else:
            self.quicktest_running = True
            self.quicktest_thread = Quicktest(self.quicktest_update, self.mac)
            self.quicktest_thread.daemon = True
            self.quicktest_thread.start()
            button.set_label("Cancel")

            old_results = self.quicktest_result.get_children()
            for w in old_results:
                self.quicktest_result.remove(w)

    def quicktest_update(self, running, status, result=None):
        if running:
            self.quicktest_spinner.start()
        else:
            self.quicktest_running = False
            self.quicktest_spinner.stop()
            self.quicktest_start.set_label("Start")

            if status == "Stopped":
                self.quicktest_start.set_sensitive(True)
        self.quicktest_status.set_label(status)

        if result:
            for block in result:
                if isinstance(block, LinkResult):
                    box = self.make_result_link(block)
                    self.quicktest_result.pack_start(box, False, False, True)
                elif isinstance(block, WiremapResult):
                    box = self.make_result_wiremap(block)
                    self.quicktest_result.pack_start(box, False, False, True)
                elif isinstance(block, PoEResult):
                    box = self.make_result_poe(block)
                    self.quicktest_result.pack_start(box, False, False, True)
            self.quicktest_result.show_all()

    def make_result(self, name):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        label = Gtk.Label(label=name, xalign=0)
        label.set_markup('<b>{}</b>'.format(name))
        box.pack_start(label, False, False, True)
        return box

    def add_class(self, widget, new_class):
        ctx = widget.get_style_context()
        ctx.add_class(new_class)

    def make_result_wiremap(self, result):
        if not isinstance(result, WiremapResult):
            return

        box = self.make_result('Wiremap')

        frame_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        # Get GTK style for the parent so the SVG doesn't look odd
        style = self.window.get_style_context()
        state = Gtk.StateFlags(1)
        font = style.get_font(state)
        font_face = font.get_family()
        font_size = str(int(font.get_size() / 1024)) + 'pt'
        font_color = style.get_color(state)

        font_color = 'rgb({}, {}, {})'.format(int(font_color.red * 255), int(font_color.green * 255),
                                              int(font_color.blue * 255))

        svg = wiremapper.wiremap.draw_wiremap(result.connections, result.shorts, family=font_face, size=font_size,
                                              color=font_color)
        stream = Gio.MemoryInputStream.new_from_bytes(GLib.Bytes.new(svg.encode('UTF-8')))
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(stream, None)
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        frame_vbox.pack_start(image, False, False, True)
        frame = Gtk.Frame()
        self.add_class(frame, 'view')
        aligner = Gtk.Alignment()
        aligner.set_padding(12, 12, 12, 12)
        aligner.add(frame_vbox)
        frame.add(aligner)
        box.pack_start(frame, False, False, 12)
        return box

    def make_result_link(self, result):
        if not isinstance(result, LinkResult):
            return

        box = self.make_result('Link')

        frame_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        if result.up:
            duplexity = 'full duplex' if result.duplex else 'half duplex'
            status = Gtk.Label(label="Connected at {} {}".format(result.speed, duplexity), xalign=0)
            frame_vbox.pack_start(status, False, False, True)

            grid = Gtk.Grid()
            frame_vbox.pack_start(grid, False, False, True)

            grid.set_row_spacing(12)
            grid.set_column_spacing(12)

            grid.attach(Gtk.Label(label="Link partner advertizing", xalign=0), 0, 0, 1, 1)
            grid.attach(Gtk.Label(label="10 Mbps", xalign=1), 0, 1, 1, 1)
            grid.attach(Gtk.Label(label="100 Mbps", xalign=1), 0, 2, 1, 1)
            grid.attach(Gtk.Label(label="1000 Mbps", xalign=1), 0, 3, 1, 1)

            grid.attach(Gtk.Label(label="Half duplex", xalign=0), 1, 0, 1, 1)
            grid.attach(Gtk.Label(label="Full duplex", xalign=0), 2, 0, 1, 1)

            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_10HD), 1, 1, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_10FD), 2, 1, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_100HD), 1, 2, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_100FD), 2, 2, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_1000HD), 1, 3, 1, 1)
            grid.attach(Gtk.CheckButton(sensitive=False, active=result.link_partner_1000FD), 2, 3, 1, 1)
        else:
            status = Gtk.Label(label="Could not establish link", xalign=0)
            frame_vbox.pack_start(status, False, False, True)

        frame = Gtk.Frame()
        self.add_class(frame, 'view')
        aligner = Gtk.Alignment()
        aligner.set_padding(12, 12, 12, 12)
        aligner.add(frame_vbox)
        frame.add(aligner)
        box.pack_start(frame, False, False, 12)
        return box

    def make_result_poe(self, result):
        if not isinstance(result, PoEResult):
            return

        box = self.make_result('PoE')

        frame_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        grid = Gtk.Grid()
        frame_vbox.pack_start(grid, False, False, True)

        grid.set_row_spacing(12)
        grid.set_column_spacing(12)

        grid.attach(Gtk.Label(label="802.3af mode A", xalign=0), 0, 0, 1, 1)
        grid.attach(Gtk.Label(label="802.3af mode B", xalign=0), 0, 1, 1, 1)
        grid.attach(Gtk.Label(label="Passive pair 1", xalign=0), 0, 2, 1, 1)
        grid.attach(Gtk.Label(label="Passive pair 2", xalign=0), 0, 3, 1, 1)
        grid.attach(Gtk.Label(label="Passive pair 3", xalign=0), 0, 4, 1, 1)
        grid.attach(Gtk.Label(label="Passive pair 4", xalign=0), 0, 5, 1, 1)

        mode_a = "{}v".format(result.poe_a_volt) if result.poe_a_volt > 3 else "no power"
        mode_b = "{}v".format(result.poe_b_volt) if result.poe_b_volt > 3 else "no power"
        pair1 = "{}v".format(result.pair_volts[0]) if result.pair_volts[0] > 3 else "no power"
        pair2 = "{}v".format(result.pair_volts[1]) if result.pair_volts[1] > 3 else "no power"
        pair3 = "{}v".format(result.pair_volts[2]) if result.pair_volts[2] > 3 else "no power"
        pair4 = "{}v".format(result.pair_volts[3]) if result.pair_volts[3] > 3 else "no power"
        grid.attach(Gtk.Label(label=mode_a, xalign=0), 1, 0, 1, 1)
        grid.attach(Gtk.Label(label=mode_b, xalign=0), 1, 1, 1, 1)
        grid.attach(Gtk.Label(label=pair1, xalign=0), 1, 2, 1, 1)
        grid.attach(Gtk.Label(label=pair2, xalign=0), 1, 3, 1, 1)
        grid.attach(Gtk.Label(label=pair3, xalign=0), 1, 4, 1, 1)
        grid.attach(Gtk.Label(label=pair4, xalign=0), 1, 5, 1, 1)

        frame = Gtk.Frame()
        self.add_class(frame, 'view')
        aligner = Gtk.Alignment()
        aligner.set_padding(12, 12, 12, 12)
        aligner.add(frame_vbox)
        frame.add(aligner)
        box.pack_start(frame, False, False, 12)
        return box


def main():
    app = WiremapperApplication("nl.brixit.wiremapper", Gio.ApplicationFlags.FLAGS_NONE)
    app.run()


if __name__ == '__main__':
    Handy.Column()
    main()
