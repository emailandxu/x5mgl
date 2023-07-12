#version 330

#if defined VERTEX_SHADER
uniform mat4 proj;
uniform mat4 view;
uniform mat4 model;

in vec3 in_position;
in vec3 in_color;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_vert;
out vec2 v_text;
out vec3 v_norm;
out vec3 v_color;

void main() {
    v_vert = in_position;
    v_text = in_texcoord_0;
    v_norm = mat3(model) * in_normal;

    v_color = in_color;
    gl_Position = proj * view * model * vec4(in_position, 1.0);

}

#elif defined FRAGMENT_SHADER
uniform vec3 Light;
uniform sampler2D Texture;

in vec3 v_vert;
in vec3 v_color;
in vec3 v_norm;
in vec2 v_text;

out vec4 f_color;

void main() {
    float lum = clamp(dot(normalize(Light), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
    
    vec3 c = texture(Texture, v_text).rgb;

    f_color = vec4(v_color*lum, 1.0);
}

#endif