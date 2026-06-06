import sys
import vtk
import numpy as np
import pyvista as pv
import time

# Configure pyvista and vtk to suppress errors because I was getting a annoying
# "Could not set shader program" error and traceback
pv.vtk_verbosity('off')
vtk_output = vtk.vtkOutputWindow.GetInstance()
vtk_output.SetInstance(vtk.vtkStringOutputWindow())

# Constants
GRAVITY = 9.81 # [m/s2]
BOX_HEIGHT = 10.0
BOX_WIDTH = 10.0
RADIUS = 1.0
COLLISION_DAMPING = 0.8

def main():
    position = np.array([0.0, 0.0, 0.0])
    velocity = np.array([0.0, 0.0, 0.0])

    pl = pv.Plotter()
    start_bounding_box(pl)
    circle = start_particles(pl)

    # Save a copy of the original points so we can modify them relatively
    original_points = circle.points.copy()

    configure_plotter(pl)
    fps = 60.0
    delta_t = 1.0/fps
    frame = 0
    try:
        while True:
            # Check if the user closed the window to break the loop cleanly
            if pl.render_window is None:
                break
            
            update(position, velocity, delta_t)
            draw(original_points, circle, position)

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
    print("Starting endless loop. Close the window to stop.")

def start_particles(pl: pv.Plotter) -> pv.PolyData:
    # Add particle
    circle = pv.Circle(radius=RADIUS)

    pl.add_mesh(circle, color='cyan', show_edges=True, lighting=False)
    return circle

def update(position: np.ndarray, velocity: np.ndarray, delta_t: float) -> None:
    # Update velocity and position
    velocity[1] += -1.0 * GRAVITY * delta_t
    position += velocity * delta_t
    resolve_collisions(position, velocity)
    

def draw(original_points: pv.PolyData, circle: pv.PolyData, position: np.ndarray) -> None:
    # Update the geometry points
    circle.points = original_points + position


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