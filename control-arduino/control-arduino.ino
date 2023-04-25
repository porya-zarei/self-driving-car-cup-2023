#include <Servo.h>

int default_speed = 120, high_speed = 160, higher_speed = 200, low_speed = 100;

#define in1 8
#define in2 9
#define ena 6
// setup ultra sonic pins
const int trigPin = 7;
const int echoPin = 4;
Servo myservo;
int delay_time = 30;

int tag_id = -1;
int steer = 95;
int traffic_light = -1; // -1 => no light 0 => green , 1 => yellow , 2 => red
int cross_walk = 0;     // 0 => no , 1 => yes

//double distances[10] = {0,0,0,0,0,0,0,0,0,0};
//int distance_index = 0,distances_size = 10;

void setup()
{
    delay(2000);
    Serial.begin(9600);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(ena, OUTPUT);
    myservo.attach(5);
    // usonic setup
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
        steer = get_data_sep_by_comma(ser_data, 0).toInt();
        steer = scale_data(steer);
        tag_id = get_data_sep_by_comma(ser_data, 1).toInt();
        traffic_light = get_data_sep_by_comma(ser_data, 2).toInt();
        cross_walk = get_data_sep_by_comma(ser_data, 3).toInt();
    }

    if (is_obstacle() || traffic_light == 2)
    {
        stop_car();
        delay(3500);
        Serial.flush();
    }
    else if (cross_walk == 1)
    {
        stop_car();
        delay(3000);
        steer = 95;
        myservo.write(steer);
        delay(5);
        forward_car(default_speed);
        delay(3000);
        Serial.flush();
    }
    else
    {
        myservo.write(steer);
        delay(5);
        switch (tag_id)
        {
        case -1: // forward
            forward_car(default_speed);
            delay(20);
            break;
        case 119:
            forward_car(default_speed);
            break;
        case 6: // stop
            stop_car();
            delay(200);
            Serial.flush();
            break;
        case 11: // left
            turn_left_car();
            break;
        case 12: // right
            turn_right_car();
            delay(20);
            // Serial.flush();
            break;
        case 2:
            stop_car();
            delay(3000);
            forward_car(default_speed);
            delay(5000);
            Serial.flush();
        case 3:
            auto_park();
            break;
        default:
            forward_car(default_speed);
            break;
        }
    }
}

bool serial_available()
{
    return Serial.available() > 0;
}

String serial_read()
{
    String msg = "";
    if (Serial.available())
    {
        delay(10);
        while (Serial.available() > 0)
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

double get_distance()
{
    double duration, distance;
    double soundSpeed = 331.4 + 0.606 * 20;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * (soundSpeed / 20000);
    //  Serial.println(String(distance));
    return distance;
}

bool is_obstacle()
{
    double distance = get_distance();
    //  Serial.println(String(distance));
    return distance <= 20;
}

int scale_data(int ser_data)
{
    // serial data = -100 ~ 100
    // servo range = 80 ~ 110 deg
    // map(ser_data,-100,100,75,105)
    if (ser_data >= 66)
    {
        return 80;
    }
    else if (ser_data < 66 && ser_data >= 43)
    {
        return 82.5;
    }
    else if (ser_data < 43 && ser_data >= 33)
    {
        return 85;
    }
    else if (ser_data < 33 && ser_data >= 15)
    {
        return 87.5;
    }
    else if (ser_data < 15 && ser_data >= 5)
    {
        return 90;
    }
    else if (ser_data < 5 && ser_data > -5)
    {
        return 95;
    }
    else if (ser_data <= -5 && ser_data > -15)
    {
        return 100;
    }
    else if (ser_data <= -15 && ser_data > -33)
    {
        return 102.5;
    }
    else if (ser_data <= -33 && ser_data > -43)
    {
        return 105;
    }
    else if (ser_data <= -43 && ser_data > -66)
    {
        return 107.5;
    }
    else if (ser_data <= -66)
    {
        return 110;
    }
}

void forward_car(uint8_t car_speed)
{
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(ena, car_speed % 255);
}
void backward_car(uint8_t car_speed)
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(ena, car_speed % 255);
}
void stop_car()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
}

void turn_left_car()
{
    steer = 95;
    myservo.write(steer);
    forward_car(low_speed);
    delay(2000);
    steer = 110;
    myservo.write(steer);
    delay(4000);
    steer = 95;
    myservo.write(steer);
    Serial.flush();
}

void turn_right_car()
{
    steer = 95;
    myservo.write(steer);
    delay(2000);

    steer = 80;
    myservo.write(steer);
    forward_car(low_speed);
    delay(2000);

    steer = 110;
    myservo.write(steer);
    backward_car(110);
    delay(2000);

    steer = 80;
    myservo.write(steer);
    forward_car(low_speed);
    delay(2000);

    steer = 95;
    myservo.write(steer);
    forward_car(low_speed);

    Serial.flush();
}

void auto_park()
{
    steer = 80;
    myservo.write(steer);
    backward_car(100);
    delay(4000);

    steer = 110;
    myservo.write(steer);
    backward_car(low_speed);
    delay(4200);

    steer = 95;
    myservo.write(steer);
    forward_car(low_speed);
    delay(2000);

    Serial.flush();
}
