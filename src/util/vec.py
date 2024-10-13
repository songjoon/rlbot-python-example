import math

from rlbot.flat import Vector3


class Vec3(Vector3):
    """
    This class should provide you with all the basic vector operations that you need, but feel free to extend its
    functionality when needed.
    The vectors found in the GameTickPacket will be flatbuffer vectors. Cast them to Vec3 like this:
    `car_location = Vec3(car.physics.location)`.

    Remember that the in-game axis are left-handed.

    When in doubt visit the wiki: https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
    """

    def __new__(
        cls, x: "float | Vec3 | Vector3" = 0, y: float = 0, z: float = 0
    ) -> "Vec3":
        """
        Create a new Vec3. The x component can alternatively be another vector with an x, y, and z component, in which
        case the created vector is a copy of the given vector and the y and z parameter is ignored. Examples:

        a = Vec3(1, 2, 3)

        b = Vec3(a)

        """
        match x:
            case Vector3(v_x, y, z) | Vec3(v_x, y, z):
                return super().__new__(cls, v_x, y, z)
            case _:
                return super().__new__(cls, x, y, z)

    def __init__(self, x: "float | Vec3 | Vector3" = 0, y: float = 0, z: float = 0): ...

    def __getitem__(self, item: int):
        return (self.x, self.y, self.z)[item]

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, scale: float) -> "Vec3":
        return Vec3(self.x * scale, self.y * scale, self.z * scale)

    def __rmul__(self, scale):
        return self * scale

    def __truediv__(self, scale: float) -> "Vec3":
        scale = 1 / float(scale)
        return self * scale

    def __str__(self):
        return f"Vec3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        return self.__str__()

    def flat(self):
        """Returns a new Vec3 that equals this Vec3 but projected onto the ground plane. I.e. where z=0."""
        return Vec3(self.x, self.y, 0)

    def length(self):
        """Returns the length of the vector. Also called magnitude and norm."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dist(self, other: "Vec3") -> float:
        """Returns the distance between this vector and another vector using pythagoras."""
        return (self - other).length()

    def normalized(self):
        """Returns a vector with the same direction but a length of one."""
        return self / self.length()

    def rescale(self, new_len: float) -> "Vec3":
        """Returns a vector with the same direction but a different length."""
        return new_len * self.normalized()

    def dot(self, other: "Vec3") -> float:
        """Returns the dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vec3") -> "Vec3":
        """Returns the cross product."""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def ang_to(self, ideal: "Vec3") -> float:
        """Returns the angle to the ideal vector. Angle will be between 0 and pi."""
        cos_ang = self.dot(ideal) / (self.length() * ideal.length())
        return math.acos(cos_ang)
