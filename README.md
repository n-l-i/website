# My personal little website

 - [Overview](#overview)
 - [Usage](#usage)
 - [Contents](#contents)
     - [Chess AI](#contents-chessai)
     - [Authentication protocol](#contents-spbmap)
     - [CT log monitor](#contents-ctl)
     - [Network simulator](#contents-networksim)

# <a name="overview"> Overview
This is the source code for my personal website where I host a small selection of my projects.

# <a name="usage"> Usage
To host the website use the `init.sh` and `run.sh` scripts.
* `init.sh [-d or -p] -u [url]`: Initialise the source code in development mode (`-d`) or production mode (`-p`) and specify where to host it.
* **Example**: `./init.sh -d -u https://localhost:5001`
* `run.sh [-d or -p]`: Host the website in development mode (`-d`) or production mode (`-p`).
* **Example**: `./run.sh -p`

# <a name="contents"> Contents
Here follows a short description of the projects present on the page.

### <a name="contents-chessai"> Chess AI
This is the chess AI I made ([link](https://github.com/n-l-i/chess_ai)).
It is a chess engine based on alpha beta pruned minimax decisions and basic value definitions.
Given 10 seconds to think through each move, the AI usually cannot win against confident players but it can pose a challenge to more inexperienced players.

### <a name="contents-spbmap"> Authentication protocol
This is the specification for the authentication protocol I made ([link](https://github.com/n-l-i/Simple_Password_Based_Mutual_Authentication_Protocol)).
It is a mutual authentication protocol designed to be easy to implement correctly.
A client registers a secret on the server and then they can each at a later time assert that the other party knows this secret.

### <a name="contents-ctl"> CT log monitor
This is the specification for the CT log monitor I made (private repository).
It is a certificate transparency log monitor, collecting the certificates submitted to common CT logs and presenting simple statistics of them.

### <a name="contents-networksim"> Network simulator
This is the specification for the network simulator I made ([link](https://github.com/n-l-i/network_simulator)).
This is a program for creating simple ad-hoc network simulations, simulating the flow of messages through a node network using different routing protocols.
