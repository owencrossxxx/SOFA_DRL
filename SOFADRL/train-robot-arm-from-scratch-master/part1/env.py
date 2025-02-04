import pyglet

class ArmEnv(object):

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass

class Viewer(pyglet.window.Window):
    bar_thc = 5     # 手臂的厚度

    def __init__(self):
        # 创建窗口的继承
        # vsync 如果是 True, 按屏幕频率刷新, 反之不按那个频率
        super(Viewer, self).__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)

        # 窗口背景颜色
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # 将手臂的作图信息放入这个 batch
        self.batch = pyglet.graphics.Batch()    # display whole batch at once

        # 添加蓝点
        self.point = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,    # 4 corners
            ('v2f', [50, 50,                # x1, y1
                     50, 100,               # x2, y2
                     100, 100,              # x3, y3
                     100, 50]),             # x4, y4
            ('c3B', (86, 109, 249) * 4))    # color

        # 添加一条手臂
        self.arm1 = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [250, 250,              # 同上, 点信息
                     250, 300,
                     260, 300,
                     260, 250]),
            ('c3B', (249, 86, 86) * 4,))    # color

        # 按理添加第二条手臂...
