import java.util.Scanner;

public class DiffieHellmanAlgorithm {
    static Scanner sc;
    public static void main(String[] args) {
        int p, q, x, y, a, b, k1, k2;
        sc = new Scanner(System.in);
        System.out.println("Enter a prime no.(p): ");
        p = sc.nextInt();
        System.out.println("Enter a prime no.(q): ");
        q = sc.nextInt();
        
        System.out.println("Enter A's Secret Key: ");
        x = sc.nextInt();
        while(!(x < q)){
            System.out.println("Enter A's Secret Key: ");
            x = sc.nextInt();
        }
        
        System.out.println("Enter B's Secret Key: ");
        y = sc.nextInt();
        while(!(y < q)){
            System.out.println("Enter B's Secret Key: ");
            y = sc.nextInt();
        }
        
        a = (int)Math.pow(p, x)%q;
        b = (int)Math.pow(p, y)%q;
        
        k1 = (int)Math.pow(b, x)%q;
        k2 = (int)Math.pow(a, y)%q;
        
        if(k1 == k2){
            System.out.println("K1 and K2 Are Equal.");
        }
        else{
            System.out.println("K1 and K2 Are Not Equal.");
        }
    }   
}
