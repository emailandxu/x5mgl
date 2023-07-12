import numpy as np
from scipy.spatial.transform import Rotation

def scale(value):
    mat = np.identity(4, dtype=np.float32) * value
    mat[-1, -1] = 1
    return mat

def scaleXYZ(xyz):
    mat = np.identity(4, dtype=np.float32)
    for idx, value in enumerate(xyz):
        mat[idx, idx] = value
    return mat

def rotate(euler, sequence="xyz"):
    return to_mat(euler, type="euler", sequence=sequence)

def translate(trans):
    mat = np.identity(4, dtype=np.float32)
    mat[:3, 3] = trans
    return mat

def to_euler(mat, sequence="xyz"):
    if mat.shape == (4,4):
        return Rotation.from_matrix(mat[:3,:3]).as_euler(sequence, degrees=False)
    else:
        return Rotation.from_matrix(mat).as_euler(sequence, degrees=False)

def to_quat(mat):
    if mat.shape == (4,4):
        return Rotation.from_matrix(mat[:3,:3]).as_quat()
    else:
        return Rotation.from_matrix(mat).as_quat()

def to_mat(rot, type="euler", sequence="xyz"):
    mat = np.identity(4, dtype=np.float32)
    if type=="euler":
        mat[:3,:3] = Rotation.from_euler(sequence, rot, degrees=False).as_matrix()
    elif type=="quat":
        mat[:3,:3] = Rotation.from_quat(rot).as_matrix()
    else:
        raise ValueError()
    return mat

def to_homo(vertices):
    return np.pad(vertices, ((0,0),(0,1)), 'constant', constant_values=(1)).T

def de_homo(hvertices):
    return hvertices.T[..., :-1]

