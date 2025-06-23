## Comprehensive-Intrusion-Detection-using-IoT

# Abstract:
The Home Intrusion Detection System is an intelligent, affordable, and efficient security
 solution designed to protect residential spaces. It is built using a Raspberry Pi as the
 central controller, integrated with infrared (IR) and light-dependent resistor (LDR) sensors
 to detect motion and ambient light changes, even in low-light conditions. A high-resolution
 camera captures 720p images upon detecting suspicious activity. The system activates a
 buzzer and LED within 0.8 seconds to alert nearby individuals and transmits alerts via
 MQTT with a latency of 3–7 seconds. Compact, energy-efficient, and easy to install, it
 offers reliable, real-time monitoring for modern smart homes.

 # Introduction:
 The Home Intrusion Detection System is a smart, efficient, and cost-effective security so
lution built around a Raspberry Pi, which serves as the central control unit. It integrates
 a camera, IR sensor, LDR sensor with laser beam, LEDs, and a buzzer to monitor and re
spond to intrusion threats in real time. The camera supports live monitoring and captures
 images upon detecting movement. The IR sensor detects motion under various lighting
 conditions, while the LDR-laser pair senses light beam interruptions, enhancing detection
 accuracy. On detecting an intrusion, the system activates a buzzer and LED for immediate
 local alerts. Simultaneously, it sends real-time alerts via the MQTT protocol, a lightweight
 and scalable messaging solution ideal for IoT applications. MQTT ensures quick delivery
 of intrusion notifications to subscribed clients such as mobile apps. Live testing confirmed
 high motion and obstruction detection accuracy, fast alert triggering, and reliable image
 capture. This layered approach significantly improves home security and responsiveness.

 # Hardware Components Used:
  Raspberry Pi 3 Model B+
  
 PIR (Passive Infrared) Sensor (HC-SR501)
 
 Light Dependent Resistor (LDR) Sensor (GL5528)
 
 Camera Module
 
 LED Indicator
 
 Buzzer (5V DC Active Buzzer)

 # Software Modules Used:
 Sensor Initialization Module
 
 Surveillance Control Module
 
 Alert Management Module
 
 Notification and Logging Module
 
 Auto Recovery Module
