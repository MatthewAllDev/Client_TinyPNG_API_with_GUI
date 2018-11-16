# GUI for TinyPNG API with keys balanced functions, based on library tkinter
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru> <GitHub @MatthewAllDev>
# version 1.0 beta dated November 16, 2018

import json
import os
import threading
import sys
import webbrowser
from tkinter import (Tk, Toplevel, StringVar, TclError,
                     Frame, Label, Entry, Button, Listbox, Spinbox, Canvas, Scrollbar, ttk,
                     messagebox, filedialog)

import ModuleTinyPNG as tPNG


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.settings = Settings()
        self.init_menu_window()
        self.pack()
        self.parent.iconbitmap(resource_path('app.ico'))
        Window.center_window(self.parent)

    def init_menu_window(self):
        window = self.MainMenuWindow(self)
        Window.destroy_elements(self)
        self.parent.title('Transform Image TinyPNG')
        window.show()
        Window.resize_window(self.parent, 'xy')

    def init_resize_and_compressing_window(self):
        window = self.ResizeAndCompressingWindow(self)
        Window.destroy_elements(self)
        self.parent.title('Resize and compressing (Transform Image TinyPNG)')
        window.show()
        self.pack(fill='x', padx=5)
        Window.resize_window(self.parent, 'y')

    def init_compressing_window(self):
        window = self.CompressingWindow(self)
        Window.destroy_elements(self)
        self.parent.title('Compressing (Transform Image TinyPNG)')
        window.show()
        self.pack(fill='x', padx=5)
        Window.resize_window(self.parent, 'y')

    def init_action_process_window(self):
        window = self.ActionProcessWindow(self)
        Window.destroy_elements(self)
        window.show()
        Window.center_window(self.parent)
        return window

    def init_settings_window(self):
        window = self.SettingsWindow(self)
        Window.destroy_elements(self)
        self.parent.title('Settings (Transform Image TinyPNG)')
        window.show()
        Window.resize_window(self.parent, 'xy')

    class MainMenuWindow:
        def __init__(self, parent):
            self.parent = parent
            self.MainFrame = Frame(self.parent)
            self.ResizeAndCompressingButton = Button(self.MainFrame, text='Resize and compressing', background='#888',
                                                     foreground='#000', padx='20', pady='8', width='20',
                                                     command=self.parent.init_resize_and_compressing_window)
            self.CompressingButton = Button(self.MainFrame, text='Compressing', background='#888', foreground='#000',
                                            padx='20', pady='8', width='20',
                                            command=self.parent.init_compressing_window)
            self.GetCompressionCountButton = Button(self.MainFrame, text='Settings', background='#888',
                                                    foreground='#000', padx='20', pady='8', width='20',
                                                    command=self.parent.init_settings_window)
            self.ExitButton = Button(self.MainFrame, text='Exit', background='#888', foreground='#000', padx='20',
                                     pady='8', width='20', command=self.parent.quit)
            self.FooterFrame = Frame(self.parent)
            self.Developer = Label(self.FooterFrame, text='Developed by')
            self.GitLink = Label(self.FooterFrame, text='@MatthewAllDev', fg="blue", cursor="hand2")
            self.GitLink.bind("<Button-1>", self.go_to_github)

        def show(self):
            self.MainFrame.pack(fill='x')
            self.ResizeAndCompressingButton.grid(row=0, column=0, ipadx=10, ipady=6, padx=10, pady=10)
            self.CompressingButton.grid(row=0, column=1, ipadx=10, ipady=6, padx=10, pady=10)
            self.GetCompressionCountButton.grid(row=1, column=0, ipadx=10, ipady=6, padx=10, pady=10)
            self.ExitButton.grid(row=1, column=1, ipadx=10, ipady=6, padx=10, pady=10)
            self.FooterFrame.pack(fill='x')
            self.GitLink.pack(side='right')
            self.Developer.pack(side='right')

        @staticmethod
        def go_to_github(*args):
            webbrowser.open_new_tab('https://github.com/MatthewAllDev')

    class ResizeAndCompressingWindow:
        def __init__(self, parent):
            self.parent = parent
            self.frame0 = Frame(self.parent)
            self.title = Label(self.frame0, text='Resize and compressing', font='arial 20')
            self.BackButton = Button(self.title, text='<< Back', background='#888', foreground='#000', padx='2',
                                     pady='0', command=self.parent.init_menu_window)
            self.frame1 = Frame(self.parent)
            self.DirectoryLabel = Label(self.frame1, text='Directory', width=6)
            self.directory = StringVar()
            self.directory.set(os.getcwd())
            self.DirectoryEntry = Entry(self.frame1, textvariable=self.directory)
            self.BrowseButton = Button(self.frame1, text='Browse', background='#888', foreground='#000', padx='2',
                                       pady='0', width='10',
                                       command=lambda: self.directory.set(
                                           filedialog.askdirectory(parent=self.parent, initialdir=self.directory.get,
                                                                   title='Please select a folder with images:')))
            self.frame2 = Frame(self.parent)
            self.MethodLabel = Label(self.frame2, text='Resizing method')
            self.method_listbox = Listbox(self.frame2, exportselection=False)
            methods = ['Scale', 'Fit', 'Cover', 'Thumb']
            for method in methods:
                self.method_listbox.insert('end', method)
            self.method_listbox.bind('<<ListboxSelect>>', self.on_select)
            self.frame3 = Frame(self.parent)
            self.SizeLabelText = StringVar()
            self.SizeLabelText.set('Change resize method!')
            self.SizeLabel = Label(self.frame3, textvariable=self.SizeLabelText, justify='left')
            self.HeightFrame = Frame(self.frame3)
            self.HeightLabel = Label(self.HeightFrame, justify='left', text='Height:')
            listvalues = ['']
            listvalues.extend(range(1, 9999 + 1, 1))
            validate_int_val = (
                self.parent.register(Window.validate_int_val), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            self.HeightSpinbox = Spinbox(self.HeightFrame, values=listvalues, state='disabled', validate='all',
                                         validatecommand=validate_int_val)
            self.WidthFrame = Frame(self.frame3)
            self.WidthLabel = Label(self.WidthFrame, justify='left', text='Width:')
            self.WidthSpinbox = Spinbox(self.WidthFrame, values=listvalues, state='disabled', validate='all',
                                        validatecommand=validate_int_val)
            self.StartButton = Button(self.frame3, text='Start', background='#888', foreground='#000', padx='2',
                                      pady='0', width='10', command=self.start_resize_and_compressing, state='disabled')

        def show(self):
            self.frame0.pack(fill='x')
            self.BackButton.pack(side='left')
            self.title.pack(fill='x', pady=5, ipady=4)
            self.frame1.pack(fill='x')
            self.DirectoryLabel.pack(side='left', padx=5, pady=5)
            self.DirectoryEntry.pack(side='left', padx=5, expand=True, fill='x')
            self.BrowseButton.pack(side='left')
            self.frame2.pack(side='left', padx=3, pady=10)
            self.MethodLabel.pack()
            self.method_listbox.pack()
            self.frame3.pack(fill='x', padx=3, pady=10)
            self.SizeLabel.pack(fill='x', ipady=10)
            self.HeightFrame.pack(fill='x')
            self.HeightLabel.pack(side='left', padx=5)
            self.HeightSpinbox.pack(side='left', padx=6)
            self.WidthFrame.pack(fill='x')
            self.WidthLabel.pack(side='left', padx=5)
            self.WidthSpinbox.pack(side='left', padx=10)
            self.StartButton.pack(fill='x', pady=10, ipady=10, side='bottom', expand=True)

        def on_select(self, event):
            widget = event.widget
            selection = widget.curselection()
            try:
                value = widget.get(selection[0])
            except IndexError:
                return
            if value == 'Scale':
                self.SizeLabelText.set('You must provide either a target width or a target height,\nbut not both.')
            else:
                self.SizeLabelText.set('You must provide both a width and a height.')
            self.HeightSpinbox.config(state='normal')
            self.WidthSpinbox.config(state='normal')
            self.StartButton.config(state='normal')

        def start_resize_and_compressing(self):
            try:
                method = self.method_listbox.get(self.method_listbox.curselection())
            except TclError:
                messagebox.showerror('Error!', 'Change resize Method.')
                return
            height = self.HeightSpinbox.get()
            width = self.WidthSpinbox.get()
            processing_thread = threading.Thread(target=tPNG.start_compressing,
                                                 args=(self.parent, self.directory.get(), method, height, width))
            processing_thread.daemon = True
            message = 'Start resize and compressing process?\n\nParameters:\nMethod : ' + method
            if height != '':
                message += '\nHeight: ' + height
            if width != '':
                message += '\nWidth: ' + width
            if height == '' or width == '':
                if method != 'Scale':
                    Window.error_message('need_width_and_height')
                elif height == '' and width == '':
                    Window.error_message('need_width_or_height')
                elif messagebox.askyesno(title='Start?', message=message):
                    processing_thread.start()
            elif method == 'Scale':
                Window.error_message('need_width_or_height')
            elif messagebox.askyesno(title='Start?', message=message):
                processing_thread.start()

    class CompressingWindow:
        def __init__(self, parent):
            self.parent = parent
            self.frame0 = Frame(self.parent)
            self.title = Label(self.frame0, text='Compressing', font='arial 20')
            self.BackButton = Button(self.title, text='<< Back', background='#888', foreground='#000', padx='2',
                                     pady='0', command=self.parent.init_menu_window)
            self.frame1 = Frame(self.parent)
            self.DirectoryLabel = Label(self.frame1, text='Directory', width=6)
            self.directory = StringVar()
            self.directory.set(os.getcwd())
            self.DirectoryEntry = Entry(self.frame1, textvariable=self.directory)
            self.BrowseButton = Button(self.frame1, text='Browse', background='#888', foreground='#000', padx='2',
                                       pady='0', width='10',
                                       command=lambda: self.directory.set(
                                           filedialog.askdirectory(parent=self.parent, initialdir=self.directory.get,
                                                                   title='Please select a folder with images:')))
            self.StartButton = Button(self.parent, text='Start', background='#888', foreground='#000', padx='2',
                                      pady='0', width='10', command=self.start_compressing)

        def show(self):
            self.frame0.pack(fill='x')
            self.BackButton.pack(side='left')
            self.title.pack(fill='x', pady=5, ipady=4)
            self.frame1.pack(fill='x')
            self.DirectoryLabel.pack(side='left', padx=5, pady=5)
            self.DirectoryEntry.pack(side='left', padx=5, expand=True, fill='x')
            self.BrowseButton.pack(side='left')
            self.StartButton.pack(fill='x', pady=10, ipady=10, side='bottom', expand=True)

        def start_compressing(self):
            processing_thread = threading.Thread(target=tPNG.start_compressing,
                                                 args=(self.parent, self.directory.get()))
            processing_thread.daemon = True
            if messagebox.askyesno(title='Start?', message='Start compressing process?'):
                processing_thread.start()

    class ActionProcessWindow:
        def __init__(self, parent):
            self.parent = parent
            self.stop_process_flag = False
            self.titleText = StringVar()
            self.title = Label(self.parent, textvariable=self.titleText, font='arial 20')
            self.ProgressText = StringVar()
            self.ProgressTextLabel = Label(self.parent, textvariable=self.ProgressText)
            self.ProgressBar = ttk.Progressbar(self.parent, mode="determinate", length=500)
            self.button_frame = Frame(self.parent)
            self.OkButton = Button(self.button_frame, text='OK', background='#888', foreground='#000', padx='2',
                                   pady='0', width='10', state='disabled')
            self.StopButton = Button(self.button_frame, text='Stop', background='#888', foreground='#000', padx='2',
                                     pady='0', width='10', command=self.stop)

        def show(self):
            self.title.pack(pady=10)
            self.ProgressTextLabel.pack()
            self.ProgressBar.pack()
            self.button_frame.pack()
            self.OkButton.pack(padx=10, pady=10, ipady=5, ipadx=10, side='left')
            self.StopButton.pack(padx=10, pady=10, ipady=5, ipadx=10, side='left')

        def stop(self):
            if messagebox.askyesno(title='Stop processing?', message='Stop processing images?'):
                self.stop_process_flag = True
                self.titleText.set('Finishing...')

    class SettingsWindow:
        def __init__(self, parent):
            self.parent = parent
            self.settings = Settings(self.parent.settings)
            self.settings.edit_flag = False
            self.frame0 = Frame(self.parent)
            self.title = Label(self.frame0, text='Settings', font='arial 20')
            self.BackButton = Button(self.title, text='<< Back', background='#888', foreground='#000', padx='0',
                                     width='8', pady='0', command=self.back)
            self.frame1 = Frame(self.parent, relief='groove', bd=1, height=150, width=480)
            self.frame1.pack_propagate(0)
            self.canvas = Canvas(self.frame1)
            self.frame_keys = Frame(self.canvas)
            self.scrollbar_keys = Scrollbar(self.frame1, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar_keys.set)
            self.frame_keys.bind("<Configure>", self.scrolling)
            self.frame_keys.bind_all("<MouseWheel>", self._on_mousewheel)
            self.frame_actions = Frame(self.parent)
            self.AddButton = Button(self.frame_actions, text='Add key', background='#888', foreground='#000', padx='2',
                                    pady='0', width='10', command=lambda: self.add_key(self.frame_keys))
            self.ClearButton = Button(self.frame_actions, text='Clear keys', background='#888', foreground='#000',
                                      padx='2',
                                      pady='0', width='10', command=lambda: self.delete_key('all', self.frame_keys))
            self.GetKeyButton = Button(self.frame_actions, text='Get API key', background='#888', foreground='#000',
                                       padx='2', pady='0', width='10',
                                       command=lambda: webbrowser.open_new_tab('https://tinypng.com/developers'))
            self.SaveButton = Button(self.parent, text='Save', background='#888', foreground='#000', padx='2',
                                     pady='0', width='10', font='arial 12',
                                     command=lambda: self.parent.settings.save_settings(self.settings,
                                                                                        self.parent.init_menu_window))

        def show(self):
            self.frame0.pack(fill='x')
            self.title.pack(fill='x', pady=5, side='left', expand=True, ipady=4)
            self.BackButton.pack(side='left')
            self.frame1.pack(fill='x', ipadx=1)
            self.frame_keys.pack(ipadx=3)
            self.scrollbar_keys.pack(side='right', fill='y')
            self.canvas.pack()
            self.canvas.create_window((0, 0), window=self.frame_keys, anchor='nw')
            self.frame_keys.rowconfigure(0, pad=2)
            self.frame_keys.columnconfigure(0, pad=2)
            self.frame_keys.columnconfigure(1, pad=1)
            self.frame_keys.columnconfigure(2, pad=1)
            self.frame_keys.columnconfigure(3, pad=1)
            self.frame_actions.pack(fill='x', pady=10)
            self.AddButton.pack(side='left', padx=4)
            self.ClearButton.pack(side='left', padx=4)
            self.GetKeyButton.pack(side='right', padx=4)
            self.SaveButton.pack(pady=10)
            self.show_keys(self.frame_keys)

        def show_keys(self, target_frame):
            if len(self.settings.keys):
                target_frame.config(background='BLACK')
                Label(target_frame, text='№', width=3).grid(row=0, column=0)
                Label(target_frame, text='API key', width=30).grid(row=0, column=1)
                Label(target_frame, text="Compression count", width=15).grid(row=0, column=2)
                Label(target_frame, text="Action", width=11).grid(row=0, column=3)
                i = 1
                for key in self.settings.keys:
                    target_frame.rowconfigure(i, pad=1)
                    Label(target_frame, text=i, width=3, height=2).grid(row=i, column=0)
                    Label(target_frame, text=key, width=30, height=2).grid(row=i, column=1)
                    Label(target_frame, text=self.settings.keys[key], width=15, height=2).grid(row=i, column=2)
                    button_frame = Frame(target_frame, width=83, height=36)
                    button_frame.pack_propagate(0)
                    button_frame.grid(row=i, column=3)
                    Button(button_frame, text='Edit', background='#888', foreground='#000', width=4, height=1, bd=1,
                           command=lambda arg=key: self.edit_key(arg, target_frame)).pack(pady=5, side='left')
                    Button(button_frame, text='Delete', background='#888', foreground='#000', width=6, height=1, bd=1,
                           command=lambda arg=key: self.delete_key(arg, target_frame)).pack(pady=5, side='left')
                    i += 1
            else:
                target_frame.config(background='')
                Label(target_frame, text='Please add your TinyPNG API key', font='arial 15').pack(fill='x', padx=70,
                                                                                                  pady=4)
                Button(target_frame, text='Get API key', background='#888', foreground='#000',
                       padx='2', pady='0', width='10', font='arial 15',
                       command=lambda: webbrowser.open_new_tab('https://tinypng.com/developers')).pack()

        def scrolling(self, event):
            height = event.height
            if height > 150:
                height = 150
            self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=440, height=height)

        def _on_mousewheel(self, event):
            self.canvas.yview_scroll(int((-1 * (event.delta / 120))), "units")

        def add_key(self, target_frame=None):
            self.AddEditWindow(self.parent, self.settings)
            if target_frame:
                Window.destroy_elements(target_frame)
                self.show_keys(target_frame)

        def edit_key(self, key, target_frame=None):
            self.AddEditWindow(self.parent, self.settings, key)
            if target_frame:
                Window.destroy_elements(target_frame)
                self.show_keys(target_frame)

        def delete_key(self, key, target_frame=None):
            if key == 'all':
                if messagebox.askyesno(title='Delete?', message='Delete all keys?'):
                    self.settings.keys.clear()
            else:
                del self.settings.keys[key]
            self.settings.edit_flag = True
            if target_frame:
                Window.destroy_elements(target_frame)
                self.show_keys(target_frame)

        def back(self):
            if self.settings.edit_flag:
                if messagebox.askyesno(title='Exit?', message='Exit without saving?'):
                    self.parent.init_menu_window()
            else:
                self.parent.init_menu_window()

        class AddEditWindow:
            def __init__(self, root, settings, key=None):
                self.window = Toplevel(root)
                key_val = StringVar()
                self.window.transient(root)
                self.window.grab_set()
                self.window.focus_set()
                if key:
                    button_text = 'Edit'
                    key_val.set(key)
                else:
                    button_text = 'Add'
                self.window.title(button_text + ' key (Transform Image TinyPNG)')
                key_entry = Entry(self.window, textvariable=key_val, width=50)
                key_entry.pack(pady=5)
                key_entry.focus_set()
                frame = Frame(self.window)
                frame.pack()
                Button(frame, text=button_text, width=10, background='#888', foreground='#000',
                       command=lambda: self.add_or_edit_key(settings, key_val, key)).pack(side='left', padx=5)
                Button(frame, text='Cancel', width=10, background='#888', foreground='#000',
                       command=self.window.destroy).pack(side='left', padx=5)
                Window.center_window(self.window)

                self.window.wait_window()

            def add_or_edit_key(self, settings, key_val, key):
                if tPNG.validate_key(key_val.get()):
                    old_keys = settings.keys
                    new_keys = {}
                    if key:
                        for old_key in old_keys:
                            if old_key == key:
                                new_keys.update({key_val.get(): ''})
                            else:
                                new_keys.update({old_key: old_keys[old_key]})
                        old_keys.clear()
                        old_keys.update(new_keys)
                    else:
                        old_keys.update({key_val.get(): ''})
                    settings.edit_flag = True
                    self.window.destroy()
                else:
                    Window.error_message('invalid_key')

    @staticmethod
    def error_message(type_error, e=None):
        if type_error == 'need_width_and_height':
            messagebox.showerror('Error!', 'You must provide both a width and a height.')
        if type_error == 'need_width_or_height':
            messagebox.showerror('Error!', 'You must provide either a target width or a target height, but not both.')
        if type_error == 'need_files_to_processing':
            messagebox.showerror('Error!', 'No images to process.\nPossibly they have already been processed earlier '
                                           'or there are files with such names in the subfolder "Processed".')
        if type_error == 'invalid_key':
            messagebox.showerror('Error!', 'Invalid key.')
        if type_error == 'none_keys':
            messagebox.showerror('Error!', 'No keys for work.\nPlease add your key TinyPNG API in settings.')
        if type_error == 'api_key_constraint_error':
            messagebox.showerror('Error!', 'Your compression limit is reached, you can wait until the next calendar '
                                           'month, or add new api key or upgrade your subscription. After verifying '
                                           'your API key and your account status, you can retry.\n\n'
                                           'Current compression count: ' + e)
        if type_error == 'api_client_error':
            if hasattr(e, 'message'):
                message = e.message
            else:
                message = e
            messagebox.showerror('Error!', 'API client error!\nPlease send your bug report ro luceo2011@yandex.ru.'
                                           '\nDetails: ' + message)
        if type_error == 'api_server_error':
            messagebox.showerror('Error!', 'Temporary issue with the server TinyPNG API.\nPlease try again later.')
        if type_error == 'network_connection_error':
            messagebox.showerror('Error!', 'A network connection error occurred.\nCheck your network connection.')

    @staticmethod
    def center_window(master):
        master.update_idletasks()
        w = master.winfo_reqwidth()
        h = master.winfo_reqheight()
        sw = master.winfo_screenwidth()
        sh = master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    @staticmethod
    def resize_window(master, mode):
        if mode == 'x':
            h = master.winfo_reqheight()
            master.update_idletasks()
            w = master.winfo_reqwidth()
        elif mode == 'y':
            w = master.winfo_reqwidth()
            master.update_idletasks()
            h = master.winfo_reqheight()
        else:
            master.update_idletasks()
            w = master.winfo_reqwidth()
            h = master.winfo_reqheight()
        master.geometry('%dx%d' % (w, h))

    @staticmethod
    def destroy_elements(target):
        lst = target.grid_slaves()
        lst.extend(target.pack_slaves())
        for l in lst:
            l.destroy()

    @staticmethod
    def validate_int_val(*args):
        text = args[4]
        if text in '0123456789':
            return True
        else:
            return False


class Settings:
    def __init__(self, parent=None):
        self.edit_flag = False
        if parent:
            self.keys = parent.keys.copy()
        else:
            self.keys = {}
            if os.name == 'nt':
                self.settings_directory_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local',
                                                            'ClientTinyPNG')
            else:
                self.settings_directory_path = os.path.join(os.path.expanduser('~'), '.config', 'ClientTinyPNG')
            self.settings_file_path = os.path.join(self.settings_directory_path, 'settings.json')
            self.read_settings()

    def read_settings(self):
        try:
            settings_file = open(self.settings_file_path, 'r')
            settings_json = settings_file.read()
            if settings_json != '':
                settings = json.loads(settings_json)
                keys = settings['keys']
                for key in keys:
                    self.keys[key] = keys[key]
            else:
                settings_file.close()
                self.default_settings(self.settings_file_path)
            settings_file.close()
        except FileNotFoundError:
            try:
                os.makedirs(self.settings_directory_path)
            except FileExistsError:
                pass
            self.default_settings(self.settings_file_path)

    def save_settings(self, new_settings=None, callback=None):
        if new_settings:
            self.keys.clear()
            self.keys.update(new_settings.keys)
        settings = {'keys': self.keys}
        settings_file = open(self.settings_file_path, 'w')
        settings_file.write(json.dumps(settings))
        settings_file.close()
        if callback:
            callback()

    def default_settings(self, settings_file_path):
        self.keys = {}
        def_settings = {'keys': self.keys}
        settings_file = open(settings_file_path, 'w')
        settings_file.write(json.dumps(def_settings))
        settings_file.close()


def resource_path(file):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, file)


def main():
    root = Tk()
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
