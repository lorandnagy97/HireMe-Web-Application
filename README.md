# HireMe

### Intro
-----
**Welcome!**
If you're reading this, I assume the reason you're here is to determine if I am skilled enough to be worthy of your employ.
For starters, thanks for taking the time to review this! There is a lot of work still to be done on this application, particularly code cleanup and unit testing; however, time is of the essence so I've decided to publish what I have so far as proof of concept. The commit history is lacking because this project was previously hosted on gitlab, but you can find proof of my gitlab proficiency via my LinkedIn page; I've passed the Git quiz confirming my abilities. Let's dive into some of the non-website related features!

### Development
-----
#### Makefile
To speed up development, I used a Makefile which allows me to automatically run the commands needed to test my application. It also has a function allowing me to publish my image to Amazon's ECR service when it's ready.

#### Dockerfile
The dockerfile containerizes my application, allowing it to run securely, robustly, and portably. It is currently using the AmazonLinux 2 AMI for the base image.

#### Organization
While creating this application, I've been using my own personalized Jira instance to keep track of my thoughts and short term goals.


### Testing it Yourself
-----
I plan to launch this application via AWS's ECS service, however since I'm not quite at a place where I'd like it to be live yet, the next best thing is running it locally on your own machine. In order to do this, all you'll need is Docker, Make, and a clone of this repository. Then, while in the project's directory, run the following command:

```
make run-local
```

This will launch the application with the local environment variable specified, bypassing any calls to unfinished cloud related functions.

