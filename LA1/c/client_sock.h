#ifndef NETWORKING_EXAMPLES_CLIENT_SOCK_H
#define NETWORKING_EXAMPLES_CLIENT_SOCK_H

// dial connects to the given host:port
// returns a sockfd if success, otherwise returns -1
int dial(const char* host, int port);

#endif //NETWORKING_EXAMPLES_CLIENT_SOCK_H
