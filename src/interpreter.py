#/usr/bin/env python

import dxfgrabber
import math

#How does the dxfreader want to parse a dxf?

#1. Split the drawing up into color groups.
#2. For each color group:
#3.   Read each entity and assign start and end points.
#4.   Assign cut order based on starts and ends.
#5.   for each entity: convert to gcode.

#DXF entities that i care about: Point, Line, LWPolyline, Arc, Circle, Polyline, Ellipse, Spline

class cutGroup(object):   
    def __init__(self):
        self.entities = []
        self.color = '0'
        self.index = -1
        self.start = [0,0]
        self.end = [0,0]

def distance(point1, point2):
    return abs(math.sqrt(math.pow(point1[0] - point2[0],2) + math.pow(point1[1] - point2[1],2)))

def gcode(cg):

    g = []
    current_pos = [0,0]
    for ent in cg.entities:
        #NEED TO SWITCH POINTS
        if distance(current_pos, ent.start) > 0.01:
            g.append("M5")
            g.extend([ "G00X{0[0]:0.6f}Y{0[1]:0.6f}".format(ent.start) ])
        
        g.extend(["M3"])
            
        if ent.dxftype == 'POINT':
            code = "G04P0.5"
            current_pos = ent.start
            g.append(code)
        if ent.dxftype == 'LINE':
            code = []
            code.append( "G01X{0[0]:0.6f}Y{0[1]:0.6f}".format(ent.end) )
            current_pos = ent.end
            g.extend(code)
        if ent.dxftype == 'LWPOLYLINE':
            code = []
            for point in ent.points[1:]:
                #if bulge
                #bulge....
                #else
                code.append("G01X{0[0]:0.6f}Y{0[1]:0.6f}".format(point))
            current_pos = ent.end
            g.extend(code)
        if ent.dxftype == 'ARC':

            if ent.start[0] > ent.center[0]:
                DIR = "G03" if math.sin(ent.startangle) > 0 else "G02"
                    
            if ent.start[0] < ent.center[0]:
                DIR = "G03" if math.sin(ent.startangle) < 0 else "G02"
            
            if ent.start[0] == ent.center[0] and ent.start[1] > ent.center[1]:
                DIR = "G03" if math.cos(ent.startangle) < 0 else "G02"
            
            if ent.start[0] == ent.center[0] and ent.start[1] > ent.center[1]:
                DIR = "G03" if math.cos(ent.startangle) > 0 else "G02"
            
            Ioffset = ent.center[0] - ent.start[0]
            Joffset = ent.center[1] - ent.start[1]

            code = []
            code.extend([ "{0:s}X{1[0]:0.6f}Y{1[1]:0.6f}I{2:0.6f}J{3:0.6f}".format(DIR, ent.end, Ioffset, Joffset) ])
            
            current_pos = ent.end
            g.extend(code)
        if ent.dxftype == 'CIRCLE':
            code = []
            ent.middle = [ent.center[0] + ent.radius , ent.center[1] + ent.radius]
            
            Ioffset = ent.center[0] - ent.start[0]
            Joffset = ent.center[1] - ent.start[1]
            code.extend([ "G02X{0[0]:0.6f}Y{0[1]:0.6f}I{1:0.6f}J{2:0.6f}".format(ent.end, Ioffset, Joffset) ])
            Ioffset = -Ioffset
            Joffset = -Joffset
            code.extend([ "G02X{0[0]:0.6f}Y{0[1]:0.6f}I{1:0.6f}J{2:0.6f}".format(ent.end, Ioffset, Joffset) ])
            current_pos = ent.end
            g.extend(code)
            
        if ent.dxftype == 'ELLIPSE':
            el_points = []
            code = []
            
            #ent.center
            #ent.majoraxis  (end point)
            #ent.ratio
            #ent.startparam (theta)
            #ent.endparam (theta)
            a = distance(ent.center,ent.majoraxis)
            b = ent.ratio *a
            theta = math.asin(( ent.majoraxis[1] - ent.center[1]) / a)
            
            #Approximate arc
            arc_res = .01
            tht = ent.startparam
            if ent.startparam < ent.endparam:
                while tht < ent.endparam:
                    x = a * math.cos(tht)
                    y = b * math.sin(tht)
                    
                    #transform and rotate point
                    x = ent.center[0] + x*math.cos(theta)
                    y = ent.center[1] + y*math.sin(theta)
                    
                    el_points.append([x,y])
                    
                    tht += arc_res
            if ent.startparam > ent.endparam:
                while tht > ent.endparam:
                    x = a * math.cos(tht)
                    y = b * math.sin(tht)
                    
                    #transform and rotate point
                    x = ent.center[0] + x*math.cos(theta)
                    y = ent.center[1] + y*math.sin(theta)
                    
                    el_points.append([x,y])
                    
                    tht -= arc_res
            for point in el_points:
                code.append( "G01X{0[0]:0.6f}Y{0[1]:0.6f}".format(point) )
            current_pos = el_points[-1]
            g.extend(code)
        if ent.dxftype == 'SPLINE':
            print 'WARNING: THERE IS CURRENTLY NO SPLINE SUPPORT'

    return g

def optimize(startPoint, cg):
    #takes an array of elements, each with a start and end point.
    print 'optimize color ' + str(cg.color) + '!!!' 
    
    ent2 = []
    
    closest = distance(cg.entities[0].start, startPoint)
    winner = None
    winnerRev = False
    
    while len(cg.entities) > 0:
        closest = distance(cg.entities[0].start, startPoint)
        for entity in cg.entities:
            #for both start and end:
            #find distance between point and startPoint
            #print entity.dxftype + ' from Start: ' + str(distance(startPoint,entity.start)) + \
            #                       ' from End: ' + str(distance(startPoint,entity.end))
            
            if closest >= distance(startPoint, entity.end):
                closest = min(closest, distance(startPoint, entity.end))
                winner = entity
                winnerRev = True
            if closest >= distance(startPoint, entity.start):
                closest = min(closest, distance(startPoint, entity.start))
                winner = entity
                winnerRev = False
            if winnerRev:
                #reverse all points
                winner.start, winner.end = winner.end, winner.start
                try:
                    winner.startangle, winner.endangle = winner.endangle, winner.startangle
                except:
                    pass
                try:
                    winner.points.reverse()
                    winner.bulge.reverse()
                except:
                    pass
                try:
                    winner.starttangent, winner.endtangent = winner.endtangent, winner.starttangent
                    winner.controlpoints.reverse()
                    winner.fitpoints.reverse()
                    winner.knots.reverse()
                    winner.weights.reverse()
                except:
                    pass

                winner.revCut = True
        startPoint = winner.start
        ent2.append(winner)
        cg.entities.remove(winner)
    print 'reshuffled ' + str(len(ent2)) + ' shapes'
    
    cg.entities = ent2
    return ent2[-1].end, cg


def startEnd(Container, VERBOSE=False, verbose=False):
    #
    #LETS FIND ALL THE START POINTS
    #
    for cg in Container:
        if verbose:
            print 'Finding color ' + str(cg.color) + ' start and end points.'
        for entity in cg.entities:
            entity.revCut = False
            if VERBOSE:
                print 'entity: ' + str(entity)
            if entity.dxftype == 'POINT':
                    print 'start/end: ' + str(entity.point[:2])
                    entity.start = [ entity.point[0], entity.point[1] ]
                    entity.end = [ entity.point[0], entity.point[1] ]
            if entity.dxftype == 'LINE':
                if VERBOSE:
                    print 'start: ' + str(entity.start[:2])
                    print 'end: ' + str(entity.end[:2])
            if entity.dxftype == 'LWPOLYLINE':
                entity.start = entity.points[0]
                entity.end = entity.points[-1]
                if VERBOSE:
                    print 'Is Closed: ' + str(entity.is_closed)
                    print 'Points:'
                    for point in entity.points:
                        print '\t' + str(point)
                    print 'Bulge: ' + str(entity.bulge)
            if entity.dxftype == 'ARC':
                entity.start = [0,0]
                entity.start[0] = math.cos( math.radians( entity.startangle )) * entity.radius + entity.center[0]
                entity.start[1] = math.sin( math.radians( entity.startangle )) * entity.radius + entity.center[1]
                entity.end = [0,0]
                entity.end[0] = math.cos( math.radians( entity.endangle )) * entity.radius + entity.center[0]
                entity.end[1] = math.sin( math.radians( entity.endangle )) * entity.radius + entity.center[1]
                if VERBOSE: 
                    print entity.dxftype
                    print 'start: ' + str(entity.start[:2])
                    print 'end: ' + str(entity.end[:2])
            if entity.dxftype == 'CIRCLE':
                entity.start = [entity.center[0]-entity.radius, entity.center[1]]
                entity.end = [entity.center[0]-entity.radius, entity.center[1]]
                if VERBOSE:
                    print entity.dxftype
                    print 'start/end: '+ str(entity.start[:2])
            if entity.dxftype == 'POLYLINE':
                entity.start = entity.points[0][:2]
                entity.end = entity.points[-1][:2]
                if VERBOSE:
                    print entity.dxftype
                    print 'start: ' + str(entity.points[0][:2])
                    print 'end: ' + str(entity.points[-1][:2])
            if entity.dxftype == 'ELLIPSE':
                entity.start = entity.majoraxis[:2]
                entity.end = entity.majoraxis[:2]
                if VERBOSE:
                    print entity.dxftype
                    print 'start/end: ' + str(entity.majoraxis[:2])
            if entity.dxftype == 'SPLINE':
                entity.start = entity.controlpoints[0][:2]
                entity.end = entity.controlpoints[-1][:2]
                if VERBOSE:
                    print entity.dxftype
                    print 'start: ' + str(entity.controlpoints[0][:2])
                    print 'end: ' + str(entity.controlpoints[-1][:2])



def Interpret(dxf, VERBOSE=False, origin=[0,0], colorOrder=None):
    drawing = dxfgrabber.read(dxf)
    
    Container = []
    
    validEnts = ['POINT','LINE', 'LWPOLYLINE','ARC','CIRCLE','ELLIPSE','SPLINE']
    
    #
    #LETS SORT BY ALL OF THE COLORS
    #  
    for entity in drawing.entities:
        if entity.dxftype in validEnts:
            newColor = True
            for cg in Container:
                if entity.color == cg.color:
                    if VERBOSE:
                        print str(entity.color) + ' paths belong in ' + str(cg.color) + ' cutgroups.'
                    cg.entities.append(entity) 
                    newColor = False       
            if newColor:
                cg = cutGroup()
                cg.color = entity.color
                Container.append(cg)
                if VERBOSE:
                    print str(entity.color) + ' paths belong in ' + str(cg.color) + ' cutgroups.'
                cg.entities.append(entity)

    #Finding all the start and end points
    startEnd(Container)
    
    
    #Reordering the container by color
    
    #TEST# colorOrder = [256,6,1,6]
    if colorOrder:
        colorOrder.reverse()
        for color in colorOrder:
            for cg in Container:
                if cg.color == color:
                    Container.insert(0,Container.pop(Container.index(cg)))
    
    #
    #LETS OPTIMIZE THE TOOL PATH
    #Start at start point.
    #On each color, find path of least jogging.
    #        
    print 'origin: ' + str(origin)
    startPoint = origin
    
    output = {}
    output['groups'] = []
    
    for cg in Container:
        startPoint, cg = optimize(startPoint, cg)
        
        cg_out = {}
        cg_out['gcode'] = gcode(cg)
        cg_out['color'] = cg.color
        output['groups'].append(cg_out)
        
    print 'endpoint: ' + str(startPoint)
        
    #LETS ACTUALLY WRITE OUT A PROGRAM
    return output

    
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
    Interpret('/home/viktor/Desktop/drawing2.dxf', VERBOSE=False, origin=[10,19])
