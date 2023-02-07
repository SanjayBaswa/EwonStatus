import os
import customtkinter
import pandas
import requests
from threading import *

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("300x100")  # 300x400

app.title("Hakuna Matata!")

switch_var = customtkinter.StringVar(value="on")


def threading():
    t1 = Thread(target=button_function)
    t1.start()


def threading_config():
    t2 = Thread(target=Open_Config)
    t2.start()


def button_function():
    # ----------
    bar.configure(mode="indeterminate")
    bar.start()
    Ewons = {}
    df = pandas.read_csv('EwonConfig.csv')
    for i in range(df.shape[0]):
        ewon_id = df.loc[i, 'EwonName ']
        try:
            if ewon_id.find(":") != -1:
                data = ewon_id.split(":")
                for i in data:
                    Ewons[i] = ''
            else:
                Ewons[ewon_id] = ''

        except:
            print("Ewon name not mentioned")
    #print(Ewons)
    expand = "300x"+str((len(Ewons)*27)+100)

    for i in range(df.shape[0]):
        try:
            url = "https://m2web.talk2m.com/t2mapi/getewons?t2maccount=" + str(
                df.loc[i, 'AccountName']) + "&t2musername=" + str(df.loc[i, ' UserName']) + "&t2mpassword=" + str(
                df.loc[i, 'Pswd']) + "&t2mdeveloperid=22da4459-e592-441c-bb80-285a64d12629"
            x = requests.get(url)
            data = x.json()
            # print(data['ewons']   , len(data['ewons']))

            for j in data['ewons']:
                if j["name"] in Ewons:
                    Ewons[j["name"]] = j["status"]
        except:
            print("Error while compling data", str(df.loc[i, 'AccountName']), "||", str(df.loc[i, ' UserName']),
                  "||",
                  str(df.loc[i, 'Pswd']))
    app.geometry(expand)
    x = 15
    y = 100
    for i in Ewons:
        cc = ("Helvetica", 15, "bold")
        lableN1 = customtkinter.CTkLabel(master=app, text=i)
        lableN1.place(x=x, y=y)
        lableS1 = customtkinter.CTkLabel(master=app,
                                         text=Ewons[i] if Ewons[i] in ('online', 'offline') else "input Error",
                                         text_color='green' if Ewons[i] == 'online' else 'red', font=cc)
        lableS1.place(x=x + 150, y=y)

        y = y + 20
    bar.stop()


def Open_Config():
    os.system("EwonConfig.csv")


button = customtkinter.CTkButton(master=app, text="Check Ewon status", command=threading)
button.place(x=30, y=50)

conf = customtkinter.CTkButton(master=app, text="Config file", command=threading_config, width=10)
conf.place(x=200, y=50)

bar = customtkinter.CTkProgressBar(master=app, width=290)
bar.place(x=5, y=10)

app.mainloop()
