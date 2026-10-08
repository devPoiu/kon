# pip install ursina

from ursina import *

app = Ursina()

def create_axis_lines(length=15):
    Entity(model=Mesh(vertices=[(-length, 0, 0), (length, 0, 0)], mode='line'), color=color.red, thickness=3)
    Entity(model=Mesh(vertices=[(0, -length, 0), (0, length, 0)], mode='line'), color=color.green, thickness=3)
    Entity(model=Mesh(vertices=[(0, 0, -length), (0, 0, length)], mode='line'), color=color.blue, thickness=3)

create_axis_lines()


cube = Entity(
    model='cube',
    color=color.rgba(1, 1, 1, 0.4),
    texture='white_cube',
    collider='box',
    position=(0.5, 0.5, 0.5)
)

pos = (-0.5, -0.5, -0.5)

vector_i = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(255, 0, 50),
    scale=(0.5, 0.5, 1.2),
    rotation=(0, 90, 0),
    position=pos,
    origin=(0, 0, -0.5)
)

vector_j = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(0, 255, 50),
    scale=(0.5, 0.5, 1.2),
    rotation=(-90, 0, 0),
    position=pos,
    origin=(0, 0, -0.5)
)

vector_k = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(0, 150, 255),
    scale=(0.5, 0.5, 1.2),
    rotation=(0, 0, 0),
    position=pos,
    origin=(0, 0, -0.5)
)


my_label = Text(text="X: 0.0 Y: 0.0 Z: 0.0", position=(-0.85, 0.45), scale=2, color=color.yellow)

def update():
    rot_speed = 120
    if held_keys['right arrow']:
        cube.rotation_y += time.dt * rot_speed
    if held_keys['left arrow']:
        cube.rotation_y -= time.dt * rot_speed
    if held_keys['up arrow']:
        cube.rotation_x -= time.dt * rot_speed
    if held_keys['down arrow']:
        cube.rotation_x += time.dt * rot_speed

    corner_x = cube.x - 0.5
    corner_y = cube.y - 0.5
    corner_z = cube.z - 0.5
    my_label.text = f"Pos > X: {round(corner_x, 1)} Y: {round(corner_y, 1)} Z: {round(corner_z, 1)}"

def input(key):
    print(key)

    if key == 'd':
        cube.x += 1 
    if key == 'a':
        cube.x -= 1 
    if key == 'w':
        cube.y += 1 
    if key == 's':
        cube.y -= 1
    if key == 'e':
        cube.z += 1
    if key == 'q':
        cube.z -= 1
    if key == 'left mouse down' and mouse.hovered_entity == cube:
        cube.color = color.random_color()

cam = EditorCamera()
cam.position = (5, 5, -10)
cam.rotation = (25, -25, 0)

app.run()
