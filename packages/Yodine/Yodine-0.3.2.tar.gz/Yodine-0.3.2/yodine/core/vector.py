import math



try:
    raise ImportError("blah")
    import numpy as np


    class _Vector(np.ndarray):
        def vsize(self) -> float:
            return np.linalg.norm(self)

        def sqsize(self) -> float:
            return np.linalg.norm(self) ** 2

        def fisrsize(self) -> float:
            return 1 / (np.linalg.norm(self) ** 2)

        def unit(self) -> 'Vector':
            sz = self.vsize()

            if sz == 0:
                return Vector(0, 0)

            elif sz == 1:
                return self

            else:
                return self / sz

        def ints(self) -> 'Vector':
            return Vector(
                int(self[0]),
                int(self[1])
            )

        def rotate(self, angle: float) -> 'Vector':
            c = math.cos(angle)
            s = math.sin(angle)

            return Vector(
                self.x * c - self.y * s,
                self.x * s + self.y * c
            )

        @property
        def x(self) -> float:
            return self[0]

        @property
        def y(self) -> float:
            return self[1]

        @x.setter
        def x(self, v: float):
            self[0] = v

        @y.setter
        def y(self, v: float):
            self[1] = v

        def dot(self, b: 'Vector') -> float:
            return self[0] * b.vec[0] + self[1] * b.vec[1]

        @classmethod
        def new(cls, _x = None, _y = None):
            # get initial values
            if _y is not None:
                x = _x
                y = _y

            elif _x is not None:
                try:
                    x, y = _x

                except TypeError:
                    raise ValueError("Non-vectorial value: {}".format(repr(_x)))

            else:
                x = 0.
                y = 0.

            return super(_Vector, cls).__new__(cls, (2,), dtype=np.float128, buffer=np.array([x, y], dtype=np.float128))

        def __iadd__(self, b: 'Vector') -> 'Vector':
            self.x += b.x
            self.y += b.y
            return self

        def __isub__(self, b: 'Vector') -> 'Vector':
            self.x -= res.x
            self.y -= res.y
            return self

        def __imul__(self, b: 'Vector') -> 'Vector':
            try:
                self.x *= b.x
                self.y *= b.y

            except AttributeError:
                self.x *= b
                self.y *= b

            return self

        def __itruediv__(self, b: 'Vector') -> 'Vector':
            try:
                self.x /= b.x
                self.y /= b.y

            except AttributeError:
                self.x /= b
                self.y /= b

            return self

    def Vector(*args, **kwargs):
        return _Vector.new(*args, **kwargs)

except ImportError:
    import struct


    class _Vector(object):
        def __init__(self, x = None, y = None):
            if y is not None:
                self.x = x
                self.y = y

            elif x is not None:
                try:
                    self.x, self.y = x

                except TypeError:
                    raise ValueError("Non-vectorial value: {}".format(repr(x)))

            else:
                self.x = 0
                self.y = 0

        def __iter__(self):
            return iter((self.x, self.y))

        def __getitem__(self, co):
            if co in (0, 'x'):
                return self.x

            if co in (1, 'y'):
                return self.y

            raise KeyError("No such key in a vector: ", repr(co))

        def ints(self):
            return Vector(
                int(self[0]),
                int(self[1])
            )

        def rotate(self, angle: float) -> 'Vector':
            c = math.cos(angle)
            s = math.sin(angle)

            return Vector(
                self.x * c - self.y * s,
                self.x * s + self.y * c,
            )

        def vsize(self) -> float:
            return math.sqrt(self[0] ** 2 + self[1] ** 2)

        def sqsize(self) -> float:
            return float(self[0] ** 2 + self[1] ** 2)

        def fisrsize(self, sqs = None) -> float:
            y = sqs or self.sqsize()
            threehalfs = 1.5
            x2 = y * 0.5
        
            packed_y = struct.pack('f', y)       
            i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int 
            i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
            packed_i = struct.pack('i', i)
            y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float
            
            y = y * (threehalfs - (x2 * y * y))  # Newton's method
            return y

        def unit(self) -> 'Vector':
            sz = self.sqsize()
            fz = self.fisrsize(sz)

            if sz == 0:
                return Vector(0, 0)

            elif sz == 1:
                return self

            else:
                return self * fz

        def __add__(self, b: 'Vector') -> 'Vector':
            return Vector(self[0] + b.x, self[1] + b.y)

        def __neg__(self) -> 'Vector':
            return Vector(-self[0], -self[1])

        def __mul__(self, b) -> 'Vector':
            try:
                return Vector(self[0] * b.x, self[1] * b.y)

            except AttributeError:
                return Vector(self[0] * b, self[1] * b)

        def __truediv__(self, b) -> 'Vector':
            try:
                return Vector(self[0] / b.x, self[1] / b.y)

            except AttributeError:
                return Vector(self[0] / b, self[1] / b)

        def __iadd__(self, b: 'Vector') -> 'ComponentVector':
            res = self + b
            self.x = res.x
            self.y = res.y
            return self

        def __isub__(self, b: 'Vector') -> 'ComponentVector':
            res = self - b
            self.x = res.x
            self.y = res.y
            return self

        def __imul__(self, b: 'Vector') -> 'ComponentVector':
            res = self * b
            self.x = res.x
            self.y = res.y
            return self

        def __itruediv__(self, b: 'Vector') -> 'ComponentVector':
            res = self / b
            self.x = res.x
            self.y = res.y
            return self

        def dot(self, b: 'Vector') -> float:
            return self[0] * b.vec[0] + self[1] * b.vec[1]

        def __sub__(self, b: 'Vector') -> 'Vector':
            return self + (-b)

        def __lshift__(self, b: 'Vector') -> 'ComponentVector':
            self.x = b.x
            self.y = b.y
            return self

        def __repr__(self) -> str:
            return "{}(x={},y={})".format(type(self).__name__, self[0], self[1])

    Vector = _Vector



def ComponentVector(component: 'Component'):
    res = component.get()

    if not (hasattr(res, 'x') and hasattr(res, 'y')):
        from .entity import VectorComponent
        res = component.entity.create_component(component.name, component.value, VectorComponent)

        return res.get()

    return res
