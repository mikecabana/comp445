package ca.concordia.echo;

import joptsimple.OptionParser;
import joptsimple.OptionSet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.concurrent.ForkJoinPool;

import static java.util.Arrays.asList;

public class BlockingEchoServer {

    private static final Logger logger = LoggerFactory.getLogger(BlockingEchoServer.class);

    private void readEchoAndRepeat(SocketChannel socket) {
        try (SocketChannel client = socket) {
            ByteBuffer buf = ByteBuffer.allocate(1024);
            for (; ; ) {
                int nr = client.read(buf);

                if (nr == -1)
                    break;

                if (nr > 0) {
                    // ByteBuffer is tricky, you have to flip when switch from read to write, or vice-versa
                    buf.flip();
                    client.write(buf);
                    buf.clear();
                }
            }
        } catch (IOException e) {
            logger.error("Echo error {}", e);
        }
    }

    private void listenAndServe(int port) throws IOException {
        try (ServerSocketChannel server = ServerSocketChannel.open()) {
            server.bind(new InetSocketAddress(port));
            logger.info("EchoServer is listening at {}", server.getLocalAddress());
            for (; ; ) {
                SocketChannel client = server.accept();
                logger.info("New client from {}", client.getRemoteAddress());
                // We may use a custom Executor instead of ForkJoinPool in a real-world application
                ForkJoinPool.commonPool().submit(() -> readEchoAndRepeat(client));
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
        BlockingEchoServer server = new BlockingEchoServer();
        server.listenAndServe(port);
    }
}