import random

def divisors( n ):
    # Small N, trial division is fine.  Want only proper divisors
    return [ d for d in xrange( 2, n ) if n % d == 0 ]

def mutate( rectangle, ySize, xSize, n ):
    # Pick a random block and move it to the corresponding position in
    # an adjacent block.
    #
    # e.g.           x     x
    # Ax   => xA. or Ax or  Ax  but not  Ax x
    # xx       xx    .x     x.           .x
    #
    # All these moves preserve out ability to tesselate "simply"
    # although the example shown can still cover the plane.
    # FIXME: maybe come back and pick that up later.
    allowed = [ p for p in rectangle if p != (0,0) ]
    startPositions = random.sample( allowed, n )

    offset = [ (ySize * i, xSize * j)
               for i in [-1, 0, 1]
               for j in [-1, 0, 1]
               if i != 0 or j != 0 ]

    finalPositions = [ b for b in rectangle if b not in startPositions ]
    
    for (sy,sx) in startPositions:
        while True:
            (dy,dx) = random.sample( offset, 1 )[0]
            newPos = ( sy + dy, sx + dx )
            if newPos not in finalPositions:
                finalPositions.append( newPos )
                break
            
    return finalPositions

def showTile( tile ):
    for y in xrange( -10, 11 ):
        s = ""
        for x in xrange( -10, 11 ):
            if (y, x) in tile:
                s += "X"
            else:
                s += "."
        print s

def buildGrid( gridY, gridX, tile, ySize, xSize ):
    grid = [ [0 for x in xrange( gridX ) ]
             for y in xrange( gridY ) ]
    num = 1
    for i in xrange( gridY / ySize ):
        for j in xrange( gridX / xSize ):
            ty = i * ySize
            tx = j * xSize
            for ( dy, dx ) in tile:
                x = ( dx + tx ) % gridX
                y = ( dy + ty ) % gridY
                grid[y][x] = num
            num += 1

    return grid

def showGrid( grid, glyphs ):
    for row in grid:
        print "".join( glyphs[i] for i in row )
        
def tesselation( gridY, gridX ):
    ySize = random.sample( divisors( gridY ), 1 )[0]
    xSize = random.sample( divisors( gridX ), 1 )[0]

    rectangle = [ ( y, x )
                  for y in xrange( ySize )
                  for x in xrange( xSize ) ]

    tile = mutate( rectangle, ySize, xSize,
                   random.randint( 1, 3 ) )

    glyphs = [ ' ' ,
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
               '+', '.', '=', '-', '*' ]
                         
    #showTile( tile )
    grid = buildGrid( gridY, gridX,
                      tile,
                      ySize, xSize )
    showGrid( grid, glyphs )
    
    
    
