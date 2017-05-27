#!/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

import sys
import time
import math
import ctypes
import random
import load_mesh

objs = []
frames = 0
lasttime = time.time()

def InitBuffer():
    global objs

    #load all mesh
    for div in load_mesh.divisions:
        (vexBeg, vexLen, idxBeg, idxLen) = (div[0] * 3, div[1] * 3, div[2], div[3])
        vertices = load_mesh.vertices[vexBeg:vexBeg+vexLen]
        normals = load_mesh.normals[vexBeg:vexBeg+vexLen]
        triangles = load_mesh.triangles[idxBeg:idxBeg+idxLen]

        vbo = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), (ctypes.c_float*len(vertices))(*vertices), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glBufferData(GL_ARRAY_BUFFER, 4 * len(normals), (ctypes.c_float*len(normals))(*normals), GL_STATIC_DRAW)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 2 * len(triangles), (ctypes.c_short*len(triangles))(*triangles), GL_STATIC_DRAW)

        print vao, ibo, len(vertices), len(triangles)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        objs.append((vao, ibo, idxLen))

def InitGL(width,height):
    glClearColor(0.5, 0.5, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)

    InitBuffer()
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    #gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    #glEnableClientState(GL_VERTEX_ARRAY)

def DrawGLSceneWithVertexBuffer():
    for i in objs:
        glBindVertexArray(i[0])
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, i[1])
        glDrawElements(GL_TRIANGLES, i[2], GL_UNSIGNED_SHORT, None)

def DrawGLSceneTraditional():
    glBegin(GL_TRIANGLES)
    for div in load_mesh.divisions:
        (vexBeg, vexLen, idxBeg, idxLen) = div
        triangles = load_mesh.triangles[idxBeg:idxBeg+idxLen]
        for i in triangles:
            v = load_mesh.vertices[vexBeg*3+i*3:vexBeg*3+i*3+3]
            glVertex3f(v[0], v[1], v[2])
    glEnd()

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    global frames, lasttime
    frames += 1
    ctm = time.time()
    if ctm - lasttime >= 1.0:
        lasttime = ctm
        glutSetWindowTitle('opengl fps: %d' % frames)
        frames = 0

    #draw world coordinate axis
    # glBegin(GL_LINES)
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(5.0, 0.0, 0.0)
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, 5.0, 0.0)
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, 0.0, 5.0)
    # glEnd()
    #rotate world
    glRotatef(30 * time.time() % 360.0, 0, 1.0, 0.0)

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    for i in xrange(36):
        glColor(math.sin(i), math.cos(i), math.sin(math.tan(i)), 1.0)

        DrawGLSceneWithVertexBuffer() if 1 else DrawGLSceneTraditional()
        glTranslatef(2.0, 0.0, 0.0)

    # what happens?
    #glutSolidSphere(0.5, 30, 30)



    glutSwapBuffers()

def MouseButton(button, mode, x, y):
    # print 'clicked at', button, mode, time.time()
    if button == 3 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1.1, 1.1, 1.1)
    elif button == 4 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1/1.1, 1/1.1, 1/1.1)
    pass

def MouseMove(x, y):
    # print x, y
    pass

def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-2, 2, -2, 2)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    gluLookAt(2, 1, 2, 0, 1, 0, 0, 1, 0)

def main():
    w, h = 800, 450

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(400, 300)
    glutCreateWindow("opengl")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutMouseFunc(MouseButton)
    glutMotionFunc(MouseMove)
    #glutPassiveMotionFunc(MouseMove)

    InitGL(w, h)

    glutMainLoop()

main()
