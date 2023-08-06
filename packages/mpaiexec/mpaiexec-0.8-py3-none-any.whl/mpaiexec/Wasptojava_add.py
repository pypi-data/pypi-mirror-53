ASPWS:
using System.Web.Services;

namespace NewWS
{
    [WebService(Namespace = "http://tempuri.org/")]

    [WebServiceBinding(ConformsTo = WsiProfiles.BasicProfile1_1)]

[System.ComponentModel.ToolboxItem(false)]
    public class WebServiceExample : System.Web.Services.WebService
    {
        [WebMethod]
        public int add(int a, int b)
        {
            return a + b;
        }
    }
}

JavaApp:
public class ASPWebService {
    public static void main(String[] args){
        System.out.println("Addition of 512 and 256 is " + add(512, 256));
    }

    private static int add(int a, int b) {
        org.tempuri.WebServiceExample service = new org.tempuri.WebServiceExample();
        org.tempuri.WebServiceExampleSoap port = service.getWebServiceExampleSoap();
        return port.add(a, b);
    }
