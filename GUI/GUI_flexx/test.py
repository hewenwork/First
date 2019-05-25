from flexx import flx


class Example(flx.Widget):

    def init(self):
        with flx.HSplit():
            flx.Button(text='foo')
            with flx.VBox():
                flx.Widget(style='background:red;', flex=1)
                flx.Widget(style='background:blue;', flex=1)


app = flx.App(Example)
app.launch('browser')  # show it now in a browser
flx.run()  # enter the mainloop