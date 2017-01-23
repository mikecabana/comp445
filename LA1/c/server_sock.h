#ifndef NETWORKING_EXAMPLES_SERVER_SOCK_H
#define NETWORKING_EXAMPLES_SERVER_SOCK_H

// listen_serve creates a socket, binds it to the given port, then listens with the given backlog
// returns the sockfd if success, otherwise returns -1
int listen_serve(int port, int backlog);

// a string presentation of the socket_addr in form "host:port"
// the returned value is guarantee only until the next call
char* str_sock_addr(struct sockaddr_storage *ss);

#endif //NETWORKING_EXAMPLES_SERVER_SOCK_H
