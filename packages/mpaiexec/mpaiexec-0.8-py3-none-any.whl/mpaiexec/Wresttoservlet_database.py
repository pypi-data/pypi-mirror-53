Restful WS:
package practice;
import java.sql.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("testing")
public class TestingRest {
    @Context
    private UriInfo context;
    public TestingRest() {
    }
    @GET
    @Produces(MediaType.TEXT_HTML)
    public String getHtml() {
        String res="";
        try{
            Class.forName("com.mysql.jdbc.Driver");
     

Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/mysql", "root", "root");
            Statement stmt=con.createStatement();
            ResultSet rs=stmt.executeQuery("Select id,name,marks from students");
            while (rs.next()){
                res += "Id: " + rs.getInt(1) + " Name: " + rs.getString(2) + " Marks: " + rs.getInt(3) + "<br> "; 
            }}
                catch(Exception e){
            res = e.getMessage();
        }
               return res;
    }
    @PUT
    @Consumes(MediaType.TEXT_HTML)
    public void putHtml(String content) {
    }}


Servlet:

package demo;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.WebTarget;

public class NewServlet extends HttpServlet {

    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
           int id = Integer.parseInt(request.getParameter("id")), marks = Integer.parseInt(request.getParameter("mid"));
           String name = request.getParameter("name"); 
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet NewServlet</title>");            
            out.println("</head>");
            out.println("<body>");
            TestingRest_JerseyClient client = new TestingRest_JerseyClient(); 
            out.println(client.getHtml());
            out.println("</body>");
            out.println("</html>");
        }
    }

    static class TestingRest_JerseyClient {

        private WebTarget webTarget;
        private Client client;


        private static final String BASE_URI = "http://localhost:8080/TestRest/webresources";

        public TestingRest_JerseyClient() {
            client = javax.ws.rs.client.ClientBuilder.newClient();
            webTarget = client.target(BASE_URI).path("testing");
        }

        public String getHtml() throws ClientErrorException {
            WebTarget resource = webTarget;
            return resource.request(javax.ws.rs.core.MediaType.TEXT_HTML).get(String.class);
        }

        public void putHtml(Object requestEntity) throws ClientErrorException {
            webTarget.request(javax.ws.rs.core.MediaType.TEXT_HTML).put(javax.ws.rs.client.Entity.entity(requestEntity, javax.ws.rs.core.MediaType.TEXT_HTML));
        }

        public void close() {
            client.close();
        }
    }
}
