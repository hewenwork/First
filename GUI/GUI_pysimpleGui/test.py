from flexx import app, ui, event


class Drawing(ui.CanvasWidget):
    CSS = """
    .flx-Drawing {background: #fff; border: 5px solid #000;}
    """

    class JS:

        def init(self):
            super().init()
            self.ctx = self.node.getContext('2d')
            self._last_ev = None

        @event.connect('mouse_move')
        def on_move(self, *events):
            for ev in events:
                last_ev = self._last_ev
                if 1 in ev.buttons and last_ev is not None:
                    self.ctx.beginPath()
                    self.ctx.strokeStyle = '#080'
                    self.ctx.lineWidth = 3
                    self.ctx.lineCap = 'round'
                    self.ctx.moveTo(*last_ev.pos)
                    self.ctx.lineTo(*ev.pos)
                    self.ctx.stroke()
                    self._last_ev = ev

        @event.connect('mouse_down')
        def on_down(self, *events):
            for ev in events:
                self.ctx.beginPath()
                self.ctx.fillStyle = '#f00'
                self.ctx.arc(ev.pos[0], ev.pos[1], 3, 0, 6.2831)
                self.ctx.fill()
                self._last_ev = ev

        @event.connect('mouse_up')
        def on_up(self, *events):
            for ev in events:
                self.ctx.beginPath()
                self.ctx.fillStyle = '#00f'
                self.ctx.arc(ev.pos[0], ev.pos[1], 3, 0, 6.2831)
                self.ctx.fill()
            self._last_ev = None


class Main(ui.Widget):
    """ Embed in larger widget to test offset.
    """

    CSS = """
    .flx-Drawing {background: #fff; border: 5px solid #000;}
    """

    def init(self):
        with ui.VBox():
            ui.Widget(flex=1)
            with ui.HBox(flex=2):
                ui.Widget(flex=1)
                Drawing(flex=2)
                ui.Widget(flex=1)
            ui.Widget(flex=1)


if __name__ == '__main__':
    m = app.serve(Main)  # 注册我们构建的应用
    app_name = m.__name__  # 获取应用的名称, 因为我们需要在elctron中调用
    port = '8899'  # 设置tornado server的端口
    app.create_server(port=port)  # 创建一个server
    import subprocess  # 用子进程启动electron

    url = 'http://localhost:{port}/{app_name}'.format(port=port, app_name=app_name)
    cmd = r'D:\programs\node-v8.10.0-win-x64\electron.cmd {}'.format(url)  # 这是启动electron的命令, 注意你需要找到electron的脚本路径
    subprocess.Popen(cmd)  # 启动进程
    app.run()  # 启动server