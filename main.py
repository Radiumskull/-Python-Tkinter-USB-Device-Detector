import re
import time
import subprocess
import tkinter as tk

            

class DeviceDetector(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Device Detector")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    device_labels = []

    def remove_devices(self):
        for device_label in self.device_labels:
            device_label.destroy()

    def update_devices(self):
        self.update_devices_handler()
        self.after(1000, self.update_devices)

    def update_devices_handler(self):
        devices = []
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i.decode('utf-8'))
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        # Remove Previous Device List
        self.remove_devices()

        # Display the New Device List
        for device in devices:
            new_device_label = tk.Label(self, text=device['tag'])
            self.device_labels.append(new_device_label)
            new_device_label.pack(pady=10, padx=10)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        refresh_button = tk.Button(self, text ="Refresh List", command = self.update_devices_handler)
        refresh_button.pack(pady=20, padx=20)
        label = tk.Label(self, text="Connected USB Devices", font='Helvetica 18 bold')
        label.pack(padx=10, pady=10)
        self.after(1000, self.update_devices)


app = DeviceDetector()
app.mainloop()
