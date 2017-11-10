# group_4_CS361

# Docker environment 
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
..* base image is ubuntu with the latest anaconda distro on it...
..* I know the full conda distro is bloaty AF for this but I want to eventually use pandas to do the analytics dashboard stuff 
..* I put vim as the text editor

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

