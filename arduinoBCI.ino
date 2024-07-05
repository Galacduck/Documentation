#define sensorPin1 Α0

int inputValue1 = 0;

String inputString = "";
boolean stringComplete = false;

void setup() {
// put your setup code here, to run once:
    Serial.begin(9600);
    while (!Serial) {
        ;   
    }
    while (Serial.available() <= 0)
    {
        sendStatus();
        delay (300);
    }
}

void loop() {
// put your main code here, to run repeatedly
    if (stringComplete)
    {
        if (inputString.startsWith("status"))
        {
            sendStatus();
        }
        else
        {
            Serial.println("Invalid Command");
        }
    
    stringComplete = false;
    inputString = "";

    }
    delay(10);
    if(Serial.available() > 0) serialEvent();
}

void sendStatus()
{
    char buffer[100];
    inputValue1 = analogRead(sensorPin1);
    sprintf(buffer, "Analog input %d is %d", sensorPin1, inputValue1)
    Serial.println(buffer);
}

void serialEvent()
{
    while(Serial.available())
    {
        char inChar = (char)Serial.read();
        inputString += inChar;
        if (inChar == '\n')
        {
            stringComplete = true;
        }
    }
}

