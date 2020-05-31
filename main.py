import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import time
from predict import *
from kivy.clock import Clock

class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.padding = 10
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None,
                                  markup=True, font_size = 15)
        self.chat_history.text = f"\n Hello, how can i help you???\n"
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):

        self.chat_history.text += '\n\n' + message

        self.layout.height = self.chat_history.texture_size[1] + 10
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):

        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

class MainApp(App):
    def build(self):

        main_layout = GridLayout(padding = 10, spacing = 10)
        main_layout.cols = 1
        main_layout.rows = 3
        main_layout.bind(size = self.adjust_fields)

        #chatting part
        self.history = ScrollableLabel(height=Window.size[1]*0.8,
                                       size_hint_y=None
                                       )
        main_layout.add_widget(self.history)
        #temp = Label(text = "")
        #main_layout.add_widget(temp)

        #input part
        self.inputpart = GridLayout(spacing = 10, cols = 2)
        self.txt = TextInput(hint_text = "Write here...",
                             width=Window.size[0]*0.8, size_hint_x=1,
                             )
        self.submit = Button(text = "Submit", size_hint=(0.1, 1))
        ########## Weeeeeeeeee------------
        self.model, self.args = prepare()
        ##########------------------------
        self.submit.bind(on_press=self.sendMess)

        self.inputpart.add_widget(self.txt)
        self.inputpart.add_widget(self.submit)
        main_layout.add_widget(self.inputpart)

        #status part
        self.status = Label(text = "No message sent~",
                            valign = 'bottom', halign = 'justify',
                            height = Window.size[1] * 0.7,
                            size_hint_y = 0.4)
        main_layout.add_widget(self.status)

        return main_layout

    def sendMess(self, instance):
        text = self.txt.text
        if text != "":
            self.txt.text = ""
            self.history.update_chat_history(f'[color=20dd20]Human: [/color] > {text}')

            ##################### Weeeeeeeeeeeeeeeee.............. do
            bot_answer = text #### Our Work here!!
            model = self.model
            args = self.args
            bot_answer = model(text, sampling_strategy=args.sampling_strategy, max_seq_len=args.max_seq_len)
            ##############---------------------------------------

            self.history.update_chat_history(f'[color=e07b39]BoBot: [/color] > {bot_answer}')
            #self.history.update_chat_history("\n")

            self.status.text = (str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        else:
            self.status.text = "No message sent~"

     # Updates page layout
    def adjust_fields(self, *_):

        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.85
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.txt.width = new_width

        # Update chat history layout
        #self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

if __name__=="__main__":
    MainApp().run()
