#include <Arduino.h>

// L298N Motor Driver Pins (adjust as needed)
const uint8_t ENA_PIN = 5;   // PWM
const uint8_t IN1_PIN = 8;
const uint8_t IN2_PIN = 9;

const uint8_t ENB_PIN = 6;   // PWM
const uint8_t IN3_PIN = 10;
const uint8_t IN4_PIN = 11;

// Default speed
uint8_t baseSpeed = 150; // 0..255

static void setMotorA(int speed) {
	// speed: -255..255
	int clamped = constrain(speed, -255, 255);
	if (clamped > 0) {
		digitalWrite(IN1_PIN, HIGH);
		digitalWrite(IN2_PIN, LOW);
		analogWrite(ENA_PIN, clamped);
	} else if (clamped < 0) {
		digitalWrite(IN1_PIN, LOW);
		digitalWrite(IN2_PIN, HIGH);
		analogWrite(ENA_PIN, -clamped);
	} else {
		digitalWrite(IN1_PIN, LOW);
		digitalWrite(IN2_PIN, LOW);
		analogWrite(ENA_PIN, 0);
	}
}

static void setMotorB(int speed) {
	int clamped = constrain(speed, -255, 255);
	if (clamped > 0) {
		digitalWrite(IN3_PIN, HIGH);
		digitalWrite(IN4_PIN, LOW);
		analogWrite(ENB_PIN, clamped);
	} else if (clamped < 0) {
		digitalWrite(IN3_PIN, LOW);
		digitalWrite(IN4_PIN, HIGH);
		analogWrite(ENB_PIN, -clamped);
	} else {
		digitalWrite(IN3_PIN, LOW);
		digitalWrite(IN4_PIN, LOW);
		analogWrite(ENB_PIN, 0);
	}
}

static void stopAll() {
	setMotorA(0);
	setMotorB(0);
}

static void forward(uint8_t speed) {
	setMotorA(speed);
	setMotorB(speed);
}

static void backward(uint8_t speed) {
	setMotorA(-speed);
	setMotorB(-speed);
}

static void left(uint8_t speed) {
	// reduce left motor to pivot slightly
	int leftSpeed = speed / 3;
	setMotorA(leftSpeed);
	setMotorB(speed);
}

static void right(uint8_t speed) {
	// reduce right motor to pivot slightly
	int rightSpeed = speed / 3;
	setMotorA(speed);
	setMotorB(rightSpeed);
}

// Parse commands like: F150, B120, L100, R180, S, V200
static void handleCommand(const String &cmd) {
	if (cmd.length() == 0) return;
	char c = cmd.charAt(0);
	String param = cmd.substring(1);
	param.trim();
	int value = param.length() ? param.toInt() : baseSpeed;
	value = constrain(value, 0, 255);

	switch (c) {
		case 'F':
			forward((uint8_t)value);
			break;
		case 'B':
			backward((uint8_t)value);
			break;
		case 'L':
			left((uint8_t)value);
			break;
		case 'R':
			right((uint8_t)value);
			break;
		case 'S':
			stopAll();
			break;
		case 'V':
			baseSpeed = (uint8_t)value;
			break;
		default:
			// unknown, ignore
			break;
	}
}

void setup() {
	pinMode(ENA_PIN, OUTPUT);
	pinMode(IN1_PIN, OUTPUT);
	pinMode(IN2_PIN, OUTPUT);

	pinMode(ENB_PIN, OUTPUT);
	pinMode(IN3_PIN, OUTPUT);
	pinMode(IN4_PIN, OUTPUT);

	stopAll();

	Serial.begin(9600); // HC-05 default
}

void loop() {
	static String buffer;
	while (Serial.available() > 0) {
		char ch = (char)Serial.read();
		if (ch == '\n' || ch == '\r') {
			buffer.trim();
			if (buffer.length() > 0) {
				handleCommand(buffer);
				buffer = "";
			}
		} else {
			buffer += ch;
			// Basic safety: bound the buffer size
			if (buffer.length() > 32) {
				buffer = "";
			}
		}
	}
}


