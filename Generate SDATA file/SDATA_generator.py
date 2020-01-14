class SDATAGenerator:
    FILE_HEADER = 'SDATA version 2.0'

    def __init__(self):
        self.NX = 2
        self.NY = 2
        self.NZ = 3

    def cells_str(self):
        return [Cell().str(iz + 1) for iz in range(self.NZ)]

    def str(self):
        SEGMENT_HEADER = '{}   {}   {}   : NX NY NT'.format(self.NX, self.NY, self.NZ)
        line = self.FILE_HEADER + '\n' + SEGMENT_HEADER
        cells_lines = ['\n\n' + cell for cell in self.cells_str()]
        line += ''.join(cells_lines)
        return line


class Cell:
    def __init__(self):
        self.NPIXELS = 4
        self.TIMESTAMP = '2008-06-14T14:49:28Z'
        self.HEIGHT_OBS = '70000.0'
        self.NSURF = 0
        self.IFGAS = 0

        self.NX = 2
        self.NY = 2
        self.NZ = 30

    def str(self, iz=None):
        CELL_HEADER = '   '.join(str(el) for el in [self.NPIXELS, self.TIMESTAMP, self.HEIGHT_OBS, self.NSURF, self.IFGAS])
        CELL_HEADER += ' : NPIXELS TIMESTAMP HOBS NSURF IFGAS   {} \n'.format(iz)
        line = CELL_HEADER + '\n'.join(self.pixels_str())
        return line

    def pixels_str(self):
        return [Pixel(ix + 1, iy + 1, self.NZ).str() for ix in range(self.NX) for iy in range(self.NY)]


class Pixel:
    def __init__(self, ix, iy, timestamp):
        self.ix = ix
        self.iy = iy
        self.icloudy = 1

        self.icol = ix + 1000
        self.irow = iy + 2345

        self._str = None

    def str(self):
        settings = '           '.join([str(el) for el in [self.ix, self.iy, self.icloudy, self.icol, self.irow]])

        line = settings
        return line


class Meas:
    def __init__(self):
        self.wl = None
        self.nwl = None
        self.meas_type = None
        self.nip = None
        self.nbvm = None

        self.sza = None
        self.vza = None
        self.raa = None


if __name__ == '__main__':
    sdata = SDATAGenerator()
    print(sdata.str())
