# Bluetooth Robot Car (Arduino + Android Native)

This project contains:
- Arduino firmware for a Bluetooth-controlled robot car (HC-05/HC-06 SPP).
- React Native app (JS/TS) using `react-native-bluetooth-classic` for Bluetooth Classic.

## Folder Structure
- `arduino/RobotCar.ino`: Arduino sketch using `Arduino.h` for motor control via L298N (or compatible) and Bluetooth command parsing via Serial.
- `react_native/RobotCarRN/`: React Native CLI app for Bluetooth Classic control of the car.

## Arduino
### Hardware
- Bluetooth module: HC-05 (default baud 9600).
- Motor driver: L298N (2 DC motors).
- Example pin mapping (edit as needed in code):
  - ENA: 5 (PWM), IN1: 8, IN2: 9
  - ENB: 6 (PWM), IN3: 10, IN4: 11
  - Power: Match your driver & motor specs; provide separate supply for motors; common GND with Arduino.

### Commands (sent over Bluetooth/Serial)
- `F<speed>`: forward (speed 0-255), e.g. `F150`
- `B<speed>`: backward
- `L<speed>`: turn left (left motor slower)
- `R<speed>`: turn right (right motor slower)
- `S`: stop
- `V<speed>`: set base speed without movement, e.g. `V180`
- All commands end with newline `\n`

### Upload
1. Open `arduino/RobotCar.ino` in Arduino IDE.
2. Select your board and port.
3. Upload.
4. Pair the HC-05 with your phone (PIN: 1234 or 0000).

## React Native App
Path: `react_native/RobotCarRN/`

### Prereqs
- Node.js LTS, JDK 17, Android SDK, device/emulator with Bluetooth Classic.
- Initialize native folders with RN CLI:
  - If you prefer a fresh init: `npx react-native init RobotCarRN --version 0.74.3`
  - Copy the contents of `react_native/RobotCarRN` `src/`, `package.json`, `index.js`, `app.json`, `babel.config.js`, `tsconfig.json` into your project (or use this provided scaffold and run install).
- Install deps:
  - `npm install` or `yarn`
  - `npx pod-install` (on macOS for iOS)
  - `npm i react-native-bluetooth-classic @react-native-community/slider`

### Android Permissions
Add to your RN Android `AndroidManifest.xml`:
```
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```
For Android 12+, request `BLUETOOTH_CONNECT` and `BLUETOOTH_SCAN` at runtime (the app does this).

### Run
1. Ensure your device is paired with `HC-05` in system settings.
2. From `react_native/RobotCarRN/`:
   - `npm run android` (or `yarn android`) on a physical device with Bluetooth.
   - Press "Connect" and control the car like the native app.

## Notes
- The Android app connects to the first bonded device named `HC-05` or `HC-06`. Adjust code to target a specific MAC if needed.
- Ensure permissions are granted (Bluetooth, location scanning depending on Android version).
- For SDK 31+, the app requests `BLUETOOTH_CONNECT` and `BLUETOOTH_SCAN`.


