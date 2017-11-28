title: Python, object operations and vectors
date: 2017-11-28
tags: python, programming, math
slug: python-object-operations-and-vectors
---

A few days ago I was bored and decided to read a book about raytracing, the code was in C++ but thanks to my love for [Jupyter notebooks]() I decided to rewrite the code in Python, so far so good (maybe one day I will post about it), then I faced a small issue, I forgot most of my vector math and linear algebra classes in high school :( (I don't hold a computer science degree). I decide to refresh my little knowledge of linear algebra and vector operations and I saw it was a good exercise to explore Python operators and special methods.

## What is a Vector and Point?

The easy way to describe a [point](https://en.wikipedia.org/wiki/Point_(geometry)) is just as a location in space. A point is described by coordinates and in some books it is described as a transposed one row matrix with its coordinates, $(x, y, z)^\top$ or as a one column matrix:

$$
\begin{bmatrix}
x \\ y \\ z
\end{bmatrix} = (x, y, z)^\top
$$

A vector doesn't have a location, but it has direction and length, the length is usually named _magnitude_. Vectors can be named and their name in mathematics are expressed by a letter with **bold** or a _bar_ name ($\mathbf{a}, \vec{a}$).

Let's describe a vector in Python:

```py
class Vector:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self) -> str:
    return f'<Vector {self.x}, {self.y}, {self.z}>'
```

## Adding and substracting vectors

This is the easiest operation, basically it is mathematically described as:

$$
\begin{bmatrix} x_v \\ y_v \\ z_v \end{bmatrix} + \begin{bmatrix} x_u \\ y_u \\ z_u \end{bmatrix} = \begin{bmatrix} x_v + x_u \\ y_v + y_u \\z_v + z_u \end{bmatrix}
$$

In Python it will look something like this:

```py
from typing import TypeVar

TVector = TypeVar('TVector', bound='Vector')

class Vector:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self) -> str:
    return f'<Vector {self.x}, {self.y}, {self.z}>'

  def add(other: TVector) -> TVector:
    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

```

But to be honest, we can use one of the [Python special methods](https://docs.python.org/3/reference/datamodel.html) so it will look more natural to do something like `Vector(1, 2, 3) + Vector(4, 5, 6)`:

```py
from typing import TypeVar

TVector = TypeVar('TVector', bound='Vector')

class Vector:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self) -> str:
    return f'<Vector {self.x}, {self.y}, {self.z}>'

  def __add__(other: TVector) -> TVector:
    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(other: TVector) -> TVector:
    return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

```

## Scaling a Vector

The operation of a Vector and a real number is called _scaling_, it is simple:

$$
k\ \begin{bmatrix} x \\ y \\ z\end{bmatrix} = \begin{bmatrix} kx \\ ky \\ kz\end{bmatrix}
$$

Again, let's use a Python special method for it, in this case the multiplication of a real and a Vector is a Vector, in this case it is not enough to override the `__mul__` operator, mostly because that will allow only operations _between a vector and an integer_ **NOT** the opposite. To allow operations _between an integer and a vector_ we will have to override the `__mul__` operator in the integer or use the `__rmul__` operator, or well, named _right multiplication_.

```py
from typing import TypeVar

TVector = TypeVar('TVector', bound='Vector')
TNumber = TypeVar('TNumber', int, float)

class Vector:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self) -> str:
    return f'<Vector {self.x}, {self.y}, {self.z}>'

  def __add__(other: TVector) -> TVector:
    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(other: TVector) -> TVector:
    return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

  def __mul__(other: TNumber) -> TVector:
    return Vector(self.x * other, self.y * other, self.z * other)

  __rmul__ = __mul__

```

## Equality

Vector are like matrices, they are equal if all the members are the same, in Python this is easy:

```py
def __eq__(self, other: TVector) -> bool:
  return self.x == other.x and self.y == other.y and self.z == other.z

```

## Length or magnitude

This is represented in mathematical notation by the vector name around bars ($|\ \mathbf{v}\ |$) and it is basically defined as:

$$
|\ \mathbf{v}\ | = \sqrt{v_x^2 + v_y^2 + v_z^2}
$$

In Python we can implement this as a property:

```py
@property
def length(self) -> float:
  return math.sqrt(self.x**2 + self.y**2 + self.z**2)

```
But Python has as well the operator `abs` so it will allow something like `abs(Vector(1, 2, 3))` and this make sense to me. Let's implement that special method:

```py
def __abs__(self):
  return self.length
```

## Unit vector

Vectors are usually used to express direction, but compare vector direction is easier if we ignore the length or _normalize_ the length of the vector to 1. This "special" vector is named _a unit vector_ and there is only one unit vector per vector. In mathematics the unit vector is expressed as _hat vector_ ($\hat{v}$) and it is equal to the vector divided by the length.

$$
\hat{v} = \frac{\vec{v}}{|\ \mathbf{v}\ |}
$$

We have to implement a vector division as well, this is as simple as the multiplication:

```py
def __truediv__(self, other: TNumber) -> TVector:
  return Vector(self.x / other, self.y / other, self.z / other)

@property
def unit(self):
  return self / self.length

```
We don't need to implement the `__rtruediv__` operation, it doesn't make sense to divide a number by a vector.

## Dot product

The [dot product]() of two vectors is basically one of the more important operations in vector maths, it is described as:

$$
\begin{align*}
\mathbf{u} \cdot \mathbf{v} & = \sum_{i=1}^n u_i v_i = u_iv_i + \cdots + u_nv_n
\end{align*}
$$

What we care is the one in the middle. We can write this in Python as:

```py
def dot(other: TVector) -> float:
  return self.x*other.x + self.y*other.y + self.z*other.z

```
I really don't like doing things like `Vector(1, 2, 3).dot(Vector(4, 5, 6))` but gladly in Python 3 we have a dot product or matrix multiplication:

```py
def __matmul__(self, other: TVector) -> float:
  return self.x*other.x + self.y*other.y + self.z*other.z

```
Now we can do `Vector(1, 2, 3) @ Vector(4, 5, 6)`.

## How does it look like?

This is how our full class looks like:

```
import math
from typing import TypeVar

TVector = TypeVar('TVector', bound='Vector')
TNumber = TypeVar('TNumber', int, float)

class Vector:
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self) -> str:
    return f'<Vector {self.x}, {self.y}, {self.z}>'

  def __add__(other: TVector) -> TVector:
    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(other: TVector) -> TVector:
    return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

  def __mul__(other: TNumber) -> TVector:
    return Vector(self.x * other, self.y * other, self.z * other)

  __rmul__ = __mul__

  def __eq__(self, other: TVector) -> bool:
    return self.x == other.x and self.y == other.y and self.z == other.z

  def __truediv__(self, other: TNumber) -> TVector:
    return Vector(self.x / other, self.y / other, self.z / other)

  @property
  def unit(self):
    return self / self.length
  
  @property
  def length(self) -> float:
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)

  def __abs__(self) -> float:
    return self.length

  def __matmul__(self, other: TVector) -> float:
    return self.x*other.x + self.y*other.y + self.z*other.z

```
