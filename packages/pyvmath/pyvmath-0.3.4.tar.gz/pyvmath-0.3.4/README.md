pyvmath
--------


C++ extension Vector Mathematics Package for 3D and 2D games.
-------------------------------------------------------------


objects
-----------------------------------------------

vec2

a 2-D vector in array-of-structures format

vec3

a 3-D vector in array-of-structures format

vec4

a 4-D vector in array-of-structures format

quat

quaternion in array-of-structures format

mat22

a 2x2 matrix in array-of-structures format

mat33

a 3x3 matrix in array-of-structures format

mat44

a 4x4 matrix in array-of-structures format



functions
-----------------------------------------------

add

add two vectors or two matrices

c = add(a, b)


sub

sub two vectors or two matrices

c = sub(a, b)


mul

multiply 2 elements

c = mul(a, b)

the following combinations are possible

vector = vector x scalar

matrix = matrix x scalar

vector = matrix x vector (transform vector)

matrix = matrix x matrix

quatanion = quatanion x quatanion

vector = vector * vector (multiply per element)


div

division vector by a scalar

vector = div(vector, scalar)

division vector per element

vector = div(vector, vector)


recip

compute the reciprocal of a vector per element

vector = recip(vector)


sqrt

compute the square root of a vector per element

vector = sqrt(vector)


rsqrt

compute the reciprocal square root of a vector per element

vector = rsqrt(vector)


abs

compute the absolute value of a vector per element

vector = abs(vector)


max

maximum element of a vector

scalar = max(vector)


min

minimum element of a vector

scalar = min(vector)


maxElem

maximum of two vectors per element

vector = matElem(vector,vector)


minElem

minimum of two vectors per element

vector = minElem(vector, vector)


sum

compute the sum of all elements of a vector

scalar = sum(vector)


dot

compute the dot product of two vectors

scalar = dot(vector, vector)


lengthSqr

compute the square of the length of a vector

scalar = lengthSqr(vector)


length

compute the length of a vector

scalar = length(vector)


normalize

normalize a vector

vector = normalize(vector)


cross

compute cross product of two vectors

scalar = cross(vec2, vec2)

vec3 = cross(vec3, vec3)


lerp

linear interpolation between two vectors

vector = lerp(t, vector, vector)  (0<= t <= 1)


slerp

spherical linear interpolation between two vectors

vector = slerp(t, vector, vector)  (0<= t <= 1)


quat_rotation

construct a quaternion

quat = quat_rotation(vec3, vec3)

construct a quaternion to rotate between two unit - length 3D vectors

the result is unpredictable if 2 vectors point in opposite directions

quat = quat_rotation(scalar, vec3)

construct a quaternion to rotate around a unit-length 3D vector

quat = quat_rotation(scalar)

construct a quaternion to rotate around a Z(0,0,1) axis


quat_rotationX

construct a quaternion to rotate around the x axis

quat = quat_rotationX(radian)


quat_rotationY

construct a quaternion to rotate around the y axis

quat = quat_rotationY(radian)


quat_rotationZ

construct a quaternion to rotate around the z axis

quat = quat_rotationZ(radian)


conj

compute the conjugate of a quaternion

quat = conj(quat)


squad

spherical quadrangle interpolation

quat = squad(t,quat, quat, quat, quat)


rotate

use a unit - length quaternion to rotate a 3D vector

vec = rotate(vec, quat)


mat_rotation

construct a matrix to rotate around a unit-length 3D vector

matrix = mat_rotation(radian, dimension, vector)

dimension is 2 or 3 or 4 to output matrix

if you omit vector, Zaxis(0,0,1) will be entered as default


mat_rotationX

construct a matrix to rotate around the Xaxis

matrix = mat_rotationX(radian, dimension)

dimension is 2 or 3 or 4 to output matrix


mat_rotationY

construct a matrix to rotate around the Yaxis

matrix = mat_rotationY(radian, dimension)

dimension is 2 or 3 or 4 to output matrix


mat_rotationZ

construct a matrix to rotate around the Zaxis

matrix = mat_rotationZ(radian, dimension)

dimension is 2 or 3 or 4 to output matrix


mat_rotationZYX

construct a matrix to rotate around the x, y, and z axes

matrix = mat_rotationZYX( (xradian, yradian, zradian) )


mat_identity

construct an identity matrix

matrix = mat_identity(dimension)

dimension is 2 or 3 or 4 to output matrix


mat_scale

construct a matrix to perform scaling

matrix = mat_scale(vector, dimension)

dimension is 2 or 3 or 4 to output matrix


mat_translation

construct a 4x4 matrix to perform translation

matrix = mat_translation(vector)


transpose

transpose of a matrix

matrix = transpose(matrix)


inverse

compute the inverse of a matrix

matrix = inverse(matrix)


orthoInverse

compute the inverse of a 4x4 matrix, which is expected to be an affine matrix with an orthogonal upper-left 3x3 submatrix

this can be used to achieve better performance than a general inverse when the specified 4x4 matrix meets the given restrictions

matrix = orthoInverse(matrix)


determinant

determinant of a matrix

scalar = determinant(matrix)


appendScale

append (post-multiply) a scale transformation to a matrix

faster than creating and multiplying a scale transformation matrix

matrix = appendScale(matrix, vector)


prependScale

prepend (pre-multiply) a scale transformation to a 4x4 matrix

faster than creating and multiplying a scale transformation matrix

matrix = prependScale(matrix, vector)


lookAt

construct viewing matrix based on eye position, position looked at, and up direction

matrix4 = lookAt(eyeVector, lookatVector, upVector)


perspective

construct a perspective projection matrix

matrix4 = perspective(fovyRadians, aspect, zNear, zFar)


frustum

construct a perspective projection matrix based on frustum

matrix4 = frustum(left, right, bottom, top, zNear, zFar)  (all scalar value)


orthographic

construct an orthographic projection matrix

matrix4 = orthographic(left, right, bottom, top, zNear, zFar)  (all scalar value)

