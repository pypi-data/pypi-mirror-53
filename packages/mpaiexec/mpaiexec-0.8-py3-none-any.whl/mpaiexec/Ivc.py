
import java.util.Scanner;

class VernamCipher {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter Plain Text: ");
        String plainText = sc.next();
        System.out.print("Enter Key: ");
        String key = sc.next();
        String cipherText = encryption(plainText, key).toString();
        System.out.println("Encrypted: " + cipherText + "\nDecryption: " + decryption(cipherText, key));
    }

    public static StringBuffer encryption(String plainText, String key) {
        StringBuffer cipherText = new StringBuffer();
        
        if(plainText.length() == key.length()){
            for (int i = 0; i < plainText.length(); i++) {
                char c = (char)(plainText.charAt(i) ^ key.charAt(i));
                cipherText.append(c);
            }
        }
        
        return cipherText;
    }

    public static StringBuffer decryption(String cipherText, String key) {
        return encryption(cipherText, key);
    }
}
