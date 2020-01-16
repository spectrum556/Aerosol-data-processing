import json


class SDATAGenerator:
    FILE_HEADER = 'SDATA version 2.0'

    def __init__(self, timestamp_info_file_name, data_file_name):
        self.timestamp_info = self.read_json(timestamp_info_file_name)

        self.data = self.read_json(data_file_name)

        self.output_file_name = 'SDATA_files/example_{}.sdat'.format(timestamp_info_file_name.split('_')[-1])

        self.NX = 2
        self.NY = 2
        self.NZ = len(self.timestamp_info.keys())

        self.result = None

    def run(self, to_file=True):
        self.result = self.str()
        print(self.result)
        if to_file:
            self.to_file(self.output_file_name, self.result)

    @staticmethod
    def read_json(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

    @staticmethod
    def to_file(file_name, line):
        with open(file_name, 'w') as file:
            file.write(line)

    def cells_str(self):
        return [Cell(timestamp, self.timestamp_info[timestamp], self.data[timestamp]).str() for timestamp in self.timestamp_info]

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

        self.data = data

    def str(self):
        CELL_HEADER = '   '.join(str(el) for el in [int(self.NPIXELS),
                                                    self.TIMESTAMP,
                                                    self.HEIGHT_OBS,
                                                    int(self.NSURF),
                                                    int(self.IFGAS)])
        CELL_HEADER += ' : NPIXELS TIMESTAMP HOBS NSURF IFGAS\n'
        line = CELL_HEADER + '\n'.join(self.pixels_str())
        return line

    def pixels_str(self):
        str_list = []
        for pixel in self.data:
            key = list(pixel.keys())[0]
            ix, iy = key.split('_')
            str_list.append(Pixel(ix, iy, pixel[key]).str())
        return str_list


class Pixel:
    def __init__(self, ix, iy, data):
        self.ix = ix
        self.iy = iy
        self.data = data

    def str(self):
        settings = '           '.join([str(el) for el in [self.ix,
                                                          self.iy,
                                                          int(self.data['icloudy']),
                                                          int(self.data['icol']),
                                                          int(self.data['irow']),
                                                          '{:.7f}'.format(round(self.data['x'], 7)),
                                                          '{:.7f}'.format(round(self.data['y'], 7)),
                                                          "{:10.6f}".format(self.data['MASL']),
                                                          "{:10.6f}".format(self.data['land_percent']),
                                                          int(self.data['nwl'])]])

        meas_list = [self.data['wl'],
                     self.data['nip'],
                     self.data['meas_type'],
                     self.data['nbvm'],
                     self.data['sza'],
                     self.data['vza'],
                     self.data['raa'],
                     self.data['meas'],
                     self.data['ifcov'],
                     self.data['ifmp']]

        meas_list = ['           '.join([str(el) if type(el) == int else '{:10.7f}'.format(round(el, 7))
                                         for el in par])
                                         for par in meas_list]

        meas = '           '.join(meas_list)

        line = settings + '           ' + meas
        return line


if __name__ == '__main__':
    sdata = SDATAGenerator(data_file_name='intermediate_data/data_MSIP.json',
                           timestamp_info_file_name='intermediate_data/timestamp_info_MSIP.json')
    sdata.run(to_file=True)
    print(sdata.str())
