 import java.util.Scanner;

public class SimpleColumnarTechnique {
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Enter Plain Text: ");
        String plainText = sc.nextLine();
        System.out.print("Enter no. of rows: ");
        int r1 = sc.nextInt();
        System.out.print("Enter no. of columns: ");
        int c1 = sc.nextInt();
        
        String[][] matrix = new String[r1][c1];
        
        int k = 0;
        for(int i = 0; i < r1; i++){
            for(int j = 0; j < c1; j++){
                if(k < plainText.length())
                    matrix[i][j] = String.valueOf(plainText.charAt(k++));
                else
                    matrix[i][j] = "_";
                System.out.print(matrix[i][j]);
            }
            System.out.println();
        }
        
        System.out.print("Enter order of columns: ");
        int[] choice = new int[c1];
        for(int i = 0; i< c1; i++){
            int z = sc.nextInt();
            choice[i] = (z);
        }
        String cipher = "";
        for(int j = 0; j < c1; j++){
            k = choice[j];
            for(int i = 0; i < r1; i++){
                cipher += matrix[i][k];
            }
        }
        cipher = cipher.replaceAll(" ", "");
        System.out.println("Cipher text: " + cipher);
    }
}
