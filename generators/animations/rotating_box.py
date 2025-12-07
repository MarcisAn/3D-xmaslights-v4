from AnimationBuilder import AnimationBuilder
import math


def point_in_rotated_box(point, box_center, box_dims, rotation_deg):
    """
    Check whether a 3D point lies inside a rotated box.

    point        : (x, y, z)
    box_center   : (cx, cy, cz)
    box_dims     : (dx, dy, dz)
    rotation_deg : (rx, ry, rz) Euler angles in degrees
    """

    px, py, pz = point
    cx, cy, cz = box_center
    dx, dy, dz = box_dims
    rx, ry, rz = rotation_deg

    # Convert to radians
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)

    # Translate point into box-centered space
    x = px - cx
    y = py - cy
    z = pz - cz

    # === Inverse rotation (apply rotations in reverse order) ===
    # Because the box is rotated Z→Y→X, the inverse is X⁻¹→Y⁻¹→Z⁻¹

    # Inverse rotate around Z
    cos_z = math.cos(-rz)
    sin_z = math.sin(-rz)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    # Inverse rotate around Y
    cos_y = math.cos(-ry)
    sin_y = math.sin(-ry)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Inverse rotate around X
    cos_x = math.cos(-rx)
    sin_x = math.sin(-rx)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Half extents
    hx, hy, hz = dx / 2, dy / 2, dz / 2

    # Check bounds in box-local space
    return abs(x) <= hx and abs(y) <= hy and abs(z) <= hz


INTERVAL_MS = 15
builder = AnimationBuilder(INTERVAL_MS)

for rotation in range(0,360, 2):
    for i in range(400):
        if point_in_rotated_box(
            (builder.cords[i][0], builder.cords[i][1], builder.cords[i][2]),
            (0, 0, 30),
            (10, 1000, 1000),
            (0,0, rotation),
        ):
            builder.light(i, 255, 0, 0)
        else:
            builder.light(i, 0, 10, 0)
    builder.update()

builder.done()
