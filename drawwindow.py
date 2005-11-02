"the main drawing window"
import gtk, os
import infinitemydrawwidget

class Window(gtk.Window):
    def __init__(self, app):
        gtk.Window.__init__(self)
        self.app = app

        self.set_title('MyPaint')
        def delete_event_cb(window, event, app): app.quit()
        self.connect('delete-event', delete_event_cb, self.app)
        self.set_size_request(600, 400)
        vbox = gtk.VBox()
        self.add(vbox)

        self.create_ui()
        vbox.pack_start(self.ui.get_widget('/Menubar'), expand=False)

        self.mdw = infinitemydrawwidget.InfiniteMyDrawWidget()
        self.mdw.allow_dragging()
        self.mdw.clear()
        self.mdw.set_brush(self.app.brush)
        vbox.pack_start(self.mdw)

        self.statusbar = sb = gtk.Statusbar()
        vbox.pack_end(sb, expand=False)
        sb.push(0, "hello world")

        self.zoomlevel_values = [0.09, 0.12, 0.18, 0.25, 0.33, 0.50, 0.66, 1.0, 1.5, 2.0, 3.0, 4.0, 5.5, 8.0]
        #self.zoomlevel_values = [0.09, 0.12, 0.18, 0.25, 0.33, 0.50, 0.66, 0.9, 1.0, 1.1, 1.5, 2.0, 3.0, 4.0, 5.5, 8.0]
        self.zoomlevel = self.zoomlevel_values.index(1.0)

        self.init_child_dialogs()

        
    def create_ui(self):
        ag = gtk.ActionGroup('WindowActions')
        # FIXME: this xml menu ony creates unneeded information duplication, I think.
        ui_string = """<ui>
          <menubar name='Menubar'>
            <menu action='FileMenu'>
              <menuitem action='Open'/>
              <menuitem action='Save'/>
              <separator/>
              <menuitem action='Zoom1'/>
              <menuitem action='ZoomIn'/>
              <menuitem action='ZoomOut'/>
              <separator/>
              <menuitem action='Clear'/>
              <separator/>
              <menuitem action='Quit'/>
            </menu>
            <menu action='DialogMenu'>
              <menuitem action='BrushSelectionWindow'/>
              <menuitem action='BrushSettingsWindow'/>
              <menuitem action='ColorSelectionWindow'/>
            </menu>
            <menu action='BrushMenu'>
              <menuitem action='InvertColor'/>
              <menuitem action='Bigger'/>
              <menuitem action='Smaller'/>
              <menuitem action='Brighter'/>
              <menuitem action='Darker'/>
              <menuitem action='PickColor'/>
              <menuitem action='ChangeColor'/>
            </menu>
            <menu action='ContextMenu'>
              <menuitem action='ContextStore'/>
              <separator/>
              <menuitem action='Context00'/>
              <menuitem action='Context00s'/>
              <menuitem action='Context01'/>
              <menuitem action='Context01s'/>
              <menuitem action='Context02'/>
              <menuitem action='Context02s'/>
              <menuitem action='Context03'/>
              <menuitem action='Context03s'/>
              <menuitem action='Context04'/>
              <menuitem action='Context04s'/>
              <menuitem action='Context05'/>
              <menuitem action='Context05s'/>
              <menuitem action='Context06'/>
              <menuitem action='Context06s'/>
              <menuitem action='Context07'/>
              <menuitem action='Context07s'/>
              <menuitem action='Context08'/>
              <menuitem action='Context08s'/>
              <menuitem action='Context09'/>
              <menuitem action='Context09s'/>
              <separator/>
              <menuitem action='ContextHelp'/>
            </menu>
            <menu action='DebugMenu'>
              <menuitem action='PrintInputs'/>
              <menuitem action='DontPrintInputs'/>
            </menu>
            <menu action='HelpMenu'>
              <menuitem action='Docu'/>
              <menuitem action='About'/>
            </menu>
          </menubar>
        </ui>"""
        actions = [
            ('FileMenu',     None, 'File'),
            ('Clear',        None, 'Clear', None, 'blank everything', self.clear_cb),
            ('Zoom1',        None, 'Zoom 1:1', None, None, self.zoom_cb),
            ('ZoomIn',       None, 'Zoom in', 'KP_Add', None, self.zoom_cb),
            ('ZoomOut',      None, 'Zoom out', 'KP_Subtract', None, self.zoom_cb),
            #('NewWindow',    None, 'New Window', '<control>N', None, self.new_window_cb),
            ('Open',         None, 'Open', '<control>O', None, self.open_cb),
            ('Save',         None, 'Save', '<control>S', None, self.save_cb),
            ('Quit',         None, 'Quit', None, None, self.quit_cb),
            ('BrushMenu',    None, 'Brush'),
            ('InvertColor',  None, 'Invert Color', 'x', None, self.invert_color_cb),
            ('Brighter',     None, 'Brighter', None, None, self.brighter_cb),
            ('Darker',       None, 'Darker', None, None, self.darker_cb),
            ('Bigger',       None, 'Bigger', 'f', None, self.brush_bigger_cb),
            ('Smaller',      None, 'Smaller', 'd', None, self.brush_smaller_cb),
            ('PickColor',    None, 'Pick Color', 'r', None, self.pick_color_cb),
            ('ChangeColor',  None, 'Change Color', 'v', None, self.change_color_cb),
            ('ContextMenu',  None, 'Brushkeys'),
            ('Context00',    None, 'restore brush 0', '0', None, self.context_cb),
            ('Context00s',   None, 'save to brush 0', '<control>0', None, self.context_cb),
            ('Context01',    None, 'restore 1', '1', None, self.context_cb),
            ('Context01s',   None, 'save 1', '<control>1', None, self.context_cb),
            ('Context02',    None, 'restore 2', '2', None, self.context_cb),
            ('Context02s',   None, 'save 2', '<control>2', None, self.context_cb),
            ('Context03',    None, 'restore 3', '3', None, self.context_cb),
            ('Context03s',   None, 'save 3', '<control>3', None, self.context_cb),
            ('Context04',    None, 'restore 4', '4', None, self.context_cb),
            ('Context04s',   None, 'save 4', '<control>4', None, self.context_cb),
            ('Context05',    None, 'restore 5', '5', None, self.context_cb),
            ('Context05s',   None, 'save 5', '<control>5', None, self.context_cb),
            ('Context06',    None, 'restore 6', '6', None, self.context_cb),
            ('Context06s',   None, 'save 6', '<control>6', None, self.context_cb),
            ('Context07',    None, 'restore 7', '7', None, self.context_cb),
            ('Context07s',   None, 'save 7', '<control>7', None, self.context_cb),
            ('Context08',    None, 'restore 8', '8', None, self.context_cb),
            ('Context08s',   None, 'save 8', '<control>8', None, self.context_cb),
            ('Context09',    None, 'restore 9', '9', None, self.context_cb),
            ('Context09s',   None, 'save 9', '<control>9', None, self.context_cb),
            ('ContextStore', None, 'save to most recently restored', 'q', None, self.context_cb),
            ('ContextHelp',  None, 'Help!', None, None, self.context_help_cb),
            ('DialogMenu',  None, 'Dialogs'),
            ('BrushSelectionWindow',  None, 'brush list', 'b', None, self.toggleBrushSelectionWindow_cb),
            ('BrushSettingsWindow',   None, 'brush settings', '<control>b', None, self.toggleBrushSettingsWindow_cb),
            ('ColorSelectionWindow',  None, 'color', 'c', None, self.toggleColorSelectionWindow_cb),
            ('DebugMenu',  None, 'Debug'),
            ('PrintInputs', None, 'Print brush input values to stdout', None, None, self.print_inputs_cb),
            ('DontPrintInputs', None, 'Stop printing them', None, None, self.dont_print_inputs_cb),
            ('Docu', None, 'Where is the documentation?', None, None, self.show_docu_cb),
            ('HelpMenu',     None, 'Help'),
            ('About', None, 'About MyPaint', None, None, self.show_about_cb),
            ]
        ag.add_actions(actions)
        self.ui = gtk.UIManager()
        self.ui.insert_action_group(ag, 0)
        self.ui.add_ui_from_string(ui_string)
        self.app.accel_group = self.ui.get_accel_group()
        self.add_accel_group(self.app.accel_group)


    def toggleWindow(self, w):
        if w.get_property('visible'):
            w.hide()
        else:
            #w.show()
            w.show_all() # might be for the first time
    def toggleBrushSelectionWindow_cb(self, action):
        self.toggleWindow(self.app.brushSelectionWindow)
    def toggleBrushSettingsWindow_cb(self, action):
        self.toggleWindow(self.app.brushSettingsWindow)
    def toggleColorSelectionWindow_cb(self, action):
        self.toggleWindow(self.app.colorSelectionWindow)

    def print_inputs_cb(self, action):
        self.app.brush.set_print_inputs(1)
    def dont_print_inputs_cb(self, action):
        self.app.brush.set_print_inputs(0)

    def show_about_cb(self, action):
        d = gtk.MessageDialog(self, buttons=gtk.BUTTONS_OK)
        d.set_markup("MyPaint - pressure sensitive painting application\n"
                     "Copyright (C) 2005 Martin Renold &lt;martinxyz@gmx.ch&gt;\n\n"
                     "Contributors:\n"
                     "Artis Rozentals\n"
                     "\n"
                     "This program is free software; you can redistribute it and/or modify"
                     "it under the terms of the GNU General Public License as published by"
                     "the Free Software Foundation; either version 2 of the License, or"
                     "(at your option) any later version."
                     )
        d.run()
        d.destroy()

    def show_docu_cb(self, action):
        d = gtk.MessageDialog(self, buttons=gtk.BUTTONS_OK)
        d.set_markup("There is a tutorial in the html directory, also available "
                     "on the MyPaint homepage. It explains the features which are "
                     "hard to discover yourself.\n\n"
                     "Comments about the brush settings are available as tooltips. "
                     " Just put your mouse over the name of a setting to see it. "
                     "The same thing works for the input names (pressure, speed, etc.)\n"
                     "\n"
                     )
        d.run()
        d.destroy()

    def new_window_cb(self, action):
        # FIXME: is it really done like that?
        #w = Window()
        #w.show_all()
        #gtk.main()
        print "Not really implemented."

    def clear_cb(self, action):
        self.mdw.clear()
        
    def invert_color_cb(self, action):
        self.app.brush.invert_color()
        
    def pick_color_cb(self, action):
        self.app.colorSelectionWindow.pick_color_at_pointer()

    def change_color_cb(self, action):
        self.app.colorSelectionWindow.show_change_color_window()

    def brush_bigger_cb(self, action):
        adj = self.app.brush_adjustment['radius_logarithmic']
        adj.set_value(adj.get_value() + 0.3)
        
    def brush_smaller_cb(self, action):
        adj = self.app.brush_adjustment['radius_logarithmic']
        adj.set_value(adj.get_value() - 0.3)

    def brighter_cb(self, action):
        cs = self.app.colorSelectionWindow 
        cs.update()
        h, s, v = cs.get_color_hsv()
        v += 0.08
        cs.set_color_hsv((h, s, v))
        
    def darker_cb(self, action):
        cs = self.app.colorSelectionWindow 
        cs.update()
        h, s, v = cs.get_color_hsv()
        v -= 0.08
        cs.set_color_hsv((h, s, v))
        
    def open_file(self, filename):
        self.mdw.load(filename)
        self.statusbar.push(1, 'Loaded from ' + filename)

    def save_file(self, filename):
        self.mdw.save(filename)
        self.statusbar.push(1, 'Saved to ' + filename)

    def init_child_dialogs(self):
        dialog = gtk.FileChooserDialog("Open..", self,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("png")
        filter.add_pattern("*.png")
        dialog.add_filter(filter)
        self.opendialog = dialog

        dialog = gtk.FileChooserDialog("Save..", self,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("png")
        filter.add_pattern("*.png")
        dialog.add_filter(filter)
        self.savedialog = dialog

    def open_cb(self, action):
        dialog = self.opendialog
        if dialog.run() == gtk.RESPONSE_OK:
            self.open_file(dialog.get_filename())
        dialog.hide()
        
    def save_cb(self, action):
        dialog = self.savedialog
        if dialog.run() == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            trash, ext = os.path.splitext(filename)
            if not ext:
                filename += '.png'
            if os.path.exists(filename):
                d2 = gtk.Dialog("Overwrite?",
                     self,
                     gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                     (gtk.STOCK_YES, gtk.RESPONSE_ACCEPT,
                      gtk.STOCK_NO, gtk.RESPONSE_REJECT))
                if d2.run() != gtk.RESPONSE_ACCEPT:
                    filename = None
                d2.destroy()
            if filename:
                self.save_file(filename)
        dialog.hide()

    def quit_cb(self, action):
        self.app.quit()

    def move_cb(self, action):
        assert False, "this function is not used any more"
        #step = 20
        step = min(self.mdw.window.get_size()) / 5
        name = action.get_name()
        if name == 'MoveLeft':
            self.mdw.scroll(-step, 0)
        elif name == 'MoveRight':
            self.mdw.scroll(+step, 0)
        elif name == 'MoveUp':
            self.mdw.scroll(0, -step)
        elif name == 'MoveDown':
            self.mdw.scroll(0, +step)
        else:
            assert 0

    def zoom_cb(self, action):
        name = action.get_name()
        if name == 'ZoomIn':
            self.zoomlevel += 1
        elif name == 'ZoomOut':
            self.zoomlevel -= 1
        elif name == 'Zoom1':
            self.zoomlevel = self.zoomlevel_values.index(1.0)
        else:
            assert 0
        if self.zoomlevel < 0: self.zoomlevel = 0
        if self.zoomlevel >= len(self.zoomlevel_values): self.zoomlevel = len(self.zoomlevel_values) - 1
        self.mdw.zoom(self.zoomlevel_values[self.zoomlevel])

    def context_cb(self, action):
        # TODO: this context-thing is not very useful like that, is it?
        #       You overwrite your settings too easy by accident.
        # - seperate set/restore commands?
        # - not storing settings under certain circumstances?
        # - think about other stuff... brush history, only those actually used, etc...
        name = action.get_name()
        store = False
        if name == 'ContextStore':
            context = self.app.selected_context
            if not context:
                print 'No context was selected, ignoring store command.'
                return
            store = True
        else:
            if name.endswith('s'):
                store = True
                name = name[:-1]
            i = int(name[-2:])
            context = self.app.contexts[i]
        self.app.selected_context = context
        if store:
            context.copy_settings_from(self.app.brush)
            preview = self.app.brushSelectionWindow.get_preview_pixbuf()
            context.update_preview(preview)
            context.save()
        else: # restore
            self.app.select_brush(context)
            self.app.brushSelectionWindow.set_preview_pixbuf(context.preview)

    def context_help_cb(self, action):
        d = gtk.MessageDialog(self, buttons=gtk.BUTTONS_OK)
        d.set_markup("This is used to quickly save/restore brush settings "
                     "using keyboard shortcuts. You can paint with one hand and "
                     "change brushes with the other without interrupting."
                     "\n\n"
                     "To assign such a shortcut, move "
                     "your mouse over the menu entry and press the key you want to assign. "
                     "There are 10 memory slots to hold brush settings.\n"
                     "Those are annonymous "
                     "brushes, they are not visible in the brush selector list. "
                     "But they will stay even if you quit. "
                     "They will also remember the selected color. In contrast, selecting a "
                     "normal brush never changes the color. "
                     )
        d.run()
        d.destroy()
