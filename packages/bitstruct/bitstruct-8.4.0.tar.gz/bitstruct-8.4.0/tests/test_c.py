from __future__ import print_function
import sys
import timeit
import unittest

if sys.version_info[0] < 3:
    print('Skipping C extension tests in Python 2.')
else:
    import bitstruct.c
    from bitstruct.c import *


class CTest(unittest.TestCase):

    def test_pack(self):
        """Pack values.

        """

        if sys.version_info[0] < 3:
            return

        packed = pack('u1u1s6u7u9', 0, 0, -2, 65, 22)
        self.assertEqual(packed, b'\x3e\x82\x16')

        packed = pack('u1', 1)
        self.assertEqual(packed, b'\x80')

        with self.assertRaises(NotImplementedError):
            packed = pack('u77', 0x100000000001000000)
            ref = b'\x00\x80\x00\x00\x00\x00\x08\x00\x00\x00'
            self.assertEqual(packed, ref)

        with self.assertRaises(NotImplementedError):
            packed = pack('u8000', int(8000 * '1', 2))
            ref = 1000 * b'\xff'
            self.assertEqual(packed, ref)

        with self.assertRaises(NotImplementedError):
            packed = pack('s4000', int(8000 * '0', 2))
            ref = 500 * b'\x00'
            self.assertEqual(packed, ref)

        packed = pack('p1u1s6u7u9', 0, -2, 65, 22)
        self.assertEqual(packed, b'\x3e\x82\x16')

        packed = pack('P1u1s6u7u9', 0, -2, 65, 22)
        self.assertEqual(packed, b'\xbe\x82\x16')

        packed = pack('p1u1s6p7u9', 0, -2, 22)
        self.assertEqual(packed, b'\x3e\x00\x16')

        packed = pack('P1u1s6p7u9', 0, -2, 22)
        self.assertEqual(packed, b'\xbe\x00\x16')

        with self.assertRaises(NotImplementedError):
            packed = pack('u1s6f32r43', 0, -2, 3.75, b'\x00\xff\x00\xff\x00\xff')
            self.assertEqual(packed, b'\x7c\x80\xe0\x00\x00\x01\xfe\x01\xfe\x01\xc0')

        packed = pack('b1', True)
        self.assertEqual(packed, b'\x80')

        packed = pack('b1p6b1', True, True)
        self.assertEqual(packed, b'\x81')

        packed = pack('b1P6b1', True, True)
        self.assertEqual(packed, b'\xff')

        packed = pack('u5b2u1', 31, False, 1)
        self.assertEqual(packed, b'\xf9')

        packed = pack('b1t24', False, u'Hi!')
        self.assertEqual(packed, b'$4\x90\x80')

        packed = pack('b1t24', False, 'Hi!')
        self.assertEqual(packed, b'$4\x90\x80')

        packed = pack('t8000', 1000 * '7')
        self.assertEqual(packed, 1000 * b'\x37')

        if sys.version_info >= (3, 6):
            packed = pack('f16', 1.0)
            self.assertEqual(packed, b'\x3c\x00')

        packed = pack('f32', 1.0)
        self.assertEqual(packed, b'\x3f\x80\x00\x00')

        packed = pack('f64', 1.0)
        self.assertEqual(packed, b'\x3f\xf0\x00\x00\x00\x00\x00\x00')

    def test_unpack(self):
        """Unpack values.

        """

        if sys.version_info[0] < 3:
            return

        unpacked = unpack('u1u1s6u7u9', b'\x3e\x82\x16')
        self.assertEqual(unpacked, (0, 0, -2, 65, 22))

        # unpacked = unpack('u1', bytearray(b'\x80'))
        unpacked = unpack('u1', b'\x80')
        self.assertEqual(unpacked, (1, ))

        with self.assertRaises(NotImplementedError):
            packed = b'\x00\x80\x00\x00\x00\x00\x08\x00\x00\x00'
            unpacked = unpack('u77', packed)
            self.assertEqual(unpacked, (0x100000000001000000,))

        with self.assertRaises(NotImplementedError):
            packed = 1000 * b'\xff'
            unpacked = unpack('u8000', packed)
            self.assertEqual(unpacked, (int(8000 * '1', 2), ))

        with self.assertRaises(NotImplementedError):
            packed = 500 * b'\x00'
            unpacked = unpack('s4000', packed)
            self.assertEqual(unpacked, (0, ))

        packed = b'\xbe\x82\x16'
        unpacked = unpack('P1u1s6u7u9', packed)
        self.assertEqual(unpacked, (0, -2, 65, 22))

        packed = b'\x3e\x82\x16'
        unpacked = unpack('P1u1s6u7u9', packed)
        self.assertEqual(unpacked, (0, -2, 65, 22))

        packed = b'\xbe\x82\x16'
        unpacked = unpack('p1u1s6u7u9', packed)
        self.assertEqual(unpacked, (0, -2, 65, 22))

        packed = b'\x3e\x82\x16'
        unpacked = unpack('p1u1s6u7u9', packed)
        self.assertEqual(unpacked, (0, -2, 65, 22))

        packed = b'\x3e\x82\x16'
        unpacked = unpack('p1u1s6p7u9', packed)
        self.assertEqual(unpacked, (0, -2, 22))

        with self.assertRaises(NotImplementedError):
            packed = b'\x7c\x80\xe0\x00\x00\x01\xfe\x01\xfe\x01\xc0'
            unpacked = unpack('u1s6f32r43', packed)
            self.assertEqual(unpacked, (0, -2, 3.75, b'\x00\xff\x00\xff\x00\xe0'))

        # packed = bytearray(b'\x80')
        packed = b'\x80'
        unpacked = unpack('b1', packed)
        self.assertEqual(unpacked, (True, ))

        packed = b'\x80'
        unpacked = unpack('b1p6b1', packed)
        self.assertEqual(unpacked, (True, False))

        packed = b'\x06'
        unpacked = unpack('u5b2u1', packed)
        self.assertEqual(unpacked, (0, True, 0))

        packed = b'\x04'
        unpacked = unpack('u5b2u1', packed)
        self.assertEqual(unpacked, (0, True, 0))

        packed = b'$4\x90\x80'
        unpacked = unpack('b1t24', packed)
        self.assertEqual(unpacked, (False, u'Hi!'))

        packed = 1000 * b'7'
        unpacked = unpack('t8000', packed)
        self.assertEqual(packed, 1000 * b'\x37')

        if sys.version_info >= (3, 6):
            unpacked = unpack('f16', b'\x3c\x00')
            self.assertEqual(unpacked, (1.0, ))

        unpacked = unpack('f32', b'\x3f\x80\x00\x00')
        self.assertEqual(unpacked, (1.0, ))

        unpacked = unpack('f64', b'\x3f\xf0\x00\x00\x00\x00\x00\x00')
        self.assertEqual(unpacked, (1.0, ))

    def test_pack_unpack_raw(self):
        """Pack and unpack raw values.

        """

        if sys.version_info[0] < 3:
            return

        with self.assertRaises(NotImplementedError):
            packed = pack('r24', b'')
            self.assertEqual(packed, b'\x00\x00\x00')

        with self.assertRaises(NotImplementedError):
            packed = pack('r24', b'12')
            self.assertEqual(packed, b'12\x00')

        packed = pack('r24', b'123')
        self.assertEqual(packed, b'123')
        packed = pack('r24', b'1234')
        self.assertEqual(packed, b'123')

        unpacked = unpack('r24', b'\x00\x00\x00')[0]
        self.assertEqual(unpacked, b'\x00\x00\x00')
        unpacked = unpack('r24', b'12\x00')[0]
        self.assertEqual(unpacked, b'12\x00')
        unpacked = unpack('r24', b'123')[0]
        self.assertEqual(unpacked, b'123')
        unpacked = unpack('r24', b'1234')[0]
        self.assertEqual(unpacked, b'123')

    def test_pack_unpack_dict(self):
        if sys.version_info[0] < 3:
            return

        unpacked = {
            'foo': 0,
            'bar': 0,
            'fie': -2,
            'fum': 65,
            'fam': 22
        }
        packed = b'\x3e\x82\x16'
        fmt = 'u1u1s6u7u9'
        names = ['foo', 'bar', 'fie', 'fum', 'fam']

        self.assertEqual(pack_dict(fmt, names, unpacked), packed)
        self.assertEqual(unpack_dict(fmt, names, packed), unpacked)

    def test_performance_mixed_types(self):
        """Test pack/unpack performance with mixed types.

        """

        if sys.version_info[0] < 3:
            return

        print()

        time = timeit.timeit("pack('s6u7r40b1t152', "
                             "-2, 22, b'\x01\x01\x03\x04\x05', "
                             "True, u'foo fie bar gom gum')",
                             setup="from bitstruct.c import pack",
                             number=50000)
        print("c pack time: {} s ({} s/pack)".format(time, time / 50000))

        time = timeit.timeit(
            "fmt.pack(-2, 22, b'\x01\x01\x03\x04\x05', "
            "True, u'foo fie bar gom gum')",
            setup="import bitstruct.c ; fmt = bitstruct.c.compile('s6u7r40b1t152')",
            number=50000)
        print("c pack time compiled: {} s ({} s/pack)".format(time, time / 50000))

        time = timeit.timeit("unpack('s6u7r40b1t152', "
                             "b'\\xf8\\xb0\\x08\\x08\\x18 "
                             "-\\x99\\xbd\\xbc\\x81\\x99"
                             "\\xa5\\x94\\x81\\x89\\x85"
                             "\\xc8\\x81\\x9d\\xbd\\xb4"
                             "\\x81\\x9d\\xd5\\xb4')",
                             setup="from bitstruct.c import unpack",
                             number=50000)
        print("c unpack time: {} s ({} s/unpack)".format(time, time / 50000))

        time = timeit.timeit(
            "fmt.unpack(b'\\xf8\\xb0\\x08\\x08\\x18 "
            "-\\x99\\xbd\\xbc\\x81\\x99"
            "\\xa5\\x94\\x81\\x89\\x85"
            "\\xc8\\x81\\x9d\\xbd\\xb4"
            "\\x81\\x9d\\xd5\\xb4')",
            setup="import bitstruct.c ; fmt = bitstruct.c.compile('s6u7r40b1t152')",
            number=50000)
        print("c unpack time compiled: {} s ({} s/unpack)".format(time, time / 50000))

    def test_compile(self):
        if sys.version_info[0] < 3:
            return

        cf = bitstruct.c.compile('u1u1s6u7u9')

        packed = cf.pack(0, 0, -2, 65, 22)
        self.assertEqual(packed, b'\x3e\x82\x16')

        unpacked = cf.unpack(b'\x3e\x82\x16')
        self.assertEqual(unpacked, (0, 0, -2, 65, 22))

    def test_compile_pack_unpack_formats(self):
        if sys.version_info[0] < 3:
            return

        fmts = [
            ('u1s2p3',         None, (1, -1)),
            # ('u1 s2 p3',       None, (1, -1)),
            ('u1s2p3',         None, (1, -1)),
            ('u1s2p3',   ['a', 'b'], {'a': 1, 'b': -1})
        ]

        for fmt, names, decoded in fmts:
            if names is None:
                cf = bitstruct.c.compile(fmt)
                packed_1 = cf.pack(*decoded)
                packed_2 = pack(fmt, *decoded)
            else:
                cf = bitstruct.c.compile(fmt, names)
                packed_1 = cf.pack(decoded)
                packed_2 = pack_dict(fmt, names, decoded)

            self.assertEqual(packed_1, b'\xe0')
            self.assertEqual(packed_2, b'\xe0')

            if names is None:
                unpacked_1 = cf.unpack(packed_1)
                unpacked_2 = unpack(fmt, packed_2)
            else:
                unpacked_1 = cf.unpack(packed_1)
                unpacked_2 = unpack_dict(fmt, names, packed_2)

            self.assertEqual(unpacked_1, decoded)
            self.assertEqual(unpacked_2, decoded)

    def test_compile_formats(self):
        if sys.version_info[0] < 3:
            return

        bitstruct.c.compile('p1u1')
        bitstruct.c.compile('p1u1', ['a'])

        with self.assertRaises(TypeError):
            bitstruct.c.compile()

    def test_pack_unpack_signed(self):
        if sys.version_info[0] < 3:
            return

        datas = [
            ('s1', 0, b'\x00'),
            ('s1', -1, b'\x80'),
            ('s63', -1, b'\xff\xff\xff\xff\xff\xff\xff\xfe'),
            ('s64', -1, b'\xff\xff\xff\xff\xff\xff\xff\xff')
        ]

        for fmt, value, packed in datas:
            self.assertEqual(pack(fmt, value), packed)
            self.assertEqual(unpack(fmt, packed), (value, ))

    def test_pack_unpack_unsigned(self):
        if sys.version_info[0] < 3:
            return

        datas = [
            ('u1', 0, b'\x00'),
            ('u1', 1, b'\x80'),
            ('u63', 0x1234567890abcdef, b'$h\xac\xf1!W\x9b\xde'),
            ('u64', 0x1234567890abcdef, b'\x124Vx\x90\xab\xcd\xef')
        ]

        for fmt, value, packed in datas:
            self.assertEqual(pack(fmt, value), packed)
            self.assertEqual(unpack(fmt, packed), (value, ))

    def test_various(self):
        if sys.version_info[0] < 3:
            return

        with self.assertRaises(ValueError):
            pack('u89999888888888888888899', 1)

        # Fewer names than fields in the format.
        with self.assertRaises(ValueError):
            pack_dict('u1u1', ['foo'], {'foo': 1})

        # Missing value for name.
        with self.assertRaises(KeyError):
            pack_dict('u1', ['foo'], {})

        # Fewer names than fields in the format.
        with self.assertRaises(ValueError):
            unpack_dict('u1u1', ['foo'], b'\xff')

        # Short data.
        with self.assertRaises(ValueError):
            unpack_dict('u1', ['foo'], b'')

        # Padding last.
        self.assertEqual(pack('u1p1', 1), b'\x80')
        self.assertEqual(pack_dict('u1p1', ['foo'], {'foo': 1}), b'\x80')

        # Short text.
        with self.assertRaises(NotImplementedError) as cm:
            pack('t16', '1')

        self.assertEqual(str(cm.exception), 'Short text.')

        # Bad float length.
        with self.assertRaises(NotImplementedError) as cm:
            pack('f1', 1.0)

        if sys.version_info >= (3, 6):
            self.assertEqual(str(cm.exception), 'Float not 16, 32 or 64 bits.')
        else:
            self.assertEqual(str(cm.exception), 'Float not 32 or 64 bits.')

        # Long bool.
        with self.assertRaises(NotImplementedError) as cm:
            pack('b65', True)

        self.assertEqual(str(cm.exception), 'Bool over 64 bits.')

        # Text not multiple of 8 bits.
        with self.assertRaises(NotImplementedError) as cm:
            pack('t1', '')

        self.assertEqual(str(cm.exception), 'Text not multiple of 8 bits.')

        # Bad format kind.
        with self.assertRaises(ValueError) as cm:
            pack('x1', '')

        self.assertEqual(str(cm.exception), "Bad format field type 'x'.")

        # Too few arguments.
        with self.assertRaises(ValueError) as cm:
            pack('u1u1', 1)

        self.assertEqual(str(cm.exception), 'Too few arguments.')

        # No format string.
        with self.assertRaises(ValueError) as cm:
            pack()

        self.assertEqual(str(cm.exception), 'No format string.')

        # No format string.
        with self.assertRaises(ValueError) as cm:
            unpack('u1', b'')

        self.assertEqual(str(cm.exception), 'Short data.')

        # Bad format in compile.
        with self.assertRaises(ValueError) as cm:
            bitstruct.c.compile('x1')

        self.assertEqual(str(cm.exception), "Bad format field type 'x'.")

        # Bad format in compile dict.
        with self.assertRaises(ValueError) as cm:
            bitstruct.c.compile('x1', ['foo'])

        self.assertEqual(str(cm.exception), "Bad format field type 'x'.")


if __name__ == '__main__':
    unittest.main()
