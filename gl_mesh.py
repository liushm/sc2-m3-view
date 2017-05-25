#!/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys
import time
import load_mesh

def InitGL(width,height):
    glClearColor(0.5, 0.5, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    #gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #draw world coordinate axis
    #glPushMatrix()
    glRotatef(30 * time.time() % 360.0, 0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)

    #for i in load_mesh.vertexes:
    #    glVertex3f(i[0], i[2], i[1])

    # for i in load_mesh.triangles:
    #     v = load_mesh.vertexes[i]
    #     glVertex3f(v[0], v[2], v[1])

    for d in load_mesh.divisions:
        x = load_mesh.triangles[d[2]:d[2]+d[3]]

        for i in x:
            v = load_mesh.vertexes[d[0]:d[0]+d[1]][i]
            glVertex3f(v[0], v[2], v[1])

    # # mesh gun
    # x = load_mesh.triangles[0:678]
    # for i in x:
    #     v = load_mesh.vertexes[i]
    #     glVertex3f(v[0], v[2], v[1])

    # # mesh nova
    # x = load_mesh.triangles[678:5262]
    # for i in x:
    #     v = load_mesh.vertexes[i+319]
    #     glVertex3f(v[0], v[2], v[1])

    glEnd()
    #glPopMatrix()

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
