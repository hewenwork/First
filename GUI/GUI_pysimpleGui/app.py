from flexx import flx

class Demo(flx.Widget):

    def init(self):
        flx.ComboBox



app = flx.App(Demo)
app.launch('browser')  # show it now in a browser
flx.run()  # enter the mainloop