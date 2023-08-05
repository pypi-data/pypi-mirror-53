from colour import COLOR_NAME_TO_RGB, hex2rgb

def to_rgb(col):
    if type(col) == type(''):
        if col in COLOR_NAME_TO_RGB:
            col = COLOR_NAME_TO_RGB[col]
        else:
            try:
                col = hex2rgb(col)
            except:
                raise ValueError("Invalid color name: %s" % col)
    assert type(col) == type(())
    return col

class SVGShape:
    def __init__(self, stroke_width=1, stroke_color='black', fill_color='white'):
        self.stroke_width = stroke_width
        self.stroke_color = to_rgb(stroke_color)
        self.fill_color = to_rgb(fill_color)

class Dot(SVGShape):
    def __init__(self, pos=(50,50), radius=10, **kws):
        super(Dot, self).__init__(**kws)
        self.pos = pos
        self.radius = radius

    def to_svg(self):
        return '<circle cx="%d" cy="%d" r="%d" stroke="%s" stroke-width="%d" fill="%s" />' % (
            self.pos[0], self.pos[1], self.radius, self.stroke_color, self.stroke_width, self.fill_color)
    
class Line(SVGShape):
    def __init__(self, begin=(0,O), end=(100,100)):
        super(Line, self).__init__(**kws)
        self.begin = begin
        self.end = end

    def to_svg(self):
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:rgb(%d,%d,%d);stroke-width:%d" />' % (
            self.begin[0], self.begin[1], self.end[0], self.end[1],
            self.stroke_color[0], self.stroke_color[1], self.stroke_color[2], self.stroke_width)

class Diagonal(SVGShape):
    def __init__(dimension=100, end_padding=0, central_padding=0, direction='asc', **kws):
        super(Diagonal, self).__init__(**kws)
        if direction in ['desc', 'descending']:
            self.direction = 'desc'
            self.begin = (end_padding, dimension - end_padding)
            self.end = (dimension - end_padding, end_padding)
        else:
            self.direction = 'asc'
            self.begin = (end_padding, end_padding)
            self.end = (dimension - end_padding, dimension - end_padding)
        self.center_begin, self.center_end = None, None
        self.central_padding = central_padding
        if central_padding:
            if self.direction == 'desc':
                self.center_begin = (dimension*1.0/2 - central_padding, dimension*1.0/2 + central_padding)
                self.center_end = (dimension*1.0/2 + central_padding, dimension*1.0/2 - central_padding)
            else:
                self.center_begin = (dimension*1.0/2 - central_padding, dimension*1.0/2 - central_padding)
                self.center_end = (dimension*1.0/2 + central_padding, dimension*1.0/2 + central_padding)

    def to_svg(self):
        if self.central_padding:
            return Line(self.begin, self.center_begin).to_svg() + '\n' + Line(self.center_end, self.end).to_svg()
        else:
            return Line(self.begin, self.end).to_svg()

class Median(SVGShape):
    def __init__(dimension=100, end_padding=0, central_padding=0, direction='hor', **kws):
        super(Median, self).__init__(**kws)
        if direction in ['vert', 'vertical']:
            self.direction = "vert"
            self.begin = (dimension*1.0/2, end_padding)
            self.end = (dimension*1.0/2, dimension - end_padding)
        else:
            self.direction = "hor"
            self.begin = (end_padding, dimension*1.0/2)
            self.end = (dimension - end_padding, dimension*1.0/2)
        self.center_begin, self.center_end = None, None
        self.central_padding = central_padding
        if central_padding:
            if self.direction == 'vert':
                self.center_begin = (dimension*1.0/2, dimension*1.0/2 - central_padding)
                self.center_end = (dimension*1.0/2, dimension*1.0/2 + central_padding)
            else:
                self.center_begin = (dimension*1.0/2 - central_padding, dimension*1.0/2)
                self.center_end = (dimension*1.0/2 + central_padding, dimension*1.0/2)

    def to_svg(self):
        if self.central_padding:
            return Line(self.begin, self.center_begin).to_svg() + '\n' + Line(self.center_end, self.end).to_svg()
        else:
            return Line(self.begin, self.end).to_svg()

class Cross(SVGShape):
    def __init__(self, dimension=100, cross_shape='+', end_padding=0, central_padding=0, **kws):
        super(Cross, self).__init__(**kws)
        self.dimension = dimension
        self.cross_shape = cross_shape
        self.end_padding = end_padding
        self.central_padding = central_padding

    def to_svg(self):
        if self.central_padding:
            pass
        else:
            if self.cross_shape in ['x', 'X']:
                return Diagonal(self.dimension, self.end_padding, self.central_padding, 'asc', **kws).to_svg() \
                    + '\n' \
                    + Diagonal(self.dimension, self.end_padding, self.central_padding, 'desc', **kws).to_svg()
            else:
                return Median(self.dimension, self.end_padding, self.central_padding, 'hor', **kws).to_svg() \
                    + '\n' \
                    + Median(self.dimension, self.end_padding, self.central_padding, 'vert', **kws).to_svg()                

class Pipe(SVGShape):
    pass

class Elbow(SVGShape):
    pass

class BackgroundImage:
    r"""An SVG image to serve as cell background
    """
    def __init__(self, dot=None, cross=None, line=None, **kws):
        pass

    def to_svg(self):
        svg_lines = []
        svg_lines.append('<svg height="%d" width="%d">' % (self.height, self.width))
        svg_lines.append('</svg>')
        return '\n'.join(svg_lines)

