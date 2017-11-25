# group_4_CS361

## Docker environment 
Make sure you have docker installed on your system 
I am using docker version 17.09.0-ce on Ubuntu 17.04

## Installation
Download or clone our git repo (group_4_CS361)
navigate to TLD (group_4_CS361) and execute the following command (as root or with sudo)

```
docker build -f Dockerfile -t demo_app . 
```
This will build a 545MB docker image (NOTE make sure you have internet connectivity and any if you are behind a proxy that you set HTTP_PROXY environment variable in the image contact Cas (donoghuc@oregonstate.edu) if you have questions on how to do this)

Image notes:
* base image is ubuntu 
* I installed miniconda to make the image small and fully python functional 
* I installed vim as a text editor for making changes to source code for testing a container

Upon a sucessfull build you can run docker images and see your demo_app image as well as the base ubuntu image
```
docker images
```
No start a container using the following command
```
docker run -ti -p 5000:5000 demo_app:latest
```
The -ti flags will but you in to a bash shell on root of container, the -p flag will forward port 5000 (that is what our flask app is running on) run the following two commands
```
cd web_app/
```
Initialize the database manually for now and ensure that there is a successful, you should see pythonsqlite.db file populate
```
python make_database.py
```
Now start the web server 
```
python app.py
````

this will start the web server
navigate to localhost:5000 in a browser and check out the app! 

### Starting a container


### View the app 


### cleanup
when you are done you can use sigterm (Ctrl c) to kill server, this will drop you back to bash shell in running container. From here you can just type "exit" and you will be dropped back to the shell you started the container from. The container should be destroyed, double check with "docker ps" if you want. 

# BOILERPLATE SOURCE!!!! 
thank you Michael Herman (mjhea0) soooo much for making this, 

see project at 

https://github.com/mjhea0/flask-boilerplate



