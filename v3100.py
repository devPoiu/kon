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

pos = Vec3(-0.5, -0.5, -0.5)
vectorLength = 0.85

vector_i = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(255, 0, 0),
    scale=vectorLength,
    rotation=(-90, 0, 0),
    position=pos,
    origin=(-0.5, 0, 0)
)

vector_j = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(0, 255, 0),
    scale=vectorLength,
    rotation=(0, 0, -90),
    position=pos,
    origin=(-0.5, 0, 0)
)

vector_k = Entity(
    parent=cube,
    model='arrow',
    color=color.rgb(0, 0, 255),
    scale=vectorLength,
    rotation=(0, -90, 0),
    position=pos,
    origin=(-0.5, 0, 0)
)

my_label = Text(
    text="", 
    position=(-0.85, 0.45), 
    scale=1.5, 
    color=color.yellow
)

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

    i_vec = cube.right
    j_vec = cube.up
    k_vec = cube.forward

    matrix_text = (
        f"i (X): [{i_vec.x:6.2f}, {i_vec.y:6.2f}, {i_vec.z:6.2f}]\n"
        f"j (Y): [{j_vec.x:6.2f}, {j_vec.y:6.2f}, {j_vec.z:6.2f}]\n"
        f"k (Z): [{k_vec.x:6.2f}, {k_vec.y:6.2f}, {k_vec.z:6.2f}]"
    )
    
    my_label.text = matrix_text

def reset_cube():
    cube.position = (0.5, 0.5, 0.5)
    cube.rotation = (0, 0, 0)


def input(key):
    print(key)

    if key == 'j': cube.x += 1 
    if key == 'g': cube.x -= 1 
    if key == 'y': cube.y += 1 
    if key == 'h': cube.y -= 1
    if key == 'u': cube.z += 1
    if key == 't': cube.z -= 1
    if key == 'r': reset_cube()

cam = EditorCamera()
cam.position = (5, 5, -10)
cam.rotation = (25, -25, 0)

app.run()
