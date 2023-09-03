#version 330 core

in vec2 fragmentTexCoord;

out vec4 color;
uniform sampler2D imageTexture;


uniform float w;
uniform float h;



//https://www.shadertoy.com/view/mtyGWy
void main() {
    vec2 uv = vec2(fragmentTexCoord);
    uv-=vec2(0.5,0.5);
    uv*=vec2(
        5*(w/1600)*2,
        5*(h/800)
    );
    float d = length(uv);
    d = 1-abs(d);
    d = step(0.1,d);
    color = vec4(d,d,d, 1.0);
}