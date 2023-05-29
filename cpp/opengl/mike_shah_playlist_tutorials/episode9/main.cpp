#include <iostream>
#include <vector>
#include <SDL2/SDL.h>
#include "glad/glad.h"


// Global variables - pure evil muahahaaha

int gScreenWidth  = 640;
int gScreenHeight = 480;
SDL_Window* gGraphicsApplicationWindow = nullptr;
SDL_GLContext gOpenGLContext = nullptr;

// VAO
GLuint gVertexArrayObject = 0;

// VBO
GLuint gVertexBufferObject = 0;

// Program objects (for our shaders)
GLuint gGraphicsPipelineShaderProgram = 0;

// Vertex Shader executes once per vertex on the GPU, and will be in charge of the final position of the vertex. 
// In this case it does not do anything
const std::string gVertexShaderSource = 
    "#version 330 core\n"
    "in vec4 position;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(postion.x, position.y, position.z, 1.0);\n"
    "}\n";

// Fragment shader executes after rasterization and it is executed per fragment (in general pixel rasterized) 
// and determines (in part) the final color that will be sent to the screen
const std::string gFragmentShaderSource =
    "#version 330 core\n"
    "out vec4 color;\n"
    "void main()\n"
    "{\n"
    "   color = vec4(1.0f, 0.5f, 0.0f, 1.0f);\n"
    "}\n"
;

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

    // Print to screen openGl info
    GetOpenGLVersionInfo();

}

void VertexSpecification() 
{
    // Lives on the CPU
    const std::vector<GLfloat> vertexPosition {
        // x   y      z
        -0.8f, -0.8f, 0.0f, // vertex 1
        0.8f , -0.8f, 0.0f, // vertex 2
        0.0f , 0.8f , 0.0f  // vertex 3
    };

    // Start setting things up on the GPU
    glGenVertexArrays(1, &gVertexArrayObject); // Creates VAO
    glBindVertexArray(gVertexArrayObject); // Select the created to VAO to be used

    // Start generating our VBO
    glGenBuffers(1, &gVertexBufferObject);
    glBindBuffer(GL_ARRAY_BUFFER, gVertexBufferObject);
    glBufferData(GL_ARRAY_BUFFER, vertexPosition.size() * sizeof(GLfloat), vertexPosition.data(), GL_STATIC_DRAW);

    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, // match the element previous call
                          3, // number of elements of vector vertexPosition that are going to be used for every node, in this case x, y and z. It could be 6 with color together, for example
                          GL_FLOAT,
                          GL_FALSE,
                          0, // use this argument if there is more information inside the VBO
                          (void*)0 // pointer to the offset used in the previous argument
    );


    // Clean-up
    glBindVertexArray(0);
    glDisableVertexAttribArray(0);
}

GLuint CompileShader(GLuint type, const std::string sourceCode)
{
    GLuint shaderObject;
    if(type == GL_VERTEX_SHADER) {
        shaderObject = glCreateShader(GL_VERTEX_SHADER);
    } else if(type == GL_FRAGMENT_SHADER) {
        shaderObject = glCreateShader(GL_FRAGMENT_SHADER);
    }

    const char* src = sourceCode.c_str();
    glShaderSource(shaderObject, 1, &src, nullptr);

    // Get compilation status
    int result;
    glGetShaderiv(shaderObject, GL_COMPILE_STATUS, &result);

    if(result == GL_FALSE) {
        int log_length;
        glGetShaderiv(shaderObject, GL_INFO_LOG_LENGTH, &log_length);
        char* errorMessages = new char[log_length];
        glGetShaderInfoLog(shaderObject, log_length, &log_length, errorMessages);
        if(type == GL_VERTEX_SHADER) {
            std::cout << "ERROR: GL_VERTEX_SHADER compilation failed!\n " << errorMessages << std::endl;
        } else if(type == GL_FRAGMENT_SHADER) {
            std::cout << "ERROR: GL_FRAGMENT_SHADER compilation failed!\n " << errorMessages << std::endl;
        }
        // Reclaim memory allocation
        delete[] errorMessages;

        // Delete broken shader
        glDeleteShader(shaderObject);
        return 0;
    }

    return shaderObject;

}

// Create the program that is going to be compiled and sent to the GPU
GLuint CreateShaderProgram(const std::string& vertexShaderSource, const std::string fragmentShaderSource) 
{
    GLuint programObject = glCreateProgram(); // Better name: create graphics pipeline

    GLuint myVertexShader   = CompileShader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint myFragmentShader = CompileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);

    // compile the program with the shaders created
    glAttachShader(programObject, myVertexShader);
    glAttachShader(programObject, myFragmentShader);
    glLinkProgram(programObject);

    //Validate our program
    glValidateProgram(programObject);

    // We should also glDetachShader, glDeleteShader after the programObject is compiled

    return programObject;

}

void CreateGraphicsPipeline()
{
   gGraphicsPipelineShaderProgram = CreateShaderProgram(gVertexShaderSource, gFragmentShaderSource);
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
    glDisable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glViewport(0, 0, gScreenWidth, gScreenHeight);
    glClearColor(1.f, 1.f, 0.f, 1.f);

    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
    glUseProgram(gGraphicsPipelineShaderProgram);
}

void Draw()
{

    glBindVertexArray(gVertexArrayObject);
    glBindBuffer(GL_ARRAY_BUFFER, gVertexBufferObject);

    glDrawArrays(GL_TRIANGLES, 0, 3);
    glUseProgram(0);
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

    // Setup window using SDL (it could use different library like qt, wxWidgets, etc)
    InitializeProgram();

    // input geometry data and create VAO and VBO
    VertexSpecification();

    // Create vertex and fragment shader, for now
    CreateGraphicsPipeline();

    // Loop for events and draw stuff to the screen
    MainLoop();

    // call destructor functions after the main loop is executed
    CleanUp();
    
    return 0;
}
