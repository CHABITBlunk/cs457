# chapter 2 - application layer

### toc

- principles of network applications
- web & http
- email, smtp, imap
- dns
- video streaming & content distribution
- socket programming with udp & tcp

## principles of network applications

### creating network app

- write programs that can
  - run on (different) end systems
  - communicate over network
  - e.g. web server software communicates with browser software
- no need to write software for network core devices
  - network core devices do not run user apps
  - apps on end systems allow for rapid app development & propagation

### peer-peer architecture

- no always-on server
- arbitrary end systems directly communicate
- peers request service from other peers, provide service in return to other peers
  - self scalability: new peers bring new service capacity, as well as new service demands
- peers intermittently connected & change ip addrs
  - complex mgmt
- e.g. p2p file sharing (bittorrent)

### procs communicating

- proc: program running within host
- within same host, 2 procs communicate with ipc (defined by os)
- procs in different hosts communicate by exchanging messages
- clients, servers
  - client proc: proc that initiates communciation
  - server proc: proc that waits to be contacted
- note: apps with p2p architectures have client procs & server procs

### sockets

- proc sends/receives messages to/from its socket
- socket analogous to door
  - sending proc shoves message out door
  - sending proc relies on transport infrastructure on other side of door to deliver message to socket at receiving proc
  - 2 sockets involved, one on each side

### addressing procs

- to receive message, proc must have identifier
- host device has unique 32-bit ip addr
- identifier includes both ip addr & port numbers associated with proc on host
- e.g. port numbers: http: 80, mail server: 25
- to send http message, you need both ip and port

### app-layer protocol defines

- types of messages exchanged (e.g. request, response)
- message syntax (what fields in messages, how fields are delineated)
- message semantics (meaning of info in fields)
- rules for when & how procs send & respond to messages
- open protocols
  - defined in rfcs, everyone has access to protocol definition
  - allows for interoperability
  - e.g. http, smtp
- proprietary protocols
  - e.g. zoom

### what transport service an app needs

- data integrity
  - some apps require 100% reliable data transfer, other apps can tolerate some loss
- timing
  - some apps require low delay to be "effective"
- throughput
  - some apps require minimum amount of throughput to be "effective", others make use of whatever throughput they get
- security
  - encryption, data integrity, etc.

### transport service requirements: common apps

| application            | data loss     | throughput                                      | time sensitive   |
| ---------------------- | ------------- | ----------------------------------------------- | ---------------- |
| file/transfer download | no loss       | elastic                                         | no               |
| email                  | no loss       | elastic                                         | no               |
| web docs               | no loss       | elastic                                         | no               |
| real-time audio/video  | loss-tolerant | audio: 5 Kbps - 1 Mbps, video: 10 Kbps - 5 Mbps | yes, 10's ms     |
| streaming audio/video  | loss-tolerant | same as above                                   | yes, few seconds |
| interactive games      | loss-tolerant | >= Kbps                                         | yes, 10's ms     |
| text messaging         | no loss       | elastic                                         | yes and no       |

### internet transport protocols services

- tcp
  - reliable transport
  - flow control: sender won't overwhelm receiver
  - congestion control: throttle sender when network overloaded
  - connection-oriented: setup required between client & server procs
  - doesn't provide timing, minimum throughput guarantee, security
- udp
  - unreliable transport
  - doesn't provide reliability, flow control, congestion control, timing, throughput guarantee, security, or connection setup

| application            | app-layer protocol                             | transport protocol |
| ---------------------- | ---------------------------------------------- | ------------------ |
| file transfer/download | ftp (rfc 959)                                  | tcp                |
| email                  | smtp (rfc 5321)                                | tcp                |
| web documents          | http (rfc 7230, 9110)                          | tcp                |
| internet telephony     | sip (rfc 3261), rtp (rfc 3550), or proprietary | tcp or udp         |
| streaming audio/video  | http (rfc 7230), dash                          | tcp                |
| interactive games      | wow, fps (proprietary)                         | udp or tcp         |

### securing tcp

- vanilla tcp & udp sockets
  - no encryption
  - cleartext passwords sent into socket traverse internet in cleartext (!)
- tls (transport layer security)
  - provides encrypted tcp connections
  - data integrity
  - endpoint authentication
- tls implemented in app layer
  - apps use tls libs that use tcp in turn
  - cleartext sent into socket traverse internet encrypted
  - more in chapter 8

## web & http

### web & http: a review

- web page consists of objects, each of which can be stored on different web servers
- object can be html file, jpeg, java applet, audio file, etc.
- web page consists of base html file which includes several referenced objects, each addressable by a url

### http overview

- stands for hypertext transfer protocol
- web's app-layer protocol
- client/server model
  - client: browser that requests, receives, displays web objects
  - server: web server sends objects in response to requests
- http uses tcp
  - client initiates tcp connection (creates socket) to server, port 80
  - server accepts tcp connection from client
  - http messages (app-layer protocol messages) exchanged between browser & web server
  - tcp connection closed
- http is stateless
  - server maintains no info about past client requests
  - protocols that maintain state are more complex
    - past history (state) must be maintained
    - if server/client crashes, views of state may be inconsistent, must be reconciled

### 2 types of http connections

- non-persistent
  - tcp connection opened
  - <= 1 object sent over connection
  - connection closed
  - downloading multiple objects requires multiple connections
  - example
    - user enters url
    - http client sends syn to http server
    - server receives syn, sends syn-ack
    - client receives syn-ack, sends ack & message indicating what object user wants to see
    - server receives ack & message, sends object
    - server closes tcp connection
    - client receives response message containing html file, displays html. (example: html file has 10 referenced jpeg, repeat steps for each jpeg)
- persistent
  - tcp connection opened to server
  - multiple objects can be sent over single tcp connection
  - connection closed
