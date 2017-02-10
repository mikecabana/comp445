/*
 * Trisha Dimayuga
 * 26922287
 * Lab 1
 */


import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.BufferUnderflowException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.channels.Channels;
import java.nio.channels.SocketChannel;
import java.nio.channels.WritableByteChannel;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

class Library{

	// GET method
	public String GET(String url, String str) throws URISyntaxException{

		String res = "";
		FileOutputStream out = null;


		URI uri =  new URI(url);
		//String scheme = uri.getScheme();
		String host = uri.getHost();
		String path = uri.getRawPath();
		String query = uri.getRawQuery();
		int port = uri.getPort();
		String uAgent = Library.class.getName();

		if(path.length() == 0 || path == null)
			path = "/";

		if(query != null)
			query = "?" + query;
		else 
			query = "";

		if(port == -1)
			port = 80;


		SocketAddress serverAddress = new InetSocketAddress(host, port);

		try(SocketChannel server = SocketChannel.open()) {

			server.connect(serverAddress);

			if(str.contains("-h ")){
				
				if(str.contains("Host"))
					host = str.substring(str.indexOf(":", str.indexOf("Host")) +1, str.indexOf(" ", str.indexOf("Host")));
				if(str.contains("User-Agent"))
					uAgent = str.substring(str.indexOf(":", str.indexOf("User-Agent")) +1, str.indexOf(" ", str.indexOf("User-Agent")));
			}
			String req = "GET " + path + query + " HTTP/1.0\r\n" +
					"Host: " + host + "\r\n" + "Connection: close\r\n" +
					"User-Agent: " + uAgent + "\r\n" + "\r\n";

			//System.out.println("req: " + req);
			Charset cs = StandardCharsets.UTF_8;
			CharBuffer cReq = CharBuffer.wrap(req);

			ByteBuffer rb = cs.encode(req);

			//server = SocketChannel.open();

			server.write(rb);

			WritableByteChannel destination; 
			ByteArrayOutputStream os = new ByteArrayOutputStream(); 
			ByteBuffer data = ByteBuffer.allocateDirect(32 * 1024);

			// if f option outputStream...
			destination = Channels.newChannel(os); 



			while(server.read(data) != -1){

				data.flip();

				destination.write(data);
				data.clear();

				res = new String(os.toByteArray(), "UTF-8");


				break;
			}	

		} catch (Exception e) {

		}
		// Verbose
		if(!str.contains("-v "))
			return res.substring(res.indexOf("{"), res.lastIndexOf("}")+1);
		return res;	
	}


	// POST method
	public String POST(String url, String str) throws URISyntaxException{
		String res = "";
		FileOutputStream out = null;

		String body = "";



		URI uri =  new URI(url);
		//String scheme = uri.getScheme();
		String host = uri.getHost();
		String path = uri.getRawPath();
		String query = uri.getRawQuery();
		int port = uri.getPort();
		String ct = "";
		int cl = 0;
		String uAgent = Library.class.getName();

		if(path.length() == 0 || path == null)
			path = "/";

		if(query == null)
			query = "";
		else 
			query = "?" + query;

		if(port == -1)
			port = 80;

		SocketAddress serverAddress = new InetSocketAddress(host, port);

		try(SocketChannel server = SocketChannel.open()) {

			server.connect(serverAddress);
			if(str.contains("-d ")){
				body = str.substring(str.indexOf("{", str.indexOf("-d")), str.indexOf("}")+1);
		
				cl = body.length();
				}

			if(str.contains("-h ")){
				
				if(str.contains("Host"))
					host = str.substring(str.indexOf(":", str.indexOf("Host")) +1, str.indexOf(" ", str.indexOf("Host")));
				if(str.contains("Content-Type"))
					ct = str.substring(str.indexOf(":", str.indexOf("Content-Type")) +1, str.indexOf(" ", str.indexOf("Content-Type")));
				if(str.contains("Content-Length"))
					cl = Integer.parseInt(str.substring(str.indexOf(":", str.indexOf("Content-Length")) +1, str.indexOf(" ", str.indexOf("Content-Length"))));
				if(str.contains("User-Agent"))
					uAgent = str.substring(str.indexOf(":", str.indexOf("User-Agent")) +1, str.indexOf(" ", str.indexOf("User-Agent")));
			}


			String req = "POST " + path + " HTTP/1.0\r\n" +
					"Host: " + host + "\r\n" + "Content-Length: " + cl + "\r\n" +
					"Content-Type: " + ct + "\r\n" + "User-Agent: " + uAgent +
					"\r\n" + "\r\n" + body;

			
			Charset cs = StandardCharsets.UTF_8;
			CharBuffer cReq = CharBuffer.wrap(req);

			ByteBuffer rb = cs.encode(req);

			//server = SocketChannel.open();

			server.write(rb);

			WritableByteChannel destination; 
			ByteArrayOutputStream os = new ByteArrayOutputStream(); 
			ByteBuffer data = ByteBuffer.allocateDirect(32 * 1024);

			// if f option outputStream...
			destination = Channels.newChannel(os); 



			while(server.read(data) != -1){

				data.flip();

				destination.write(data);
				data.clear();

				res = new String(os.toByteArray(), "UTF-8");


				break;
			}	

		} catch (Exception e) {

		}
		// Verbose
		if(!str.contains("-v "))
			return res.substring(res.indexOf("{"), res.lastIndexOf("}")+1);
		return res;	

	}

}