WS:
package si_example;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

@WebService(serviceName = "SimpleInterest")
public class SimpleInterest {
    @WebMethod(operationName = "calculateSI")
    public float calculateSI(@WebParam(name = "p") float p, @WebParam(name = "r") float r, @WebParam(name = "t") float t) {
        return p*r*t/100;
    }
}

Servlet:
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.ws.WebServiceRef;
import si_example.SimpleInterest_Service;

public class SimpleInterestConsumer extends HttpServlet {

    @WebServiceRef(wsdlLocation = "WEB-INF/wsdl/localhost_8080/SimpleInterest/SimpleInterest.wsdl")
    private SimpleInterest_Service service;


    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
            int p = 1000, r = 2, t = 4;
            float si = calculateSI(p, r, t);
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head><title>Servlet SimpleInterestConsumer</title></head><body>");
            out.println("<h3>Principle Amount: " + p + ";Rate: " + r + ";Time: " + t + "</h3><br><h1>Result: " + si +"</h1>");
            out.println("</body></html>");
        }
    }

 private float calculateSI(float p, float r, float t) {
        // Note that the injected javax.xml.ws.Service reference as well as port objects are not thread safe.
        // If the calling of port operations may lead to race condition some synchronization is required.
        si_example.SimpleInterest port = service.getSimpleInterestPort();
        return port.calculateSI(p, r, t);
    }
}

