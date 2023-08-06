WebService:
package tempconversion_example;
import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

@WebService(serviceName = "ConvertTemperature")
public class ConvertTemperature {
    @WebMethod(operationName = "celsiusToFahrenheit")
    public float celsiusToFahrenheit(@WebParam(name = "celsius") float celsius) {
        return celsius*1.8f + 32;
    }
    @WebMethod(operioatnName = "fahrenheitToCelsius")
    public float fahrenheitToCelsius(@WebParam(name = "fahrenheit") float fahrenheit) {
        return (fahrenheit - 32)/1.8f;
    }
}

JavaApp:
public class TemperatureConversionConsumer {
    public static void main(String[] args){
        System.out.println("Celsius is 37, Fahrenheit is: " + celsiusToFahrenheit(37));
        System.out.println("Fahrenheit is 100, Celsius is: " + fahrenheitToCelsius(100));
    }
    private static float celsiusToFahrenheit(float celsius) {
 tempconversion_example.ConvertTemperature_Service service = new tempconversion_example.ConvertTemperature_Service();
        tempconversion_example.ConvertTemperature port = service.getConvertTemperaturePort();


        return port.celsiusToFahrenheit(celsius);
    }
    private static float fahrenheitToCelsius(float fahrenheit) {
        tempconversion_example.ConvertTemperature_Service service = new tempconversion_example.ConvertTemperature_Service();
        tempconversion_example.ConvertTemperature port = service.getConvertTemperaturePort();
        return port.fahrenheitToCelsius(fahrenheit);
    }
}






