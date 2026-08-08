import math
import inspect
import sys
import vtk
import numpy as np
import pyvista as pv

import random

import time
from dataclasses import dataclass


# Configure pyvista and vtk to suppress errors because I was getting a annoying
# "Could not set shader program" error and traceback
#pv.vtk_verbosity('off')
#vtk_output = vtk.vtkOutputWindow.GetInstance()
#vtk_output.SetInstance(vtk.vtkStringOutputWindow())

# Constants
GRAVITY = 9.81 # [m/s2]
BOX_HEIGHT = 10.0 # [m]
BOX_WIDTH = 10.0 # [m]
RADIUS = 0.1 # [m]
COLLISION_DAMPING = 0.6 # [-]
NUM_PARTICLES = 25 # [-]
BETWEEN_PARTICLE_SPACING = 0.0 # [m]
SMOOTHING_RADIUS = 10.0 # [m]
MASS = 1.0 # [kg]
TARGET_DENSITY = 0.15 # [kg/m2]
PRESSURE_MULTIPLIER = 100.0 # [m4/s2]

DEBUG = False
DISPLAY_INITIAL_CONDITION = False
DISPLAY_FIRST_TIME_ITERATION = False

def main():
    pl = pv.Plotter()

    start_bounding_box(pl)
    # positions: list[np.ndarray] = []
    # velocities: list[np.ndarray] = []
    positions: np.ndarray = np.zeros(shape=(NUM_PARTICLES, 3), dtype=float)
    velocities: np.ndarray = np.zeros(shape=(NUM_PARTICLES, 3), dtype=float)
    densities: np.ndarray = np.zeros(NUM_PARTICLES, dtype=float)
    # draw_particles(pl, positions)

    # fields: properties computed on a cartesian grid
    xx = np.linspace(-0.5 * BOX_WIDTH, 0.5 * BOX_WIDTH, 5)
    yy = np.linspace(-0.5 * BOX_HEIGHT, 0.5 * BOX_HEIGHT, 5)
    density_field = np.zeros((len(xx) , len(yy)))
    pressure_field = np.zeros((len(xx) , len(yy)))

    grid_x, grid_y, grid_z = np.meshgrid(xx, yy, 0.0)

    def update_fields(density_field, pressure_field):
        for j, y in enumerate(yy):
            for i, x in enumerate(xx):
                sample_point = np.array([x, y, 0.0])
                density_field[j, i] = calculate_density(sample_point, positions)
                pressure_field[j, i] = TARGET_DENSITY - density_field[j, i]
                if DEBUG:
                    function_name = inspect.currentframe().f_code.co_name
                    print(f"\n{function_name}")
                    print(f"{sample_point=}, {density_field[j, i]=}, {pressure_field=}")

    update_fields(density_field, pressure_field)
    fields = pv.StructuredGrid(grid_x, grid_y, grid_z)

    fields.point_data["densities"] = density_field.ravel(order="F")
    fields.point_data["pressures"] = density_field.ravel(order="F")

    pl.add_mesh(fields, scalars="densities", cmap="PuOr")

    circles = start_particles_random(pl, positions)

    # Save a copy of the original points so we can modify them relatively
    original_points = []
    original_positions = positions.copy()
    for circle in circles:
        original_points.append(circle.points.copy())
    # print(original_points)

    configure_plotter(pl)
    if DISPLAY_INITIAL_CONDITION:
        pl.show()
        sys.exit()

    fps = 24.0
    delta_t = 1.0/fps
    frame = 0
    try:
        while True:
            # Check if the user closed the window to break the loop cleanly
            if pl.render_window is None:
                break
            
            update_fields(density_field, pressure_field)
            fields.point_data["densities"] = density_field.ravel(order="F")
            fields.point_data["pressures"] = pressure_field.ravel(order="F")
            update(positions, velocities, densities, delta_t, circles)
            if DISPLAY_FIRST_TIME_ITERATION:
                pl.show()
                sys.exit()

            # Crucial: Tell PyVista to redraw the scene
            pl.update()

            time.sleep(delta_t)
            frame += 1

    except Exception as e:
        print(f"Loop interrupted: {e}")
        raise

    finally:
        # Ensure resources are closed out properly if stopped
        pl.close()
        sys.exit()
    
def start_bounding_box(pl: pv.Plotter) -> None:
    # Add bounding box
    box = pv.Quadrilateral(
        [
            [-0.5 * BOX_WIDTH, -0.5 * BOX_HEIGHT, 0.0],
            [0.5 * BOX_WIDTH, -0.5 * BOX_HEIGHT, 0.0],
            [0.5 * BOX_WIDTH, 0.5 * BOX_HEIGHT, 0.0],
            [-0.5 * BOX_WIDTH, 0.5 * BOX_HEIGHT, 0.0],
        ]
    )
    pl.add_mesh(box, color='white', line_width=5.0, show_edges=True, lighting=False)

def configure_plotter(pl: pv.Plotter) -> None:
    pl.view_xy()
    pl.disable_shadows()
    pl.disable_anti_aliasing()
    pl.render_window.SetPosition(1920, 0)
    # pl.show_axes()
    # pl.show_bounds()
    pl.show(interactive_update=True)
    # pl.show()
    # sys.exit(0)
    print("Starting endless loop. Close the window to stop.")


def start_particles_grid(pl: pv.Plotter, positions: np.ndarray) -> list[pv.PolyData]:
    # Place particles in a grid formation
    particles_per_row = int(math.sqrt(NUM_PARTICLES))
    particles_per_col = int((NUM_PARTICLES - 1) / particles_per_row + 1)
    spacing = 2.0 * RADIUS + BETWEEN_PARTICLE_SPACING

    for i in range(NUM_PARTICLES):
        x = (i % particles_per_row - particles_per_row / 2.0 + 0.5) * spacing
        y = (int(i / particles_per_row) - particles_per_col / 2.0 + 0.5) * spacing
        positions[i][0] = x
        positions[i][1] = y

    circles = []
    for i in range(NUM_PARTICLES):
        circle = pv.Circle(radius=RADIUS, resolution=10)
        # circle.translate(positions[i], inplace=True)
        circle.points += positions[i]
        pl.add_mesh(circle, color='black', show_edges=True, lighting=False)
        circles.append(circle)
    return circles


def start_particles_random(pl: pv.Plotter, positions: np.ndarray) -> list[pv.PolyData]:
    random.seed(42)

    for i in range(NUM_PARTICLES):
        x = - 0.5 * BOX_WIDTH + random.random() * BOX_WIDTH
        y = - 0.5 * BOX_HEIGHT + random.random() * BOX_HEIGHT
        positions[i][0] = x
        positions[i][1] = y

    circles = []
    for i in range(NUM_PARTICLES):
        circle = pv.Circle(radius=RADIUS, resolution=10)
        # circle.translate(positions[i], inplace=True)
        circle.points += positions[i]
        pl.add_mesh(circle, color='black', show_edges=True, lighting=False)
        circles.append(circle)
    return circles

def update(positions: np.ndarray, velocities: np.ndarray, densities: np.ndarray, delta_t: float, circles: list[pv.PolyData]) -> None:
    # Serial
    for idx in range(NUM_PARTICLES):
    # for (position, velocity, density, circle) in zip(positions, velocities, densities, circles):
        # velocities[idx][1] += -1.0 * GRAVITY * delta_t # [m/s]
        densities[idx] = calculate_density(positions[idx], positions) # [kg/m2]

        # pressure_force = np.array([0.0, 0.0, 0.0])
        pressure_force = calculate_pressure_force(idx, positions, densities) # [kg.m/s2]

        # Why divide by density instead of mass?
        pressure_acceleration = pressure_force / densities[idx] # [kg.m/s2] * [m2/kg] = [m3/s2]
        velocities[idx] += pressure_acceleration * delta_t # [m3/s] - got wrong units

        positions[idx] += velocities[idx] * delta_t # [m/s] * [s] = [m]
        resolve_collisions(positions[idx], velocities[idx])

        circles[idx].points += velocities[idx] * delta_t
    # Parallel
    

def draw(original_points: list[pv.PolyData], circles: list[pv.PolyData], positions: np.ndarray) -> None:
    # Update the geometry points
    for (orig, circle, position) in zip(original_points, circles, positions):
        print(f"{position=}")
        print(f"{orig=}")
        # circle.points = orig + position
        circle.points += delta_x
        print(f"after {circle.points=}")


def resolve_collisions(position: np.ndarray, velocity: np.ndarray):
    bounds_size = np.array([BOX_WIDTH, BOX_HEIGHT, 0.0])
    half_bounds_size = 0.5 * bounds_size - RADIUS

    if abs(position[0]) > half_bounds_size[0]:
        position[0] = half_bounds_size[0] * np.sign(position[0])
        velocity[0] *= -1.0 * COLLISION_DAMPING

    if abs(position[1]) > half_bounds_size[1]:
        position[1] = half_bounds_size[1] * np.sign(position[1])
        velocity[1] *= -1.0 * COLLISION_DAMPING
        
def smoothing_kernel(dst: float) -> float:
    # value = max(0.0, dst * dst - SMOOTHING_RADIUS * SMOOTHING_RADIUS) # [m2]
    value = max(0.0, SMOOTHING_RADIUS * SMOOTHING_RADIUS - dst * dst) # [m2]

    # Used to normalize the value.
    volume_factor = math.pow(SMOOTHING_RADIUS, 8) * math.pi / 4.0 # [m8]
    if DEBUG:
        function_name = inspect.currentframe().f_code.co_name
        print(f"\n{function_name}")
        print(f"{value=}")
        print(f"{volume_factor=}")

    # It's called volume but in 2D it has a area unit
    return value * value * value / volume_factor  # [1/m2]

def smoothing_kernel_derivative(dst: float) -> float:
    if dst >= SMOOTHING_RADIUS:
        return 0.0
    
    value = max(0.0, SMOOTHING_RADIUS * SMOOTHING_RADIUS - dst * dst) # [m2]
    scale = - 24.0 / (math.pi * math.pow(SMOOTHING_RADIUS, 8)) # [1/m8]
    if DEBUG:
        function_name = inspect.currentframe().f_code.co_name
        print(f"\n{function_name}")
        print(f"{value=}")
        print(f"{scale=}")
    return scale * dst * value * value # [1/m3]



def calculate_density(sample_point: np.ndarray, positions: np.ndarray):
    density = 0.0
    for position in positions:
        dst = np.linalg.norm(position - sample_point) # [m]
        influence = smoothing_kernel(dst) # [1/m2]
        density += MASS * influence # [kg/m2]

        if DEBUG:
            function_name = inspect.currentframe().f_code.co_name
            print(f"\n{function_name}")
            print(f"{sample_point=}")
            print(f"{position=}")
            print(f"{dst=}")
            print(f"{influence=}")
            print(f"{density=}")
    
    return density # [kg/m2]

def calculate_property(sample_point: np.ndarray, positions: np.ndarray, particle_properties: np.ndarray) -> float:
    """General function with SPH method to compute any property"""
    particle_property = 0.0

    for i, position in enumerate(positions):
        dst = np.linalg.norm(sample_point - position)
        influence = smoothing_kernel(dst)
        density = calculate_density(sample_point, positions)
        particle_property += particle_properties[i] * influence * MASS / density

    return particle_property

def calculate_pressure_force(particle_idx: int, positions: np.ndarray, densities: np.ndarray) -> np.ndarray:
    pressure_force = np.array([0.0, 0.0, 0.0])
    sample_point = positions[particle_idx]

    for i, position in enumerate(positions):
        if i == particle_idx:
            continue
        dst = np.linalg.norm(sample_point - position) # [m]
        direction = np.array([random.random(), random.random(), 0.0]) # FIXME change to random direction
        if dst > 1.0e-3:
            direction = (sample_point - position) / dst
        density = densities[i] # [kg/m2]
        slope = smoothing_kernel_derivative(dst) # [1/m3]
        pressure_factor = calculate_pressure_factor(density) # [kg/m2.s2]
        if density < 1.0e-6:
            continue
        pressure_force +=  direction * pressure_factor * slope *  MASS / density # [kg/m2.s2] * [1/m3] * [kg] * [m2/kg]
        if DEBUG:
            function_name = inspect.currentframe().f_code.co_name
            print(f"\n{function_name}")
            print(f"{sample_point=}")
            print(f"{position=}")
            print(f"{dst=}")
            print(f"{density=}")
            print(f"{slope=}")
            print(f"{pressure_factor=}")
            print(f"{pressure_force=}")
    


    return pressure_force # [kg.m/s2]

def calculate_pressure_factor(density: float) -> float:
    density_error = density - TARGET_DENSITY # [kg/m2]
    pressure_factor = PRESSURE_MULTIPLIER * density_error # [m4/s2] * [kg/m2]
    return pressure_factor # [kg/m2.s2]

    

if __name__ == "__main__":
    main()
