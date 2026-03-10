# Emco Compact 5 CNC Modernization

*ME462 Mechatronic Design Project by group Despacito*

The objective of this project is to revive an old cnc lathe (Emco Compact 5 CNC).

<u>Group Members:</u> Egemen İlikmen, Yalın Şahin, Mehmet Furkan Doğan

![FrontView.jpeg](/Pictures/FrontView.jpeg)

## Using Emco Compact 5 CNC

## Powering the Lathe

The lathe should be plugged in to 220V AC through the power cable at the back. The electric plug can be used to power other things after the machine is plugged in. (That plug is not connected to any fuse or emergency stop button) To give power to the electronics inside of the lathe, the emergency stop button should be deactivated.

After that, there are two requirements to activate the PSU that powers everything.

* Make sure that there is a casette tape inside and the lid is closed

* The switch with a key is at the on position

After that the lathe should be powered on.

## Using the Lathe

 There are three parts of this project:

1. **Controlling the X and Z axes**
   
   The g-code can be sent through the serial with a baud rate of 115200 using the usb cable at the back. The settings of grbl can be seen using '##' command. For more information about grbl: [grbl Wiki](https://github.com/gnea/grbl/wiki)

2. **Controlling the Speed of the Spindle**
   
   The speed cannot be controlled but it can be masured using a beam breaker encoder. [Speed_Reading_Code](/codes/Speed_Reading_Code/Speed_Reading_Code.ino) can be uploaded to the arduino on top to get speed readings in rpm through the serial port with a baud rate of 9600.

3. **Automatic Tool Changing**
   
   [tool_changer](/codes/tool_changer/tool_changer.ino) can be uploaded to the arduino on top to control the tool changer. The tool number should be sent through the serial port with a baud rate of 9600 to use the desired tool. Remember that the tools are changed incrementally. Therefore, the 1st tool must be selected before end of the operation.

## Controlling the X and Z axis

---

Two steppers motors are used for controlling the X and Z axis. Those motors are driven in unipolar configuration by TB6600 stepper motor drivers.

### Motor Info - Warner Electric Brake & Clutch sm-072-0060-ra

![z-step-specs.jpeg](/Documents/z-step-specs.jpeg)

| Date Submitted     | Nov 03, 1999                   |
| ------------------ | ------------------------------ |
| Motor Manufacturer | Warner Electric Brake & Clutch |
| Motor Part Number  | sm-072-0060-ra                 |

 **<u><font face="Arial">Electrical Specifications</font></u>**

|                                    |       |                |
| ---------------------------------- | ----- | -------------- |
| Phase Resistance                   | 4.6   | ohms           |
| Phase Inductance                   |       | mH             |
| Nominal Phase Current (1 Phase On) | 2     | A              |
| Nominal Phase Voltage              | 9 vdc | V              |
| Electrical Time Constant           |       | ms             |
| Back EMF Amplitude                 |       | V / ksteps / s |

 **<u><font face="Arial">Mechanical Specifications</font></u>**

| Holding Torque @ Nominal Current |     | oz-in       |
| -------------------------------- | --- | ----------- |
| Detent Torque                    |     | oz-in       |
| Step Angle                       |     | deg/step    |
| Angular Acceleration             |     | rad/s^2     |
| Angular Accuracy                 |     | % full-step |
| Resonant Frequency               |     | Hz          |
| Shaft Diameter                   | 1/4 | in          |

| Mounting Frame (NEMA Standard) | 17/8X17/8" holes |
| ------------------------------ | ---------------- |

### Step Motor Driver Info - TB6600

Motor connections is made using the unipolar configuration.

![stepper_motor_diagram.png](/Documents/stepper_motor_diagram.png)

### Programming

To program the CNC lathe, an Arduino related software [GRBL](https://github.com/gnea/grbl) is used. The g-code can be sent directly through the serial port to the Arduino. [Universal Gcode Sender](https://github.com/winder/Universal-G-Code-Sender) is another way to send g-code to Arduino easily.

Here is another GCode sender for GRBL: [svenhb/GRBL-Plotter](https://github.com/svenhb/GRBL-Plotter)

## Controlling the Speed of the Spindle

---

### Measuring the Spindle Speed

In the spindle assembly, there is a disc that has 100 holes equidistant form origin. A beam breaker sensor is put on this circle to count the number of holes that are being passed in a time interval during operation. 

Arduino board is used for this application. The main idea is to count the number of holes during a specific time interval. This time interval is adjusted with the interrupt frequency settings of the timer interrupt and is adjusted to 0.1 seconds (or 10 Hz interrupt frequency) in this application. It can be changed as instructed in the speed control code written in Arduino. During operation, the hole count per second, which is also equal to revolution of the spindle per second (rps), is calculated using another interrupt. With proper unit conversions, rotational speed of the spindle in revolutions per minute (rpm) is found and published via a display screen.

### Driving the Spindle Motor

The spindle motor has 180 VDC nominal voltage rate. As this is a high voltage rate supplying necessary voltage to the motor is challenging. To change and regulate the AC power coming from the grid, an AC  dimmer and a full bridge rectifier is planned to be used. The speed can be controlled closed loop by rotating the potentiometer using a servo motor. In this system, the measured spindle speed is aimed to be used as the feedback of the control loop.

## Automatic Tool Changing

---

There is a 12 V DC motor and a rachet mechanism inside the gearbox to control the tool changer. Since there is no sensor in this system, the motor is controlled open loop using a seperate Arduino board. The desired tool number is sent to that Arduino through serial port to change the tool.

## Electrical Scheme & Wiring

---

### Electrical Sub-System

After preparing the sub-systems of the lathe, the electrical system is designed to distribute the required power to every component. The general scheme is shared below:

(Figure)

For safety measures, an emergency stop button is connected to the main power line coming from the grid. Once pushed, it cuts all the power on the lathe but the socket's. The socket can be used for any application, it does not harm the lathe's electric system.

Secondly, a fuse is equipped to the electrical system, after the emergency stop button and the power distribution terminal. Considering the power need of the lathe, 8A rated fuse is selected.

A fan is used in the system to cool the electrical components. It is powered by 220VAC, so it is connected to the main line, after the fuse.

Apart from the emergency stop button, two serial connected switches are present also. For the machine to work fully, the key switch must be turned on and a casette should be in its box. If both switches are off, the AC power reaches to the power supply and converted to DC. From its different output wires, 12V voltage is transferred to the buck converters and regulated to 9V, which is the rated voltage of the stepper motors and the drivers. At last, the output of the converter is connected to the drivers and after that to the stepper motors.

The power supply is taken from an old computer and its specifications are shared below:

 (specifications of the power supply)

The two controller boards (Arduino Uno) are powered differently. The below one, the main board which is controlling the axes, is powered from the computer via a cable. And the above one, which is used to control the tool changer and measure speed control, is fed from the main arduino, from Vin pin.

## Wiring

The connections of the lathe with its electronic components is shown with a picture and tabulated below:

![(Arka kısmın fotosu)](/Pictures/RearView_Open2.jpeg)

| From | To  | Number |
|:----:|:---:| ------ |
|      |     |        |
|      |     |        |
|      |     |        |
|      |     |        |

# Possible Improvements

## Spindle Motor & Drive

The spindle motor has a high nominal voltage rate (180VDC). The motor can be changed with a lower voltage motor that supplies the same power and speed. That way, the effort on the power electronics side may be less.

For the motor drive, an industrial motor driver may be selected and used, for a reliable operation. The motor voltage and current limits of the driver are important parameters for choosing the most suitable motor driver.

## Stepper Motors

We are using the stepper motors in unipolar configuration at their rated voltage. This results in double the current draw which in turn doubles the power consumption heating the motor. We suggest replacing the stepper motors with ones that can be driven in bipolar configuration.

## X axis Limitation

There is a sheet metal part that prevents chips from falling to the lead screw of the x-axis. However, this part is bent and limits the movement of the X axis towards the negative X direction. This part can be fixed or replaced to further improve the performance of the lathe.

## GRBL Limitations

GRBL is a tool that is designed for a wide range of CNC applications from laser cutters to routers. However, due to the limitations of the hardware (Arduino Uno in that case), GRBL is not very good at all of the applications that it seems to support. The biggest problem we had encounter while using GRBL was the lack of tool changer support. Here are the possible solutions to that problem:

* **(The one that we tried) Using the abandoned features of GRBL to make tool changer work**
  
  Coolant control pin can be used to send a signal for changing the tool. In order that to work, the original g-code can be manipulated before being sent to GRBL so that the tool changing commands (*T# and M06*) is replaced with coolant control and pause commands (M08, M09 and G04 P#).

* **Using a GRBL alternative that has tool changer support**
  
  Possible candidates are:
  
  * [µCNC](https://github.com/Paciente8159/uCNC)
  
  * [grblHAL driver for RP2040 (Pi Pico)](https://github.com/grblHAL/RP2040)
  
  * [LinuxCNC](http://linuxcnc.org/)

* **Coding a GRBL alternative or modifying GRBL to just have what we need and nothing more**

## Tool Changer Limitations

The toolchanger works incrementally right now. Therefore it should be resetted manually after every uses. There is a light line on the side of the tool holder. An optic encoder can be used to reset the tool position automatically.
