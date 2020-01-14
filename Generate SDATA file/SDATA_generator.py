import json

class SDATAGenerator:
    FILE_HEADER = 'SDATA version 2.0'

    def __init__(self):
        self.NX = 2
        self.NY = 2
        self.NZ = 30

        self.timestamp_info = self.read_json('timestamp_info.json')

        self.file_data = 'data.json'

    @staticmethod
    def read_json(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

    def cells_str(self):
        return [Cell(timestamp, self.timestamp_info[timestamp]).str() for timestamp in self.timestamp_info]

    def str(self):
        SEGMENT_HEADER = '{}   {}   {}   : NX NY NT'.format(self.NX, self.NY, self.NZ)
        line = self.FILE_HEADER + '\n' + SEGMENT_HEADER
        cells_lines = ['\n\n' + cell for cell in self.cells_str()]
        line += ''.join(cells_lines)
        return line


class Cell:
    def __init__(self, timestamp, info, data):
        self.TIMESTAMP = timestamp

        self.NPIXELS = info['NPIXELS']
        self.HEIGHT_OBS = info['HEIGHT_OBS']
        self.NSURF = info['NSURF']
        self.IFGAS = info['IFGAS']

        self.NX = 2
        self.NY = 2
        self.NZ = 30

    def str(self):
        CELL_HEADER = '   '.join(str(el) for el in [self.NPIXELS, self.TIMESTAMP, self.HEIGHT_OBS, self.NSURF, self.IFGAS])
        CELL_HEADER += ' : NPIXELS TIMESTAMP HOBS NSURF IFGAS\n'
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
