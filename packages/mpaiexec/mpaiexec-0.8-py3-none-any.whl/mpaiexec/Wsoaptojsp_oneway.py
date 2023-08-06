WS:


Code:
package project17_example;

import javax.jws.Oneway;
import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

@WebService(serviceName = "Area51")
public class Area51 {
    public boolean feedback = false;
    
    @WebMethod(operationName = "oneWay")
    @Oneway
    public void oneWay() {
        feedback = true;
    }

    @WebMethod(operationName = "square")
    public Integer square(@WebParam(name = "num") int num) {
        if(feedback)
            return num * num;
        else
            return num;    
    }
}

JSP:
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <form action="" method="post">
            <input type="text" name="num1" required />
            <input type="submit" name="sq" value="Square" /><br><br>
            <input type="submit" name="ping" value="Ping" />
        </form>
        
        <%
            project17_example.Area51_Service service = new project17_example.Area51_Service();
            project17_example.Area51 port = service.getArea51Port();





            if (request.getParameter("ping") != null) {
                port.oneWay();
            } else if (request.getParameter("sq") != null) {
                out.println("Square: " + port.square(Integer.parseInt(request.getParameter("num1"))));
            }
        %>
    </body>
</html>
