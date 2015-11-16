from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import api_requests


# LAYOUT

layout = FloatLayout(size=(300, 300))
url_label = Label(text="Base url:", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.85})
url_text = TextInput(text="https://maja-iot.lodz2.comarch:10443", multiline=False, font_size=12, size_hint=(0.3, 0.05), pos_hint={'x': 0.12, 'y': 0.85}, write_tab=False)

login_label = Label(text="Login:", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.77})
login_text = TextInput(multiline=False, font_size=12, size_hint=(0.2, 0.05), pos_hint={'x': 0.12, 'y': 0.77}, write_tab=False)

pass_label = Label(text="Password:", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.69})
pass_text = TextInput(multiline=False, font_size=12, password=True, size_hint=(0.2, 0.05), pos_hint={'x': 0.12, 'y': 0.69})

button1 = Button(text="Get Types", font_size=15, size_hint=(0.12, 0.06), pos_hint={'x': 0.12, 'y': 0.61})

textbox = TextInput(text="First instructions...", font_size=15, size_hint=(0.45, 0.8), pos_hint={'x': 0.5, 'y': 0.1})

type_label = Label(text="Type Name", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.53})
type_spinner = Spinner(text='Select type', size_hint=(0.35, 0.05), pos_hint={'x': 0.12, 'y': 0.53})

device_label = Label(text="Device Name", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.45})
device_text = TextInput(multiline=False, font_size=12, size_hint=(0.2, 0.05), pos_hint={'x': 0.12, 'y': 0.45}, write_tab=False)

ble_label = Label(text="Device ID:", font_size=15, size_hint=(0.05, 0.05), pos_hint={'x': 0.03, 'y': 0.37})
ble_text = TextInput(multiline=False, font_size=12, size_hint=(0.2, 0.05), pos_hint={'x': 0.12, 'y': 0.37})

button2 = Button(text='Add Sensor', font_size=15, size_hint=(0.12, 0.06), pos_hint={'x': 0.12, 'y': 0.29})

layout.add_widget(url_label)
layout.add_widget(url_text)
layout.add_widget(login_label)
layout.add_widget(login_text)
layout.add_widget(pass_label)
layout.add_widget(pass_text)
layout.add_widget(button1)
layout.add_widget(textbox)

# GLOBAL VARIABLES
types_id_list = []


# FUNCTIONS

def get_types_pressed(instance):
    if login_text.text == "" or pass_text.text == "":
        content_button = Button(text='OK', height=50)
        popup = Popup(title="Enter login and password!", content=content_button, size_hint=(None, None), size=(250, 200))
        content_button.bind(on_press=popup.dismiss)
        popup.open()
    else:
        global types_id_list
        response = api_requests.get_types(url_text.text, login_text.text, pass_text.text)
        if response[1].status_code == 200:

            types_id_list = response[0]
            textbox.text = "Get types response HTTP Code: " + str(response[1].status_code)
            types_names = []

            for entry in types_id_list:
                types_names.append(entry['name'])

            type_spinner.values = types_names
            layout.add_widget(type_label)
            layout.add_widget(type_spinner)
            layout.add_widget(device_label)
            layout.add_widget(device_text)
            layout.add_widget(ble_label)
            layout.add_widget(ble_text)
            layout.add_widget(button2)
            instance.disabled = True
        else:
            textbox.text = "Problem with getting types [HTTP ERROR]: " + str(response[1].status_code)


def add_device_action(instance):
    if device_text.text == "" or ble_text.text == "" or type_spinner.text == "Select type":
        content_button = Button(text='OK', height=50)
        popup = Popup(title="Enter device type, name and id!", content=content_button, size_hint=(None, None), size=(250, 200))
        content_button.bind(on_press=popup.dismiss)
        popup.open()
    else:
        type_name = type_spinner.text
        for entry in types_id_list:
            if entry['name'] == type_name:
                type_id = entry['id']
        device_name = device_text.text
        device_id = ble_text.text

        post_response = api_requests.add_sensor(url_text.text, login_text.text, pass_text.text, type_id, type_name, device_name, device_id)
        textbox.text = "SENT QUERY: \n" + str(post_response[0]) + "\nSERVER REPLY: " + post_response[1] + "\nADD TO PORTAL: " + post_response[2]

# ACTIONS

button1.bind(on_press=get_types_pressed)
button2.bind(on_press=add_device_action)


# MAIN CLASS

class IoTHelperApp(App):
    def build(self):
        return layout

# BASE PROGRAM

if __name__ == "__main__":
    IoTHelperApp().run()
