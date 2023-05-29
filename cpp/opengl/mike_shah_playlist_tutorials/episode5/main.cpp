#include <iostream>
#include <SDL2/SDL.h>
#include "glad/glad.h"


// Global variables - pure evil muahahaaha

int gScreenWidth  = 640;
int gScreenHeight = 480;
SDL_Window* gGraphicsApplicationWindow = nullptr;
SDL_GLContext gOpenGLContext = nullptr;

bool gQuit = false; // if true we quit (OH RLY?)

void GetOpenGLVersionInfo()
{
    std::cout << "Vendor: " << glGetString(GL_VENDOR) << std::endl;
    std::cout << "Renderer: " << glGetString(GL_RENDERER) << std::endl;
    std::cout << "Version: " << glGetString(GL_VERSION) << std::endl;
    std::cout << "Shading Language: " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;
}

/// @brief Starts the necessary components
void InitializeProgram()
{
    // initialize sdl library's video subssystem, responsible for creating a window
    if(SDL_Init(SDL_INIT_VIDEO < 0)) {
        std::cerr << "SDL2 could not initialize video subsystem" << std::endl;
        exit(1);
    }

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE); // It means it will use only the modern functionalitty of opengl
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1); // Turn on double buffer, one is drawn while the other is shows
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24); // The size (in bytes) of the depth buffer (used to detect if objects are overlaping)

    gGraphicsApplicationWindow = SDL_CreateWindow("White rabbit", 0, 0, gScreenWidth, gScreenHeight, SDL_WINDOW_OPENGL);

    if (gGraphicsApplicationWindow == nullptr) {
        std::cerr << "Could not create window" << std::endl;
        exit(1); 
    }

    gOpenGLContext = SDL_GL_CreateContext(gGraphicsApplicationWindow);
    if (gOpenGLContext == nullptr) {
        std::cerr << "Could not create opengl context" << std::endl;
        exit(1); 
    }

    // initialize the glad library, implementation of openGL
    // SDL_GL_GetProcAddress: get the function pointer to the SDL implementation. Here is where the connection between SDL2 and glad is made
    if(!gladLoadGLLoader(SDL_GL_GetProcAddress)) {
        std::cerr << "Could not start glad function" << std::endl;
        exit(1);
    }

    GetOpenGLVersionInfo();
}


void Input()
{
    SDL_Event event;
    
    while(SDL_PollEvent(&event) != 0){
        if(event.type == SDL_QUIT) {
            std::cout << "Goodbye" << std::endl;
            gQuit = true;
        }
    }

}

void PreDraw()
{

}

void Draw()
{

}

/// @brief Checks for inputs, update parameters and render the window
void MainLoop()
{
    while(!gQuit) {
        Input();

        PreDraw();

        Draw();

        // Update the screen
        SDL_GL_SwapWindow(gGraphicsApplicationWindow);
    }

}

/// @brief Delete stuff
void CleanUp()
{
    SDL_DestroyWindow(gGraphicsApplicationWindow);
    SDL_Quit();

}
int main(int argc, char const *argv[])
{
    InitializeProgram();

    MainLoop();

    CleanUp();
    
    return 0;
}
