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

### http request message

- ascii (human-readable format)
- request line (get, post, head commands)
- format
  method url version\r\n
  header field value\r\n
  ...
  \r
  body

### http request messages

- post method
  - web page often includes form input
  - user input sent from client to server in message body
- head method
  - requests headers (only) that would be returned if specified url were requested with get method
- get method (sending data to server)
  - include user data in url field of get request message (following '?', separated by '&')
- put method
  - uploads new file (object) to server
  - completely replaces file that exists at specified url with content in entity body of post request message

### response message

- status line (protocol code phrase)
- codes
  - 200 ok
  - 301 moved permanently
  - 400 bad request
  - 403 forbidden
  - 404 not found
  - 505 http version not supported

### maintaining user/server state: cookies

- http is stateless, so how do we "maintain state"?
- no notion of multi-step exchanges of http messages to complete a web transaction
  - no need for client/server to track state of multi-step exchange
  - all http requests are independent of each other
  - no need for client/server to recover from partially complete transaction
- cookies maintain some state between transactions with 4 components
  - cookie header line of http response message
  - cookie header line in next http request message
  - cookie file kept on user's host, managed by browser
  - backend database at web site
- use of cookies
  - authorization
  - shopping carts
  - recommendations
  - user session state (web email)
- how to keep state?
  - at endpoints over several transactions
  - in messages: cookies in http messages carry state
- track user's browsing behavior
  - first party cookies track on a site
  - third party cookies track across multiple websites without user ever choosing to visit tracker site (!)
  - tracking may be (is) invisible to user
  - third party tracking via cookies disabled by default in safari & firefox, disabled in chrome in 2023

### gdpr (eu general data protection regislation)

- if cookies can identify individual -> considered personal data -> subject to gdpr personal data regulations

### web caches (aka proxy servers)

- goal: satisfy client requests without involving origin server
- user configures browser to point to local web cache
- browser sends all http requests to cache
  - if object in cache, cache returns object to client
  - else cache requests object from origin server, caches received object, returns object to client
- acts as both client & server: server for original requesting client, client to origin server
- server tells cache about object's allowable caching in response header
- why?
  - reduce response time for client request bc cache is closer to client
  - reduce traffic on institution's access link
  - internet saturated with caches
    - enables poor content providers to more effectively deliver content

### browser caching: conditional get

- goal: don't send object if browser has up-to-date cached version
  - no object transmission delay (or use of network resources)
- client: specify date of browser-cached copy in http request (if-modified-since)
- server: response contains no object if browser-cached copy is up-to-date: http/1.0 304 not modified

### http versions

- http1.1
  - introduced multiple pipelined gets over single tcp connection
  - server responds fcfs to get requests
  - with fcfs, small objects may have to wait for transmission (head-of-line (hol) blocking) behind large objects
  - loss recovery (retransmitting lost tcp segments) stalls object transmission
- http2 (rfc 7540, 2015) increases flexibility at server in sending objects to client
  - key goal: decreased delay in multi-object http requests
  - methods, status codes, most header fields unchanged from http1.1
  - transmission order of requested objects based on client-specified object priority (not necessarily fcfs)
  - push unrequested objects to client
  - divide objects into frames, schedule frames to mitigate hol blocking
- http3
  - http2 over single tcp connection means:
    - recovery from packet loss still stalls all object transmissions
      - like in http1.1, browsers have incentive to open multiple parallel tcp connections to reduce stalling & increase overall throughput
    - no security over vanilla tcp connection
  - add security, per-object error & congestion control (more pipelining) over udp

### quic: quick udp internet connections

- app-layer protocol on top of udp
  - increase performance of http
  - deployed on many google servers & apps (chrome, youtube mobile)
- adopts approaches for connection establishment, error control, congestion control
  - error & congestion control: "readers familiar with tcp's loss detection & congestion control will find algorithms here that parallel well-known tcp ones"
  - connection establishment: reliability, congestion control, authentication, encryption, state established in one rtt
- rather than both a tcp and tls handshake, quic does a 1 rtt handshake that establishes connection & handles security, then sends data
- client can use last session ticket for encryption & authentication for new connection -> 0 rtt delay

## email, smtp, imap

### email - 3 major components

- user agent
  - composes, edits,reads mail
- mail server
  - outgoing & incoming messages stored on mail server
  - mailbox contains incoming messages for user
  - message queue of outgoing mail messages to be sent
- simple mail transfer protocol: smtp
  - client: sending mail server, "server": receiving mail server

### smtp (rfc 5321)

- uses tcp to reliably transfer email message from client (mail server initiating connection) to server, port 25
  - direct transfer: sending server (acting like client) to receiving server
- 3 phases of transfer
  - handshaking
  - message transfer
  - closure
- command/response interaction like http
  - commands: ascii text
  - response: status code & phrase

### scenario: a sends email to b

1. a uses user agent to compose email message to b@someschool.edu
2. a's ua sends message to her mail server using smtp, message placed in queue
3. client side of smtp at mail server opens tcp connection with bob's mail server
4. smtp client sends alice's message over tcp connection
5. bob's mail server places message in bob's mailbox
6. bob invokes ua to read message

### smtp: observations

- compared to http
  - http: client pull
  - smtp: client push
  - both have ascii command/response interaction & status codes
  - http: each object encapsulated in its own response message
  - smtp: multiple objects sent in multi-part message
  - smtp uses persistent connections
  - smtp requires message to be in 7-bit ascii
  - smtp server uses \r\n.\r\n to determine end of message

### mail message format

- rfc 5321 defines protocol for _exchanging_ email messages
- rfc 2822 defines _syntax_ for email itself, like html defines syntax for web documents
  - header lines, e.g. to, from, subject
  - body: message, ascii only

### retrieving email: mail access protocols

- smtp: delivery/storage of email messages to receiver's server
- mail access protocol: retrieval from server
  - imap: internet mail access protocol (rfc 3501): messages stored on server, imap provides retrieval, deletion, folders of stored messages on server
- http can provide web-based interface on top of smtp & pop/imap to retrieve email

## dns

### dns: domain name system

- distributed database implemented in hierarchy of many name servers
- app-layer protocol: hosts & dns servers communicate to translate names to addrs
- core internet function
- complexity at network's "edge"

### dns services & structure

- services
  - hostname-to-ip translation
  - host aliasing
    - canonical, alias names
  - mail server aliasing
  - load distribution
    - replicated web servers: many ip addrs correspond to one name

### thinking about dns

- enormous distributed database: ~ billions records, each simple
- handles many trillions of queries per day
  - many more reads than writes
  - performance matters: almost every internet transaction interacts with dns - ms count!
- organizationally & physically decentralized
  - millions of different orgs responsible for their records
- reliability, security

### dns: distributed, hierarchical database

- client wants address for amazon.com, 1st approximation
  - queries root server to find .com dns server
  - queries .com dns server to get amazon.com dns server
  - queries amazon.com dns server to get amazon.com ip

### root name servers

- official, contact-of-last-resort by name servers that can't resolve name
- incredibly important internet function
  - internet couldn't function without it
  - dnssec - provides security (authentication, message integrity)
- icann (internet corporation for assigned names & numbers) manages root dns domain

### top-level domain (tld) & authoritative servers

- tld servers
  - responsible for .com, .org, .net, .edu, .aero, .jobs, .museums, all top-level country domains, e.g. .cn, .uk, .fr, .ca, .jp
  - network solutions: authoritative registry for .com, .net tld
  - educause: .edu tld
- authoritative servers
  - org's own dns server(s), providing authoritative hostname-to-ip mappings for org's named hosts
  - can be maintained by org or service provider

### local dns servers

- when host makes dns query, sent to local dns server
  - local dns server returns reply, answering:
    - from its local cache of recent name-addr translation pairs (possibly out of date!)
    - forwarding request into dns hierarchy for resolution
  - each isp has local dns, how to find it
    - macos: `scutil --dns`
    - windows: `ipconfig \all`
- local dns server doesn't strictly belong to hierarchy

### query types

- iterated query
  - contacted server replies with name of server to contact
  - "i don't know this name, but ask this server"
- recursive query
  - put burden of name resolution on contacted name server
  - heavy load at upper levels of hierarchy?

### catching dns info

- once any name server learns mapping, it caches mapping, immediately returns cached mapping in response to query
  - caching improves response time
  - cache entries timeout after some time (ttl)
  - tld servers typically cached in local name servers
- cached entries may be out of date
  - if named host changes ip addr, may not be known internet-wide until all ttls expire
  - best-effort name-addr translation

### dns records

- resource records (rr) format: (`name, value, type, ttl`)
- type=A
  - `name` is hostname, `value` is ip
- type=NS
  - `name` is domain (e.g. foo.com)
  - `value` is hostname of authoritative name server for this domain
- type=CNAME
  - `name` is alias name for some canonical (real) name
- type=MX
  - `value` is name of smtp mail sever associated with `name`

### dns protocol messages

- ds query and reply messages have same format
  - header
    - identification: 16-bit number for query, reply to query uses same number
    - flags
      - query/reply
      - recursion desired
      - recursion available
      - reply is authoritative
  - body
    - name, type fields for query
    - rrs in response to query
    - records for authoritative servers
    - additional "helpful" info that may be used

### getting info into dns

- register website name at dns registrar
  - provide names, ip addrs of authoritative name server (primary & secondary)
  - registrar inserts ns, a rrs into .com tld server (example.com, dns1.example.com, NS) (dns1.example.com, x.x.x.1, A)
- create authoritative server locally with ip addr x.x.x.1
  - type a record for www.example.com
  - type mx record for example.com

### dns security

- ddos attacks
  - bombard root servers with traffic
    - not successful to date
    - traffic filtering
    - local dns servers cache ips of tld servers, allowing root server bypass
  - bombard tld servers
    - potentially more dangerous
- spoofing attacks
  - intercept dns queries, return bogus replies
    - dns cache poisoning
    - rfc 4033: dnssec authentication services

## video streaming & cdn

### context

- stream video traffic: major consumer of internet bandwidth
  - netflix, youtube, amazon prime: 80% of residential isp traffic (2020)
- challenge: scale - how to reach ~1b users?
- challenge: heterogeneity
  - different users have different capabilities (e.g. wired vs. mobile, high vs low bandwidth)
- solution: distributed, app-level infrastructure

### multimedia: video

- video: sequence of images displayed at constant rate
- digital image: array of pixels
  - each pixel represented by bits
- coding: use redundancy within & between images to decrease number of bits used to encode image
  - spatial (within image)
  - temporal (from one image to next)
- cbr (constant bitrate): fixed encoding rate
- vbr (variable bitrate): encoding rate changes as amount of spatial & temporal encoding changes
- examples
  - mpeg 1 (cd-rom): 1.5 Mbps
  - mpeg 2 (dvd): 3-6 Mbps
  - mpeg 4 (often used on internet): 64 Kbps - 12 Mbps

### streaming stored video

- challenges
  - server-client bandwidth will vary over time, with changing network congestion levels (in house, access network, network core, video server)
  - packet loss, delay due to congestion will delay playout, or result in poor video quality
  - continuous playout constraint: during client video playout, playout timing must match original timing
    - but network delays are visible (jitter), so will need client-side buffer to match continuous playout constraint
  - client interactivity: pause, fast-forward, rewind, jump through video
  - video packets may be lost, retransmitted
- playout buffering
  - client-side buffering & playout delay: compensate for network-added delay, delay jitter

### streaming multimedia: dash (dynamic, adaptive streaming over http)

- server
  - divides video file into multiple chunks
  - each chunk encoded at multiple different rates
  - different rate encodings stored in different files
  - files replicated in various cdn nodes
  - manifest file: provides urls for different chunks
- client
  - periodically estimates server-client bandwidth
  - consulting manifest, requests 1 chunk at a time
    - chooses maximum coding rate sustainable for current bandwidth
    - can choose different coding rates at different points in time (depending on available bandwidth), & from different servers
- "intelligence" at client: client determines
  - when to request chunk (so that buffer starvation/overflow doesn't occur)
  - what rate to request (higher quality when more bandwidth available)
  - where to request chunk (can reqeust from url server closer to client or that has higher available bandwidth)
  - streaming video = encoding + dash + playout buffering
