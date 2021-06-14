from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import re


class polygon:

    def __init__(self, shapeAttributes):
        self.vertices = shapeAttributes[0]
        self.color = shapeAttributes[1]
        self.mode = shapeAttributes[2]

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_POLYGON)
        glColor3fv(self.color)
        for coords in self.vertices:
            glVertex2fv(coords)
        glEnd()
        if self.mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_POLYGON)
            glColor3f(0.0, 0.0, 0.0)
            for coords in self.vertices:
                glVertex2fv(coords)
            glEnd()


class shape(polygon):

    def draw(self):
        glColor3fv(self.color)
        for coords in self.vertices:
            glVertex2fv(coords)

    def drawBorder(self):
        glColor3f(0.0, 0.0, 0.0)
        for coords in self.vertices:
            glVertex2fv(coords)


class polyGroup:
    type = 5

    def __init__(self):
        self.shapeList = []

    def draw(self):
        for sh in self.shapeList:
            sh.draw()

    def addShape(self, newShape):
        self.shapeList.append(newShape)


class shapeGroup(polyGroup):
    type = 1

    def __init__(self):
        super().__init__()
        self.shapeBorderList = []

    def draw(self):
        if self.shapeList:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.__typeBegin()
            for sh in self.shapeList:
                sh.draw()
            glEnd()
            if self.shapeBorderList:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.__typeBegin()
                for sh in self.shapeBorderList:
                    sh.drawBorder()
                glEnd()

    def __typeBegin(self):
        if self.type == 1:
            glBegin(GL_POINTS)
        elif self.type == 2:
            glBegin(GL_LINES)
        elif self.type == 3:
            glBegin(GL_TRIANGLES)
        elif self.type == 4:
            glBegin(GL_QUADS)

    def addShape(self, newShape):
        self.shapeList.append(newShape)
        if newShape.mode:
            self.shapeBorderList.append(newShape)

    def setType(self, newType):
        self.type = newType


class window:
    drawList = []
    x = 0
    y = 0

    def __init__(self, width, height, coords, vector, fileName):
        self.width = width
        self.height = height
        self.coords = coords
        self.vector = vector
        self.setData(fileName)

    def __setupView(self):
        glClearColor(100, 0, 0, 1)
        glViewport(0, 0, self.width, self.height)
        glPointSize(10)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.width / 2, self.width / 2, -self.height / 2, self.height / 2, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initWindow(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGB)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.coords[0], self.coords[1])
        glutCreateWindow(b"Lab 1 by Nikitin Bohdan")
        self.__setupView()
        glutDisplayFunc(self.__draw)
        glutMouseFunc(self.__mouseEvent)
        glutKeyboardFunc(self.__keyBoardEvent)
        glutMainLoop()

    def __keyBoardEvent(self, key, x, y):
        if key == b'w' or key == b'W':
            self.y += 25
        elif key == b's' or key == b'S':
            self.y -= 25
        elif key == b'a' or key == b'A':
            self.x -= 25
        elif key == b'd' or key == b'D':
            self.x += 25
        elif key == b'r' or key == b'R':
            self.y = 0
            self.x = 0
        elif key == b'v' or key == b'V':
            self.x += self.vector[0]
            self.y += self.vector[1]

        glutPostRedisplay()
        glLoadIdentity()

    def __mouseEvent(self, button, state, xPos, yPos):
        pass

    def __draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glTranslatef(self.x, self.y, 0)
        for el in self.drawList:
            el.draw()
        glFinish()

    def setData(self, filePath):
        with open(filePath, 'r') as file:
            data = file.read()
            print(data)
            num = lambda n: '[;]'.join(['[-]?\d+(?:[.]\d+)?'] * n)
            shapeAtr = lambda shapeRow: [
                [[float(el) for el in re.findall(f'{num(1)}', x)] for x in re.findall(f'\({num(2)}\)', shapeRow)],
                [float(el) for el in re.findall(f'{num(1)}', re.findall(f'\({num(3)}\)', shapeRow)[0])],
                float(re.findall(f'\({num(1)}\)', shapeRow)[0].rstrip(')').lstrip('('))]
            shapeList = sorted([shapeAtr(row) for row in re.findall(r'\[.+]', data)], key=lambda el: len(el[0]))
            print(shapeList)
            shapeType = len(shapeList[0][0])
            group = shapeGroup()
            group.setType(shapeType)
            for sh in shapeList:
                t = len(sh[0])
                if shapeType < t and shapeType < 5:
                    if group.shapeList:
                        self.drawList.append(group)
                    shapeType = t
                    if shapeType < 5:
                        group = shapeGroup()
                        group.setType(shapeType)
                    else:
                        group = polyGroup()
                if t < 5:
                    s = shape(sh)
                else:
                    s = polygon(sh)
                group.addShape(s)
            if group.shapeList:
                self.drawList.append(group)


if __name__ == '__main__':
    w, h = 500, 500
    filePath = 'vertices.txt'
    vector = [125, 250]
    ww = window(w, h, [100, 100], vector, filePath)
    ww.initWindow()
