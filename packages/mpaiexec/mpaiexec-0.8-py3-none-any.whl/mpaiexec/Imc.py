
import java.util.Scanner;

class MonoalphabeticCipher {

    public static void main(String[] args) {
        String key = "KEYWORDABCFGHIJLMNPQSTUVXZ";
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter Plain Text: ");
        String plainText = sc.next();
        String cipherText = encryption(plainText, key).toString();
        System.out.println("Encrypted: " + cipherText + "\nDecryption: " + decryption(cipherText, key));
    }

    public static StringBuffer encryption(String plainText, String key) {
        StringBuffer cipherText = new StringBuffer();
        plainText = plainText.toUpperCase();
        for (int i = 0; i < plainText.length(); i++) {
            int alphabetNo = plainText.charAt(i) - 65;
            char c = key.charAt(alphabetNo);
            cipherText.append(c);
        }

        return cipherText;
    }

    public static StringBuffer decryption(String cipherText, String key) {
        StringBuffer plainText = new StringBuffer();
        cipherText = cipherText.toUpperCase();
        for (int i = 0; i < cipherText.length(); i++) {
            char c = (char) (key.indexOf(cipherText.charAt(i)) + 65);
            plainText.append(c);
        }
        return plainText;
    }
}
