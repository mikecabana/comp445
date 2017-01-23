# Java networking examples

There are several examples to help you be familiar with networking programming in JDK. It is recommended to use common tools to develop your assignment. Therefore we use Maven for this example.

## Requirement
1. [Oracle JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
2. [Apache Maven](https://maven.apache.org/) 

## Structure
There are 5 applications in this example for the echo and time protocols.

### Echo Protocol
- **Blocking Echo Server** - an implementation of the echo server using a blocking NIO socket
- **Blocking Echo Client** - an implementation of the echo client using a blocking NIO socket
- **Multiplex Echo Server** - an implementation of the cho server using the select mechanism of the NIO socket

### Time Protocol
- **Blocking Time Server** - an implementation of the time server using a blocking NIO socket
- **Blocking Time Client** - an implementation of the time client using a blocking NIO socket

## Compile and package
1. Open the terminal and cd to the `netsample` directory
2. Run `mvn package` to compile and package this example
You should see two jar files in the `target` directory: one with all dependencies (we use logging and argument parse libraries); one without dependencies.

## Run the sample applications
Use the following the commands to run applications.

### Blocking Echo Server
`java -cp target/netsample-1.0-SNAPSHOT-jar-with-dependencies.jar ca.concordia.echo.BlockingEchoServer --port 8007`
You should see the message 'ca.concordia.echo.BlockingEchoServer - EchoServer is listening at /0:0:0:0:0:0:0:0:8007' which means your echo server is ready.

### Blocking Echo Client
Once your echo server client is listening, you can use the echo client by this command
`java -cp target/netsample-1.0-SNAPSHOT-jar-with-dependencies.jar ca.concordia.echo.BlockingEchoClient --host localhost --port 8007`
If there is no error, you should be able to type into your console; and receive an echo from the echo server.

### Blocking Time Server
`java -cp target/netsample-1.0-SNAPSHOT-jar-with-dependencies.jar ca.concordia.time.BlockingTimeServer --port 8037`

### Blocking Time Client
`java -cp target/netsample-1.0-SNAPSHOT-jar-with-dependencies.jar ca.concordia.time.BlockingTimeClient --host localhost --port 8037`

### Multiplex Echo Server
This implementation demonstrates how to use `select` mechanism to handle multiple clients with a single thread in non-blocking manner. This example is useful for your future assignment.

## Using with IDE
You can either Intellij, Eclipse, or Netbeans to run, and extend these examples.