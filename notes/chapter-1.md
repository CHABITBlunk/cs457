# chapter 1 - introduction

### internet - a "nuts and bolts view"

- billions of connected computing devices
  - hosts: end systems running network apps at internet's "edge"
- packet switches - forward packets (e.g. routers, switches)
- communication links
  - fiber, copper, radio, satellite
  - bandwidth - transmission rate
- networks
  - connection of devices, routers, links managed by organization
- internet: network of networks
  - interconnected isps
- protocols are everywhere
  - control sending & receiving messages (e.g. http, tcp, ip, &c.)
- internet standards
  - rfc: request for comments
  - ietf: internet engineering task force

### internet - services view

- infrastructure that provides services to apps
  - web, streaming video, multimedia teleconferencing, email, games, ecommerce, social media, interconnected appliances
  - provides programming interface to distributed apps
    - hooks allowing sending/receiving apps to connect to, use internet transport service
    - provides service options, analogous to postal service

### what is a protocol?

- define format, order of messages sent & received among entities, & actions taken on message transmission & receipt
- rules for:
  - specific message sent
  - specific actions taken when message received or other events
- human protocols
  - "what's the time?"
  - "i have a question"
  - introductions
- network protocols
  - computers (devices) rather than humans

### network edges

- hosts: clients & servers
- servers often in data centers
- access networks & physical media through wired or wireless comms links

### network core

- interconnected routers
- network of networks

### how to connect end systems to edge router?

- residential access nets
- institutional access networks (school, company)
- mobile access networks (wifi, 4g/5g)

access networks

- cable-based access
  - frequency division multiplexing (fdm)
    - different channels transmitted in different frequency bands
  - hfc: hybrid fiber coax
    - asymmetric - up to 40 Mbps - 1.2 Gbps downstream transmission rate, 30-100 Mbps upstream transmission rate
  - network of cable, fiber attaches home to isp router
    - homes share access network to cable headend
- digital subscriber line (dsl)
  - use existing phon eline to central office dslam
    - data over dsl phone line goes to internet
    - voice over dsl phone line goes to phone net
  - 24-52 Mbps dedicated downstream transmission rate
  - 3.5-16 Mbps dedicated upstream transmission rate
- wireless
  - shared wireless access network connects end system to router via base station (aka access point)
  - wlan
    - typically within or around building (~100 ft)
    - 802.11.b/g/n (wifi): 11, 54, 450 Mbps transmission rate
  - wide-area cellular access networks
    - provided by mobile, cellular network operator (10s of km)
    - 10s of Mbps
    - 4g/5g cellular networks
- enterprise networks
  - companies, universities, etc
  - mix of wired, wireless link technologies, connecting a mix of switches & routers
    - ethernet: wired access at 100 Mbps, 1 Gbps, 10 Gbps
    - wifi: wireless access points at 11, 54, 450 Mbps
- data center networks
  - high-bandwidth links (10s to 100s Gbps) connect hundreds to thousands of servers together and to internet

### host: sends packets of data

- host sending function
  - takes application message
  - breaks into smaller chunks (packets) with length $L$ bits
  - transmits packet into access network at transmission rate $R$
    - link transmission rate (link capacity, link bandwidth)
    - packet transmission delay = time needed to transmit $L$-bit packet into link = $L / R$

### links: physical media

- bit: propagates between transmitter/receiver pairs
- physical link: what lies between transmitter & receiver
- guided media
  - signals propagate in solid media: copper, fiber, coax
- unguided media
  - signals propagate freely, e.g. radio
- coaxial cable
  - 2 concentric Cu conductors
  - bidirectional
  - broadband
    - multiple frequency channels on cable, 100s Mbps per channel
- fiber optic cable
  - glass fiber carrying light pulses, each pulse a bit
  - high-speed operation
    - high speed point-to-point transmission (10s-100s Gbps)
  - low error rate
    - repeaters spaced far apart
    - immune to EM noise
- wireless radio
  - signal carried in various "bands" in EM spectrum
  - no physical wire
  - broadcast, "half-duplex" (sender to receiver)
  - propagation environment effects
    - reflection
    - obstruction by objects
    - interference/noise
  - radio link types
    - wlan (wifi) - 10-100s Mbps, 10s of meters
    - wide-area (e.g. 4g/5g cellular) - 100s Mbps (4g/5g), over ~10 km
    - bluetooth - short distances, limited rates
    - terrestrial microwave - point-to-point, 45 Mbps
    - satellite - up to < 100 Mbps (starlink) downlink, 270 ms end-end delay (geostationary)

### network core

- mesh of interconnected routers
- packet switching: hosts break app-layer messages into packets
  - network forwards packets from one router to next, across links on path from source to destination
- 2 key functions
  - forwarding (switching)
    - local action: move arriving packets from router's input link to appropriate router output link
  - routing
    - global action: determine source-destination paths taken by packets
    - routing algorithms

### packet switching

- store-and-forward
  - packet transmission delay: takes $L / R$ seconds to transmit (push out) $L$-bit packet into link at R bps
  - store and forward: entire packet must arrive at router before can be transmitted on next link
- queuing
  - occurs when work arrives faster than can be serviced
  - if arrival rate to link exceeds transmission rate for some period of time
    - packets will queue, waiting to be transmitted on output link
    - packets can be dropped if buffer in router fills up

### circuit switching

- alternative to packet switching
- end-end resources allocated to, reserved for "call" between source & destination
  - dedicated resources: no sharing -> circuit-like (guaranteed) performance
  - circuit segment idle if not used by call (no sharing)
  - commonly used in traditional phone networks

### packet switching vs circuit switching

- example
  - 1 Gbps link
  - each user: 100 Mbps when active, active 10% of time
  - how many users can use this network under circuit switching & packet switching?
    - circuit switching: 10 users
    - packet switching: with 35 users, probability > 10 active at same time less than 0.0004
- packet switching
  - better for data that comes in bursts due to resource sharing & simpler setup without calls
  - excessive congestion possible: packet delay & loss due to buffer overflow
    - need protocols to control congestion & transfer data reliably
- how to provide circuit-like behavior with packet switching?
  - various techniques for this

### internet structure: "network of networks"

- hosts connect to internet via access isps
- access isps must be interconnected so any 2 hosts can send packets to each other
- resulting network of networks very complex
  - evolution driven by capitalism
- how to connect millions of access isps?
  - option: connect each access isp to a global transit isp - customer & provider isps have economic agreement
    - if one global isp is viable business, there will be competitors who want to be connected
    - regional networks may arise to connect access nets to isps
    - content provider networks may run their own network to bring services & content close to end users
- at center: small number of well-connected large networks
  - tier-1 commercial isps (e.g. level 3, sprint, at&t, ntt): national & international coverage
  - content provider networks (e.g. google, facebook): private network that connects data centers to internet, often bypassing tier-1, regional isps

### packet delay & loss

- packets queue in router buffers, waiting for turn in transmission
  - queue length grows when arrival rate to link (temporarily) exceeds output link capacity
- loss occurs when memory to hold queued packets fills up
- nodal delay = nodal processing delay + queuing delay + transmission delay + propagation delay
- $La/R$ ~ 0: avg queuing delay small; $La/R$ <= 1: queuing delay large; $La/R$ > 1: more work arriving than can be serviced - infinite delay

### "real" internet delays & routes

- what do "real" internet delay & loss look like?
  - traceroute provides source -> router delay mgmt along end-end internet path towards destination
  - for all i
    - send 3 packets that will reach router i on path towards destination (ttl = i)
    - router i will return packets to sender
    - sender measures time between transmission & reply

### packet loss

- queue (buffer) preceding link in buffer capacity is finite
- packet arriving to full queue dropped
- dropped packet may be retransmitted by previous node, source end system, or not at all (depending on protocol)

### throughput

- throughput: rate (bits/time) at which bits are sent from sender to receiver
  - instantaneous: rate at given time
  - average: rate over period of time
- bottleneck link: link on end-end path that constrains throughput

### network security

- internet not originally designed with (much) security in mind
  - original vision: group of mutually trusting users attached to transparent network
  - internet protocol designers must always catch up
  - security considerations in all layers
- what to think about nowadays
  - how people can attack networks
  - how we can defend networks against attacks
  - how to design architectures immune to attacks

### malicious activities

- packet interception
  - sniffing
    - broadcast media (shared ethernet, wireless)
    - promiscuous network interface reads/records all packets passing by
- fake identity
  - ip spoofing: injection of packets with false source addr
- denial of service
  - dos: attackers make resources unavailable to legit traffic by overwhelming resource with illegit traffic
    - select target
    - break into hosts around network
    - send packets to target from compromised hosts

### lines of defense

- authentication
- confidentiality
- integrity
- access restrictions
- firewalls

### protocol layers & reference models

- layering
  - explicit structure allows identification, relationship of system pieces
  - modularization eases maintenance & system updates
    - change in service implementation: transparent to rest of system
  - layered stack
    - application: supporting network apps
    - transport: proc-proc data transfer
    - network: routing of diagrams source -> destination
    - link: data transfer between neighboring network elements
    - physical: bits on wire
  - offers encapsulation

### history

- 1961-1972: early packet switching principles
  - 1961: kleinrock - queuing theory shows effectiveness of packet switching
  - 1964: baran - packet switching in military nets
  - 1967: arpanet conceived by advanced research projects agency (arpa)
  - 1969: first arpanet node operational
  - 1972: arpanet public demo, ncp (network control protocol) first host-host protocol, first email program, arpanet has 15 nodes
- 1972-1980: internetworking, new & proprietary networks
  - 1970: alohanet satellite network in hawaii
  - 1974: cerf & kahn - architecture for interconnecting networks - define today's internet architecture
    - minimalism, autonomy - no internal changes required to interconnect networks
    - best-effort service model
    - stateless routing
    - decentralized control
  - 1976: ethernet at xerox parc
  - late 70s: proprietary architectures: decnet, sna, xna
  - 1979: arpanet has 200 nodes
- 1980-1990: new protocols, proliferation of networks
  - 1983: deployment of tcp/ip
  - 1982: smtp
  - 1983: dns
  - 1985: ftp
  - 1988: tcp congestion protocol
  - new national networks: csnet, bitnet, nsfnet, minitel
  - 100k hosts connected to confederation of networks
- 1990s-2000s: commercialization, web, new apps
  - early 1990s: arpanet decommissioned
  - 1991: nsf lifts restrictions on commercial use of nsfnet (decommissioned 1995)
  - early 1990s: web
    - hypertext
    - berners-lee: html, http
    - 1994: mosaic, later netscape
    - late 1990s: commercialization of web
  - late 1990s-2000s
    - more killer apps, instant messages, p2p
    - network security to forefront
    - est 50m host, 100m+ users
    - backbone links running at Gbps
  - 2005-present: scale, sdn, mobility, cloud
    - aggressive deployment of broadband home access (10-100s Mbps)
    - 2008: software-defined networking (sdn)
    - increasing ubiquity of high-speed wireless: 4g/5g, wifi
    - service providers (google, facebook, microsoft) create own networks
      - bypass commercial internet to connect "close" to end user, providing "instantaneous" access to social media, search, video content
    - enterprises run their services in "cloud" (e.g. aws, azure)
    - rise of smartphones: more mobile than fixed devices on internet (2017)
    - 2023: ~15b devices attached to internet
