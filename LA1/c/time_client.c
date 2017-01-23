#include <err.h>
#include <errno.h>
#include <sys/socket.h>
#include <time.h>
#include <printf.h>
#include <memory.h>
#include <getopt.h>
#include <stdlib.h>
#include "client_sock.h"
#include "time_protocol.h"

void usage(char *argv[]);

int main(int argc, char *argv[]) {
    int c;
    int port = DEFAULT_TIME_PORT;
    char *host = "localhost";
    while ((c = getopt(argc, argv, "p:h:")) != -1) {
        switch (c) {
            case 'p':
                port = atoi(optarg);
                break;
            case 'h':
                host = optarg;
                break;
            default:
                usage(argv);
                exit(2);
        }
    }

    int client_fd = dial(host, port);
    if (client_fd < 0) {
        errx(1, "failed to dial to %s:%d with error: %s", host, port, strerror(errno));
    }

    //Get the server time
    u_int32_t epoch;
    ssize_t rc = recv(client_fd, &epoch, sizeof epoch, MSG_WAITALL);
    if (rc < 0) {
        errx(1, "failed to receive data: %s", strerror(errno));
    }
    if (rc != 4) {
        errx(1, "expected to receive 4 bytes, but received %zi bytes", rc);
    }
    time_t r_time = ntohl(epoch) - NUM_SECONDS_1900_TO_1970;

    // Print the server time
    struct tm *tm = localtime(&r_time);
    char time_str[32] = {'\0'};
    strftime(time_str, sizeof time_str, "%d/%m/%Y %H:%M:%S", tm);
    printf("Server time is %s\n", time_str);

    return 0;
}

void usage(char *argv[]) {
    printf("usage: %s [-h host] [-p port]\n", argv[0]);
    printf("  -h string\n");
    printf("     time server hostname or address (default \"localhost\")\n");
    printf("  -p int\n");
    printf("     time server listening port (default %d)\n", DEFAULT_TIME_PORT);
}