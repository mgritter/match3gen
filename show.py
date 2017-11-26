import gi
gi.require_version( "Gtk", "3.0" )
from gi.repository import Gtk
import cairo as pycairo
import cairocffi as cairo

def _UNSAFE_pycairo_context_to_cairocffi(pycairo_context):
    # Sanity check. Continuing with another type would probably segfault.
    if not isinstance(pycairo_context, pycairo.Context):
        raise TypeError('Expected a cairo.Context, got %r' % pycairo_context)

    # Magic from API documentation
    return cairo.Context._from_pointer(
        cairo.ffi.cast('cairo_t **',
                       id(pycairo_context) + object.__basicsize__)[0],
        incref=True)

class Show(Gtk.Window):
    def __init__( self,
                  surface,
                  title = "" ):
        super(Show, self).__init__()
        self.initUi( surface, title )
        self.surface = surface

    def run( self ):
        Gtk.main()
        
    def initUi( self, surface, title ):
        self.drawing = Gtk.DrawingArea()
        self.drawing.connect( "draw", self.on_draw )
        self.add( self.drawing )
        
        self.set_title( title )
        self.resize( surface.get_width(), surface.get_height() )
        self.connect( "delete-event", Gtk.main_quit )
        self.show_all()

    def on_draw( self, wd, cr ):
        cr = _UNSAFE_pycairo_context_to_cairocffi( cr )
        cr.set_source_surface( self.surface )
        cr.paint()

def sample():
    s = cairo.ImageSurface( cairo.FORMAT_ARGB32, 200, 200 )
    c = cairo.Context( s )
    c.set_source_rgba( 255, 255, 255 )
    c.rectangle( 0, 0, 200, 200 )
    c.fill()
    c.set_source_rgba( 255, 0, 0 )
    c.rectangle( 50, 50, 100, 100 )
    c.stroke()
    Show( s ).run()
    
    
