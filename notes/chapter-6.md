# chapter 6 - link layer

### toc

- intro
- error detection & correction
- lans
  - addressing, arp
  - ethernet
  - switches
  - vlans
- link virtualization: mpls
- data center networking

## intro

### intro

- terminology
  - hosts, routers: nodes
  - comm channels that connect adjacent nodes along comm path: links
    - wired or wireless
    - lans
  - layer 2 pkt: frame, encapsulates datagram
- link layer has responsibility of transfering datagram from one node to physically adjacent node over link

### context

- datagram transferred by different link protocols over different links
  - wifi, ethernet, etc
- each link protocol provides different services
  - may or may not provide reliable data transfer over link

### transport analogy

- trip from princeton to lausanne
  - car: princeton to jfk
  - plane: jfk to geneva
  - train: geneva to lausanne
- tourist is a datagram
- transport segment is comm link
- transport mode is link layer protocol
- travel agent is routing algorithm

### link layer services

- framing & link access
  - encapsulate datagram into frame, adding header & trailer
  - channel access if shared medium
  - mac addrs in frame headers identify src & dst (different from ip addr)
- reliable delivery between adjacent nodes
  - we already know how to do this
  - seldom used on low bit error links
  - wireless links: high error rates
    - why both link level & e2e reliability?
- flow control
  - pacing between adjacent sending & receiving nodes
- error detection
  - errors caused by signal attenuation & noise
  - receiver detects errors, signals retransmission, or drops frame
- error correction
  - receiver identifies & corrects bit errors without retransmission
- half duplex & full duplex
  - with half duplex, nodes at both ends of link can transmit, but not at same time

### host link layer implementation

- in each & every host
- link layer implemented on chip or in nic
- attaches into host's system buses
- combo of hardware, software, & firmware

### interfaces comms

- sending side
  - encapsulates datagram in frame
  - adds error checking bits, rdt, flow control, etc
- receiving side
  - looks for errors, rdt, flow control, etc
  - extracts datagram, passes to upper layer at receiving side

## error detection & correction

### edc (error detection & correction)

- not 100% reliable
  - protocol may miss some errors, but rarely
  - larger edc field yields better detection & correction

### parity checking

- can detect & correct errors without retransmission
  - 2 dimensional parity: detect & correct single bit errors
- single bit parity
  - detect single bit errors
- at receiver
  - compute parity of d received bits
  - compare with received parity bit

### cyclic redundancy check (crc)

- more powerful error detection coding
- d: data bits (given)
- g: bit pattern (generator) of r + 1 bits (given)
- <d, r> = d \* 2^r xor r
- sender: compute r crc bits, r, such that <d, r> exactly divisible by g (mod 2)
  - receiver knows g, divides <d, r> by g. if nonzero remainder, error detected
  - can detect all burst errors less than r + 1 bits
  - widely used in practice (ethernet, 802.11 wifi)

## multiple access protocols

### multiple access links & protocols

- 2 types of links
  - p2p
    - p2p link between ethernet switch & host
    - ppp for dial up internet
  - broadcast (shared wire or medium)
    - old school ethernet
    - upstream hfc in cable based access network
    - 802.11 wireless lan, 4g/5g, satellite

### multiple access protocols

- single shared broadcast protocol
- 2+ simultaneous transmissions by nodes: interference
  - collision if node receives 2+ signals at same time
- multiple access protocol
  - distributed algorithm that determines how nodes can share channel, i.e. determine when node can transmit
  - comm about channel sharing must use channel itself
    - no out of band channel for coordination

### ideal multiple access protocol

- given: multiple access channel of rate r bps
- desiderata
  - when one node wants to transmit, it can send at rate r
  - when m nodes want to transmit, each can send at avg rate r/m
  - fully decentralized
    - no special node to coordinate transmissions
    - no synchronization of clocks or slots
  - simple

### multiple access channel protocols: taxonomy

- channel partitioning
  - divide channel into smaller pieces (time slots, frequency, code)
  - allocate piece to node for exclusive use
- random access
  - channel not divided, allow collisions
  - recover from collisions
- taking turns
  - nodes take turns, but nodes with more to send can take longer turns

### tdma: time division multiple access

- access to channel in rounds
- each station gets fixed length slot (length = pkt transmission time) in each round
- unused slots go idle
- example: 6 station lan, 1, 3, 4 have pkts to send, slots 2, 5, 6 idle

### fdma: frequency division multiple access

- channel spectrum divided into frequency bands
- each station gets fixed frequency band
- unused transmission time in frequency bands go idle
- example: 6 station lan, 1, 3, 4 have pkts to send, frequency bands 2, 5, 6 idle

### random access protocols

- when node has pkt to send
  - transmit at full channel data rate r
  - no a priori coordination among nodes
- 2+ transmitting nodes: collision
- random access protocol specifies how to detect & recover from collisions
- examples
  - aloha, slotted aloha
  - csma, csma/cd, csma/ca

### slotted aloha

- assumptions
  - all frames same size
  - time divided into equal size slots (time to transmit 1 frame)
  - nodes start to transmit only slot beginning
  - nodes are synchronized
  - if 2+ nodes transmit in slot, all nodes detect collision
- operation
  - when node obtains fresh frame, transmits in next slot
    - if no collision, node can send new frame in next slot
    - if collision, node retransmits frame in each subsequent fslot with probability p until success
      - why random?
- pros
  - single active node can continuously transmit at full rate of channel
  - highly decentralized: only slots in nodes need to be in sync
  - simple
- cons
  - collisions, wasting slots
  - idle slots
  - nodes may be able to detect collision in less than time to transmit pkt
  - clock synchronization
- efficiency
  - efficiency: long run fraction of successful slots (many nodes, all with many frames to send)
    - suppose n nodes with many frames to send, each transmits in slot with probability p
      - prob that given node has success in a slot: p(1 - p)^(n - 1)
      - prob that any node has success: np(1 - p)^(n - 1)
      - max efficiency: find p\* that maximizes np(1 - p)^(n - 1)
      - for many nodes, take limit of np(1 - p)^(n - 1) as n goes to infinity, gives 1/e = 0.37
  - at best: used for useful transmissions 37% of the time

### pure aloha

- unslotted aloha: simpler, no synchronization
  - when frame first arrives, transmit immediately
- collision probability increases with no synchronization
  - frame sent at t0 collides with other frames send tin [t0 - 1, t0 + 1]
- pure aloha efficiency: 18%

### csma (carrier sense multiple access)

- simple csma: listen before transmit
  - if channel sensed idle, transmit entire frame
  - if channel sensed busy, defer
- no interruption
- csma/cd: csma with collision detection
  - collisions detected within short time
  - colliding transmissions aborted, reducing channel wastage
  - collision detection easy with wired, difficult with wireless

### csma collisions

- collisions can still occur with carrier sensing
  - propagation delay means 2 nodes may not hear each other's transmission that just started
- collision: entire pkt transmission time wasted
  - distance & propagation delay play role in determining collision probability

### csma/cd

- reduces amount of time wasted in collisions
  - transmission aborted on collision detection
- efficiency
  - tprop: max prop delay between 2 lan nodes
  - ttrans: time to transmit max size frame
  - goes to 1 as tprop goes to 0 and as ttrans goes to infinity
  - better than aloha, and simple, clean, cheap, and decentralized

### ethernet csma/cd algorithm

- ethernet receives datagram from network layer, creates frame
- if ethernet senses channel
  - if idle, start transmitting
  - if busy, wait until idle
- if entire frame transmitted without collision, done
- after aborting, enter binary (exponential) backoff
  - after mth collision, chooses k at random from {0, 1, 2, ..., 2^n - 1}
  - ethernet waits k \* 512 bit times, returns to step 2
  - more collisions -> longer backoff interval

### taking turns protocols

- channel partitioning protocols
  - share channel efficiently & fairly at high load
  - inefficient at low load: delay in channel access, 1/n bandwidth allocated even if only 1 active node
- random access protocols
  - efficient at low load: single node can fully utilize channel
  - high load: collision overhead
- taking turns protocols
  - look for both of best worlds

### taking turns multiple access channel protocols

- token passing
  - control token msg explicitly passed from one node to next sequentially
    - transmit while holding token
  - concerns
    - token overhead
    - latency
    - token is single point of failure

### cable access network: fdm, tdm, & random access

- multiple downstream (broadcast) fdm channels: up to 1.6 Gbps/channel
  - single cmts transmits into channels
- multiple upstream channels (up to 1 Gbps/channel)
  - multiple access: all users contend (random access) for certain upstream channel time slots; others assigned tdm

### cable access network

- docsis (data over cable service interface spec)
  - fdm over upstream, downstream frequency channels
  - tdm upstream: some slots assigned, some have contention
    - downstream map frame: assigns upstream risks
    - request for upstream slots (& data) transmitted random access (binary backoff) in selected slots

### summary of mac protocols

- channel partitioning by time, frequency, or code
  - time division, frequency division
- random access (dynamic)
  - aloha, s-aloha, csma, csma/cd
  - carrier sensing: easy in some media (wire), hard in others (wireless)
  - csma/cd used in ethernet
  - csma/ca used in 802.11
- taking turns
  - polling from central site, token passing
  - bluetooth, fddi, token ring

## lans

## addressing & arp

### mac addrs

- 32 bit ip addr
  - network layer addr for interface
  - used for layer 3 forwarding
- mac (or lan or physical or ethernet) addr
  - function: used locally to get frame from one interface to another interface in same subnet
  - 48 bit mac addr (for most lans) burned in nic rom, also sometimes software settable
- mac addr allocation administered by ieee
- manufacturer buys portion of mac addr space to assure uniqueness
- analogy
  - mac addr: like social security number
  - ip addr: like postal addr
- mac flat addr: portability
  - can move interface from one lan to another
  - recall ip addr not portable: depends on ip subnet to which node it is attached

### arp (addr resolution protocol)

- arp table: each ip node (host, router) on lan has table
  - ip/mac addr mappings for some lan nodes
    - <ip addr, mac addr, ttl>
  - ttl (time to live): time after which addr mapping will be forgotten (typically 20 min)

### arp in action

- example: a wants to send datagram to b
- a broadcasts arp query, containing b's ip addr
  - all nodes on lan receive arp query
- when b receives a's arp msg, adds a to its arp table, sends frame back to a

### routing through another subnet: addressing

- scenario: a and b on different subnets but both connected to r
- walkthrough sending a datagram from a to b via r
  - focus on addressing - at ip (datagram) & mac (frame) layer levels
  - assume that
    - a knows b's ip
    - a knows ip addr of first hop router
    - a knows r's mac addr
  - a creates ip datagram with ip (src a, dst b)
  - a creates link layer frame containing ip datagram from a to b
    - r's mac addr is frame's dst
  - frame sent from a to r
  - frame received at r, datagram removed, passed up to ip
  - r determines outgoing interface, passes datagram with ip src a, dst b to link layer
  - r creates link layer frame containing datagram from a to b. frame dst addr: b's mac addr
  - r determines outgoing interface, passes datagram with ip src a, dst b to link layer
  - r creates link layer frame containing a to b ip datagram. frame dst addr: b's mac addr
  - transmits link layer frame

## ethernet

### ethernet

- dominant wired lan medium
  - first widely used lan tech
  - simple, cheap
  - kept up with speed race: 10 Mbps-400 Gbps
  - single chip, multiple speeds
- physical topology
  - bus: popular through mid 90s
    - all nodes in same collision domain (can collide with each other)
  - switched: prevails today
    - active link layer 2 switch in center
    - each spoke runs a separate ethernet protocol (nodes do not collide with each other)
- frame structure
  - sending interface encapsulates ip datagram (or other network layer protocol pkt) in ethernet frame
  - preamble
    - used to synchronize receiver & sender clock rates
    - 7 bytes of 10101010 followed by one byte of 10101011
  - addrs: 6 byte src & dst mac addrs
    - if adapter receives frame with matching dst addr or with broadcast addr (e.g. arp pkt), passes data in frame to network layer protocol
      - otherwise, discard frame
  - type: indicates higher layer protocol
    - mostly ip but others possible, e.g. novell ipx, appletalk
    - used to demux at receiver
  - crc at receiver
    - error detected: frame dropped
