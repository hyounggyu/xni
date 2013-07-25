import sys, collections
import struct
import numpy as np

tag_names = {
    256: 'ImageWidth',
    257: 'ImageLength',
    258: 'BitsPerSample',
    259: 'Compression',
    262: 'PhotometricInterpretation',
    270: 'ImageDescription',
    271: 'Make',
    272: 'Model',
    273: 'StripOffsets',
    277: 'SamplesPerPixel',
    278: 'RowsPerStrip',
    279: 'StripByteCount',
    282: 'XResolution',
    283: 'YResolution',
    284: 'PlanarConfiguration',
    296: 'ResolutionUnit',
    305: 'Software',
    306: 'DateTime',
}

dtype_info = {
    1: (1,'B'),  # Byte
    2: (1,'c'),  # Char
    3: (2,'H'),  # Short
    4: (4,'I'),  # Integer
    5: (8,'II'), # Rational
}

default_dir = {
    256: 0, # ImageWidth
    257: 0, # ImageLength
    258: 0, # BitsPerSample
    259: 0, # Compression
    262: 0, # PhotometricInterpretation
    270: 0, # ImageDescription
    271: 0, # Make
    272: 0, # Model
    273: 0, # StripOffsets
    277: 0, # SamplesPerPixel
    278: 0, # RowsPerStrip
    279: 0, # StripByteCount
    282: 0, # XResolution
    283: 0, # YResolution
    284: 0, # PlanarConfiguration
    296: 0, # ResolutionUnit
    305: 0, # Software
    306: 0, # DateTime
}

class imread:
    endian = ''
    next_diroff = 0
    directory = {}
    
    def __init__(self, fname):
        self.fp = open(fname, 'rb') # check error
        
        block = self.fp.read(2)
        (magic,) = struct.unpack('H', block)
        if magic == 0x4d4d:
            self.endian = '>'
        elif magic == 0x4949:
            self.endian = '<'
        else:
            return None # raise error

        block = self.fp.read(6)
        (version, self.next_diroff) = struct.unpack(self.endian+'HI', block)
        if version != 42:
            return None # raise error
            
        self.read_dir()
        if not self.is_ok():
            return None # raise error

    def read_dir(self):
        diroff = self.next_diroff
        self.fp.seek(diroff, 0)
        block = self.fp.read(2)
        (dircount,) = struct.unpack(self.endian+'H', block)
        self.directory = {}

        for i in range(dircount):
            block = self.fp.read(8)
            (tag, dtype, count) = struct.unpack(self.endian+'HHI', block)
            block = self.fp.read(4)
            size, fmt_type = dtype_info.get(dtype, (-1,''))
            if dtype == 2:
                fmt_type = 's'
            fmt = str(count)+fmt_type
            if size*count > 4:
                (offset,) = struct.unpack(self.endian+'I', block)
                cur_offset = self.fp.tell()
                self.fp.seek(offset, 0)
                block = self.fp.read(size*count)
                values = struct.unpack(self.endian+fmt, block)
                self.fp.seek(cur_offset, 0)
            elif size*count > 0:
                values = struct.unpack(self.endian+fmt, block[:size*count])
            else:
                values = None
            if values == None:
                continue
            if len(values) == 1:
                values = values[0]
                if isinstance(values, basestring):
                    values = values[:-1]
            self.directory[tag] = {'dt': dtype, 'c': count, 'v': values}

        block = self.fp.read(4)
        (self.next_diroff,) = struct.unpack(self.endian+'I', block)

    def to_array(self):
        w  = self.directory[256]['v'] # width
        l  = self.directory[257]['v'] # length
        bs = self.directory[258]['v'] # bits per sample
        r  = self.directory[278]['v'] # rows per strip
        bc = self.directory[279]['v'] # byte count
        of = self.directory[273]['v'] # offsets        
        
        c = len(bc)
        if c != len(of):
            return 0 # raise error
            
        if bs == 8:
            dt = np.uint8
        elif bs == 16:
            dt = np.uint16
            
        arr = np.empty((l,w), dtype=dt)
        for i in range(c):
            self.fp.seek(of[i], 0)
            a = np.fromfile(self.fp, dtype=dt, count=bc[i])
            for j in range(r):
                arr[i*r+j] = a[w*j:w*(j+1)]

        return arr

    def is_ok(self):
        d = self.directory
        # cannot read tiled file
        ret = d[259] == 1 and d[277] == 1 and (d[258] == 8 or d[258] == 16)
        return ret
        
    def get_dir(self):
        return self.directory

    def info(self):
        for k, v in self.directory.items():
            tname = tag_names.get(k, k)
            print tname, v['v']

class imwrite:
    directory = {}
    arr = np.array([])
    ifd_offset_off = 0
    bitspersample = 0
    
    def __init__(self, fname, arr, directory):
        self.fp = open(fname, 'wb')
        self.arr = arr
        self.directory = directory
        
        # set bits per sample from dtype
        if arr.dtype == 'uint8':
            self.bitspersample = 8
        elif arr.dtype == 'uint16':
            self.bitspersample = 16
        else:
            return None # raise error
        self.directory[258]['v'] = self.bitspersample

        # this writer forces only one row per strip
        self.directory[278]['v'] = 1 # Rowsperstrip
        # add more directory info. compression, ...

        self.write_header()
        self.write_data()
        self.write_dir()

    def write_header(self):
        magic = 0x4949 if sys.byteorder == 'little' else 0x4d4d
        version = 42
        # temporary directory offset
        buf = struct.pack('HHI', magic, version, 0)
        self.ifd_offset_off = 4
        self.fp.write(buf)

    def write_data(self):
        img_offset = self.fp.tell()
        l, w = self.arr.shape
        self.arr.tofile(self.fp)
        bcperpixel = self.bitspersample/8
        of = [img_offset+i*w*bcperpixel for i in range(l)]
        bc = [w*bcperpixel for i in range(l)]
        self.directory[273] = {'dt': 4, 'c': l, 'v': of} # StripOffsets
        self.directory[279] = {'dt': 4, 'c': l, 'v': bc} # StripByteCount

    def write_dir(self):
        # write image file directory offset
        ifd_offset = self.fp.tell()
        self.fp.seek(self.ifd_offset_off, 0)
        buf = struct.pack('I', ifd_offset)
        self.fp.write(buf)
        self.fp.seek(ifd_offset, 0)
        
        # write directory count
        dircount = len(self.directory.keys())
        buf = struct.pack('H', dircount)
        self.fp.write(buf)
        
        # set value offset
        val_offset = ifd_offset + 2 + dircount*12 + 4
        
        for tag, v in self.directory.items():
            dtype = v['dt']
            count = v['c']
            values= v['v']
            
            size, fmt_type = dtype_info.get(dtype, (-1,''))
            # set string value as bytearray
            if dtype == 2:
                values = bytearray(values)
                if len(values) == 0:
                    values = bytearray('\x00')
                elif values[-1] != '\x00':
                    values = values + '\x00'
                count = len(values)
            fmt = str(count)+fmt_type
            
            if size*count > 4:
                buf = struct.pack('HHII', tag, dtype, count, val_offset)
                self.fp.write(buf)
                cur_offset = self.fp.tell()
                self.fp.seek(val_offset, 0)
                if type(values) == bytearray:
                    self.fp.write(values)
                else:
                    buf = struct.pack(fmt, *values)
                    self.fp.write(buf)
                val_offset = self.fp.tell()
                self.fp.seek(cur_offset, 0)
            elif size*count > 0:
                buf = struct.pack('HHI', tag, dtype, count)
                if type(values) == bytearray:
                    buf = buf + values
                elif isinstance(values, collections.Sequence):
                    buf = buf + struct.pack(fmt, *values)
                else:
                    buf = buf + struct.pack(fmt, values)
                buf = buf + '\x00'*(4-size*count)
                self.fp.write(buf)
            else:
                pass # add something?

        self.ifd_offset_off = self.fp.tell()
        self.fp.write('\x00'*4)
        
