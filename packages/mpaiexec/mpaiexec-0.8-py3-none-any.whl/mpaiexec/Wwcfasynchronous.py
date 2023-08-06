Webform1.aspx:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="WcfExample3.WebForm1" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
    <script type="text/javascript">
        function display() {
            Service2.GreetMessage(function(response){
                document.getElementById("Label1").innerHTML = response;
            });
        }
    </script>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <asp:ScriptManager ID="ScriptManager1" runat="server">
                <Services>
                    <asp:ServiceReference Path="~/Service2.svc" />
                </Services>
            </asp:ScriptManager>
            <asp:Label ID="Label1" runat="server"></asp:Label><br />
            <input id="Button1" type="button" value="Consume" onclick="display();" />
        </div>
    </form>
</body>
</html>
        
Service2.svc.cs:
using System.ServiceModel;
using System.ServiceModel.Activation;

namespace WcfExample3
{
    [ServiceContract(Namespace = "")]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Allowed)]
    public class Service2
    {
        
        [OperationContract]
        public string GreetMessage()
        {
            
            return "Hello world!";
        }
    }
}
