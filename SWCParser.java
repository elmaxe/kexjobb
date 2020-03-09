import java.util.Scanner;
import java.util.Arrays;
import java.util.ArrayList;

public class SWCParser {

    //Pipe file content
    public static void main(String[] args) {
        // String filename = args[0];
        Scanner scanner = new Scanner(System.in);
        ArrayList<MBR> data = new ArrayList<>();

        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            
            //Comment, don't parse
            if (line.matches("\\s*#.*")) {
                continue;
            }

            String[] numbers = line.split("\\s+");

            int index = Integer.parseInt(numbers[0]);
            int flag = Integer.parseInt(numbers[1]);
            double x = Double.parseDouble(numbers[2]);
            double y = Double.parseDouble(numbers[3]);
            double z = Double.parseDouble(numbers[4]);
            double radius = Double.parseDouble(numbers[5]);
            int parent = Integer.parseInt(numbers[6]);

            MBR mbr = new MBR(x - radius, y - radius, z - radius, x + radius, y + radius, z + radius);

            data.add(mbr);
        }
        
        for (MBR m : data) {
            System.out.println(m.toString());
        }

    }

    /**
     * Class for representing a MBR.
     */
    private static class MBR {
        
        double xmin, xmax, ymin, ymax, zmin, zmax;
        
        public MBR(double xmin, double ymin, double zmin, double xmax, double ymax, double zmax) {
            this.xmin = xmin;
            this.ymin = ymin;
            this.zmin = zmin;
            this.xmax = xmax;
            this.ymax = ymax;
            this.zmax = zmax;   
        }
        
        @Override
        public String toString() {
            return String.format("%f %f %f %f %f %f", xmin, xmax, ymin, ymax, zmin, zmax);
        }
    }
}