import java.util.Random;
public class Lab1 {
    public static void main(String[] args) {
        Random rnd = new Random();
        short[] z = new short[15];
        double[] x = new double[12];
        double[][] zz = new double[15][12];
        short current_value = 20;
        for (int i = 0; i < 15; i++) {
            z[i] = current_value;
            current_value--;
        }
        for (int i = 0; i < 12; i++) {
            x[i] = rnd.nextDouble(-14.0, 3.0);
        }
        for (int i = 0; i < 15; i++) {
            for (int j = 0; j < 12; j++) {
                if (z[i] == 13) {
                    zz[i][j] = Math.cos(Math.sin(Math.tan(x[j])));
                }
                if (z[i] == 7 | z[i] == 8 | z[i] == 9 | z[i] == 11 | z[i] == 14 | z[i] == 16 | z[i] == 19) {
                    zz[i][j] = Math.pow(Math.E,(Math.sin(Math.pow(x[j],1/3))));
                } else {
                    zz[i][j] = Math.atan(Math.pow((1/Math.pow(Math.E,Math.cos(Math.log(2*Math.abs(x[j]))))),2));
                }
            }
        }
        for (int i = 0; i < 15; i++) {
            for (int j = 0; j < 12; j++) {
                System.out.printf("%.5f", zz[i][j]);
                System.out.print("  ");
            }
            System.out.println();
        }
    }
}