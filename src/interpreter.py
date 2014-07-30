#/usr/bin/env python

import dxfgrabber

def Interpret(dxf):
    drawing = dxfgrabber.readfile(dxf)
    
    colors = {}
    
    for entity in drawing.entities:
        if not colors.get(str(entity.color)):
            colors[str(entity.color)] = []
        colors[str(entity.color)].append(entity)
    
    print 'Here are all the pretty colors:'
    print colors.keys()
    #everything is now sorted by colors
    
    #lets add some start and end points to the shape objects
    for color in colors:
        for entities in color:
            if entity.dxftype == 'Circle':
                entity['start'] = [entity.center[0]-entity.radius, entity.center[1]]
                entity['end'] = [entity.center[0]-entity.radius, entity.center[1]]
            if entity.dxftype == 'ARC':
                entity['start'] = [entity.radius*cos(entity.startangle),entity.radius*sin(entity.startangle)]
                entity['end'] = [entity.radius*cos(entity.endangle),entity.radius*sin(entity.endangle)]
            
            
'''
    for entity in drawing.entities:
        if entity.dxftype == 'LINE':
            print '(LINE)'
            start = entity.start
            end = entity.end
            print 'G0X'+str(start[0])+'Y'+str(start[1])
            print 'G0X'+str(end[0])+'Y'+str(end[1])
        elif entity.dxftype == 'CIRCLE':
            #g2x0y0i0j0
            #i=x(center)
            #j=y(center)
            print '(CIRCLE)'
            print entity.center
            print entity.radius
            start_point=[entity.center[0]-entity.radius, entity.center[1]]
            end_point=start_point
            #lets break this circle up into 90deg arcs
            x = entity.center[0]-entity.radius
            y = entity.center[1]
            i = entity.radius
            j = 0
            print 'G2 X%(x)4.2f Y%(y)4.2f I%(i)4.2f J%(j)4.2f' % locals()
            
        elif entity.dxftype == 'ARC':
            print '(ARC)'
            print entity.center
            print entity.radius
            print entity.startangle
            print entity.endangle
        elif entity.dxftype == 'LWPOLYLINE':
            print 'LWPOLYLINE'
'''            
if __name__ == '__main__':
    Interpret('/home/viktor/Desktop/drawing.dxf')
