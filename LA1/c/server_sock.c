#include <getopt.h>
#include <sys/socket.h>
#include <netdb.h>
#include <memory.h>
#include <stdio.h>
#include <arpa/inet.h>

int listen_serve(int port, int backlog) {
    struct addrinfo hints, *res, *p;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;
    char portstr[16] = {'\0'};
    snprintf(portstr, sizeof portstr, "%d", port);
    if (getaddrinfo(NULL, portstr, &hints, &res) < 0) {
        return -1;
    }

    int rc = -1;
    int sockfd = -1;

    for (p = res; p != NULL; p = p->ai_next) {
        int yes = 1;
        sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (sockfd < 0) {
            break;
        }
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
            close(sockfd);
            continue;
        }
        rc = bind(sockfd, p->ai_addr, p->ai_addrlen);
        if (rc < 0) {
            close(sockfd);
            continue;
        }
        break;
    }
    freeaddrinfo(res);
    if (rc < 0 || sockfd < 0) {
        return -1;
    }
    if (listen(sockfd, backlog) < 0) {
        close(sockfd);
        return -1;
    }
    return sockfd;
}

char *str_sock_addr(struct sockaddr_storage *ss) {
    char ipstr[INET6_ADDRSTRLEN] = {'\0'};
    int port;
    if (ss->ss_family == AF_INET) {
        struct sockaddr_in *sa = (struct sockaddr_in *) ss;
        inet_ntop(ss->ss_family, &sa->sin_addr, ipstr, sizeof ipstr);
        port = ntohs(sa->sin_port);
    } else {
        struct sockaddr_in6 *sa = (struct sockaddr_in6 *) ss;
        inet_ntop(ss->ss_family, &sa->sin6_addr, ipstr, sizeof ipstr);
        port = ntohs(sa->sin6_port);
    }

    static char buf[32];
    memset(buf, 0, sizeof buf);
    snprintf(buf, sizeof buf, "%s:%d", ipstr, port);
    return buf;
}