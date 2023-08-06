import java.util.Scanner;

public class CaesarCipher {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Enter plain text: ");
        String P = sc.nextLine();
        System.out.print("Enter key: ");
        int K = sc.nextInt();
        
        String C = encryption(P, K).toString();
        System.out.println("\nCipher Text: " + C);
        System.out.println("Plain Text: " + decryption(C, K).toString());
    }
    
    public static StringBuffer encryption(String p, int k){
        StringBuffer CipherText = new StringBuffer();
        for(int i = 0; i < p.length(); i++){
            int pascii = p.charAt(i);
            char pchar = p.charAt(i);
            if(pascii >= 97 && pascii <= 122){
                pchar = (char) ((pascii + k - 97)%26 + 97);
            }
            else if(pascii >= 65 && pascii <= 90){
                pchar = (char) ((pascii + k - 65)%26 + 65);
            }
            CipherText.append(pchar);
        }
        return CipherText;
    }
    
    public static StringBuffer decryption(String p, int k){
        StringBuffer CipherText = new StringBuffer();
        for(int i = 0; i < p.length(); i++){
            int pascii = p.charAt(i);
            char pchar = p.charAt(i);
            if(pascii >= 97 && pascii <= 122){
                if(pascii - k < 97)
                    pchar = (char) (122 + pascii + k - 96);
                else
                    pchar = (char) (pascii - k);
            }
            else if(pascii >= 65 && pascii <= 90){
                if(pascii - k < 65)
                    pchar = (char) (90 + pascii - k - 64);
                else
                    pchar = (char) (pascii - k);
            }
            CipherText.append(pchar);
        }
        return CipherText;
    }
}
