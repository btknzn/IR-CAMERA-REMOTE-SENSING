//This code is written by BATU KAAN ÖZEN
//This code can detect maximal 4 person
// MLX90640_API and MLX90640_I2C_Driver are pre-written code.They are making embedded comunication
//arduino_secrets is the linkf of where you will write your data and also your wifi ıd and password
// THİS CODE SHOULD START İN ONE ROOM WİTHOUT HUMAN about 12 hours to arrange best filter for enviroment
// THİS CODE İS WRİTTEN FOR TEENSY 3.6 board with MLX90640 IR ARRAY (SPARKFUN 110-75 Degrees)  AND ADAFRUİT AİRLİFT WİFİ
// MLX90640 sparkfun is conected to Teensy 3.6 for I2C  18.Teensy pin--> SDA 19.Teensy pin-->SCL
// ADAFRUİT AİRLİFT WİFİ is connected to Teensy 3.6 for SPI Communuicaition 13.Teensy pin --> SCK 12.""--> MISO 11.Teensy pin-->MOSI 5.Teensy pin--> CS 9.Teensy pin-->BUSY 6.Teensy pin--> REST
// AİM OF THİS SYSTEM İS THAT:
// FİRST TAKE IMAGE FİND CLUSTER ON DATA AND THEN SEND THE SERVER that how many clusters, how big are they and also how is their movement
// IT send like Amountofcluster-how big first cluster- how big second cluster- how big thir cluster-how big first clusters' movement-how big second clusters' movement- how big thir clusters' movement
// If you have any question, please do not hesitate to ask. Email=ozenbatukaan@gmail.com Telefon=+90 531 742 68 18( you can reach me via Whatsapp)
#include <Wire.h>
#include "MLX90640_API.h"
#include "MLX90640_I2C_Driver.h"
#include <SPI.h>
#include <WiFiNINA.h> 
const byte MLX90640_address = 0x33;
//Default 7-bit unshifted address of the MLX90640
#define TA_SHIFT 8 
//Default shift for MLX90640 in open air
float mlx90640To[768];
// mlx90640TO is IR CAMERA Pixels
paramsMLX90640 mlx90640;
//parsed data
float Image[32][24];
//IT IS IMAGE ON WHICH I AM GOİNG TO MAKE OPERATİON
float average[32][24];
// IT IS AVERAGE IMAGE for detecting noises
float averagecounter=0;
// WHEN WE APPLY AVERAGE IMAGE WE APPLY AVERAGING
float incomingByte = 0;
float center[2][2][10];
//above is declaration of both centers.
// WHEN WE DETECT SPEED WE WILL SUBRATC FROM FIRST CENTER TO ANOTHER ONE.
float data[30];
  // between data[0] and data[9] are amount of CLUSTER
  //0000000000=0
  //0000000001=1
  //0000000010=2
  //0000000100=3
  //0000001000=4
  //0000010000=5
  //0000100000=6
  //0001000000=7
  //0010000000=8
  //0100000000=9
  //1000000000=10
  // between data[10] and data[19] are how big these cluster
  // betweem data [20] and data[29] ara  location difference in these arrays
  // When our code looking locatioon difference first it calculate cluster on first Image and find its center and then ıt calculate center of clusterse
  //and then ıt checks  on new ımage its cluster center and find smallest difference on each cluster and give them smallest value
  // In case of lack of  Cluster, this system is going to give 0 for this cluster location difference
  // AND THİS SYSTEM GOİNG TO SEND DATA[30] array on serial port.
  // BUT to increase the success of Machine Learning part. our code we are going to convert data like that.( IT CAN DETECT 0cluster,1cluster,2clusters and 3clusters.Other number of cluster is going to be ignored and system is going to take first 3 bigest cluster.)
  //Numberofcluster(0-3)-How big first cluster- How big second cluster- how big third cluster-how big first clusters' movement-how big second clusters' movement-how big third clusters' movement 
// The reason why we 2 size amountofCluster is that we want to detect our movement.
int amountOfCluster[2];
int object[10][32][24];
int detectionMatrix[32][24];
int onedetectionBefore[32][24];
int numberofCluster;
#define SPIWIFI       SPI  // The SPI port
#define SPIWIFI_SS     5   // Chip select pin
#define ESP32_RESETN   6   // Reset pin
#define SPIWIFI_ACK    9   // a.k.a BUSY or READY pin
#define ESP32_GPIO0   -1
int keyIndex = 0;
int status = WL_IDLE_STATUS;
int clientData[7]; 
IPAddress server(193,196,175,153);
WiFiClient client;
#include "arduino_secrets.h" 
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
void setup()
{
  // First we initilize Wifi module
  initilizeWireless();
  // After we initilize our Camera
  initilizeCamera();
}

void loop()
{
  // This code make Feature set which I mentioned above (data[30])
  makeDataset();
  // This part we convert our data[30] to small matrix clientData[7] Which has information about How big first cluster- How big second cluster- how big third cluster-how big first clusters' movement-how big second clusters' movement-how big third clusters' movement 
  convert();
  // After converting our data, We send clientData to our server 
  sendDataServer();
}

void convert(){
  // First we initilizing our clientData[0] to number of cluster
  clientData[0] = data[0]*1+data[1]*2+data[2]*3+data[3]*4+data[4]*5+data[5]*6+data[6]*7+data[7]*8+data[8]*9;
  // this code(sortVoid()) find three biggest clusters on IR ımage
  sortVoid();
  // afrer how big first cluster
  clientData[1] = data[19];
  // after how big second cluster
  clientData[2] = data[18];
  // after how big thirc cluster
  clientData[3] = data[17];
  // after how big movement of first cluster
  clientData[4] = data[29];
  // after how big movement of second cluster
  clientData[5] = data[28];
  // after how big movement of thir cluster
  clientData[6] = data[27];

}
// FINDING THREE BİG CLUSTERS in Image
void sortVoid(){
  int holder;
  for (int i=0;i<9;i++){
    for(int j=0;j<9-i;j++){
      if ( data[j+10] > data[j+11]){
        int holder;
        holder = data[j+11];
        data[j+11]= data[j+10];
        data[j+10] = holder;
        holder = data[j+21];
        data[j+21] = data[j+20];
        data[j+20] = holder; 
        
      }
    }
  }
  
}
//THİS CODE(sendDataServer) SEND OUR DATA TO SERVER
void sendDataServer(){
    //Serial.println("connected");
    int index;
    int i=77;
    //for(int i=1;i<4;i++){
    client.connect(server,80);
    client.print("GET /es_lebt_in.php?DEV=0815&STATE=");
    client.print(i);
    client.print("&KEY=");
      for(int j=0;j<7;j++){
        client.print(clientData[j]);
        client.print("-");
      }
    client.println();
    //}
    //if (client.connect(server,80)){
    //  client.println("GET /es_lebt_in.php?DEV=0815&STATE=99&KEY=XXX");
    //}
    //else {
      //Serial.println("server başarısızı");
    //}
}

// This code initilize wireless connection
void initilizeWireless(){
  Serial.begin(9600);
  WiFi.setPins(SPIWIFI_SS, SPIWIFI_ACK, ESP32_RESETN, ESP32_GPIO0, &SPIWIFI);
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }
  String fv = WiFi.firmwareVersion();
  if (fv < "1.0.0") {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WEP network, SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, keyIndex, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
  Wire.begin();
  Wire.setClock(400000); //Increase I2C clock speed to 400kHz
  //while (!Serial); //Wait for user to open terminal
  //Serial.println("MLX90640 IR Array Example");
  if (isConnected() == false)
  {
    Serial.println("MLX90640 not detected at default I2C address. Please check wiring. Freezing.");
    while (1);
  }
  int status;
  uint16_t eeMLX90640[832];
  status = MLX90640_DumpEE(MLX90640_address, eeMLX90640);
  if (status != 0)
    //Serial.println("Failed to load system parameters");

  status = MLX90640_ExtractParameters(eeMLX90640, &mlx90640);
  if (status != 0)
    //Serial.println("Parameter extraction failed");

  //Once params are extracted, we can release eeMLX90640 array
  if (client.connect(server,80)){
    //Serial.println("connected");
    client.println("GET /es_lebt_in.php?DEV=0815&STATE=99&KEY=XXX");
  }
  else {
    //Serial.println("server başarısızı");
  }
  
}
// this code make data set
void makeDataset(){
  //FIRSTLY I TOOK ONE IR IMAGE(TEMPETERAL IMAGE)
  takeImageFromIRcamera();
  // I DETECT AVERAGE OF THİS IMAGE EVERY TİME IT DETECTS AVERAGE VALUE OF IMAGE AND EACH TIME IN LOOP CHANGE IT
  FINDaverage();
  //FOR DETECTİNG IMAGE MY CODE WORKS LIKE  noiseREDUCTEDIMAGE = IMAGEONSCREEN - AVERAGEDIMAGE(WE SHOULD AVERAGE MY IMAGE IN LONG TIME);
  noiseReduction();
  // WE SEDN OUR IMAGE İN SERİAL PORT
  
  //Serial.println("1.");
  //sendImageFromSerial();
   matrixInitiliz();
  // FIRST WE FİND tHE CLUSTERS ON IMAGE
   findDatasonImage();
  //sendObject();
  // AND thEN FIND NUMBER OF CLUStER
  putAmoutofcluster();
  // FIND SIZE OF CLUSTER
  putMassofcluster();
  // FIND OUR FIRST CLUSTER CENTER
   initilizeCenters();
  // FIND AMOUNT OF CLUSTER CENTER AND SEND THEM LİKE 00000000=0 or 00000=1 like that
  putAmoutofcluster();
  //TAKE NEW IMAGE
  takeImageFromIRcamera();
  //SAME AS ABOVE FINDAVERAGE
  FINDaverage();
  //SAME AS ABOVE NOSİSE REDUCTİON
  noiseReduction();
  //Serial.println("2.");
  // SAME AS ABOVE FINDDATAONIMAGE
  findDatasonImage();
  //sendImageFromSerial();
  // WE INITILIZATE SECOND CENTER OF CLUSTER
  initilizeSecondCenters();
  //outPuttwoImageCenter();
  // WE CALCULATE MOVEMENT OF CLUSTERS.( LIKE FIRST cluster center minus second cluster centers )
  putMovement();
  // WE SEND ALLL dATA SET FROM SERIAL
  sendDatasetFromSerial();
}
// This code take IR ımage from camera
void takeImageFromIRcamera(){
  long startTime = millis();
  for (byte x = 0 ; x < 2 ; x++)
  {
    uint16_t mlx90640Frame[834];
    int status = MLX90640_GetFrameData(MLX90640_address, mlx90640Frame);

    float vdd = MLX90640_GetVdd(mlx90640Frame, &mlx90640);
    float Ta = MLX90640_GetTa(mlx90640Frame, &mlx90640);

    float tr = Ta - TA_SHIFT; //Reflected temperature based on the sensor ambient temperature
    float emissivity = 0.95;

    MLX90640_CalculateTo(mlx90640Frame, &mlx90640, emissivity, tr, mlx90640To);
  }
  long stopTime = millis();
  convertImageArray(mlx90640To);
}

// This code send data[30] to serial to inform about Dataset
void sendDatasetFromSerial(){
 //Serial.println();
 for(int i=0;i<3;i++){
  for(int j=0;j<10;j++){
    int location;
    location = i*10+j;
    Serial.print(int(data[location]));
    Serial.print("-");
    
  }
  Serial.println();
  Serial.println();
  Serial.println();
  
 }
  
}



// THİS CODE MAKE one dimention array which comes from our IR cammera embedded code converting two dimention array

void convertImageArray(float dataFromCamera[768]){
  int index = 0;
  for (int i = 0 ; i < 24;i++){
    for (int j = 0; j < 32;j++){
      index=i*32+j;
      Image[j][i]=dataFromCamera[index];
    }
  }
  
}

//This code initilize camera
void initilizeCamera(){
  Wire.begin();
  Wire.setClock(400000); //Increase I2C clock speed to 400kHz
  Serial.begin(115200); //Fast serial as possible

  //while (!Serial); //Wait for user to open terminal
  //Serial.println("MLX90640 IR Array Example");

  if (isConnected() == false)
  {
    Serial.println("MLX90640 not detected at default I2C address. Please check wiring. Freezing.");
    while (1);
  }

  //Get device parameters - We only have to do this once
  int status;
  uint16_t eeMLX90640[832];
  status = MLX90640_DumpEE(MLX90640_address, eeMLX90640);
  if (status != 0)
    Serial.println("Failed to load system parameters");

  status = MLX90640_ExtractParameters(eeMLX90640, &mlx90640);
  if (status != 0)
    Serial.println("Parameter extraction failed");

  //Once params are extracted, we can release eeMLX90640 array

  //MLX90640_SetRefreshRate(MLX90640_address, 0x02); //Set rate to 2Hz
  MLX90640_SetRefreshRate(MLX90640_address, 0x03); //Set rate to 4Hz
  //MLX90640_SetRefreshRate(MLX90640_address, 0x07); //Set rate to 64Hz
}

//this code check our camera connection

boolean isConnected()
{
  Wire.beginTransmission((uint8_t)MLX90640_address);
  if (Wire.endTransmission() != 0)
    return (false); //Sensor did not ACK
  return (true);
}

void sendImageFromSerial(){
  for (int i=0 ; i < 24 ;i++){
    for (int j=0; j<32; j++){
      Serial.print((Image[j][i]));
      Serial.print(",");
    }
    Serial.println();
  }
  Serial.println();
  Serial.println();
  Serial.println();
}


//THİS CODE İS NOT IMPORTANT

void outPuttwoImageCenter(){
  //Serial.println();
  //Serial.print("First Image center cordinate  ");
  for (int i=0; i<10;i++){
    //Serial.print("        ");
    //Serial.print(i);
    //Serial.print(":");
    //Serial.print(center[0][0][i]);
    //Serial.print(",");
    //Serial.print(center[0][1][i]);
  }
  //Serial.println();
  //Serial.print("Second Image center cordinate  ");
  for (int i=0; i<10;i++){
    //Serial.print("        ");
    //Serial.print(i);
    //Serial.print(":");  
    //Serial.print(center[1][0][i]);
    //Serial.print(",");
    //Serial.print(center[1][1][i]);
  }
  //Serial.println();
}


// THIS CODE CALCULATE  AMOUNT OF TWO CENTERS DIFFERENCE AND İNİTİLİZE EACH CLUSTERS LOCATİON DİFFERENCE FIRST IMAGE AND SECOND IMAGE CLUSTER CENTER
void putMovement(){
  float distance[amountOfCluster[1]][amountOfCluster[0]];
  for (int i=0; i<amountOfCluster[0];i++){
    for (int j=0; j<amountOfCluster[1];j++){
      float xdistance;
      float ydistance;
      xdistance = (center[0][0][i]-center[1][0][j]);
      ydistance = (center[1][1][i]-center[1][1][j]);
      distance[j][i] = (xdistance*xdistance+ydistance*ydistance);
    }
  }
  float minDistance[amountOfCluster[0]];
  for (int i=0;i<amountOfCluster[0];i++){
    minDistance[i]=100000;
  }
  for (int i=0; i<amountOfCluster[0];i++){
    for (int j=0; j<amountOfCluster[1];j++){
        if( distance[j][i]<minDistance[i])
          minDistance[i] = distance[j][i];
      }
    }
  for (int i=0; i<amountOfCluster[0];i++){
    data[20+i] = minDistance[i];
  }
  for ( int i=0; i<10;i++){
    if (data[20+i] ==100000){
      data[20+i] =0;
    }
  }
  
}


// THIS CODE FIND THE CLUSTER CENTERS
void initilizeCenters(){
  amountOfCluster[0] = numberofCluster;
  for(int i=0;i<numberofCluster;i++){
    center[0][0][i]= centerLocationOnX(i);
    center[0][1][i]= centerLocationOnY(i);
  }
  //for (int i=0; i<10;i++){
  //  Serial.print(center[0][0][i]);
  //  Serial.print("X");
  //}
  //Serial.println();
  //for (int i=0; i<10;i++){
  //  Serial.print(center[0][1][i]);
   // Serial.print("Y");
  //}
}

// THIS CODE FIND SECOND CLUSTER CENTERS
void initilizeSecondCenters(){
  //Serial.println("selam");
  amountOfCluster[1] = numberofCluster;
  for(int i=0;i<numberofCluster;i++){
    center[1][0][i]= centerLocationOnX(i);
    center[1][1][i]= centerLocationOnY(i);
  }
  //Serial.println();
  //for (int i=0; i<10;i++){
  //  Serial.print(center[1][0][i]);
  //  Serial.print("X");
  //}
  //Serial.println();
  //for (int i=0; i<10;i++){
  //  Serial.print(center[1][1][i]);
  //  Serial.print("Y");
  //}
}
// FIND CENTER ON X AXİS
float centerLocationOnX(int i){
  int massofObject = 0;
  massofObject = calculateMass(i);
  int moment = 0;
  for(int t=0;t<24;t++){
    for(int j=0;j<32;j++){
        moment = moment + object[i][j][t]*j;
      }
  }
  int average= 0;
  average = moment/massofObject;
  return average; 
}

// FIND CENTER ON Y AXIS
float centerLocationOnY(int i){
  int massofObject = 0;
  massofObject = calculateMass(i);
  int moment = 0;
  for(int t=0;t<24;t++){
    for(int j=0;j<32;j++){
        moment = moment + object[i][j][t]*t;
      }
  }
  int average = 0;
  average = moment/massofObject;
  //Serial.println(average);
  return average;
}




// THIS CODE PUT AMOUNT OF CLUSTER IN DATA SET AS YOU BELOW SEE.
void putAmoutofcluster(){
  //0000000000=0
  //0000000001=1
  //0000000010=2
  //0000000100=3
  //0000001000=4
  //0000010000=5
  //0000100000=6
  //0001000000=7
  //0010000000=8
  //0100000000=9
  //1000000000=10
 for (int i=0;i<10;i++){
  if (i == numberofCluster-1){
    data[i]=1;
  }
  else {
    data[i]=0;
  }
 }
}


// THIS CODE PUT CENTER OF EACH CLUSTER
void putMassofcluster(){
for(int i=0;i<10;i++){
  data[i+10]=calculateMass(i);
}
}

// THIS CODE CALCULATE THE  MASS OF CLUSTER
int calculateMass(int i){
  int Mass =0;
    for (int k=0 ; k < 24 ;k++){
      for (int j=0; j<32; j++){
        Mass = Mass+ object[i][j][k];
      }
    }
return Mass;
}

//THIS CODE INITILIZE THE OBJECT AS 0 BECAUSE WE USE THIS FUNCTİON EACH TIME NEW
void matrixInitiliz(){
  for (int b=0;b<10;b++){
    for(int i=0;i<24;i++){
      for(int j=0;j<32;j++){
        object[b][j][i]=0;
      }
    }
  }
  for (int i = 0 ; i < 24;i++){
    for (int j = 0; j < 32;j++){
      detectionMatrix[j][i]=0;
    }
   }
  for (int i =0 ; i<30;i++){
    data[i]=0;
  }
  for (int i=0; i<10;i++){
    for(int j=0;j<2;j++){
      for(int k=0;k<2;k++){
        center[k][j][i]=0;
      }
    }
  }
  
}

// THIS CODE SEND DETECTİON
void sendDetectionMatrix(){
  for (int i=0 ; i < 24 ;i++){
    for (int j=0; j<32; j++){
      //Serial.print(int(detectionMatrix[j][i]));
      //Serial.print(",");
    }
    //Serial.println();
  }
  //Serial.println();
  //Serial.println();
  //Serial.println();
}

// THUS CODE SEND OBJECTS
void sendObject(){
  for(int t=0 ; t<10;t++){
  //Serial.print(t);
  //Serial.println(".obect over there");
  for (int i=0 ; i < 24 ;i++){
    for (int j=0; j<32; j++){
      //Serial.print(int(object[t][j][i]));
      //Serial.print(",");
    }
    //Serial.println();
  }
  //Serial.println();
  //Serial.println();
  //Serial.println();

}
}

// THIS CODE DETECT CLUSTER ON IMAGE AND FIND AMOUNT OF CLUSTER
void findDatasonImage(){
  boolean ImageControl;
  numberofCluster=0;
  for (int i=0;i<24;i++){
      for(int j=0;j<32;j++){
         ImageControl = beforedetected(j,i);
         if ( ImageControl){
            continue;
         }   
         clusterAlgorithm(j,i,numberofCluster);  
         //sendDetectionMatrix();
         numberofCluster = numberofCluster +1;
        // Serial.print("number of clusters");
        // Serial.println(numberofCluster);   
      }
  } 
}

//THIS CODE HELPS findDatasonImage
boolean beforedetected(int x, int y){
  if (detectionMatrix[x][y]==0 and Image[x][y]==1){
    return false;
  }
  return true;
}


// FIND EACH MEMBER OF CLUSTERS
void clusterAlgorithm(int x, int j, int numberofCluster ){
   
   object[numberofCluster][x][j]=1;
   detectionMatrix[x][j] =1;
 
  if((x-1>=0) and (j-1>=0) and (detectionMatrix[x-1][j-1]==0) and (Image[x-1][j-1]==1) ){
     
    clusterAlgorithm(x-1,j-1,numberofCluster);
  }
  
  if((j-1>=0) and (detectionMatrix[x][j-1]==0) and  (Image[x][j-1]==1) ){
     
    clusterAlgorithm(x,j-1,numberofCluster);
  }
  
  if((x+1<=32) and (j-1>=0) and (detectionMatrix[x+1][j-1]==0) and (Image[x+1][j-1]==1 )){
    
    clusterAlgorithm(x+1,j-1,numberofCluster); 
  }
  
  if((x+1<=32) and (detectionMatrix[x+1][j]==0) and (Image[x+1][j]==1 ) ){
    
    clusterAlgorithm(x+1,j,numberofCluster); 
  }
  
  if((x+1<=32) and (j+1<=24) and (detectionMatrix[x+1][j+1]==0) and (Image[x+1][j+1]==1 )){
     
    clusterAlgorithm(x+1,j+1,numberofCluster);
  }
  
  if((j+1<=31) and (detectionMatrix[x][j+1]==0)  and (Image[x][j+1]==1)){
    
    clusterAlgorithm(x,j+1,numberofCluster); 
  }

  if((x-1>=0) and (j+1<=24) and (detectionMatrix[x-1][j+1]==0) and (Image[x-1][j+1]==1)){
   
    clusterAlgorithm(x-1,j+1,numberofCluster);
  }
  
  if((x-1>=0) and (detectionMatrix[x-1][j]==0) and  (Image[x-1][j]==1 )){
    
    clusterAlgorithm(x-1,j,numberofCluster); 
  }

  
}





  


//  Every time in this code I calculate average of My Image and adjust average Image and continue.

void FINDaverage(){
  for (int i=0;i<24;i++){
    for(int j=0;j<32;j++){
      float ara =average[j][i];
      average[j][i]=((float)ara*(float)averagecounter+(float)Image[j][i])/((float)averagecounter+1);
    }
  }
  int solver=0;
  solver = averagecounter;
  averagecounter=solver+1;
//We stopp  that  averagecounter can not pass THE MAXIMAL INT VALUE
  if (averagecounter==30000){
    averagecounter=15000;
  }
  delay(1000);

}
// IN THIS PART I LOOK  DIFFERENCE=IMAGE-AVERAGE_IMAGE
// DIFFIRENCE>3 WE HAVE our IMAGE because It is not stabil and enough for our system
void noiseReduction(){
  int oneStepBeforeImage[32][24];
  for (int i=0;i<24;i++){
    for(int j=0;j<32;j++){
        oneStepBeforeImage[j][i]=Image[j][i];
      }
    }
    for(int i=0;i<24;i++){
      for(int j=0;j<32;j++){
        Image[j][i]=oneStepBeforeImage[j][i]-average[j][i];
      }
    }
  for (int i=0;i<24;i++){
    for(int j=0;j<32;j++){
        oneStepBeforeImage[j][i]=Image[j][i]>2;
      }
    }
   for (int i=0;i<24;i++){
    for(int j=0;j<32;j++){
        Image[j][i]=oneStepBeforeImage[j][i];
      }
    }
    

   
    
    
}
