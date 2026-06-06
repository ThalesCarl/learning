from pyvista import examples

print("wake up, Neo")
mesh = examples.download_bunny()
mesh.plot(cpos='xy')