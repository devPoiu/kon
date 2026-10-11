# pip install ursina
from ursina import *

app = Ursina()

window.color = color.rgb(200, 200, 200)

def create_axis_lines(length=15, tick_size=0.1):
    Entity(model=Mesh(vertices=[(-length, 0, 0), (length, 0, 0)], mode='line'), color=color.red, thickness=3)
    Entity(model=Mesh(vertices=[(0, -length, 0), (0, length, 0)], mode='line'), color=color.green, thickness=3)
    Entity(model=Mesh(vertices=[(0, 0, -length), (0, 0, length)], mode='line'), color=color.blue, thickness=3)

    tolch = 0.0075

    for i in range(-length, length + 1):
        if i == 0:
            continue
        
        Entity(model='cube', position=(i, 0, 0), scale=(tolch, tick_size * 2, tolch), color=color.red)
        Entity(model='cube', position=(0, i, 0), scale=(tick_size * 2, tolch, tolch), color=color.green)
        Entity(model='cube', position=(0, 0, i), scale=(tick_size * 2, tolch, tolch), color=color.blue)

create_axis_lines()

vectorLength = (1, 2, 3)
# Опорный объект (Pivot), к которому привязано все вращение и перемещение
cube = Entity(
    position=(0, 0, 0),
    scale=(1, 1, 1)
)

# 1. Полупрозрачные грани параллелепипеда
volume_mesh = Entity(
    parent=cube,
    model=Mesh(),
    color=color.rgba(1, 1, 1, 0.4),
    texture='white_cube'
)

# 2. Каркасная сетка (wireframe) ребер фигуры
wireframe_mesh = Entity(
    parent=cube,
    model=Mesh(mode='line'),
    color=color.rgb(60, 60, 60),
    thickness=2
)

# 3. Базисные векторы, построенные в виде толстых 3D-линий через кастомный Mesh
vector_i_mesh = Entity(parent=cube, model=Mesh(mode='line'), color=color.red, thickness=5)
vector_j_mesh = Entity(parent=cube, model=Mesh(mode='line'), color=color.green, thickness=5)
vector_k_mesh = Entity(parent=cube, model=Mesh(mode='line'), color=color.blue, thickness=5)

# --- МАТРИЧНЫЙ ИНТЕРФЕЙС ВВОДА/ВЫВОДА ---
matrix_fields = []
start_x, start_y = 0.50, 0.40
step_x, step_y = 0.11, 0.06

default_matrix = [
    ["1.00", "0.00", "0.00"],
    ["0.00", "2.00", "0.00"],
    ["0.00", "0.00", "3.00"]
]

Text(text="Transformation Matrix (3x3):", position=(start_x, start_y + 0.06), color=color.black)

for r in range(3):
    row_fields = []
    for c in range(3):
        f = InputField(
            default_value=default_matrix[r][c], 
            position=(start_x + c * step_x, start_y - r * step_y), 
            scale=(0.09, 0.04)
        )
        f.character_limit = 6
        row_fields.append(f)
    matrix_fields.append(row_fields)

# Локальные векторы трансформации фигуры (внутри Pivot объекта cube)
# Фигура строится от локального нуля (0, 0, 0) наружу
local_i = Vec3(1, 0, 0)
local_j = Vec3(0, 2, 0)
local_k = Vec3(0, 0, 3)

def update_volume_geometry():
    """Перестраивает вершины параллелепипеда, контуров и векторов от точки (0,0,0)"""
    v0 = Vec3(0, 0, 0)
    v1 = local_k
    v2 = local_j
    v3 = local_j + local_k
    v4 = local_i
    v5 = local_i + local_k
    v6 = local_i + local_j
    v7 = local_i + local_j + local_k

    # Обновляем грани меша параллелепипеда
    volume_mesh.model.vertices = [
        v0, v4, v6, v2,  # Сзади
        v1, v3, v7, v5,  # Спереди
        v0, v1, v5, v4,  # Снизу
        v2, v6, v7, v3,  # Сверху
        v0, v2, v3, v1,  # Слева
        v4, v5, v7, v6   # Справа
    ]
    volume_mesh.model.triangles = [
        0, 1, 2,  0, 2, 3,
        4, 5, 6,  4, 6, 7,
        8, 9, 10, 8, 10, 11,
        12, 13, 14, 12, 14, 15,
        16, 17, 18, 16, 18, 19,
        20, 21, 22, 20, 22, 23
    ]
    volume_mesh.model.uvs = [(0,0), (1,0), (1,1), (0,1)] * 6
    volume_mesh.model.generate()

    # Обновляем линии ребер каркаса параллелепипеда (12 ребер)
    wireframe_mesh.model.vertices = [
        v0, v4,  v4, v6,  v6, v2,  v2, v0,
        v1, v5,  v5, v7,  v7, v3,  v3, v1,
        v0, v1,  v4, v5,  v6, v7,  v2, v3
    ]
    wireframe_mesh.model.generate()

    # Обновляем векторы. Строим их математически от (0,0,0) до вершин осей
    vector_i_mesh.model.vertices = [v0, v4]
    vector_i_mesh.model.generate()

    vector_j_mesh.model.vertices = [v0, v2]
    vector_j_mesh.model.generate()

    vector_k_mesh.model.vertices = [v0, v1]
    vector_k_mesh.model.generate()

def apply_matrix_to_cube():
    """Считывает значения из ячеек UI-матрицы и применяет их к локальной геометрии сцены"""
    global local_i, local_j, local_k
    try:
        # Считывание по столбцам: 1-й столбец -> вектор i, 2-й -> j, 3-й -> k
        local_i = Vec3(float(matrix_fields[0][0].text), float(matrix_fields[1][0].text), float(matrix_fields[2][0].text))
        local_j = Vec3(float(matrix_fields[0][1].text), float(matrix_fields[1][1].text), float(matrix_fields[2][1].text))
        local_k = Vec3(float(matrix_fields[0][2].text), float(matrix_fields[1][2].text), float(matrix_fields[2][2].text))
        
        # Перерисовываем всю геометрию
        update_volume_geometry()
        
    except (ValueError, ZeroDivisionError):
        pass

apply_btn = Button(
    text="Apply Matrix", 
    position=(start_x + step_x, start_y - 3 * step_y), 
    scale=(0.2, 0.04), 
    color=color.azure,
    on_click=apply_matrix_to_cube
)

def is_any_field_active():
    for row in matrix_fields:
        for f in row:
            if f.active: return True
    return False

def update():
    global local_i, local_j, local_k
    rot_speed = 120
    # Вращение всей конструкции клавишами
    if held_keys['q']: cube.rotation_z -= time.dt * rot_speed
    if held_keys['e']: cube.rotation_z += time.dt * rot_speed
    if held_keys['right arrow']: cube.rotation_y += time.dt * rot_speed
    if held_keys['left arrow']: cube.rotation_y -= time.dt * rot_speed
    if held_keys['up arrow']: cube.rotation_x -= time.dt * rot_speed
    if held_keys['down arrow']: cube.rotation_x += time.dt * rot_speed

    # Вычисляем мировые координаты векторов (с учетом вращения cube)
    i_world = cube.right * local_i.x + cube.up * local_i.y + cube.forward * local_i.z
    j_world = cube.right * local_j.x + cube.up * local_j.y + cube.forward * local_j.z
    k_world = cube.right * local_k.x + cube.up * local_k.y + cube.forward * local_k.z

    # Если мы не редактируем инпуты, они работают как HUD и показывают координаты мировых векторов
    if not is_any_field_active():
        matrix_values = [
            [i_world.x, j_world.x, k_world.x],
            [i_world.y, j_world.y, k_world.y],
            [i_world.z, j_world.z, k_world.z]
        ]
        for r in range(3):
            for c in range(3):
                matrix_fields[r][c].text = f"{matrix_values[r][c]:.2f}"

def reset_cube():
    global local_i, local_j, local_k
    cube.rotation = (0, 0, 0)
    cube.position = (0, 0, 0)
    local_i, local_j, local_k = Vec3(1,0,0), Vec3(0,2,0), Vec3(0,0,3)
    update_volume_geometry()
    
    for r in range(3):
        for c in range(3):
            matrix_fields[r][c].text = default_matrix[r][c]

def input(key):
    if is_any_field_active(): return
    print(key)
    # Перемещение всей конструкции в пространстве
    if key == 'j': cube.x += 1 
    if key == 'g': cube.x -= 1 
    if key == 'y': cube.y += 1 
    if key == 'h': cube.y -= 1
    if key == 'u': cube.z += 1
    if key == 't': cube.z -= 1
    if key == 'r': reset_cube()

# Инициализируем всю графическую сцену при старте
apply_matrix_to_cube()

cam = EditorCamera()
cam.position = (5, 5, -10)
cam.rotation = (25, -25, 0)

app.run()
