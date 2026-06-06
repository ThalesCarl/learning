import sys
import vtk
import numpy as np
import pyvista as pv
import time

# Configure pyvista and vtk to suppress errors because I was getting a ennoying
# "Could not set shader program" error and traceback
pv.vtk_verbosity('off')
vtk_output = vtk.vtkOutputWindow.GetInstance()
vtk_output.SetInstance(vtk.vtkStringOutputWindow())

# Constants
GRAVITY = 9.81 # [m/s2]
BOX_HEIGHT = 10.0
BOX_WIDTH = 10.0

def main():
    position = np.array([0.0, 0.0, 0.0])
    velocity = np.array([0.0, 0.0, 0.0])

    pl = pv.Plotter()
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
    
    # Add particle
    circle = pv.Circle(radius=1.0)

    # Save a copy of the original points so we can modify them relatively
    original_points = circle.points.copy()

    pl.add_mesh(circle, color='cyan', show_edges=True, lighting=False)
    pl.view_xy()
    pl.disable_shadows()
    pl.disable_anti_aliasing()
    # pl.show_axes()
    # pl.show_bounds()
    pl.show(interactive_update=True)
    print("Starting endless loop. Close the window to stop.")

    fps = 60.0
    delta_t = 1.0/fps
    frame = 0
    try:
        while True:
            # Check if the user closed the window to break the loop cleanly
            if pl.render_window is None:
                break
            
            # Update velocity and position
            velocity[1] += -1.0 * GRAVITY * delta_t
            position += velocity * delta_t
            
            # Update the geometry points
            circle.points = original_points + position

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

if __name__ == "__main__":
    main()