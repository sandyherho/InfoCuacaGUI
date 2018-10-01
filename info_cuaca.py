# InfoCuaca

"""
Program diseminasi informasi cuaca ini saya susun berdasarkan sumber - sumber gratis di internet.
Program ini tidak ada kaitannya dengan pekerjaan saya di WCPL ITB. Benarnya program ini menjadi tanggungjawab mereka,
salahnya program ini menjadi tanggungjawab saya secara pribadi.

Silakan kalau mau dimanfaatkan
Salam,
Email: sandyherho@meteo.itb.ac.id
website: sandyherho.github.io
"""

import tkinter as tk
import pyowm
import time
import json
from datetime import datetime
from collections import OrderedDict


class WeatherInfo(tk.Tk):
    templates = OrderedDict([
        ('temp', 'Temperatur: {temp:.1f} C'),
        ('humid', 'Kelembapan: {humid}%'),
        ('status', 'Kondisi: {status}'),
        ('sunrise', 'Waktu Matahari Terbit: {sunrise:%H:%M:%S}'),
        ('sunset', 'Waktu Matahari Terbenam: {sunset:%H:%M:%S}'),
        ('day_length', 'Durasi Siang: {day_length:.1f} jam'),
        ('night_length', 'Durasi Malam: {night_length:.1f} jam')])

    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_title('InfoCuaca')
        self.tk_info = {key: tk.StringVar(
            self, value='') for key in WeatherInfo.templates}

        self.ask = tk.LabelFrame(self, text='Lokasi')
        self.ask.pack(fill='both', expand='yes')
        self.kw_label = tk.Label(self.ask, text='Kota:')
        self.kw_label.pack(side=tk.LEFT)
        self.kw = tk.Entry(self.ask)
        self.kw.pack(side=tk.LEFT)
        self.rb = tk.Button(self.ask, text='Jalankan', command=self.main)
        self.rb.pack(side=tk.RIGHT)
        self.owm = pyowm.OWM('67523ffe1f85355a0f661ea33db1b56e')

        self.output = tk.LabelFrame(self, text='Informasi')
        self.output.pack(fill='both', expand='yes')
        self.labels = []
        for key in WeatherInfo.templates:
            self.labels.append(
                tk.Label(self.output, textvariable=self.tk_info[key]).pack())
        button = tk.Button(master=self, text='Keluar', command=self._quit)
        button.pack(side=tk.BOTTOM)

    def search(self):
        obs = self.owm.weather_at_place(self.kw.get())
        try:
            return json.loads(obs.get_weather().to_JSON())
        except AttributeError:
            self.tk_info['temp'].set('Pilih cuaca kota yang hendak anda ketahui.')

    def parse(self, w):
        parsed_weather = {'temp': w['temperature']['temp'] - 273.15,
                          'humid': w['humidity'],
                          'status': w['status'],
                          'sunrise': datetime.fromtimestamp(w['sunrise_time']),
                          'sunset': datetime.fromtimestamp(w['sunset_time']),
                          'day_length': (w['sunset_time'] - w['sunrise_time']) / 3600,
                          'night_length': 24 - (w['sunset_time'] - w['sunrise_time']) / 3600}
        return parsed_weather

    def update(self, report):
        for key, template in WeatherInfo.templates.items():
            self.tk_info[key].set(template.format(**report))

    def main(self):
        report = self.search()
        if report:
            self.update(self.parse(report))

    def _quit(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = WeatherInfo()
    app.mainloop()