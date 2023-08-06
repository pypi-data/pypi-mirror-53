import java.security.MessageDigest;
import javax.xml.bind.DatatypeConverter;

public class MD5
{
    public static String getHash(byte[] inputBytes,String algorithm)
    {
        String hashvalue =" ";
        try{
            MessageDigest messageDigest = MessageDigest.getInstance(algorithm);
            messageDigest.update(inputBytes);
            byte[] digestedBytes = messageDigest.digest();
            //print hexbinary return the value in uppercase.
            hashvalue = DatatypeConverter.printHexBinary(digestedBytes).toUpperCase();

        }
        catch(Exception e)
        {
        }
        return hashvalue;
    }
    public static void main(String[]args)
    {
        String somestring = "this is some string";
        System.out.println(getHash(somestring.getBytes(), "SHA-1"));
    }
}
