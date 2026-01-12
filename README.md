# vBHADRA
A tool for Rapid Detection an Blocking of Pornography

## Demo Video

**vBHADRA – Harmful Content Detection and Blocking Demo**

This video demonstrates the **vBHADRA** tool detecting regions of harmful content on the screen and dynamically blacking out the corresponding pixels in real time.

 https://github.com/user-attachments/assets/f7dd7a80-7014-48ac-af9b-17a6cbc7ba2d

## Setup
Note:- The blocking program (blackout1.cpp) works only for Windows OS.
1. Clone the repository. 
2. Create a new virutal env using conda, or uv (faster)
3. Install the modules using requirements.txt ```pip install -r requirements.txt```
4. Edit the path to weights in ```server.py```
5. Open Powershell, start the server.py ```python server.py```
6. Compile the blocking program.(Needed to be done only once) ```g++ blackout1.cpp -o blackout -lgdi32```
7. In another Powershell window, start the Client ```python client.py```

Note:- Start the client only in a seprate powershell window outside any vitual env. While developing it was found that running the ```client.py``` inside a terminal in VS code or venv, did not trigger the blocking. So to correctly trigger the blocking program, start the client in a new seprete window.

## Description
Pornograpghic content has increased exponentially in past few years. It is impossible to block every website. Therefore we need mechanisms to block any harmful content appearing on our screens. vBHADRA helps in blocking any kind of harmful content appearing on the screen, from any source (browser, gallery etc). It can swiftly detect and block the harmful content (<1s). vBHADRA uses YOLO-v8 under the hood the detect and uses a custom blocking program (uses Windows API) to black out the regions detected. vBHADRA works entirely offline.

The dataset to train the model was built from scratch using 4000+ images , comprising of different classes. The model was trained on Kaggle. The trained [weights](https://drive.google.com/file/d/1o7vgBBGOoIP51LROnF14lY_gBdUpN2l5/view?usp=sharing) can be downloaded from the link. It also logs every detection, by saving the output from the YOLO model.

## Future Scope
1. Making the entire application easily installable as a Windows desktop application, thereby significantly improving accessibility and simplifying the setup process.
2. Incorporate a more robust reporting mechanism. So that any detection can be reported to parents or guardians.
3. Train the model to also detect harmful content in thumbnails of videos
4. Making the tool work for Android (on the way ;) )


