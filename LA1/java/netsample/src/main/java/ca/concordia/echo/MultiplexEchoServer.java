package ca.concordia.echo;


import joptsimple.OptionParser;
import joptsimple.OptionSet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;

import static java.nio.channels.SelectionKey.OP_ACCEPT;
import static java.nio.channels.SelectionKey.OP_READ;
import static java.util.Arrays.asList;

public class MultiplexEchoServer {

    private static final Logger logger = LoggerFactory.getLogger(MultiplexEchoServer.class);

    // Uses a single buffer to demonstrate that all clients are running in a single thread
    private final ByteBuffer buffer = ByteBuffer.allocate(1024);

    private void readAndEcho(SelectionKey s) {
        SocketChannel client = (SocketChannel) s.channel();
        try {
            for (; ; ) {
                int n = client.read(buffer);
                // If the number of bytes read is -1, the peer is closed
                if (n == -1) {
                    unregisterClient(s);
                    return;
                }
                if (n == 0) {
                    return;
                }
                // ByteBuffer is tricky, you have to flip when switch from read to write, or vice-versa
                buffer.flip();
                client.write(buffer);
                buffer.clear();
            }
        } catch (IOException e) {
            unregisterClient(s);
            logger.error("Failed to receive/send data", e);
        }
    }

    private void newClient(ServerSocketChannel server, Selector selector) {
        try {
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            logger.info("New client from {}", client.getRemoteAddress());
            client.register(selector, OP_READ, client);
        } catch (IOException e) {
            logger.error("Failed to accept client", e);
        }
    }

    private void unregisterClient(SelectionKey s) {
        try {
            s.cancel();
            s.channel().close();
        } catch (IOException e) {
            logger.error("Failed to clean up", e);
        }
    }

    private void runLoop(ServerSocketChannel server, Selector selector) throws IOException {
        // Check if there is any event (eg. new client or new data) happened
        selector.select();

        for (SelectionKey s : selector.selectedKeys()) {
            // Acceptable means there is a new incoming
            if (s.isAcceptable()) {
                newClient(server, selector);

            // Readable means this client has sent data or closed
            } else if (s.isReadable()) {
                readAndEcho(s);
            }
        }
        // We must clear this set, otherwise the select will return the same value again
        selector.selectedKeys().clear();
    }

    private void listenAndServe(int port) throws IOException {
        try (ServerSocketChannel server = ServerSocketChannel.open()) {
            server.bind(new InetSocketAddress(port));
            server.configureBlocking(false);
            Selector selector = Selector.open();

            // Register the server socket to be notified when there is a new incoming client
            server.register(selector, OP_ACCEPT, null);
            for (; ; ) {
                runLoop(server, selector);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        OptionParser parser = new OptionParser();
        parser.acceptsAll(asList("port", "p"), "Listening port")
                .withOptionalArg()
                .defaultsTo("8007");

        OptionSet opts = parser.parse(args);
        int port = Integer.parseInt((String) opts.valueOf("port"));
        new MultiplexEchoServer().listenAndServe(port);
    }
}
