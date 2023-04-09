#include <Servo.h>

#define in1 8
#define in2 9
#define ena 6
//setup ultra sonic pins
const int trigPin = 7;
const int echoPin = 4;
long duration;
int distance;
Servo myservo;
int delay_time = 30;

int tag_id = -1;
int steer = 90;

void setup()
{
  delay(20000);
  Serial.begin(9600);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(ena, OUTPUT);
  myservo.attach(5);
  //usonic setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myservo.write(steer);
}
void loop()
{
  // Drive motor forward
  if (serial_available())
  {
    String ser_data = serial_read();
    delay(50);
    steer = get_data_sep_by_comma(ser_data, 0).toInt();
    tag_id = get_data_sep_by_comma(ser_data, 1).toInt();
    steer = scale_data(steer);
//    Serial.println(String("new data : " + String(steer) + ", " + String(tag_id)));
    delay(50);
  }
  myservo.write(steer);
  switch (tag_id)
  {
    case -1: // no sign
      forward_car();
//      Serial.println("FORWARD SECTION -1");
      delay(50);
      break;
    case 119:
      forward_car();
      break;
    case 6: // stop
      stop_car();
//      Serial.println("STOP SECTION 666");
      delay(50);
      break;
    default:
      forward_car();
      break;
  }
  //    tag_id = -1;
  //    Serial.println(String("data => steer:")+String(steer)+", tag_id:"+String(tag_id));
  //    delay(1000);
}
void servo_move(int steer)
{
  myservo.write(steer);
}
bool serial_available()
{
  return Serial.available() > 0;
}
String serial_read()
{
  String msg = "";
  if(Serial.available())
  {
    delay(10);
    while(Serial.available()>0)
    {
      msg += (char)Serial.read();
    }
    Serial.flush();
 }
 return msg;
//  return Serial.readString();
}

String get_data_sep_by_comma(String text, int index)
{
  int comma_index = 0, comma_count = 0;
  for (int i = 0; i < text.length(); i++)
  {
    if (comma_count == index)
    {
      break;
    }
    if (text[i] == ',')
    {
      comma_count++;
      comma_index = i + 1;
    }
  }
  String result = "";
  for (int i = comma_index; text[i] != '\0' && text[i] != ','; i++)
  {
    result += text[i];
  }
  return result;
}

int get_distance()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}
bool is_obstacle()
{
  return get_distance() <= 20;
}
int scale_data(int ser_data)
{
  // serial data = -100 ~ 100
  // servo range = 105 ~ 75 deg
  // map(ser_data,-100,100,75,105)
  if (ser_data >= 66)
  {
    return 80;
  }
  if (ser_data < 66 && ser_data >= 33)
  {
    return 85;
  }
  if (ser_data < 33 && ser_data >= 10)
  {
    return 90;
  }
  if (ser_data < 10 && ser_data > -10)
  {
    return 95;
  }
  if (ser_data <= -10 && ser_data > -33)
  {
    return 100;
  }
  if (ser_data <= -33 && ser_data > -66)
  {
    return 105;
  }
  if (ser_data <= -66)
  {
    return 110;
  }
}
void forward_car()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(ena, 120);
}
void stop_car()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}
