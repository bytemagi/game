MULTIPLIERS = [
    (1,  0,  0,  1),
    (0,  1,  1,  0),
    (-1, 0,  0,  1),
    (0, -1,  1,  0),
    (-1, 0,  0, -1),
    (0, -1, -1,  0),
    (1,  0,  0, -1),
    (0,  1, -1,  0),
]

def compute_fov(tiles, ox, oy, radius, map_w, map_h):
    visible = set()
    visible.add((ox, oy))
    for xx, xy, yx, yy in MULTIPLIERS:
        _cast_light(tiles, visible, ox, oy, radius, 1, 1.0, 0.0, xx, xy, yx, yy, map_w, map_h)
    return visible

def _cast_light(tiles, visible, ox, oy, radius, row, start, end, xx, xy, yx, yy, map_w, map_h):
    if start < end:
        return
    blocked = False
    for j in range(row, radius + 1):
        if blocked:
            break
        dy = -j
        for dx in range(-j, 1):
            l_slope = (dx - 0.5) / (dy + 0.5)
            r_slope = (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            if end > l_slope:
                break
            tx = ox + dx * xx + dy * xy
            ty = oy + dx * yx + dy * yy
            if 0 <= tx < map_w and 0 <= ty < map_h:
                if dx * dx + dy * dy <= radius * radius:
                    visible.add((tx, ty))
                is_wall = tiles[ty][tx] == "wall"
                if blocked:
                    if is_wall:
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if is_wall and j < radius:
                        blocked = True
                        _cast_light(tiles, visible, ox, oy, radius, j + 1, start, l_slope,
                                    xx, xy, yx, yy, map_w, map_h)
                        new_start = r_slope
        if blocked:
            break
