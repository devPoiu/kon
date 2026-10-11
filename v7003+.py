from ursina import *

app = Ursina()

window.color = color.rgb(200, 200, 200)

def create_axis_lines(length=15, tick_size=0.1):
    Entity(model=Mesh(vertices=[(-length, 0, 0), (length, 0, 0)], mode='line'), color=color.red, thickness=3)
    Entity(model=Mesh(vertices=[(0, -length, 0), (0, length, 0)], mode='line'), color=color.green, thickness=3)
    Entity(model=Mesh(vertices=[(0, 0, -length), (0, 0, length)], mode='line'), color=color.blue, thickness=3)

    tolch = 0.0075
    for i in range(-length, length + 1):
        if i == 0: continue
        Entity(model='cube', position=(i, 0, 0), scale=(tolch, tick_size * 2, tolch), color=color.red)
        Entity(model='cube', position=(0, i, 0), scale=(tick_size * 2, tolch, tolch), color=color.green)
        Entity(model='cube', position=(0, 0, i), scale=(tick_size * 2, tolch, tolch), color=color.blue)

create_axis_lines()

# Главный Pivot-объект
cube = Entity(position=(0, 0, 0), rotation=(0, 0, 0))

# Векторы базиса теперь строятся через динамический Mesh (линии), 
# так как при произвольной матрице (например, скосе) стрелки должны наклоняться, а не просто вращаться.
vector_i_mesh = Entity(model=Mesh(mode='line'), color=color.red, thickness=7)
vector_j_mesh = Entity(model=Mesh(mode='line'), color=color.green, thickness=7)
vector_k_mesh = Entity(model=Mesh(mode='line'), color=color.blue, thickness=7)

# Полупрозрачные грани фигуры параллелепипеда
ploscost = Entity(
    model=Mesh(), 
    color=color.rgba(1, 1, 1, 0.5), 
    texture='white_cube'
)
# Отключаем скрытие внутренних граней, чтобы фигура была видна со всех сторон
ploscost.two_sided = True 

# Проволочный каркас ребер
rebra = Entity(model=Mesh(mode='line'), color=color.rgb(40, 40, 40), thickness=3)

hud = Text(text="", position=(-0.85, 0.45), scale=1.5, color=color.black)

matrix_fields = []
start_x, start_y = 0.6, 0.40
step_x, step_y = 0.11, 0.06

# Изначально задаем базисные векторы
# Локальные векторы трансформации относительно объекта cube
local_i = Vec3(1, 0, 0)
local_j = Vec3(0, 3, 0)
local_k = Vec3(0, 0, 2)

default_matrix = [
    ["1.00", "0.00", "0.00"],
    ["0.00", "3.00", "0.00"],
    ["0.00", "0.00", "2.00"]
]

for r in range(4):
    row_fields = []
    for c in range(3):
        if r == 0:
            names = ["i", "j", "k"]
            q = Text(text=names[c], position=(start_x + c * step_x, start_y - r * step_y), color=color.black)
            row_fields.append(q)
            continue
        f = InputField(
            default_value=default_matrix[r-1][c], 
            position=(start_x + c * step_x, start_y - r * step_y), 
            scale=(0.1, 0.04)
        )
        f.character_limit = 6
        row_fields.append(f)
    matrix_fields.append(row_fields)

def update_ui_fields(i_vec, j_vec, k_vec):
    for r in range(1, 4):
        for c in range(3):
            if matrix_fields[r][c].active: 
                return 

    vectors = [i_vec, j_vec, k_vec]
    for r in range(1, 4):
        for c in range(3):
            val = vectors[c][r-1]
            matrix_fields[r][c].text = f"{val:.2f}"

def apply_matrix():
    try:
        global local_i, local_j, local_k
        local_i = Vec3(float(matrix_fields[1][0].text), float(matrix_fields[2][0].text), float(matrix_fields[3][0].text))
        local_j = Vec3(float(matrix_fields[1][1].text), float(matrix_fields[2][1].text), float(matrix_fields[3][1].text))
        local_k = Vec3(float(matrix_fields[1][2].text), float(matrix_fields[2][2].text), float(matrix_fields[3][2].text))
    except ValueError:
        pass

apply_btn = Button(
    text="ok", 
    position=(start_x + step_x, start_y - 4 * step_y), 
    scale=(0.2, 0.04), 
    color=color.azure,
    on_click=apply_matrix
)

def update():
    global local_i, local_j, local_k
    
    typing = False
    for r in range(1, 4):
        for c in range(3):
            if matrix_fields[r][c].active:
                typing = True

    # Управление вращением контейнера конструкции
    if not typing:
        rot_speed = 120
        if held_keys['q']: cube.rotation_z -= time.dt * rot_speed
        if held_keys['e']: cube.rotation_z += time.dt * rot_speed
        if held_keys['right arrow']: cube.rotation_y += time.dt * rot_speed
        if held_keys['left arrow']: cube.rotation_y -= time.dt * rot_speed
        if held_keys['up arrow']: cube.rotation_x -= time.dt * rot_speed
        if held_keys['down arrow']: cube.rotation_x += time.dt * rot_speed

    # Рассчитываем положение векторов в мировом пространстве с учетом вращения cube
    i_world = cube.right * local_i.x + cube.up * local_i.y + cube.forward * local_i.z
    j_world = cube.right * local_j.x + cube.up * local_j.y + cube.forward * local_j.z
    k_world = cube.right * local_k.x + cube.up * local_k.y + cube.forward * local_k.z

    hud.text = (
        f"Transformed Basis Vectors:\n"
        f"i: [{i_world.x:6.2f}, {i_world.y:6.2f}, {i_world.z:6.2f}]\n"
        f"j: [{j_world.x:6.2f}, {j_world.y:6.2f}, {j_world.z:6.2f}]\n"
        f"k: [{k_world.x:6.2f}, {k_world.y:6.2f}, {k_world.z:6.2f}]"
    )

    if not typing:
        update_ui_fields(i_world, j_world, k_world)

    # Строим вершины параллелепипеда в мировых координатах от текущей позиции cube
    O = cube.position 
    v0 = O
    v1 = O + k_world   # Направление k
    v2 = O + j_world   # Направление j
    v3 = O + j_world + k_world
    v4 = O + i_world   # Направление i
    v5 = O + i_world + k_world
    v6 = O + i_world + j_world
    v7 = O + i_world + j_world + k_world

    # Пересобираем визуальные оси-векторы как утолщенные 3D-линии от начала координат
    vector_i_mesh.model.vertices = [v0, v4]
    vector_i_mesh.model.generate()
    
    vector_j_mesh.model.vertices = [v0, v2]
    vector_j_mesh.model.generate()
    
    vector_k_mesh.model.vertices = [v0, v1]
    vector_k_mesh.model.generate()

    # 8 уникальных вершин структуры параллелепипеда
    unique_vertices = [v0, v1, v2, v3, v4, v5, v6, v7]

    # Для корректного наложения текстур и объема разворачиваем куб по 4 вершины на грань (всего 24 вершины)
    # Это решает проблему искажения освещения и невидимости граней
    explicit_vertices = [
        v0, v4, v6, v2,  # Задняя грань
        v1, v3, v7, v5,  # Передняя грань
        v0, v1, v5, v4,  # Нижняя грань
        v2, v6, v7, v3,  # Верхняя грань
        v0, v2, v3, v1,  # Левая грань
        v4, v5, v7, v6   # Правая грань
    ]

    triangles_indices = [
        0, 1, 2,     0, 2, 3,
        4, 5, 6,     4, 6, 7,
        8, 9, 10,    8, 10, 11,
        12, 13, 14,  12, 14, 15,
        16, 17, 18,  16, 18, 19,
        20, 21, 22,  20, 22, 23
    ]

    # Стандартная UV-карта для кубической развертки белой текстуры
    uv_coords = [(0,0), (1,0), (1,1), (0,1)] * 6

    # Назначение геометрии плоскостям объема
    ploscost.model.vertices = explicit_vertices
    ploscost.model.triangles = triangles_indices
    # ploscost.model.uvs = uv_coords
    ploscost.model.generate()

    # Каркасная сетка ребер (12 линий связей между 8 вершинами)
    lines_indices = [
        0,1,  1,3,  3,2,  2,0,  # Заднее кольцо
        4,5,  5,7,  7,6,  6,4,  # Переднее кольцо
        0,4,  1,5,  2,6,  3,7   # Соединительные ребра
    ]

    rebra.model.vertices = unique_vertices
    rebra.model.triangles = lines_indices
    rebra.model.generate()

def reset_cube():
    global local_i, local_j, local_k
    cube.position = (0, 0, 0)
    cube.rotation = (0, 0, 0)
    local_i, local_j, local_k = Vec3(1,0,0), Vec3(0,3,0), Vec3(0,0,2)
    for r in range(1, 4):
        for c in range(3):
            matrix_fields[r][c].text = default_matrix[r-1][c]

def input(key):
    for r in range(1, 4):
        for c in range(3):
            if matrix_fields[r][c].active: return

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
