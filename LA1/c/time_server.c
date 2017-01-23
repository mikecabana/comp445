#include <err.h>
#include <sys/socket.h>
#include <string.h>
#include <errno.h>
#include <printf.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include "server_sock.h"
#include "time_protocol.h"

void usage(char *argv[]);

ssize_t report_time(int client) {
    time_t now;
    time(&now);
    uint32_t seconds = (uint32_t) htonl(now + NUM_SECONDS_1900_TO_1970);
    return send(client, &seconds, sizeof seconds, 0);
}

void run_loop(int server_fd) {
    for (;;) {
        struct sockaddr_storage their_addr;
        socklen_t addr_len = sizeof their_addr;
        int client_fd = accept(server_fd, (struct sockaddr *) &their_addr, &addr_len);
        if (client_fd < 0) {
            fprintf(stderr, "failed to accept new client: %s\n", strerror(errno));
            continue;
        }

        //report_time will complete quickly, thus we don't need concurrency
        printf("New client from %s\n", str_sock_addr(&their_addr));
        if (report_time(client_fd) < 0) {
            fprintf(stderr, "failed to report time: %s\n", strerror(errno));
        }
        close(client_fd);
    }
}

int main(int argc, char *argv[]) {
    int c;
    int port = DEFAULT_TIME_PORT;
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
        errx(1, "failed to listen at %d: %s", port, strerror(errno));
    }
    printf("Time server is listening at %d\n", port);
    run_loop(server_fd);
}

void usage(char *argv[]) {
    printf("usage: %s [-p port]\n", argv[0]);
    printf("  -p int\n");
    printf("     time server listening port (default %d)\n", DEFAULT_TIME_PORT);
}