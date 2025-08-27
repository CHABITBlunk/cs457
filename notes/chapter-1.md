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
