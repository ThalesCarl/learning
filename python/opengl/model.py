
import numpy as np
import glm

class Triangle:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.shader_program = self.get_shader_program('default')
        self.vbo = self.get_vbo()

    def render(self):
        self.vao = self.get_vao()
        self.vao.render()
    
    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vertex_data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype='f4') # f4 == np.float32
        return vertex_data

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('cube')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()

    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
    
    def get_model_matrix(self):
        m_model = glm.vec4()
        return m_model

    def render(self):
        self.vao.render()
    
    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, -1,-1), (1, -1,-1), (1, 1,-1), (-1, 1,-1)]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (0, 6, 7),
            (6, 5, 4), (4, 7, 7),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[idx] for triangle in indices for idx in triangle]
        return np.array(data, dtype='f4')

    def get_vao(self):
        vertex_data = np.array(vertex_data, dtype='f4') # f4 == np.float32
        return vertex_data

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
