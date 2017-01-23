package ca.concordia.time;

import joptsimple.OptionParser;
import joptsimple.OptionSet;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.SocketChannel;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDateTime;

import static java.util.Arrays.asList;

public class BlockingTimeClient {

    private static void runClient(SocketAddress endpoint) throws IOException {
        try (SocketChannel client = SocketChannel.open()) {
            client.connect(endpoint);
            ByteBuffer bs = ByteBuffer.allocate(4).order(ByteOrder.BIG_ENDIAN);
            int n = client.read(bs);
            if (n != 4) {
                throw new IOException(String.format("Expected to receive 4 bytes, but %d bytes", n));
            }
            // We don't have unsigned types in Java, therefore we have to use Long as unsigned int
            // Without conversion, you eventually receive an negative integer
            long seconds = Integer.toUnsignedLong(bs.getInt(0));
            LocalDateTime rtime = Instant.ofEpochSecond(seconds - 2208988800L)
                    .atZone(Clock.systemDefaultZone().getZone())
                    .toLocalDateTime();
            System.out.println("Server time is " + rtime);
        }
    }

    public static void main(String[] args) throws IOException {
        OptionParser parser = new OptionParser();
        parser.acceptsAll(asList("host", "h"), "TimeServer hostname")
                .withOptionalArg()
                .defaultsTo("localhost");

        parser.acceptsAll(asList("port", "p"), "TimeServer listening port")
                .withOptionalArg()
                .defaultsTo("8037");

        OptionSet opts = parser.parse(args);

        String host = (String) opts.valueOf("host");
        int port = Integer.parseInt((String) opts.valueOf("port"));

        SocketAddress endpoint = new InetSocketAddress(host, port);
        runClient(endpoint);
    }
}
