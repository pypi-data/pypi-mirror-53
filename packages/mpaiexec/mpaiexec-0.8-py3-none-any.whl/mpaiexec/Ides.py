import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

public class DES {
    public static void main(String[] args) throws Exception {
        KeyGenerator mygenerator = KeyGenerator.getInstance("DES");
        SecretKey myDesKey = mygenerator.generateKey();
        Cipher desCipher = Cipher.getInstance("DES");
        desCipher.init(Cipher.ENCRYPT_MODE, myDesKey);
        byte[] myBytes = "This message is important".getBytes();
        byte[] myEncryptedBytes = desCipher.doFinal(myBytes);
        desCipher.init(Cipher.DECRYPT_MODE, myDesKey);
        byte[] myDecryptedBytes = desCipher.doFinal(myEncryptedBytes);
        
        System.out.println("Encrypted Text: " + myEncryptedBytes + "\nDecrypted Text: " + new String(myDecryptedBytes));
    }
