from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import json
import math


class shape:
    def __init__(self, shapeAttributes):
        self.attributes = shapeAttributes

    def draw(self):
        pass


class cube(shape):
    def draw(self):
        glColor3fv(self.attributes['color'])
        glPushMatrix()
        c = self.attributes['center']
        glTranslatef(c[0], c[1], c[2])
        if self.attributes['fill']:
            glutSolidCube(self.attributes['size'])
        else:
            glutWireCube(self.attributes['size'])
        glPopMatrix()


class dodecahedron(shape):
    def draw(self):
        glColor3fv(self.attributes['color'])
        glPushMatrix()
        c = self.attributes['center']
        glTranslatef(c[0], c[1], c[2])
        if self.attributes['fill']:
            glutSolidDodecahedron()
        else:
            glutWireDodecahedron()
        glPopMatrix()


class sphere(shape):
    def draw(self):
        glColor3fv(self.attributes['color'])
        glPushMatrix()
        c = self.attributes['center']
        glTranslatef(c[0], c[1], c[2])
        if self.attributes['fill']:
            glutSolidSphere(self.attributes['radius'], 100, 100)
        else:
            glutWireSphere(self.attributes['radius'], 100, 100)
        glPopMatrix()


class plane(shape):
    def __init__(self, shapeAttributes):
        super().__init__(shapeAttributes)
        self.planeVertex = []
        self.func()

    def func(self):
        z = lambda a, b: math.sin(b) * math.sqrt(a)
        for i in range(0, 10):
            x = i * 0.05
            for j in range(-10, 10):
                y = j * 0.05
                self.planeVertex.append([x, y, z(x, y)])
                self.planeVertex.append([x, y + 0.05, z(x, y + 0.05)])
                self.planeVertex.append([x + 0.05, y, z(x + 0.05, y)])

                self.planeVertex.append([x + 0.05, y, z(x + 0.05, y)])
                self.planeVertex.append([x + 0.05, y + 0.05, z(x + 0.05, y + 0.05)])
                self.planeVertex.append([x, y + 0.05, z(x, y + 0.05)])

    def draw(self):
        glColor3fv(self.attributes['color'])
        glPushMatrix()
        c = self.attributes['center']
        glTranslatef(c[0], c[1], c[2])
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.planeVertex)
        glDrawArrays(GL_TRIANGLES, 0, len(self.planeVertex))
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()


class window:
    drawList = []
    cameraPos = [0, 0, 5]
    cameraAngle = [0, 0]
    cameraRadius = 5
    cameraUp = 1

    def __init__(self, fileName):
        self.setData(fileName)

    def initWindow(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.coords[0], self.coords[1])
        glutCreateWindow(b"Lab 2 by Nikitin Bohdan")
        glutDisplayFunc(self.__draw)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyBoardEvent)
        glutMouseFunc(self.__mouseEvent)
        glutMainLoop()

    def __keyBoardEvent(self, key, x, y):
        if key in [b'o', b'O', b'p', b'P', b'w', b'W', b's', b'S', b'a', b'A', b'd', b'D', b'r', b'R', b't', b'T', b'f',
                   b'F', b'g', b'G']:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if key == b'o' or key == b'O':
                glOrtho(-2, 2, -2, 2, -2, 10)
            elif key == b'p' or key == b'P':
                glFrustum(-1, 1, -1, 1, 3, 10)
            elif key == b'w' or key == b'W':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraAngle[0] += math.pi / 7.5
                self.cameraPos[0] = 0
                self.cameraPos[1] = math.sin(self.cameraAngle[0]) * self.cameraRadius
                self.cameraPos[2] = math.cos(self.cameraAngle[0]) * self.cameraRadius
                if (self.cameraAngle[0] // (math.pi / 2)) % 4 in [1, 2]:
                    self.cameraUp = -1
                else:
                    self.cameraUp = 1
            elif key == b's' or key == b'S':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraAngle[0] -= math.pi / 7.5
                self.cameraPos[0] = 0
                self.cameraPos[1] = math.sin(self.cameraAngle[0]) * self.cameraRadius
                self.cameraPos[2] = math.cos(self.cameraAngle[0]) * self.cameraRadius
                if (self.cameraAngle[0] // (math.pi / 2)) % 4 in [1, 2]:
                    self.cameraUp = -1
                else:
                    self.cameraUp = 1
            elif key == b'a' or key == b'A':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraAngle[1] -= math.pi / 7.5
                self.cameraPos[0] = math.sin(self.cameraAngle[1]) * self.cameraRadius
                self.cameraPos[1] = 0
                self.cameraPos[2] = math.cos(self.cameraAngle[1]) * self.cameraRadius
            elif key == b'd' or key == b'D':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraAngle[1] += math.pi / 7.5
                self.cameraPos[0] = math.sin(self.cameraAngle[1]) * self.cameraRadius
                self.cameraPos[1] = 0
                self.cameraPos[2] = math.cos(self.cameraAngle[1]) * self.cameraRadius
            elif key == b'r' or key == b'R':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraUp = 1
                self.cameraPos[0] += .2
            elif key == b't' or key == b'T':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraUp = 1
                self.cameraPos[0] -= .2
            elif key == b'f' or key == b'F':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraUp = 1
                self.cameraPos[1] += .2
            elif key == b'g' or key == b'G':
                glOrtho(-2, 2, -2, 2, -2, 10)
                self.cameraUp = 1
                self.cameraPos[1] -= .2
            gluLookAt(self.cameraPos[0],
                      self.cameraPos[1],
                      self.cameraPos[2], 0, 0, 0, 0, self.cameraUp, 0)
        glutPostRedisplay()

    @staticmethod
    def __reshape(width, height):
        glClearColor(1, 1, 1, 1)
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glDepthRange(-1, 1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2, 2, -2, 2, -2, 10)
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def __mouseEvent(self, button, state, xPos, yPos):
        pass

    def __draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for shape in self.drawList:
            shape.draw()

        glutSwapBuffers()

    def setData(self, filePath):
        with open(filePath, "r") as f:
            data = json.load(f)
            self.width = data["windowWidth"]
            self.height = data["windowHeight"]
            self.coords = data["windowCoords"]
            for shape in data['shapes']:
                if shape['type'] == 'cube':
                    self.drawList.append(cube(shape['attributes']))
                elif shape['type'] == 'plane':
                    self.drawList.append(plane(shape['attributes']))
                elif shape['type'] == 'dodecahedron':
                    self.drawList.append(dodecahedron(shape['attributes']))
                elif shape['type'] == 'sphere':
                    self.drawList.append(sphere(shape['attributes']))


if __name__ == '__main__':
    filePath = 'lab3/shapes.json'
    ww = window(filePath)
    ww.initWindow()
