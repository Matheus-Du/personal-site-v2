[![Docker Build](https://github.com/Matheus-Du/personal-site-v2/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Matheus-Du/personal-site-v2/actions/workflows/docker-image.yml)

# personal-site-v2
Revamped personal site written with __HTMX__ and __Flask__ (for now) with a new UI and some API (and scraping) integrations. Used as a place to write some stuff, show off what I've been reading, and display some internet things that I've liked recently. Deployed on my __Linux__ Home Server using __Docker__, __Nginx__, and __Cloudflare CDN__. This updated site came about mainly due to frustration around updating and deploying my old personal site built with React; I wanted to create a platform that was easy to develop new features for by focusing on container orchestration and __CI/CD__. The result is a simple and efficient deployment experience that makes developing new features actually fun and interesting (mainly due to the fact that I'm not spending most of my time debugging in prod to find issues missed during deployment).

## Frontend
The main goal of this revamped personal site is to create a dynamic site that requires _0_ lines of __JavaScript__. This is done using __HTMX__ to issue HTTP requests to the backend, allowing for more complex page updates than would be possible using plain __HTML__. In theory, this will keep load times and Total Blocking Time down (it's currently at 0ms), but we can achieve similar results using JS-heavy applications as well since web frameworks like React can build well-optimized deployments anyways. It currently uses __Flask__ for page routing but I'll probably change this as an exercise in writing web servers in different languages.

## Backend
Using a __Flask REST API__ for the backend that gets data from a __MongoDB__ instance running locally. Since I'm using __HTMX__, this is a true __RESTful API__, since it sends data to the Frontend as __HTML__, making the data actually REpresentational. This is just a couple of endpoints and nothing too interesting, but still requires a little bit of container orchestration. Since it's relatively simple, I'd like to use it as a future base for trying out other languages (mabe Rust or Prolog).

## Database
Uses a container running a __MongoDB__ instance to store data. The Docker container has an external volume that stores the data to allow persistance over system reboots. The Backend service connects to this DB using __Docker__ container networking. Since the data is small and has consistent formatting already, I mostly just wanted something that allows me to dump JSON info into it, which made a __NoSQL DB__ preferrable. Relational DBs could probably do a better job at representing the stored data since it's all pretty normalized, but it would add some complexity to the data retrieval and submission that probably wouldn't be worth the effort.

## Deployment
The entire stack is deployed using __Docker Compose__ to allow for efficient containerization and networking between the different containers. This makes startup and updating simple while also providing consistency between the dev and prod environments. The Frontend and Backend __Flask__ applications are run in prod using __Gunicorn__.

The container stack is deployed on an __Ubuntu__ Home Server. __Nginx__ is used for routing incoming requests to the Frontend container port and for ensuring secure __HTTPS__ connections using __SSL/TLS__. A __Cloudflare Reverse Proxy__ is placed in front of this to block malicious traffic and provide common __CDN__ functionality such as cacheing and locality.

When new code is pushed to main, a __Github Actions__ script runs to update the prod deployment automatically using a __self-hosted runner__. This makes the deployment process painless while ensuring that the production system is identical to the dev environment. The end result is me spending essentially no time debugging in prod. This is protected by GitHub actions settings to ensure the self-hosted runner can't execute any code from outside collaborators.

## Future Plans
I'd like to continue using this site to write blog posts and project retrospectives in my free time. __RSS__ feed functionality would allow other people to get updates on this, so it's a feature I'd like to implement, especially since it would allow me to work with something I've never interacted with before (even if that requires touching XML...).

Changing the web servers for the Frontend and Backend from __Flask__ to another programming language or framework would be a nice challenge and is always a good way to learn a new paradigm. My conventional choice for this would be __Rust__ since it's well-regarded as a fast, efficient, and secure language. Rust error handling would also make it easier to develop a correct system in a way that Python struggles with (less try-catch statements is always nice). Another option for this would be __Prolog__, which probably isn't as bad of a choice as it seems. This would likely need to be paired with a more conventional language and thus requires more work, but in theory backtracking and Logic Programming would allow for a simple, efficient, and correct system with relatively few bells and whistles.

The current version has basically no tests since I'm the only contributor and don't really feel like adding them. I have some experience with __Test-Driven Development__ and enjoyed it, so maybe future features will be implemented using a TTD approach.

There's miscellaneous stuff as well - especially new feature implementation - that I'd like to get around to, but that's outside the bounds of a ReadMe. The main goal is just to have a stable, consistent platform to make developing and deploying new features as simple as possible.
