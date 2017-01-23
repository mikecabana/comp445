#include <err.h>
#include <sys/socket.h>
#include <string.h>
#include <errno.h>
#include <printf.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <getopt.h>
#include <stdlib.h>
#include "server_sock.h"
#include "echo_protocol.h"

void usage(char *argv[]);

void *handle_client(void *sockfd) {
    size_t BUFF_SIZE = 1024;
    int client = *(int *) sockfd;
    unsigned char buf[BUFF_SIZE];

    for (;;) {
        ssize_t n = recv(client, &buf, BUFF_SIZE, 0);
        // n is 0 means the peer socket is closed
        if (n == 0) {
            return NULL;
        }
        // n < 0 means errors occurred
        if (n < 0) {
            fprintf(stderr, "failed to accept new client: %s\n", strerror(errno));
            return NULL;
        }
        // Just reply what received
        n = send(client, &buf, (size_t) n, 0);
        if (n <= 0) {
            return NULL;
        }
    }
}

int main(int argc, char **argv) {
    int c;
    int port = DEFAULT_ECHO_PORT;
    while ((c = getopt(argc, argv, "p:")) != -1) {
        switch (c) {
            case 'p':
                port = atoi(optarg);
                break;

            default:
                usage(argv);
                exit(2);
        }
    }
    int server_fd = listen_serve(port, 5);
    if (server_fd < 0) {
        errx(1, "failed to listening at %d: %s", port, strerror(errno));
    }

    printf("Echo server is listening at %d\n", port);

    for (;;) {
        struct sockaddr_storage peer_addr;
        socklen_t addr_len = sizeof peer_addr;
        int client_fd = accept(server_fd, (struct sockaddr *) &peer_addr, &addr_len);
        if (client_fd < 0) {
            fprintf(stderr, "failed to accept new client: %s\n", strerror(errno));
            continue;
        }
        printf("New client from %s\n", str_sock_addr(&peer_addr));
        // In the real application, we should limit the number of threads
        // as this may lead to out of resources.
        pthread_t tid;
        pthread_create(&tid, NULL, handle_client, &client_fd);
    }
}

void usage(char *argv[]) {
    printf("usage: %s [-p port]\n", argv[0]);
    printf("  -p int\n");
    printf("     echo server listening port (default %d)\n", DEFAULT_ECHO_PORT);
}