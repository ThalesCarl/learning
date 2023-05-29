#version 410 core

in vec4 position;

void main()
{
   gl_Position = vec4(postion.x, position.y, position.z, 1.0);
}

