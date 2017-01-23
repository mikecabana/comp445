package ca.concordia.echo;

import joptsimple.OptionParser;
import joptsimple.OptionSet;

import java.io.EOFException;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

import static java.util.Arrays.asList;

public class BlockingEchoClient {

    // readFully reads until the request is fulfilled or the socket is closed
    private static void readFully(SocketChannel socket, ByteBuffer buf, int size) throws IOException {
        while (buf.position() < size) {
            int n = socket.read(buf);
            if (n == -1) {
                break;
            }
        }
        if (buf.position() != size) {
            throw new EOFException();
        }
    }

    private static void readEchoAndRepeat(SocketChannel socket) throws IOException {
        Charset utf8 = StandardCharsets.UTF_8;
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            ByteBuffer buf = utf8.encode(line);
            int n = socket.write(buf);
            buf.clear();

            // Receive all what we have sent
            readFully(socket, buf, n);
            buf.flip();
            System.out.println("Replied: " + utf8.decode(buf));
        }
    }

    private static void runClient(SocketAddress endpoint) throws IOException {
        try (SocketChannel socket = SocketChannel.open()) {
            socket.connect(endpoint);
            System.out.println("Type any thing then ENTER. Press Ctrl+C to terminate");
            readEchoAndRepeat(socket);
        }
    }

    public static void main(String[] args) throws IOException {
        OptionParser parser = new OptionParser();
        parser.acceptsAll(asList("host", "h"), "EchoServer hostname")
                .withOptionalArg()
                .defaultsTo("localhost");

        parser.acceptsAll(asList("port", "p"), "EchoServer listening port")
                .withOptionalArg()
                .defaultsTo("8007");

        OptionSet opts = parser.parse(args);

        String host = (String) opts.valueOf("host");
        int port = Integer.parseInt((String) opts.valueOf("port"));

        SocketAddress endpoint = new InetSocketAddress(host, port);
        runClient(endpoint);
    }
}

