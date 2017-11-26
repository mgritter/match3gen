"""Random generation of polynominoes"""

import random

# This is an implementation of the algorithm described in
#
# Hugh Redelmeier
# "Counting polyominoes: Yet another attack"
# Discrete Mathematics
# Volume 36, Issue 2, 1981, Pages 191-203
#
# The algorithm returns fixed polyominoes, so rotated/flipped versions
# will be included.
#
# I used Python dictionaries for the linked list and the free points,
# instead of allocating 2-d arrays of the required size.
def allPolyominoesRecursive( targetSize,
                             polyomino,
                             untriedHead,
                             untriedList,
                             freePoints ):
    # print "polyomino", polyomino
    # print "untried", untriedHead, untriedList
    
    while True:
        # 1. Remove an arbitrary element from the untried set
        # For efficiency this is just the first element
        # popped off the list (but don't change the link!)
        # FIXME: since we're just walking this list and it doesn't
        # change we could probably clean up the prevHead business.
        
        cell = untriedHead
        if cell == None:
            # End of list
            return
        untriedHead = untriedList[untriedHead]

        # 2. Place a cell at this point.
        newPoly = polyomino + [ cell ]

        # 3. Count this new polynomial.
        if len( newPoly ) == targetSize:
            yield newPoly
        else:
            # 4. If the size is less than targetDepth,
            # 4(a) add the new neighbors to the untried set
            # New == not in freePoints (border and untried points have
            # already been removed)
            (y,x) = cell
            neighbors = [ ( y+1, x ), ( y-1, x ), ( y, x+1), (y, x-1 ) ]
            new = []
            childHead = untriedHead
            
            for n in neighbors:
                if n in freePoints:
                    freePoints.remove( n )
                    new.append( n )
                    # Push onto front of list
                    untriedList[n] = childHead
                    childHead = n
                    
            # print "New neigbors", new
            
            # 4(b) call this algorithm recursively
            # untriedList is "its own copy" of the set because the
            # order relationship never changes
            for p in allPolyominoesRecursive( targetSize,
                                              newPoly,
                                              childHead,
                                              untriedList,
                                              freePoints ):
                yield p

            for n in new:
                freePoints.add( n )
            
        # 5. Remove newest cell
        # trivial?
        
def allPolyominoes( n ):
    untriedHead = (0,0)
    untriedList = { (0,0) : None }
    freePoints = set( [ (y,x)
                        for y in xrange( 0, n )
                        for x in xrange( -n+1, n )
                        if not ( y == 0 and x <= 0 ) ] )

    for p in allPolyominoesRecursive( n,
                                      [],
                                      untriedHead,
                                      untriedList,
                                      freePoints ):
        yield p

def printPolyominoes( n ):
    count = 0
    for p in allPolyominoes( n ):
        count += 1
        print count
        s = ""
        for y in xrange( n, -1, -1 ):
            for x in xrange( -n+1, n ):
                if (y,x) in p:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        print s
        

import cairocffi as cairo
from show import Show
    
def showPolyominoes( n ):
    pList = list( allPolyominoes( n ) )
    numPoly = len( pList )
    cellPixels = 4
    maxWidth = 1024
    polyPerRow = maxWidth / ( (n+1) * cellPixels )
    width = polyPerRow * (n+1) * cellPixels - cellPixels
    polyRows = ( numPoly + polyPerRow - 1 ) / polyPerRow
    height = polyRows * (n+1) * cellPixels - cellPixels

    currX = 0
    currY = 0
    surface = cairo.ImageSurface( cairo.FORMAT_ARGB32,
                                  width=width,
                                  height=height )
    context = cairo.Context( surface )
    context.set_source_rgba( 1.0, 1.0, 1.0 )
    context.rectangle( 0, 0, width, height )
    context.fill()

    context.set_line_width( 2 )
    for p in pList:
        context.set_source_rgba( 0.1, 0.2, 1.0, 1 ) 
        # Polyominoes are aligned their bottom row at 0
        # but may extend either +X or -X
        minX = min( x for (y,x) in p )

        for (py, px) in p:
            context.rectangle( ( currX * (n+1) + px - minX ) * cellPixels,
                               ( currY * (n+1) + py ) * cellPixels,
                               cellPixels - 1,
                               cellPixels - 1 )
            context.fill()
            
        currX += 1
        if currX == polyPerRow:
            currX = 0
            currY += 1
            
    Show( surface ).run()

    surface.write_to_png( "fixed-polyominoes-" + str( n ) + ".png" )
    
    
