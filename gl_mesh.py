#!/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys
import time
import ctypes
import load_mesh

gvbo = None
gibo = None
objs = []
frames = 0
lasttime = time.time()

def InitGL(width,height):
    glClearColor(0.5, 0.5, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    #gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    glEnableClientState(GL_VERTEX_ARRAY)
    global gvbo, gibo, objs

    #test load
    # gvbo = glGenBuffers(1)
    # glBindBuffer(GL_ARRAY_BUFFER, gvbo)
    # vertices = load_mesh.vertices
    # glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), (ctypes.c_float*len(vertices))(*vertices), GL_STATIC_DRAW)

    # gibo = glGenBuffers(1)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gibo)
    # triangles = load_mesh.triangles[678:]
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, 2 * len(triangles), (ctypes.c_short*len(triangles))(*triangles), GL_STATIC_DRAW)

    #load all mesh
    for div in load_mesh.divisions:
        (vexBeg, vexLen, idxBeg, idxLen) = (div[0] * 3, div[1] * 3, div[2], div[3])
        vertices = load_mesh.vertices[vexBeg:vexBeg+vexLen]
        triangles = load_mesh.triangles[idxBeg:idxBeg+idxLen]

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), (ctypes.c_float*len(vertices))(*vertices), GL_STATIC_DRAW)

        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 2 * len(triangles), (ctypes.c_short*len(triangles))(*triangles), GL_STATIC_DRAW)

        print vbo, ibo, len(vertices), len(triangles)

        objs.append((vbo, ibo, idxLen))

def DrawGLSceneWithVertexBuffer():
    for i in objs:
        glBindBuffer(GL_ARRAY_BUFFER, i[0])
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, i[1])
        glVertexPointer(3, GL_FLOAT, 0, None)
        glDrawElements(GL_TRIANGLES, i[2], GL_UNSIGNED_SHORT, None)

    # glBindBuffer(GL_ARRAY_BUFFER, gvbo)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gibo)
    # glVertexPointer(3, GL_FLOAT, 0, None)
    # glDrawElements(GL_TRIANGLES, 678, GL_UNSIGNED_SHORT, None)

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
    #rotate world
    glRotatef(30 * time.time() % 360.0, 0, 1.0, 0.0)


    #glColor(1.0, 1.0, 1.0, 1.0)
    DrawGLSceneWithVertexBuffer() if 1 else DrawGLSceneTraditional()



    glutSwapBuffers()

def MouseButton(button, mode, x, y):
    print 'clicked at', button, mode, time.time()
    if button == 3 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1.1, 1.1, 1.1)
    elif button == 4 and mode == GLUT_DOWN:
        glMatrixMode(GL_PROJECTION)
        glScalef(1/1.1, 1/1.1, 1/1.1)
    pass

def MouseMove(x, y):
    print x, y

def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-2, 2, -2, 2)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    gluLookAt(2, 1, 2, 0, 1, 0, 0, 1, 0)

    print 'resized'

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
