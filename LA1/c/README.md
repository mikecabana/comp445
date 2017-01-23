# Requirements
1. C compiler
2. Unix-like system (eg. OSX, GNU/Linux)
3. CMake 2.8.12 or later
4. Pthread library

# Build the project

1. Make a new directory named `build`
2. `cd build`
3. Run `cmake ..`
4. Run `make`

You should see 4 executable files `echoserver`, `echoclient`, `timeserver`, `timeclient` in the build directory.

# Run echo server

`./echoserver -p 8007`

# Run echo client

1. `g++ -g echoclient.cpp -o echoclient.o`
`./echoclient -h localhost -p 8007`

# Run time server

`./timeclient -h localhost -p 8007`

# Run time client

`./timeserver -h localhost -p 8007`
