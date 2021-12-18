from dataclasses import dataclass

def make_rocket_go_now(area, steps):
    # try a bunch of trajectories
    valid_dx = find_valid_x_trajs(area)
    print(f"Found {len(valid_dx)} valid x trajectories.")
    count = 0
    batch_size = 100
    max_y = 0
    while count < steps:
        dy_min, dy_max = count*batch_size+1, (count+1)*batch_size+1
        print(f"Trying y trajectories {dy_min}-{dy_max}...")
        valid_dy = find_valid_y_trajs(area, dy_min, dy_max)
        for dx in valid_dx:
            for dy in valid_dy:
                hit, highest_y = fire(dx, dy, area)
                if hit and highest_y > max_y:
                    print(f"New high {highest_y} with trajectory ({dx},{dy})")
                    max_y = highest_y
        count += 1


def fire(_dx, _dy, area):
    dx, dy = _dx, _dy
    pos = (0,0)
    highest_y = 0
    while not area.inside(pos[0], pos[1]) and not area.beyond(pos[0], pos[1]):
        pos = (pos[0]+dx, pos[1]+dy)
        if pos[1] > highest_y:
            highest_y = pos[1]
        if dx != 0:
            dx += -1 if dx > 0 else 1
        dy -= 1
    return area.inside(pos[0], pos[1]), highest_y


def fire_x(_dx, area):
    dx = _dx
    pos = 0
    while not area.xmax >= pos >= area.xmin and not pos > area.xmax and dx != 0:
        pos += dx
        if dx != 0:
            dx += -1 if dx > 0 else 1
    return area.xmax >= pos >= area.xmin

def fire_y(_dy, area):
    dy = _dy
    pos = 0
    while not area.ymax >= pos >= area.ymin and not pos < area.ymin:
        pos += dy
        dy -= 1
    return area.ymax >= pos >= area.ymin

def find_valid_x_trajs(area):
    valid_dx = []
    for dx in range(1, area.xmax + 1):
        if fire_x(dx, area):
            valid_dx.append(dx)
    return valid_dx

def find_valid_y_trajs(area, dy_min, dy_max):
    valid_dy = []
    for dy in range(dy_min, dy_max):
        if fire_y(dy, area):
            valid_dy.append(dy)
    return valid_dy


@dataclass
class Area:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def inside(self, x, y):
        return self.xmax >= x >= self.xmin and self.ymax >= y >= self.ymin

    def beyond(self, x, y):
        return x > self.xmax or y < self.ymin

if __name__ == "__main__":
    # area = Area(20, 30, -10, -5)
    area = Area(29, 73, -248, -194)
    make_rocket_go_now(area, 20)