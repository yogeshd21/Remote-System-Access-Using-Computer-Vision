# Remote-System-Access-Using-Computer-Vision
## Description: 
A model for remote computer system access with applications like cursor control and audio control.

## Abstract:
The increase in electronic waste because of small computer input-output devices and the environmental hazards caused by that is one of the most highlighted and growing issues these days. These problems need a sustainable solution and more precisely an alternate option which could replace their requirement with the same or similar performance factor. To address a scope of work in this direction we have proposed an effective approach which could be used to replace the physical hardware in the computer system setup and instead use a non-contact computer vision-based approach to achieve the same performance. We propose our idea in terms of an action recognition and pose based system, where the action recognition will help us identify the application based on the signature actions and will further be processed based on the pose-based hand points. With the inclusion of such methods and techniques as a part of our normal system it won’t just help in reducing the hardware waste but will also make the systems more easily accessible with the effective use of the advanced technology and algorithms developed these days.

## Demo Video:
[YouTube Demo Video](https://youtu.be/YOxCYI1V5Y0)

## Outputs:
![image](https://user-images.githubusercontent.com/83297868/145293166-9effb809-fbfa-4b76-9cf9-d0acf901db0a.png)
![image](https://user-images.githubusercontent.com/83297868/145293191-cef763e7-db16-4f55-a1d8-a77b4714440c.png)  
![image](https://user-images.githubusercontent.com/83297868/145293363-35e2238b-d939-4155-8723-9117241db29e.png)
![image](https://user-images.githubusercontent.com/83297868/145293378-d06bf7e1-a0a4-4160-b273-847b8c2d2d48.png)  
![image](https://user-images.githubusercontent.com/83297868/145293389-e1ef5b32-5aac-4574-9d1c-d9905a27d4f6.png)
![image](https://user-images.githubusercontent.com/83297868/145293411-803d61f8-6fda-4716-aeaa-c4ba5c87ff98.png)

Figures (a), (b) and (c) demonstrate the reach of the cursor in the different corners as per the display size and how it covers the extreme corners as well as task bar area well. Figure (d) demonstrates the actual system volume changes when we change the distance between the index finger and thumb for the audio control application. Figures (e) and (f) are consecutive images which demonstrate the click function for the cursor control application as the display window maximizes in the consecutive frame.

## Computation Instructions:
Other than the standard libraries you will have to install mediapipe library, autopy library (as per date compatible with python 3.8 version and below) and pycaw library.

HandTracking.py - It is the module which is written to help in different computations required.<br/>
VirtualAll.py - This is the code you have to run to access the module/application.
