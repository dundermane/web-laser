#/usr/bin/env python

import dxfgrabber

def Interpret(dxf):
    drawing = dxfgrabber.readfile(dxf)
    
    for entity in drawing.entities:
        if entity.dxftype == 'LINE':
            start = entity.start
            end = entity.end
            print 'G0X'+str(start[0])+'Y'+str(start[1])
            print 'G0X'+str(end[0])+'Y'+str(end[1])
        elif entity.dxftype == 'CIRCLE':
            print 'CIRCLE'
            print entity.center
            print entity.radius
        elif entity.dxftype == 'ARC':
            print 'ARC'
            print entity.center
            print entity.radius
            print entity.startangle
            print entity.endangle
        elif entity.dxftype == 'LWPOLYLINE':
            print 'LWPOLYLINE'
            
if __name__ == '__main__':
    Interpret('/home/viktor/Desktop/drawing.dxf')
