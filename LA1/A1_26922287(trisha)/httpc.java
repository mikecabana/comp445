/*
 * Trisha Dimayuga
 * 26922287
 * Lab 1
 */

import java.util.Scanner;

public class httpc{
	public static void main(String[]args) throws Exception{
		Library lib = new Library();
		Scanner kb = new Scanner(System.in);
		System.out.print("> ");
		String input = kb.nextLine();
		
		System.out.println();

		// GET
		if(input.contains("get")){
			String url = input.substring(input.indexOf("http://"), input.length()-1);
			String data= input.substring(input.indexOf("get")+4, input.indexOf("http://")-1);
			System.out.println(lib.GET(url, data));
		}
		
		// POST
		if(input.contains("post")){
			String url = input.substring(input.indexOf("http://"), input.length());
			String data= input.substring(input.indexOf("post")+5, input.indexOf("http://")-1);
			
			System.out.println(lib.POST(url, data));
		}

	}
}