#include <getopt.h>
#include <sys/socket.h>
#include <netdb.h>
#include <memory.h>
#include <stdio.h>

int dial(const char *host, int port) {
    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    char portstr[16] = {'\0'};
    snprintf(portstr, sizeof portstr, "%d", port);

    // Resolve the addrinfo for the given host:port
    if (getaddrinfo(host, portstr, &hints, &res) < 0) {
        return -1;
    }

    // Create a socket descriptor, and then connect to the resolved address one by one
    int sockfd = -1;
    for (struct addrinfo *p = res; p != NULL; p = p->ai_next) {
        sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (sockfd < 0) {
            break;
        }
        if (connect(sockfd, res->ai_addr, res->ai_addrlen) < 0) {
            close(sockfd);
            sockfd = -1;
            continue;
        }
    }
    freeaddrinfo(res);
    return sockfd;
}