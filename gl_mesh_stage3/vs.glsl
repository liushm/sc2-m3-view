#version 400

layout (location = 0) in vec3 VertexPosition;
layout (location = 1) in vec3 VertexNormal;

out vec3 color;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

// TODO
vec4 lightPosition = vec4(5.0, 5.0, 5.0, 0.0);
vec3 kd = vec3(1.0, 1.0, 1.0);
vec3 ld = vec3(1.0, 1.0, 1.0);
mat3 normalMatrix = mat3(transpose(inverse(modelViewMatrix)));

void main()
{
    vec3 tnorm = normalize(normalMatrix * VertexNormal);
    vec4 eyeCoords = modelViewMatrix * vec4(VertexPosition, 1.0);
    vec3 s = normalize(vec3(lightPosition - eyeCoords));

    color = ld * kd * max( dot(s, tnorm), 0.0 );
    gl_Position = projectionMatrix * modelViewMatrix * vec4(VertexPosition, 1.0);
}
