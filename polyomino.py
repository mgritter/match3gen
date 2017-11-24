"""Random generation of polynominoes"""

import random

# This is an implementation of the algorithm described in
#
# Hugh Redelmeier
# "Counting polyominoes: Yet another attack"
# Discrete Mathematics
# Volume 36, Issue 2, 1981, Pages 191-203

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
            # Save the head for later
            prevHead = untriedHead
            
            for n in neighbors:
                if n in freePoints:
                    freePoints.remove( n )
                    new.append( n )
                    # Push onto front of list
                    untriedList[n] = untriedHead
                    untriedHead = n
                    
            # print "New neigbors", new
            
            # 4(b) call this algorithm recursively
            # untriedList is "its own copy" of the set because the
            # order relationship never changes
            for p in allPolyominoesRecursive( targetSize,
                                              newPoly,
                                              untriedHead,
                                              untriedList,
                                              freePoints ):
                yield p

            for n in new:
                freePoints.add( n )
            untriedHead = prevHead
            
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

def printPolyominos( n ):
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
        
                    
