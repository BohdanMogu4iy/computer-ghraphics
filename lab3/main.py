from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import json
import math
import time


class shape:
    def __init__(self, shapeAttributes):
        self.attributes = shapeAttributes

    def draw(self):
        pass


class sphere(shape):

    def __init__(self, shapeAttributes):
        super().__init__(shapeAttributes)
        self.attributes["distance"] = math.sqrt(sum(map(lambda x: x ** 2, self.attributes['center'])))
        self.attributes["angle"] = 0

    def draw(self):
        glPushMatrix()
        c = self.attributes['center']
        if self.attributes["move"]:
            glTranslatef(self.attributes["distance"] * math.sin(self.attributes["angle"]),
                         c[1], self.attributes["distance"] * math.cos(self.attributes["angle"]))
            self.attributes["angle"] += self.attributes["moveSpeed"]

        else:
            glTranslatef(c[0], c[1], c[2])
        if self.attributes["type"] == "planet":
            glMaterialfv(GL_FRONT, GL_EMISSION, [0, 0, 0, 1])
        elif self.attributes["type"] == "star":
            glMaterialfv(GL_FRONT, GL_EMISSION, self.attributes["color"])

        ambient = list(map(lambda x: x / 8, self.attributes["color"]))
        ambient.append(self.attributes["alpha"])

        diffuse = self.attributes["color"]
        diffuse.append(self.attributes["alpha"])

        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

        if self.attributes['fill']:
            glutSolidSphere(self.attributes['radius'], 40, 40)
        else:
            glutWireSphere(self.attributes['radius'], 40, 40)
        glPopMatrix()


class window:
    drawList = []
    cameraPos = [0, 0, 5]
    cameraAngle = [0, 0]
    cameraRadius = 5
    cameraUp = 1
    shine = True
    seconds = 0

    def __init__(self, fileName):
        with open(fileName, "r") as f:
            data = json.load(f)
            self.width = data["windowWidth"]
            self.height = data["windowHeight"]
            self.coords = data["windowCoords"]
            for sh in data['shapes']:
                if sh['type'] == 'sphere':
                    self.drawList.append(sphere(sh['attributes']))
            self.light = data['light']

    def initWindow(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.coords[0], self.coords[1])
        glutCreateWindow(b"Lab 3 by Nikitin Bohdan")
        self.__init()
        glutDisplayFunc(self.__display)
        glutIdleFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyBoardEvent)
        glutMouseFunc(self.__mouseEvent)
        glutMainLoop()

    def __keyBoardEvent(self, key, x, y):
        if key in [b'o', b'O', b'p', b'P', b'w', b'W', b's', b'S', b'a', b'A', b'd', b'D', b'r', b'R', b't', b'T', b'f',
                   b'F', b'g', b'G', b'q', b'Q']:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if key == b'o' or key == b'O':
                glOrtho(-2, 2, -2, 2, -3, 10)
            elif key == b'p' or key == b'P':
                glFrustum(-2, 2, -2, 2, 3, 10)
            elif key == b'w' or key == b'W':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraAngle[1] = 0
                self.cameraAngle[0] += math.pi / 7.5
                self.cameraPos[0] = 0
                self.cameraPos[1] = math.sin(self.cameraAngle[0]) * self.cameraRadius
                self.cameraPos[2] = math.cos(self.cameraAngle[0]) * self.cameraRadius
                if (self.cameraAngle[0] // (math.pi / 2)) % 4 in [1, 2]:
                    self.cameraUp = -1
                else:
                    self.cameraUp = 1
            elif key == b's' or key == b'S':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraAngle[1] = 0
                self.cameraAngle[0] -= math.pi / 7.5
                self.cameraPos[0] = 0
                self.cameraPos[1] = math.sin(self.cameraAngle[0]) * self.cameraRadius
                self.cameraPos[2] = math.cos(self.cameraAngle[0]) * self.cameraRadius
                if (self.cameraAngle[0] // (math.pi / 2)) % 4 in [1, 2]:
                    self.cameraUp = -1
                else:
                    self.cameraUp = 1
            elif key == b'a' or key == b'A':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraAngle[0] = 0
                self.cameraAngle[1] -= math.pi / 7.5
                self.cameraPos[0] = math.sin(self.cameraAngle[1]) * self.cameraRadius
                self.cameraPos[1] = 0
                self.cameraPos[2] = math.cos(self.cameraAngle[1]) * self.cameraRadius
            elif key == b'd' or key == b'D':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraAngle[0] = 0
                self.cameraAngle[1] += math.pi / 7.5
                self.cameraPos[0] = math.sin(self.cameraAngle[1]) * self.cameraRadius
                self.cameraPos[1] = 0
                self.cameraPos[2] = math.cos(self.cameraAngle[1]) * self.cameraRadius
            elif key == b'r' or key == b'R':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraUp = 1
                self.cameraPos[0] += .2
            elif key == b't' or key == b'T':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraUp = 1
                self.cameraPos[0] -= .2
            elif key == b'f' or key == b'F':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraUp = 1
                self.cameraPos[1] += .2
            elif key == b'g' or key == b'G':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraUp = 1
                self.cameraPos[1] -= .2
            elif key == b'q' or key == b'Q':
                glOrtho(-2, 2, -2, 2, -3, 10)
                self.cameraAngle = [0, 0]
                self.cameraPos = [0, 0, 5]
                self.cameraUp = 1

            gluLookAt(self.cameraPos[0],
                      self.cameraPos[1],
                      self.cameraPos[2], 0, 0, 0, 0, self.cameraUp, 0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
        glutPostRedisplay()

    def __init(self):
        glEnable(GL_DEPTH_TEST)
        glDepthRange(-2, 2)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        self.__setLight()
        self.__turnLightOn()

    @staticmethod
    def __reshape(width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2, 2, -2, 2, -3, 10)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def __mouseEvent(self, button, xPos, yPos):
        pass

    def __display(self):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for sh in self.drawList:
            sh.draw()

        if time.time() - self.seconds >= 20:
            self.shine = not self.shine
            if self.shine:
                self.__turnLightOn()
            else:
                self.__turnLightOff()

        glutSwapBuffers()

    def __setLight(self):

        glPushMatrix()

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.light["mainAttributes"]["ambient"])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light["mainAttributes"]["diffuse"])
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.light["mainAttributes"]["specular"])
        glLightfv(GL_LIGHT0, GL_POSITION, self.light["mainAttributes"]["position"])

        if self.light["type"] == "point":
            glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, self.light["specialAttributes"]["constant"])
            glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, self.light["specialAttributes"]["linear"])
            glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, self.light["specialAttributes"]["quadratic"])

        glPopMatrix()

    def __turnLightOn(self):
        glEnable(GL_LIGHT0)
        self.seconds = time.time()

    def __turnLightOff(self):
        glDisable(GL_LIGHT0)
        self.seconds = time.time()


if __name__ == '__main__':
    filePath = 'shapes.json'
    ww = window(filePath)
    ww.initWindow()
