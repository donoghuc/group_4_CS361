# group_4_CS361

### Docker environment 
You can build the docker image yourself with the provided Dockerfile.
I would highly recommend you do this. It will take a while the first time but layers are cached so when you do any dev to
the image it will only take the time to copy in the new improvements. (note do this as root, the -t flag sets the "name" of the image)
```
docker build -t demo_app . 
```
Alternatively I saved a tar'd version for you guys if this will be easier for you (showing command for this below)
```
docker save -o ./demo_app demo_app:latest
```
You can load it like this
```
docker load -i demo_app
```
Image notes:
* base image is ubuntu with the latest anaconda distro on it...
* I know the full conda distro is bloaty AF for this but I want to eventually use pandas to do the analytics dashboard stuff 
* I put vim as the text editor

Test it out
Once you have either built the image yourself or loaded in the saved image try the following 
```
docker run -ti -p 5000:5000 demo_app:latest
```
The -ti flags will but you in to a bash shell on root of container, the -p flag will forward port 5000 (that is what our flask app is running on) run the following two commands
```
cd group_4_boilerplate/
```
```
python app.py
```
this will start the web server
navigate to localhost:5000 in a browser and check out the app! 

### Starting a container
![terminal session](group_4_boilerplate/screenshots/start_docker_app.png?raw=true "term ss")

### View the app 
![website](group_4_boilerplate/screenshots/about_view.png?raw=true "website ss")

### cleanup
when you are done you can use sigterm (Ctrl c) to kill server, this will drop you back to bash shell in running container. From here you can just type "exit" and you will be dropped back to the shell you started the container from. The container should be destroyed, double check with "docker ps" if you want. 

# BOILERPLATE SOURCE!!!! 
thank you Michael Herman (mjhea0) soooo much for making this, 

see project at 

https://github.com/mjhea0/flask-boilerplate



