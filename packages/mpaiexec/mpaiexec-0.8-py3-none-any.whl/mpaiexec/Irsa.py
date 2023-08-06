import java.util.*;
import java.math.*;

public class TY_RSA {
   public static void main(String [] args)
    {
        BigInteger one,p,q,E,D,n,P,Q;
        Scanner sc=new Scanner(System.in);
        Scanner t=new Scanner(System.in);
        System.out.println("Enter A's Prime number:");
        p=sc.nextBigInteger();
        System.out.println("Enter B's Prime number:");
        q=sc.nextBigInteger();
        n=p.multiply(q);
        P=p.subtract(BigInteger.ONE);
        Q=q.subtract(BigInteger.ONE);
        int x=0;
        do{
            System.out.println("Enter public key");
            E=sc.nextBigInteger();
            if(((P.gcd(E)).equals(BigInteger.ONE))&&((Q.gcd(E)).equals(BigInteger.ONE)))
                x++;
        }while(x==0);
        for(int i=1;;i++){
            D=new BigInteger(String.valueOf(i));
            if(((D.multiply(E)).mod(P.multiply(Q))).equals(BigInteger.ONE))
                break;
        }
        System.out.println("Enter Plain Text:");
        String in=" ",out=" ",text=t.nextLine();
        for(int i=0;i<text.length();i++){
            BigInteger T=new BigInteger(String.valueOf((int)(text.charAt(i))));
            BigInteger O,TF;
            O=T.modPow(E,n);
            out+=(char)O.intValue();
            TF=O.modPow(D,n);
            in+=(char)TF.intValue();
        }
        System.out.println("Encrypted text:"+out);
        System.out.println("Decrypted text:"+in);
    }
}

