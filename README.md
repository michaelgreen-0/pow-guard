![image](https://github.com/user-attachments/assets/822c973e-a4c2-4da8-b818-ac3b7bcff9e1)

# Layer 7 DDoS Guard

This service sits between the client and server as a means of preventing DDoS attacks that act on the application layer.

## Description

For infrastructure that requires protection, _Layer 7 DDoS Guard_ sits as a service between the client and the given server. The service provides clients with a proof-of-work problem which must be solved before being allowed through via proxy.

For given actors carrying out denial-of-service attacks, the computational power (and therefore cost) outweighs the gain of taking down the underlying infrastructure.

This is in contrast to conventional anti-DDoS measures like CAPTCHA problems. Firstly, this does not require human intervention and instead acts purely on the limitation of computational power of the attackers. CAPTCHA's are also increasingly vulnerable to attacks by bots as AI/ML models become increasingly powerful, making them easy to circumvent with computer-vision techniques.

## How it Works
TBC

## Configuration

Create a .env from the .env.default file and copy your given variables.
{{ INSERT ENV VARIABLES TABLE }}

## Deployment

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
