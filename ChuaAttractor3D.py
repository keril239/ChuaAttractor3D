from manim import *

class TestChuaAttractor3D(ThreeDScene):
    def construct(self):
        # Добавляем оси
        axes = ThreeDAxes(
            x_range=[-10, 10],
            y_range=[-10, 10],
            z_range=[-6, 6],
            x_length=10,
            y_length=10,
            z_length=6
        )
        self.add(axes)

        # Устанавливаем ориентацию камеры
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Начинаем вращение камеры
        self.begin_ambient_camera_rotation(rate=0.1)

        # Начальные условия для системы Чуа
        x, y, z = 0.1, 0, 0
        a, b, m0, m1 = 15.6, 28, -1.143, -0.714
        dt = 0.001
        num_steps = 10000

        def f(x):
            return m1 * x + 0.5 * (m0 - m1) * (abs(x + 1) - abs(x - 1))

        # Массив для хранения точек траектории
        trajectory_points = []

        # Численное интегрирование системы Чуа
        for _ in range(num_steps):
            dx = (a * (y - x - f(x))) * dt
            dy = (x - y + z) * dt
            dz = -b * y * dt

            x += dx
            y += dy
            z += dz

            trajectory_points.append([x, y, z])

        # Создаем траекторию как параметрическую функцию
        trajectory_curve = ParametricFunction(
            lambda t: trajectory_points[int(t * (num_steps - 1))],
            t_range=[0, 1],
            color=RED
        )

        # Анимация для создания траектории
        self.play(Create(trajectory_curve), run_time=10, rate_func=linear)

        '''
        # Создаем точку, которая будет двигаться по траектории
        moving_dot = Dot3D(point=trajectory_points[0], radius=0.1, color=YELLOW)
        self.add(moving_dot)

        # Анимация точки вдоль траектории
        self.play(MoveAlongPath(moving_dot, trajectory_curve), run_time=5, rate_func=linear)
        '''

class ChuaAttractor3D(ThreeDScene):
    def construct(self):
        # Добавляем оси
        axes = ThreeDAxes(
            x_range=[-10, 10],
            y_range=[-10, 10],
            z_range=[-6, 6],
            x_length=10,
            y_length=10,
            z_length=6
        )
        self.add(axes)

        # Устанавливаем ориентацию камеры
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Начинаем вращение камеры
        self.begin_ambient_camera_rotation(rate=0.1)

        # Начальные условия для системы Чуа
        a, b, m0, m1 = 15.6, 28, -1.143, -0.714
        dt = 0.001
        num_steps = 10000

        def f(x):
            return m1 * x + 0.5 * (m0 - m1) * (abs(x + 1) - abs(x - 1))
        
        # Функция для численного интегрирования системы Чуа
        def chua_trajectory(x_start, y_start, z_start):
            x, y, z = x_start, y_start, z_start
            trajectory_points = []

            for _ in range(num_steps):
                dx = (a * (y - x - f(x))) * dt
                dy = (x - y + z) * dt
                dz = -b * y * dt

                x += dx
                y += dy
                z += dz

                trajectory_points.append([x, y, z])
            return trajectory_points

        # Список начальных условий для нескольких траекторий
        initial_conditions = [
            (0.1, 0, 0),
            (0.2, 0, 0),
            (0.1, 0, 0.2),
            (0.2, 0, 0.1)
        ]

        # Список цветов для разных траекторий
        colors = [RED, BLUE, GREEN, YELLOW]

        # Список для хранения всех траекторий
        trajectories = []

        for i, (x0, y0, z0) in enumerate(initial_conditions):
            trajectory_points = chua_trajectory(x0, y0, z0)

            # Создаем траекторию как параметрическую функцию
            trajectory_curve = ParametricFunction(
                lambda t, trajectory_points=trajectory_points: trajectory_points[int(t * (num_steps - 1))],
                t_range=[0, 1],
                color=colors[i]
            )

            trajectories.append(trajectory_curve)

        # Анимация для создания всех траекторий
        self.play(*[Create(trajectory) for trajectory in trajectories], run_time=10, rate_func=linear)