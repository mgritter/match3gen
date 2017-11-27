"""Random generations of tesselations of the rectangular grid."""

import random

def divisors( n ):
    # Small N, trial division is fine.  Want only proper divisors
    return [ d for d in xrange( 2, n ) if n % d == 0 ]

def allowedAny( rectangle, ySize, xSize ):
    return [ p for p in rectangle if p != (0,0) ]

def allowedBorder( rectangle, ySize, xSize ):
    return [ (y,x) for (y,x) in rectangle
             if (y,x) != (0,0) and
             ( y == 0 or y == ySize - 1 or x == 0 or x == xSize - 1) ]

def bottomRightBorder( rectangle, ySize, xSize ):
    return [ (y,x) for (y,x) in rectangle
             if y == ySize - 1 or x == xSize - 1 ]

def anyOffset( ySize, xSize, sy, sx ):
    offsets = [ (ySize * i, xSize * j)
                for i in [-1, 0, 1]
                for j in [-1, 0, 1]
                if i != 0 or j != 0 ]
        
    return random.sample( offsets, 1 )[0]

def oppositeOffset( ySize, xSize, sy, sx ):
    offsets = []
    if sy == 0:
        offsets.append( ( +ySize, 0 ) )
    if sx == 0:
        offsets.append( ( 0, +xSize ) )
    # (0,0) not permitted?
        
    if sy == ySize - 1:
        offsets.append( ( -ySize, 0 ) )
        if sx == xSize - 1:
            offsets.append( ( -ySize, -xSize ) )

    if sx == xSize - 1:
        offsets.append( ( 0, -xSize ) )

    if len( offsets ) > 0:
        return random.sample( offsets, 1 )[0]
    else:
        return anyOffset( ySize, xSize )

def smallRandom( ySize, xSize ):
    return random.randint( 1, 3 )

def xyRandom( ySize, xSize ):
    return random.randint( 0, ySize + xSize - 1 )

def mediumRandom( ySize, xSize ):
    return random.randint( 0, 2 * ySize + 2 * ( xSize - 1) - 1 )

def largeRandom( ySize, xSize ):
    return random.randint( 0, ySize * xSize - 1 )

# Factory function for cell pickers based on random function and
# allowed function
def cellChooserFactory( allowedCells, randomRange ):
    def func( rectangle, ySize, xSize ):
        allowed = allowedCells( rectangle, ySize, xSize )
        n = min( randomRange( ySize, xSize ), len( allowed ) )
        return random.sample( allowed, n )
                
    return func

def mutate( rectangle, ySize, xSize,
            cellPicker,
            offsetPicker ):
    # Pick a random block and move it to the corresponding position in
    # an adjacent block.
    #
    # e.g.           x     x
    # Ax   => xA. or Ax or  Ax  but not  Ax x
    # xx       xx    .x     x.           .x
    #
    # All these moves preserve our ability to tesselate "simply"
    # although the example shown can still cover the plane.
    # FIXME: maybe come back and pick that up later.

    startPositions = cellPicker( rectangle, ySize, xSize )
    finalPositions = [ b for b in rectangle if b not in startPositions ]
    
    for (sy,sx) in startPositions:
        while True:
            (dy,dx) = offsetPicker( ySize, xSize, sy, sx )
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

def tesselation( gridY, gridX,
                 numCells = mediumRandom,
                 allowedCells = allowedAny,
                 allowedOffsets = anyOffset ):
    ySize = random.sample( divisors( gridY ), 1 )[0]
    xSize = random.sample( divisors( gridX ), 1 )[0]

    rectangle = [ ( y, x )
                  for y in xrange( ySize )
                  for x in xrange( xSize ) ]

    cellChooser = cellChooserFactory( allowedCells, numCells )
    
    tile = mutate( rectangle, ySize, xSize,
                   cellChooser,
                   allowedOffsets )


    return ( tile, ySize, xSize )

def printTesselation( gridY, gridX ):
    glyphs = [ ' ' ,
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
               '+', '.', '=', '-', '*' ]

    ( tile, ySize, xSize ) = tesselation( gridY, gridX )
    #showTile( tile )
    grid = buildGrid( gridY, gridX,
                      tile,
                      ySize, xSize )
    showGrid( grid, glyphs )

import cairocffi as cairo
from show import Show

def showTesselation( gridHeight, gridWidth ):
    cellPixels = 20
    width = cellPixels * gridWidth
    height = cellPixels * gridHeight
    
    ( tile, ySize, xSize ) = tesselation( gridHeight, gridWidth )

    surface = cairo.ImageSurface( cairo.FORMAT_ARGB32,
                                  width=width,
                                  height=height )
    context = cairo.Context( surface )
    context.set_source_rgba( 1.0, 1.0, 1.0 )
    context.rectangle( 0, 0, width, height )
    context.fill()

    colors = [
        [ (0.0, 0.0, 1.0), (0.0, 0.5, 0.5), (0.0, 1.0, 0.0) ],
        [ (0.8, 1.0, 0.8), (0.2, 0.2, 0.2), (0.0, 0.8, 1.0) ],
        [ (0.5, 0.5, 0.5), (0.0, 0.7, 0.3), (0.0, 0.3, 0.7) ]
        ]
    for yi in xrange( 0, gridHeight, ySize ):
        yc = ( yi / ySize ) % 3
        for xi in xrange( 0, gridWidth, xSize ):
            xc = ( xi / xSize ) % 3
            context.set_source_rgba( *(colors[yc][xc]) )

            # Special example tile
            if yi == ySize and xi == xSize:
                context.set_source_rgba( 1.0, 0.0, 0.0 )

            for ( dy, dx ) in tile:
                y = ( ( yi + dy ) % gridHeight ) * cellPixels
                x = ( ( xi + dx ) % gridWidth ) * cellPixels
                yw = cellPixels - 1
                xw = cellPixels - 1

                # If neighbors exist, extend to meet them
                if ( dy + 1, dx ) in tile:
                    yw += 1
                if ( dy, dx+1 ) in tile:
                    xw += 1

                context.rectangle( x, y, xw, yw )
                
            context.fill()
                
    Show( surface ).run()

    
    
    
