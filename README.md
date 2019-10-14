# Door-opener-With-Face-Using-Raspberry

This is a project that works on Raspberry Pi3b+ or Pi4, using this project you can unlock your dormitory door which related to how your lock work.

file gpio.py is the function privide the ability to control your motor, that means you'd like to change the GPIO port accroding to what it actually is.

file add.py is used isolatly for add a face with a ONLY-ONE-PERSON picture, it will detect if there exist a encoded file '.npy' , if not , create it ,if do append the new face encodings

The file mian.py is the main file of the project, you can just run 

python3 main.py

to start the program , or 

nohup python3 main.py 

to run it constantly 
