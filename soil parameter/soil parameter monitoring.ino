#include <SoftwareSerial.h>
#include <dht.h>                                    //importing temperature and humidity sensor library 
#define DEBUG 1                                     // change value to 1 to enable debuging using serial monitor  
#define dht_pin 12                                  
#define motor 6
int levelup=600;
int leveldown=300;
int probein = 1;                                  //analog pin 1 is used for taking readings from moisture sensor
double probevalue;

dht DHT;

SoftwareSerial esp8266Module(10, 11);               // RX, TX

String network = "MOTOG";                            // your access point SSID
String password = "passwordkyahai";                  // your wifi Access Point password
#define IP "184.106.153.149"                        // IP address of thingspeak.com
String GET = "GET /update?api_key=IFMAOPRGBJRWDDJ8";    // thingspeak channel key


void setup()
{
  if(DEBUG){
    Serial.begin(115200);                             // Setting hardware serial baud rate to 115200
  }  
  esp8266Module.begin(115200);                        
  delay(2000);
pinMode(motor, OUTPUT);
}
void loop() 
{
    setupEsp8266();                                   
    DHT.read11(dht_pin);
    double humi = DHT.humidity;          //reading humidity data from sensor
    double temp = DHT.temperature;       //reading temperature data from sensor
    Serial.print("Humidity :  ");
    Serial.println(humi);
    Serial.print("Temperature:  ");
    Serial.println(temp);
    probevalue = analogRead(probein);    //soil moisture data
    Serial.print("Soil Moisture: ");
    Serial.println(probevalue);
    updateTemp(String(temp), String(humi), String(probevalue));  
    delay(3000);
    water();
}


// Following function setup the esp8266, put it in station made and 
// connect to wifi access point.

void setupEsp8266()                                   
{
    if(DEBUG){
      Serial.println("Reseting esp8266");
    }
    esp8266Module.flush();
    esp8266Module.println(F("AT+RST"));
    delay(7000);
    if (esp8266Module.find("OK"))
    {
      if(DEBUG){
        Serial.println("Found OK");
        Serial.println("Changing espmode");
      }  
      esp8266Module.flush();
      changingMode();
      delay(5000);
      esp8266Module.flush();
      connectToWiFi();
    }
    else
    {
      if(DEBUG){
        Serial.println("OK not found");
      }
    }
}

// setting esp8266 to station mode

bool changingMode()
{
    esp8266Module.println(F("AT+CWMODE=1"));
    if (esp8266Module.find("OK"))
    {
      if(DEBUG){
        Serial.println("Mode changed");
      }  
      return true;
    }
    else if(esp8266Module.find("NO CHANGE")){
      if(DEBUG){
        Serial.println("Already in mode 1");
      }  
      return true;
    }
    else
    {
      if(DEBUG){
        Serial.println("Error while changing mode");
      }  
      return false;
    }
}


//connecting esp8266 to wifi access point

bool connectToWiFi()
{
  if(DEBUG){
    Serial.println("inside connectToWiFi");
  }  
  String cmd = F("AT+CWJAP=\"");
  cmd += network;
  cmd += F("\",\"");
  cmd += password;
  cmd += F("\"");
  esp8266Module.println(cmd);
  delay(15000);
  
  if (esp8266Module.find("OK"))
  {
    if(DEBUG){
      Serial.println("Connected to Access Point");
    }  
    return true;
  }
  else
  {
    if(DEBUG){
      Serial.println("Could not connect to Access Point");
    }  
    return false;
  }
}

//following function operates the motor based on soil moisture
void water()
{
  if (probevalue>levelup)
{
  digitalWrite(motor, LOW);
}
 else if(probevalue<leveldown)
{
  digitalWrite(motor, HIGH);
}

}
//sends sensor data to thingspeak.com (cloud)

void updateTemp(String voltage1,String voltage2,String voltage3)
{  
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += IP;
  cmd += "\",80";
  esp8266Module.println(cmd);
  delay(5000);
  if(esp8266Module.find("Error")){
    if(DEBUG){
      Serial.println("ERROR while SENDING");
    }  
    return;
  }
  cmd = GET + "&field1=" + voltage1 + "&field2=" + voltage2 + "&field3=" + voltage3 + "\r\n";
  esp8266Module.print("AT+CIPSEND=");
  esp8266Module.println(cmd.length());
  delay(15000);
  if(esp8266Module.find(">"))
  {
    esp8266Module.print(cmd);
    if(DEBUG){
      Serial.println("Data sent");
    }
  }else
  {
    esp8266Module.println("AT+CIPCLOSE");
    if(DEBUG){
      Serial.println("Connection closed");
    }  
  }
}
