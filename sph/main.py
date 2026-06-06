import math
import sys
import vtk
import numpy as np
import pyvista as pv
import time
from dataclasses import dataclass

# Configure pyvista and vtk to suppress errors because I was getting a annoying
# "Could not set shader program" error and traceback
pv.vtk_verbosity('off')
vtk_output = vtk.vtkOutputWindow.GetInstance()
vtk_output.SetInstance(vtk.vtkStringOutputWindow())

# Constants
GRAVITY = 9.81 # [m/s2]
BOX_HEIGHT = 10.0
BOX_WIDTH = 10.0
RADIUS = 0.3
COLLISION_DAMPING = 1.0
NUM_PARTICLES = 5
BETWEEN_PARTICLE_SPACING = 0.0

def main():
    pl = pv.Plotter()

    start_bounding_box(pl)
    # positions: list[np.ndarray] = []
    # velocities: list[np.ndarray] = []
    positions: np.ndarray = np.zeros(shape=(NUM_PARTICLES, 3), dtype=float)
    velocities: np.ndarray = np.zeros(shape=(NUM_PARTICLES, 3), dtype=float)
    circles = start_particles(pl, positions)
    # draw_particles(pl, positions)

    # Save a copy of the original points so we can modify them relatively
    original_points = []
    original_positions = positions.copy()
    for circle in circles:
        original_points.append(circle.points.copy())
    # print(original_points)

    configure_plotter(pl)
    fps = 60.0
    delta_t = 1.0/fps
    frame = 0
    try:
        while True:
            # Check if the user closed the window to break the loop cleanly
            if pl.render_window is None:
                break
            
            update(positions, velocities, delta_t, circles)
            # draw(original_points, circles, positions)
            # print(circles)
            # if frame == 1:
            #     pl.show()
            #     sys.exit()

            # Crucial: Tell PyVista to redraw the scene
            pl.update()

            time.sleep(delta_t)
            frame += 1

    except Exception as e:
        print(f"Loop interrupted: {e}")

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
    # pl.show_axes()
    # pl.show_bounds()
    pl.show(interactive_update=True)
    # pl.show()
    # sys.exit(0)
    print("Starting endless loop. Close the window to stop.")

def start_particles(pl: pv.Plotter, positions: np.ndarray) -> list[pv.PolyData]:
    # Place particles in a grid formation
    particles_per_row = int(math.sqrt(NUM_PARTICLES))
    particles_per_col = int((NUM_PARTICLES - 1) / particles_per_row + 1)
    spacing = 2.0 * RADIUS + BETWEEN_PARTICLE_SPACING

    colors={0: 'red', 1: 'green', 2: 'blue', 3: 'cyan', 4: 'magenta'}
    circles = []
    for i in range(NUM_PARTICLES):
        x = (i % particles_per_row - particles_per_row / 2.0 + 0.5) * spacing
        y = (int(i / particles_per_row) - particles_per_col / 2.0 + 0.5) * spacing
        positions[i][0] = x
        positions[i][1] = y
        circle = pv.Circle(radius=RADIUS, resolution=100)
        # circle.translate(positions[i], inplace=True)
        circle.points += positions[i]
        pl.add_mesh(circle, color=colors[i], show_edges=True, lighting=False)
        circles.append(circle)
    return circles


def update(positions: np.ndarray, velocities: np.ndarray, delta_t: float, circles: list[pv.PolyData]) -> None:
    for (position, velocity, circle) in zip(positions, velocities, circles):
        velocity[1] += -1.0 * GRAVITY * delta_t
        position += velocity * delta_t
        resolve_collisions(position, velocity)

        circle.points += velocity * delta_t
    

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
        
if __name__ == "__main__":
    main()