"""Iterated function systems."""

import random

class IFSError(Exception):
    pass

class Mapping:
    def __init__(self, *data):
        "Contraction mapping."
        if len(data) < 6:
            raise IFSError, "not enough mapping values"

        self.a = float(data[0])
        self.b = float(data[1])
        self.c = float(data[2])
        self.d = float(data[3])
        self.e = float(data[4])
        self.f = float(data[5])

        if len(data) == 6:
            self.p = None
        else:
            self.p = float(data[6])

        if self.contraction() >= 1:
            raise IFSError, "not a contraction mapping"

    def transform(self, x, y):
        "Transform point according to mapping."
        return (x * self.a + y * self.b + self.e,
                x * self.c + y * self.d + self.f)

    def contraction(self):
        "Return contraction factor."
        return abs(self.a * self.d - self.b * self.c)

class Colourmap:
    def __init__(self, default = (255, 255, 255)):
        self.colours = []
        self.lastval = -1
        self.default = default

    def add(self, val, colour):
        if val < 0 or val <= self.lastval or val > 1:
            raise IFSError, "colourmap values must be increasing in [0-1]"

        self.colours.append((val, colour))
        self.lastval = val

    def lookup(self, val):
        for i in xrange(len(self.colours) - 1):
            (vmin, cmin) = self.colours[i]
            (vmax, cmax) = self.colours[i + 1]

            if val >= vmin and val <= vmax:
                fac = (val - vmin) / (vmax - vmin)
                rgb = [0, 0, 0]

                for j in xrange(3):
                    rgb[j] = int(cmin[j] + fac * (cmax[j] - cmin[j]))

                return tuple(rgb)

        raise IFSError, "colourmap lookup error: " + str(val)

class Pointset:
    def __init__(self, xsize, ysize, points):
        self.xsize = xsize
        self.ysize = ysize
        self.points = points

    def image(self, colourmap = None):
        import Image
        im = Image.new("RGB", (self.xsize, self.ysize))

        if colourmap:
            vmin = 1e8
            vmax = -1e8
            for (x, y) in self.points.keys():
                val = self.points[(x, y)]
                vmin = min(vmin, val)
                vmax = max(vmax, val)

        for (x, y) in self.points.keys():
            if colourmap:
                val = self.points[(x, y)]
                fac = float(val - vmin) / (vmax - vmin)
                colour = colourmap.lookup(fac)
            else:
                colour = (255, 255, 255)

            try:
                im.putpixel((x, y), colour)
            except IndexError:
                pass

        return im.transpose(Image.FLIP_TOP_BOTTOM)

class IFS:
    def __init__(self, *mappings):
        self.mappings = mappings[:]

        # Calculate total contraction factor.
        calc = 0
        total = 0
        for m in self.mappings:
            total += m.contraction()
            if not m.p:
                calc = 1

        # Check it's not singular.
        if total < 1e-7:
            raise IFSError, "all mappings are singular"

        # Calculate probabilities if required.
        if calc:
            for m in self.mappings:
                m.p = m.contraction() / total

        # Check probabilities add up to 1.
        total = 0
        for m in self.mappings:
            total += m.p

        if total != 1:
            raise IFSError, "probabilities don't add up"

    def random(self, xsize = 100, ysize = 100, iterations = 10000,
               initrand = 10, margin = 0.1, clip = 0):
        "Generate randomized IFS pointset."
        self.setscale(xsize, ysize, margin = margin, clip = clip)

        x = y = 0
        s = {}

        for i in xrange(initrand + iterations):
            (x, y) = self.randmap().transform(x, y)
            if i >= initrand:
                ix = int(self.scale * (x - self.xoff))
                iy = int(self.scale * (y - self.yoff))
                n = s.get((ix, iy), 0)
                s[(ix, iy)] = n + 1

        return Pointset(self.xsize, self.ysize, s)

    def deterministic(self, xsize = 100, ysize = 100, iterations = 10,
                      margin = 0.1, clip = 0):
        "Generate deterministic IFS pointset."
        self.setscale(xsize, ysize, margin = margin, clip = clip)

        s = {}
        for x in xrange(xsize):
            for y in xrange(ysize):
                s[(x, y)] = 0

        for i in xrange(iterations):
            new = {}

            for (ix, iy) in s:
                x = self.xoff + ix / self.scale
                y = self.yoff + iy / self.scale

                for m in self.mappings:
                    (xnew, ynew) = m.transform(x, y)
                    ixnew = int(self.scale * (xnew - self.xoff))
                    iynew = int(self.scale * (ynew - self.yoff))
                    n = new.get((ixnew, iynew), 0)
                    new[(ixnew, iynew)] = n + 1

            s = new

        return Pointset(self.xsize, self.ysize, s)

    def setscale(self, xsize = 100, ysize = 100, iterations = 1000,
                 initrand = 10, margin = 0.1, clip = 0):
        "Calculate X/Y offsets and scaling factor."
        x = y = 0
        for i in xrange(iterations):
            (x, y) = self.randmap().transform(x, y)

            if i == initrand:
                xmin = xmax = x
                ymin = ymax = y
            elif i > initrand:
                xmin = min(xmin, x)
                ymin = min(ymin, y)
                xmax = max(xmax, x)
                ymax = max(ymax, y)

        xdiff = xmax - xmin
        ydiff = ymax - ymin

        xmin -= margin * xdiff
        xmax += margin * xdiff
        ymin -= margin * ydiff
        ymax += margin * ydiff

        sx = xsize / (xmax - xmin)
        sy = ysize / (ymax - ymin)

        if clip:
            if sx < sy:
                ysize = int(ysize * sx / sy) + 1
            else:
                xsize = int(xsize * sy / sx) + 1

        self.scale = min(sx, sy)
        self.xoff = xmin
        self.yoff = ymin
        self.xsize = xsize
        self.ysize = ysize

    def randmap(self):
        "Return a random mapping based on probabilities."
        total = 0
        x = random.random()

        for m in self.mappings:
            total += m.p
            if total >= x:
                return m

        # Shouldn't get here!
        raise IFSError, "internal random mapping problem"

if __name__ == "__main__":
    c = Colourmap()
    c.add(0.000, (255, 200,   0))
    c.add(0.003, (255, 255,   0))
    c.add(0.007, (  0, 255,   0))
    c.add(1.000, (  0, 255,   0))

    m1 = Mapping(0, 0, 0, 0.16, 0, 0, 0.01)
    m2 = Mapping(0.85, 0.04, -0.04, 0.85, 0, 1.6, 0.85)
    m3 = Mapping(0.2, -0.26, 0.23, 0.22, 0, 1.6, 0.07)
    m4 = Mapping(-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07)

    ifs = IFS(m1, m2, m3, m4)
    points = ifs.random(300, 300, 20000, clip = 1)
    points.image(c).show()
