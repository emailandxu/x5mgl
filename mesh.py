import numpy as np
import pymeshlab as pml

class Mesh():
    def __init__(self, vertices, faces, normals) -> None:
        self.vertices, self.faces, self.normals = vertices, faces, normals

    @classmethod
    def load(cls, path):
        ms = pml.MeshSet()
        ms.load_new_mesh(path)
        m = ms.current_mesh()
        return cls.from_pml_mesh(m)
    
    @classmethod
    def from_pml_mesh(cls, m):
        vertices, faces, normals = m.vertex_matrix(), m.face_matrix(), m.vertex_normal_matrix()
        vertices, _, _ = cls.unit_size(vertices)
        vertices, faces, normals = vertices.astype(np.float32).copy(), faces.astype(np.int32).copy(), normals.astype(np.float32).copy()
        return cls(vertices, faces, normals)

    def reduce(self, target=2000, optimalplacement=True):
        m = pml.Mesh(self.vertices, self.faces, )
        ms = pml.MeshSet()
        ms.add_mesh(m, 'mesh')
        ms.meshing_decimation_quadric_edge_collapse(targetfacenum=int(target), optimalplacement=optimalplacement)
        return self.__class__.from_pml_mesh(ms.current_mesh())

    @classmethod
    def aabb(cls, vertices):
        return np.min(vertices, axis=0), np.max(vertices, axis=0)

    @classmethod
    def unit_size(cls, vertices):
        vmin, vmax = cls.aabb(vertices)
        scale = 2 / np.max(vmax - vmin).item()
        offset = -(vmax + vmin) / 2
        print(f"unit size the mesh: scale:{scale}, offset - {offset}")
        vertices = vertices + offset # Center mesh on origin
        vertices = vertices * scale
        return vertices, offset, scale

    def create_vao(self, ctx, prog, texcoords=None):
        vertices, faces, normals = self.vertices, self.faces, self.normals 
        vbo = ctx.buffer(vertices)
        cbo = ctx.buffer(np.ones_like(vertices, dtype=np.float32))
        ibo = ctx.buffer(faces)
        nbo = ctx.buffer(normals)
        vao = ctx.vertex_array(prog, [ (vbo, "3f", "in_position"), (cbo, "3f", "in_color"), (nbo, "3f", "in_normal"), ], ibo)
        return vao
    
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # 创建一些随机顶点
    mesh = Mesh.load("resources/bunny/bunny.obj")
    
    vertices = mesh.reduce(1000, True).vertices

    # 创建3D图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    # 使用scatter来绘制顶点
    ax.scatter(vertices[..., 0], vertices[..., 1], vertices[..., 2])

    # 设置轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

