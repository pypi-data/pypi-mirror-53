import java.util.Scanner;

public class RailFence {
    public static StringBuffer encryption(String plainText, int key){
        StringBuffer cipherText = new StringBuffer();
        String cipherRows[] = new String[key]; 
        for(int m = 0;m < key; m++)
            cipherRows[m] = new String();
        int i = 0;
        while(i < plainText.length()){
            int j = 0;
            while(j < key && i < plainText.length())
                cipherRows[j++] += plainText.charAt(i++);
            j--;
            while(j > 1 && i < plainText.length())
                cipherRows[--j] += plainText.charAt(i++);
        }
        for(int m = 0;m < cipherRows.length; m++)
            cipherText.append(cipherRows[m]); 
        return cipherText;
    }
    
    public static StringBuffer decryption(String cipherText, int key){
        StringBuffer plainText = new StringBuffer(); 
        String[][] rail = new String[key][cipherText.length()];
        for(int i = 0;i < key; i++){
            for(int j = 0;j < cipherText.length(); j++)
                rail[i][j] = "_";
        } 
        boolean dirDown = true;
        int row = 0, col = 0; 
        for(int i = 0;i < cipherText.length();i++){ 
            if(row == 0) 
                dirDown = true;
            if(row == key - 1)
                dirDown = false; 
            rail[row][col] = "*";
            col += 1; 
            if(dirDown) 
                row += 1;
            else 
                row -= 1;
        } 
        int index = 0;
        for(int i=0; i<key; i++){ 






            for(int j = 0; j<cipherText.length(); j++){
                if (rail[i][j].equals("*") && index < cipherText.length()){ 
                    rail[i][j] = String.valueOf(cipherText.charAt(index)); 
                    index++;
                }}}
        row = 0; col = 0;
        for(int i = 0; i < cipherText.length(); i++){
            if(row == 0) 
                dirDown = true;
            if(row == key-1)
                dirDown = false; 
            if(!rail[row][col].equals("*")){
                plainText.append(rail[row][col]);
                col += 1;
            }
            if(dirDown)
                row += 1;
            else 
                row -= 1;
        }
        return plainText;
    }
    
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter plain text: ");
        String P = sc.nextLine();
        System.out.print("Enter key: ");
        int K = sc.nextInt();
        String C = encryption(P, K).toString();
        System.out.println("\nCipher Text: " + C);
        System.out.println("Plain Text: " + decryption(C, K).toString());
    }
}
