#include <getopt.h>
#include <sys/socket.h>
#include <err.h>
#include <errno.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include "client_sock.h"
#include "echo_protocol.h"

void usage(char *argv[]);

void remove_newline(char *s) {
    ssize_t len = strlen(s);
    if (len > 0 && s[len - 1] == '\n') {
        s[len - 1] = '\0';
    }
}

// read_echo_print reads a line from console, sends to the echo server, waits for reply, then prints
// returns 0 if all operations are successful, otherwise returns -1
int read_echo_print(int client) {
    char buf[1024] = {'\0'};

    //Read a message from console
    fflush(stdout);
    fgets(buf, sizeof buf, stdin);
    remove_newline(buf);

    //Send the message to the server
    size_t msg_len = strlen(buf);
    if (msg_len == 0) {
        return 0;
    }

    if (send(client, buf, msg_len, 0) <= 0) {
        return -1;
    }

    // MSG_WAITALL means wait for full request or error
    memset(buf, 0, sizeof buf);
    if (recv(client, &buf, msg_len, MSG_WAITALL) <= 0) {
        //recv did not set errno if a connection reset by peer
        if (errno == 0) {
            errno = ECONNRESET;
        }
        return -1;
    }

    printf("Replied: %s\n", buf);
    return 0;
}

int main(int argc, char *argv[]) {
    int c;
    int port = DEFAULT_ECHO_PORT;
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

    printf("Type any thing then ENTER. Press Ctrl+C to terminate\n");
    int err;
    while ((err = read_echo_print(client_fd)) == 0);
    close(client_fd);

    if (err != 0) {
        errx(1, "failed to echo: %s", strerror(errno));
    }
    return 0;
}

void usage(char *argv[]) {
    printf("usage: %s [-h host] [-p port]\n", argv[0]);
    printf("  -h string\n");
    printf("     echo server hostname or address (default \"localhost\")\n");
    printf("  -p int\n");
    printf("     echo server listening port (default %d)\n", DEFAULT_ECHO_PORT);
}