# WASABI
WASABI stands for Well Applied Server Automated Biological Interface. Wasabi is a 5 bar linkage based pipetting robot that is automated via raspberry pi and the python flask library This page contains both the information and documentation for the software package as well as the mechanical assembly of the pipetting robot. The pipetting robot in this build is a slightly modified version of the [Phil pipetting robot](https://www.biorxiv.org/content/10.1101/2021.07.04.448641v1.full). Though the rpi and stepper breakout boards can be used with any machine and the wasabi machine config can be modified for any 5-bar based pipetting robot.  
## [Bill of Materials (BOM)](https://docs.google.com/spreadsheets/d/16TOlXRDoKtlOAvTiCGKz8jH9Rkvl1hXIs9z1LAUZMCc/edit?usp=sharing)

(currently working actively with this BOM but if you decide to build this project you should make your own copy and make sure to clear all of the material statuses and reset them to red so you can track)

## software outline
The core of Wasabi has three main goals:
1. intuitively program and store experiments through a visual interface 
2. run experiments and directly control the robot 
3. configure machine parameters, plate dimensions, and pump contents

### diagram
[insert diagram here]




