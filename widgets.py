import imgui
import numpy as np
from pyrr import Matrix44
from mathutil import *

def float3_widget(name, min, max, default_values=None):
    if default_values is None:
        default_values = (0, 0, 0)

    assert len(default_values) == 3
    value = list(default_values)

    def widget():
        nonlocal value
        _, value[:] = imgui.slider_float3(f"{name}", *value, min, max, format="%.4f")

        if imgui.button(f"reset {name}"):
            value = list(default_values)
        return value

    return widget

def int_widget(name, min, max, default_value=None):
    if default_value is None:
        default_value = 0
    
    assert isinstance(default_value, int)
    value = default_value

    def widget():
        nonlocal value
        _, value = imgui.slider_int(f"{name}", value, min, max, format="%d")
        return value
    return widget

def bool_widget(name, default=False):
    bool=default
    def widget():
        nonlocal bool
        _, bool = imgui.checkbox(f"if_{name}", bool)
        return bool
    return widget

def camera_widget(aspect, fov=45.0, near=0.1, far=100.0, campos=(0, 0, 3)):       
    pos_widget = float3_widget("camera_pos", -5, 5, campos)
    lookat_widget = float3_widget("camera_lookat", -5, 5, (0, 0, 0))
    
    def move_camera():
        with imgui.begin("camera"):
            x, y, z = np.array(pos_widget())
            lookat = np.array(lookat_widget())
        proj = Matrix44.perspective_projection(fov, aspect, near, far)
        view = Matrix44.look_at(
            (-x, y, -z),
            lookat,
            (0.0, 1.0, 0.0),
        )
        light_pos = np.array([-x, y, -z])
        return proj, view, light_pos

    return move_camera

def transform_widget(name, trans=(0, 0, 0), eulers=(0, 0, 0), scale=(1, 1, 1)):
    wtrans = float3_widget(f"{name}_trans", -5, 5, trans)
    weulers = float3_widget(f"{name}_eulers", -np.pi, np.pi, eulers)
    wscale = float3_widget(f"{name}_scale", 0.1, 1.0, scale)
    
    def widget():
        with imgui.begin(f"{name}_transform"):
            trans, eulers, scale = wtrans(), weulers(), wscale()
        # strange feature of Matrix44, must treat the rotation as z up
        eulers = eulers[0], -eulers[2], eulers[1]
        model = Matrix44.from_translation(trans) * Matrix44.from_eulers(eulers) * Matrix44.from_scale(scale)
        return model
    return widget