cmake_minimum_required(VERSION 2.8.12)

PROJECT(Networking_Examples)

# Echo server application
SET(ECHO_SERVER_SRCS server_sock.c echo_server.c)
ADD_EXECUTABLE(echoserver ${ECHO_SERVER_SRCS})

# Echo client application
SET(ECHO_CLIENT_SRCS client_sock.c echo_client.c)
ADD_EXECUTABLE(echoclient ${ECHO_CLIENT_SRCS})


# Time server application
SET(TIME_SERVER_SRCS server_sock.c time_server.c)
ADD_EXECUTABLE(timeserver ${TIME_SERVER_SRCS})

# Time client application
SET(TIME_CLIENT_SRCS client_sock.c time_client.c)
ADD_EXECUTABLE(timeclient ${TIME_CLIENT_SRCS})