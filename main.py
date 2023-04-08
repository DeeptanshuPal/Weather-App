import configparser
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder


class Weather(Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("560x670+500+70")
        self.config(background="#9fbce9")
        self.iconbitmap(r"Images/weather_icon.ico")
        self.resizable(False, False)
        # self.__gui()
        threading.Thread(target=self.__gui).start()

    def __gui(self):
        # placing the black border for search
        self.img = Image.open(r"Images/black_border.png")
        self.resizeimg = self.img.resize((482, 35))
        self.finalimg = ImageTk.PhotoImage(self.resizeimg)
        Label(image=self.finalimg).place(x=20, y=20)

        # creating the search button
        self.img1 = Image.open(r"Images/search_btn.png")
        self.resizeim1 = self.img1.resize((29, 29))
        self.finalimg1 = ImageTk.PhotoImage(self.resizeim1)
        self.b1 = Button(image=self.finalimg1, bg="black", command=self.threading)
        self.b1.place(x=505, y=22)
        self.bind("<Return>", self.threading)

        # creating the search textbox
        self.search = StringVar()
        self.search_textbox = Entry(textvariable=self.search, font=("Segoe UI", 14, 'bold'), width=43, justify="center",
                                    relief="flat")
        self.search_textbox.place(x=25, y=25)

        # creating the current weather label to display the city name and city time
        Label(text="Current Weather :", font='Arial 14 bold', fg="Dark Blue", bg="#9fbce9").place(x=40, y=347)

        # location image logo
        self.img2 = Image.open(r'Images/location.png')
        self.resizeimg2 = self.img2.resize((20, 20))
        self.finalimg2 = ImageTk.PhotoImage(self.resizeimg2)
        Label(image=self.finalimg2, bg="#9fbce9").place(x=45, y=386)

        # location label
        self.location = Label(text='', font='Calibri 15', bg="#9fbce9")
        self.location.place(x=70, y=384)

        # time label for the searched city
        self.timelbl = Label(text="", font=("Cambria", 16), bg="#9fbce9")
        self.timelbl.place(x=40, y=410)

        # creating the label for the logo according to main
        self.img3 = Image.open(r"Icons/main.png")
        self.resizeimg3 = self.img3.resize((200, 190))
        self.finalimg3 = ImageTk.PhotoImage(self.resizeimg3)
        self.icons = Label(image=self.finalimg3, bg="#9fbce9")
        self.icons.place(x=35, y=110)

        # creating the label to display the temperature
        self.temperature = Label(text="", font=("Cambria", 75, 'bold'), fg="white", bg="#9fbce9")  ##
        self.temperature.place(x=270, y=140)
        self.degree = Label(text="", font="Cambria 40 bold", bg="#9fbce9")
        self.degree.place(x=390, y=135)

        # feels like label and sunny or fog like labels
        self.feel = Label(text="", font=("Nirmala UI", 16, "bold"), bg="#9fbce9")
        self.feel.place(x=280, y=245)

        # sunrise logo
        self.finalimg4 = ImageTk.PhotoImage(image=Image.open(r"Images/sunrise.png").resize((40, 40)))
        Label(image=self.finalimg4,bg="#9fbce9").place(x=310, y=345)
        self.sunrise = Label(text="Sunrise : ", font=("Segoe UI", 14, 'bold'), bg="#9fbce9")
        self.sunrise.place(x=353, y=345)

        # sunset logo
        self.finalimg5 = ImageTk.PhotoImage(image=Image.open(r"Images/sunset.png").resize((40, 30)))
        Label(image=self.finalimg5, bg="#9fbce9").place(x=309, y=400)
        self.sunset = Label(text="Sunset : ", font=("Segoe UI", 14, 'bold'), bg="#9fbce9")
        self.sunset.place(x=353, y=400)

        # bottom bar
        self.finalimg6 = ImageTk.PhotoImage(image=Image.open(r'Images/bottom_bar.png'))
        Label(image=self.finalimg6, bg='#9fbce9').place(x=5, y=475)

        # placing the labels
        Label(text="Humidity", font="Calibri 20 bold", bg='#8aa3bd', fg='white').place(x=75, y=485)
        Label(text="Pressure", font="Calibri 20 bold", bg='#8aa3bd', fg='white').place(x=360, y=485)
        Label(text="Description", font="Calibri 20 bold", bg='#8aa3bd', fg='white').place(x=62, y=565)
        Label(text="Visibility", font="Calibri 20 bold", bg='#8aa3bd', fg='white').place(x=360, y=565)

        # humidity label
        self.humidity = Label(text="", font=("Calibri", 20, 'bold'), bg='#8aa3bd', fg='black')
        self.humidity.place(x=100, y=525)

        # pressure label
        self.pressure = Label(text="", font=("Calibri", 20, 'bold'), bg='#8aa3bd', fg='black')
        self.pressure.place(x=350, y=525)

        # description label
        self.des = Label(text="", font=("Calibri", 20, 'bold'), bg='#8aa3bd', fg='black', width=13, justify="center")
        self.des.place(x=37, y=600)

        # visibility label
        self.vis = Label(text="", font=("Calibri", 20, 'bold'), bg='#8aa3bd', fg='black')
        self.vis.place(x=370, y=600)

    def __get_weather(self):
        try:
            # getting the weather information
            city = self.search.get()
            config_file = configparser.ConfigParser()
            config_file.read("config.ini")
            api = config_file['Openweather']['api']
            data = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
            weather = requests.get(data).json()
            self.__set_information(weather=weather)

        except requests.exceptions.ConnectionError:
            messagebox.showwarning('Connect', "Connect to The internet")
        except:
            messagebox.showerror('Error', "Some Errored Occured\nTry again Later!")

    def __set_information(self, weather):
        # print(weather)
        if weather['cod'] == '404' and weather['message'] == 'city not found':
            messagebox.showerror("Error", "Entered City Not Found")
            self.search.set("")
        elif weather['cod'] == '400' and weather['message'] == 'Nothing to geocode':
            messagebox.showinfo("Warning", 'Enter The city name')
            self.search.set('')
        else:
            # getting time according to timezone
            lon = weather['coord']['lon']  # longitutde
            lat = weather['coord']['lat']  # latitude
            tf = TimezoneFinder()
            result = tf.timezone_at(lng=lon, lat=lat)
            home = pytz.timezone(result)
            local = datetime.datetime.now(home).strftime("%d/%m/%y  %I:%M %p")
            self.timelbl['text'] = local
            self.des['text'] = weather['weather'][0]['description']
            self.feel[
                'text'] = f"Feels Like {int(weather['main']['feels_like'] - 273)}° | {weather['weather'][0]['main']}"
            type = weather['weather'][0]['main']
            self.place_image(type)

            # sets the temperature and degree label
            temp = int(weather['main']['temp'] - 273)
            self.degree['text'] = "°C"
            self.degree.config(fg="white")
            if temp >= 100:
                self.degree.place(x=450, y=135)
            elif temp <= 9 and temp >= 0:
                self.degree.place(x=340, y=135)
            elif temp <= 99 and temp >= 10:
                self.degree.place(x=390, y=135)
            elif temp < 0 and temp >= -9:
                self.degree.place(x=358, y=135)
            elif temp <= -10 and temp >= -99:
                self.degree.place(x=419, y=135)
            self.temperature['text'] = int(weather['main']['temp'] - 273)
            self.humidity['text'] = weather['main']['humidity'], '%'
            self.pressure['text'] = weather['main']['pressure'], 'mBar'
            #self.city['text'] = weather['name']
            #self.country['text'] = weather['sys']['country']
            self.location.config(text=weather['name']+', '+weather['sys']['country'])
            self.vis['text'] = int(weather['visibility'] / 1000), 'km'
            self.sunrise[
                'text'] = f"Sunrise : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunrise'])).strftime('%d/%m/%y  %I:%M %p')}"
            self.sunset[
                'text'] = f"Sunset : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunset'])).strftime('%d/%m/%y   %I:%M %p')}"

    def place_image(self, type):
        if type == "Clear":
            img = "clear.png"
            self.set_image(img)
        elif type == "Clouds":
            img = 'clouds.png'
            self.set_image(img)
        elif type == "Rain":
            img = 'rain.png'
            self.set_image(img)
        elif type == 'Haze':
            img = 'haze.png'
            self.set_image(img)
        elif type == "Snow":
            img = 'snow.png'
            self.set_image(img)
        elif type == "Stormy":
            img = 'stormy.png'
            self.set_image(img)
        elif type == "Windy":
            img = 'Windy.png'
            self.set_image(img)
        elif type == "Smoke":
            img = 'Haze.png'
            self.set_image(img)
        else:
            img = 'general.png'
            self.set_image(img)

    def set_image(self, img):
        self.img3 = Image.open(f"Icons/{img}")
        self.resizeimg3 = self.img3.resize((190, 190))
        self.finalimg3 = ImageTk.PhotoImage(self.resizeimg3)
        self.icons = Label(image=self.finalimg3)
        self.icons.place(x=65, y=110)

    def threading(self, event=0):
        t1 = threading.Thread(target=self.__get_weather)
        t1.start()


if __name__ == "__main__":
    c = Weather()
    c.mainloop()
