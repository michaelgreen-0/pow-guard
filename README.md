![image](https://github.com/user-attachments/assets/672e885d-ffce-419a-984b-4bbdbfdb7e58)

# Layer 7 DDoS Guard

This service sits between the client and server as a means of preventing DDoS attacks that act on the application layer.

## Description

For infrastructure that requires protection, _Layer 7 DDoS Guard_ sits as a service between the client and the given server. The service provides clients with a proof-of-work problem which must be solved before being allowed through via proxy.

For given actors carrying out denial-of-service attacks, the computational power (and therefore cost) outweighs the gain of taking down the underlying infrastructure. This imbalance increases for every increase in difficulty of the given proof-of-work problem.

This is in contrast to conventional anti-DDoS measures like CAPTCHA problems. Firstly, this does not require human intervention and instead acts purely on the limitation of computational power of the attackers. CAPTCHA's are also increasingly vulnerable to attacks by bots as AI/ML models become increasingly powerful, making them easy to circumvent with computer-vision techniques.

## How it Works
The service is setup as an intermediate step before the client is allowed to pass through to the desired URL. To pass through, the following steps are taken:

 - Client requests access to a protected webserver
 - *Layer 7 DDoS Guard* then carries out the following steps:
	 - Checks the browser's cookies to see if the client is verified.
	 - If not, the client is redirected to /pow to solve a proof-of-work problem via browser JavaScript.
	 - Once the client has a solution, it is handed back to the server for verification.
	 - The server verifies that the solution is correct for the challenge.
	 - If the solution is correct then a cookie is handed back to the browser and the service acts as a proxy to the desired URL.

### The Proof-of-Work Problem
The problem is defined with a challenge and an associated difficulty "D". Where the client is trying to find the nonce that when the SHA256 hash is applied to the combination of *challenge+nonce*, the produced hash has "D" leading zeros.

E.g. For a challenge *NPO8DyMd8u85ssgK* with a difficulty 5. The client would increment a nonce by 1 until the SHA256-produced hash started with 5 zeros. E.g.  NPO8DyMd8u85ssgK0, NPO8DyMd8u85ssgK1, NPO8DyMd8u85ssgK2 ... The client would then reach NPO8DyMd8u85ssgK1066074 which happens to produce a hash 000003e7cc8... Once *Layer 7 DDoS Guard* verifies that this solution works, then the client is a given a verification cookie and is then proxied through to the desired service.

![Proof of work problem diagram](https://github.com/michaelgreen-0/layer7-ddos-guard/blob/main/docs/proof-of-work-problem.png?raw=true)

A quad core i7-8650U @ 1.90GHz solves a problem with difficulty 5 in approximately 5 seconds. With a difficulty of 6 this increases to 2 to 3 minutes.


## Configuration

Create a .env from the .env.default file and fill in your given variables.
| Variable | Default | Description
|--|--|--|
| BACKEND_URL | http://mockserver:5001 | URL for protection. This is where users are proxied through to once verified. |
| POW_DIFFICULTY | 3 | Difficulty level of the proof-of-work problem to solve. This is the number of 0-bits required in the produced hash. |
| COOKIE_LIFETIME | 300 | Time in seconds that a verified session is active for. Clients will need to resolve the proof-of-work problem once the session expires. |
| CHALLENGE_LIFETIME | 300 | Time in seconds that a client has to solve a given challenge. |
| REDIS_HOST | redis | Redis service host. |
| REDIS_PORT | 6379 | Redis service port. |

The above default environment variables (BACKEND_URL and REDIS_HOST) make use of docker networks through a docker-compose setup. Check out the *docker/docker-compose.yaml* file. This is ideal for testing and/or simple setups.

Depending on your use-case it may be recommended to use separate servers for your backend service and the *Layer 7 DDoS Guard*. Your backend URL and Redis setup would then need to be updated accordingly. This is scenario dependent and depends on your threat vectors.

## Deployment
As above, your setup will vary depending on your scenario. The following goes through a simple docker compose setup.

 - Ensure your .env file is setup according to the above.
 - Setup your reverse proxy (Nginx in my case) to point to your localhost port 5000. If you want to use a different port then make sure this is reflected in Dockerfile.app and the docker-compose file.
 - Running `docker compose -f docker/docker-compose.yaml up -d --build` will then start Redis and *Layer 7 DDoS Guard* together.
 - Navigate to your protected service either locally or through the internet and you will be taken to the pow page for verification.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
