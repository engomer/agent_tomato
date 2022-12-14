/*  
 *  GPRS/GSM Quadband Module (SIM900)
 *  
 *  Copyright (C) Libelium Comunicaciones Distribuidas S.L. 
 *  http://www.libelium.com 
 *  
 *  This program is free software: you can redistribute it and/or modify 
 *  it under the terms of the GNU General Public License as published by 
 *  the Free Software Foundation, either version 3 of the License, or 
 *  (at your option) any later version. 
 *  a
 *  This program is distributed in the hope that it will be useful, 
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of 
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License 
 *  along with this program.  If not, see http://www.gnu.org/licenses/. 
 *  
 *  Version:           2.0
 *  Design:            David Gascón 
 *  Implementation:    Alejandro Gallego & Marcos Martinez
 */

//Include arduPi library
#include "arduPi.h"

int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout);
int8_t sendATcommand(const char* ATcommand, const char* expected_answer, unsigned int timeout);

void power_on();


int8_t answer;
int onModulePin= 2;

char data[512];
int data_size;

char aux_str[100];
char aux;
int x = 0;

char pin[]="*******";
char apn[]="*******";
char user_name[]="*******";
char password[]="*******";

char url[ ]="test.libelium.com/test-get-post.php?a=1&b=2";

void setup(){

    pinMode(onModulePin, OUTPUT);
    Serial.begin(115200);   

    printf("Starting...\n");
    power_on();

    delay(3000);

    //sets the PIN code
    snprintf(aux_str, sizeof(aux_str), "AT+CPIN=%s", pin);
    sendATcommand(aux_str, "OK", 2000);

    delay(3000);

    while (sendATcommand2("AT+CREG?", "+CREG: 0,1", "+CREG: 0,5", 2000) == 0);


    // sets APN , user name and password
    sendATcommand("AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK", 2000);
    snprintf(aux_str, sizeof(aux_str), "AT+SAPBR=3,1,\"APN\",\"%s\"", apn);
    sendATcommand(aux_str, "OK", 2000);
    
    snprintf(aux_str, sizeof(aux_str), "AT+SAPBR=3,1,\"USER\",\"%s\"", user_name);
    sendATcommand(aux_str, "OK", 2000);
    
    snprintf(aux_str, sizeof(aux_str), "AT+SAPBR=3,1,\"PWD\",\"%s\"", password);
    sendATcommand(aux_str, "OK", 2000);

    while (sendATcommand("AT+SAPBR=1,1", "OK", 20000) == 0)
    {
        delay(5000);
    }


}
void loop(){
    // Initializes HTTP service
    answer = sendATcommand("AT+HTTPINIT", "OK", 10000);
    if (answer == 1)
    {
        // Sets CID parameter
        answer = sendATcommand("AT+HTTPPARA=\"CID\",1", "OK", 5000);
        if (answer == 1)
        {
            // Sets url 
            
            snprintf(aux_str, sizeof(aux_str), "AT+HTTPPARA=\"URL\",\"%s\"", url);
            answer = sendATcommand(aux_str, "OK", 5000);
            if (answer == 1)
            {
                // Starts GET action
                answer = sendATcommand("AT+HTTPACTION=0", "+HTTPACTION:0,200", 10000);
                
                if (answer == 1)
                {
                    x=0;
                    do{
                        sprintf(aux_str, "AT+HTTPREAD=%d,100", x);
                        if (sendATcommand2(aux_str, "+HTTPREAD:", "ERROR", 30000) == 1)
                        {
                            data_size = 0;
                            while(Serial.available()==0);
                            aux = Serial.read();
                            do{
                                data_size *= 10;
                                data_size += (aux-0x30);
                                while(Serial.available()==0);
                                aux = Serial.read();        
                            }while(aux != 0x0D);

                            printf("Data received: %d\n",data_size);

                            if (data_size > 0)
                            {
                                while(Serial.available() < data_size);
                                Serial.read();

                                for (int y = 0; y < data_size; y++)
                                {
                                    data[x] = Serial.read();
                                    x++;
                                }
                                data[x] = '\0';
                            }
                            else
                            {
                                printf("Download finished\n");    
                            }
                        }
                        else if (answer == 2)
                        {
                            printf("Error from HTTP\n");
                        }
                        else
                        {
                            printf("No more data available\n");
                            data_size = 0;
                        }
                        
                        sendATcommand("", "+HTTPACTION:0,200", 20000);
                    }while (data_size > 0);
                    
                    printf("Data received: %s\n",data);
                    
                }
                else
                {
                    printf("Error getting the url\n");
                }
            }
            else
            {
                printf("Error setting the url\n");
            }
        }
        else
        {
            printf("Error setting the CID\n");
        }    
    }
    else
    {
        printf("Error initializating\n");
    }
    
    sendATcommand("AT+HTTPTERM", "OK", 5000);

    delay(5000);

}

void power_on(){

    uint8_t answer=0;

    // checks if the module is started
    answer = sendATcommand("AT", "OK", 2000);
    if (answer == 0)
    {
        // power on pulse
        digitalWrite(onModulePin,HIGH);
        delay(3000);
        digitalWrite(onModulePin,LOW);

        // waits for an answer from the module
        while(answer == 0){  
            // Send AT every two seconds and wait for the answer   
            answer = sendATcommand("AT", "OK", 2000);    
        }
    }

}


int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout){

    uint8_t x=0,  answer=0;
    char response[100];
    unsigned long previous;

    memset(response, '\0', 100);    // Initialize the string

    delay(100);

    Serial.println(ATcommand);    // Send the AT command 


        x = 0;
    previous = millis();

    // this loop waits for the answer
    do{
        if(Serial.available() != 0){    
            response[x] = Serial.read();
            printf("%c",response[x]);
            x++;
            // check if the desired answer is in the response of the module
            if (strstr(response, expected_answer1) != NULL)    
            {
				printf("\n");
                answer = 1;
            }
        }
        // Waits for the asnwer with time out
    }
    while((answer == 0) && ((millis() - previous) < timeout));    

    return answer;
}



int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, 
const char* expected_answer2, unsigned int timeout){

    uint8_t x=0,  answer=0;
    char response[100];
    unsigned long previous;

    memset(response, '\0', 100);    // Initialize the string

    delay(100);

    Serial.println(ATcommand);    // Send the AT command 


        x = 0;
    previous = millis();

    // this loop waits for the answer
    do{        
        if(Serial.available() != 0){    
            response[x] = Serial.read();
            printf("%c",response[x]);
            x++;
            // check if the desired answer 1 is in the response of the module
            if (strstr(response, expected_answer1) != NULL)    
            {
				printf("\n");
                answer = 1;
            }
            // check if the desired answer 2 is in the response of the module
            if (strstr(response, expected_answer2) != NULL)    
            {
				printf("\n");
                answer = 2;
            }
        }
        // Waits for the asnwer with time out
    }while((answer == 0) && ((millis() - previous) < timeout));    

    return answer;
}

int main (){
    setup();
    while(1){
        loop();
    }
    return (0);
}
	