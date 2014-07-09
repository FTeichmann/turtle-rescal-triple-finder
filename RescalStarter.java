import java.util.*;
import java.io.*;


public class RescalStarter {
    public static void main(String[] args) {

        Scanner userInputScanner = new Scanner(System.in);
        System.out.println("Do you need to rewrite the config file?(Y/n)");
        String answer = userInputScanner.nextLine();
        if(answer == "Y"){
            System.out.println("Where can I find rescal?");
            String pathToRescal = userInputScanner.nextLine();
            System.out.println("What .ttl file do you wish to analyze?");
            String pathToTurtleFile = userInputScanner.nextLine();
            System.out.println("Please enter threshhold.");
            String threshhold = userInputScanner.nextLine();
            //lets rewrite the config now
            try {
                PrintWriter configWriter = new PrintWriter("config.ini", "UTF-8");
                configWriter.println("[paths]");
                configWriter.println("pathToRescal: "+pathToRescal);
                configWriter.println("pathToTurtleFile: "+pathToTurtleFile);
                configWriter.close();
            }catch (IOException e) {
            System.err.println("Problem writing to the file config.ini");
            }
        }
        System.out.println("Please enter threshold.");
        String threshold = userInputScanner.nextLine();
        System.out.println("Please enter rank of the factorization.");
        String rank = userInputScanner.nextLine();

        System.out.println("Starting turtleReader in python now");
        try{
            int number1 = 10;
            int number2 = 32;
            Process p = Runtime.getRuntime().exec("python turtleReader.py "+threshold +" "+rank);

            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String response = "";
            String line = "";
                while ((line = in.readLine()) != null) {
                response += line;
            }
            System.out.println("python response: "+response);
        }catch(Exception e){
        System.err.println("Problem with java-python bridge occured.");
        }
    }
}


