# chapter 3

### toc

- transport layer
- multiplexing & demultiplexing
- udp
- bandwidth & delay
- principles of reliable data transfer
- tcp
- principles of congestion control
- tcp congestion control
- evolution of tls

## transport layer

### transport services & protocols

- provide logical comms between app procs running on different hosts
- transport protocol actions in end systems
  - sender: breaks app messages into segments, passes to network layer
  - receiver: reassembles segments into messages, passes to application layer

### transport vs network layer services & protocols

- transport: comms between procs
  - relies on, enhances network layer services
- network: comms between hosts

## multiplexing & demultiplexing

### multiplexing/demultiplexing

- multiplexing as sender
  - handle data from multiple sockets, add transport header (later used for demultiplexing)
- demultiplexing as receiver
  - use header info to deliver received segments to correct socket
- how demultiplexing works
  - host receives ip datagrams
    - each datagram has source & destination ip

### connless demultiplexing

- when creating socket, must specify host-local port num
- when creating datagram to send to udp socket, must specify destination ip & destination port
- when receiving host receives udp segment, checks destination port num in segment, directs udp segment to socket with that port num
- ip/udp datagrams with same destination port but different source ips and/or source ports will be directed to same socket at receiving host
- uses only destination port

### conn-oriented demultiplexing

- tcp socket identified by 4-tuple
  - source ip
  - source port
  - dest ip
  - dest port
- demux: receiver uses all 4 values to direct segment to appropriate socket

## udp

### udp

- no frills, bare bones internet transport protocol
- best effort service, udp segments may be lost or delivered out of order
- connless
  - no handshake between udp sender & receiver
  - each udp segment handled independently of others
- why it exists
  - no conn establishment (avoid rtt delay)
  - simple: no conn state at sender or receiver
  - small header size
  - no congestion control
    - can keep throwing pkts out as fast as desired
    - can function in the face of congestion
- use cases
  - streaming multimedia apps (loss tolerant, rate senstive)
  - dns
  - snmp
  - http/3
- if reliable transfer needed over udp (e.g. http/3)
  - add needed reliability at app layer
  - add congestion control at app layer
- udp also contains a checksum in header that receiver has to check to ensure network is good

### internet checksum

- detect errors in transmitted segment
- sender
  - treat contents of udp segment (including udp header fields & ips) as sequence of 16-bit ints
  - checksum: one's complement sum of segment content
  - checksum value put into udp checksum field
- receiver
  - compute checksum of received segment
  - check if computed checksum = checksum field value
    - not equal -> error
    - equal -> no apparent error, but maybe errors nonetheless?

## bandwidth & delay

### delay \* bandwidth

- think of channel between pair of procs as hollow pipe
  - latency (delay) - length of pipe
  - bandwidth - width of pipe
- delay 50 ms, bandwidth 45 Mbps
  - 50e-3 seconds \* 45e6 bits/second
  - 2.25e6 = 280 KB data

### bandwidth-delay product

- very important consideration in network design
- determines how much data can actually be transmitted

### bandwidth-delay product & performance

- latency = propagation + transmit + queue + processing
- propagation = distance/speed
- transmit = size/bandwidth
- one bit transmission - propagation is important
- large byte transmission - bandwidth is important

### bandwidth \* delay

- relative importance of bandwidth & latency depends on app
- tells us how many bits sender must transmit before first bit arrives at receiver if sender keeps pipe full
- takes another one-way latency to receive response
- sender doesn't fill pipe -> send whole delay \* bandwidth product's worth of data before it stops to wait for a signal - sender will not fully utilize network

### reliable transmission

- checksum used to detect errors
  - some error codes strong enough to correct errors
  - overhead typically too high
- corrupt frames must be discarded
- transport layer protocol that wants to deliver segments reliably must recover from discarded segments
- accomplished using a combination of acknowledgements & timeouts

### ack frame

- small control segment (i.e. header only) that protocol sends back to peer saying it received an earlier segment
- receipt of ack tells sender that its segment was successfully delivered
- if sender doesn't receive ack within timeout, will re-send frame
- ack & timeouts called automatic repeat request (arq)

### stop & wait protocol

- after transmitting one segment, sender waits for ack
- if ack not received after certain amount of time, segment sent again

## principles of reliable data transfer

### principles of reliable data transfer

- complexity of reliable data transfer protocol depends strongly on characteristics of unreliable channels (lose, corrupt, reorder data)
- sender & receiver don't know each other's state unless communicated via a message

### reliable data transfer protocol (rdt): interfaces

- rdt_send(): called from above, passes data to deliver to receiver upper layer
- udt_send(): called by rdt to transfer pkt over unreliable channel to receiver
- rdt_rcv(): called when pkt arrives on receiver side of channel
- deliver_data(): called by rdt to deliver data to upper layer

### getting started

- incrementally develop sender & receiver sides of rdt
- consider only unidirectional data transfer, but control info will flow in both directions
- use finite state machines (fsm) to specify sender & receiver

### rdt 1.0: reliable transfer over reliable channel

- underlying channel perfectly reliable
  - no bit errors
  - no pkt loss
- separate fsms for sender & receiver
  - sender sends data into underlying channel
  - receiver reads data from underlying channel

### rdt 2.0: channel with bit errors

- underlying channel may flip bits in pkt
  - checksum to detect bit errors
- how to recover from errors?
  - ack: receiver tells sender pkt received ok
  - nak: receiver tells sender pkt had errors
  - sender retransmits pkt on receipt of nak
- stop & wait!
- what happens if ack/nak corrupted?
  - sender doesn't know what happened at receiver
  - can't just retransmit: possible duplicate
- handling duplicates
  - sender retransmits current pkt if ack/nak corrupted
  - sender adds sequence num to each pkt
  - receiver discards duplicates

### rdt2.1: handling garbled ack/nak

- sender
  - sends pkt with sequence num (0, 1 will suffice), waits for ack/nak
  - if corrupted, re-send
  - if ack, keep sending
  - if nak, re-send pkt
- receiver
  - receives pkt with sequence num
  - check if pkt is duplicate
  - if pkt not corrupt, send ack
  - if pkt corrupt, send nak
  - wait for more data from sender

### rdt2.2: nak-free

- same functionality as rdt2.1, only using acks
- instead of ack, receiver sends ack for last pkt received ok
  - receiver must include seq num of pkt being acked
- duplicate ack at sender results in same action as nak: retransmit current pkt
- tcp uses rdt2.2 to be nak-free

### rdt3.0: channels with errors & loss

- channel can also lose pkts
  - checksum, sequence nums, acks, retransmissions will be of help, but not quite enough
- sender waits reasonable amount of time for ack
  - retransmits if no ack received in time
  - if pkt or ack just delayed (not lost)
    - retransmission will be duplicate, but seq already handles this
    - receiver must specify seq of pkt being acked
  - use countdown timer to interrupt after reasonable amount of time
- performance
  - usender: utilization - fraction of time sender busy sending
  - e.g.: 1 Gbps link, 15 ms dprop, 8000 bit pkt - D = L/R = 8000 bits/10e9 b/s = 8 microseconds
  - performance is bad because it limits performance of underlying infrastructure
- pipelined protocols operation
  - pipelining: sender allows multiple, "in-flight", yet to be acked pkts
  - range of sequence nums must be increased
  - buffering at sender and/or receiver

### go-back-n

- sender
  - sender: window of up to n, consecutive transmitted but unacked pkts
    - k-bit seq in pkt header
  - cumulative ack: ack(n): acks all pkts up to, including seq n
    - on receipt of ack(n): move window forward to begin at n + 1
  - timer for oldest in-flight pkt
  - timeout(n): retransmit pkt n and all higher seq num pkts in window
- receiver
  - ack-only: always send ack for correctly received pkt so far, with highest in-order seq num
    - may generate duplicate acks
    - need only remember rcv_base
  - on receipt of out of order pkt
    - can discard or buffer - implementation decision
    - re-ack pkt with highest in-order seq num

### selective repeat approach

- pipelining: multiple pkts in flight
- receiver individually acks all correctly received pkts
  - buffers pkts as needed for in-order delivery to upper layer
- sender
  - maintains (conceptually) a timer for each unacked pkt
    - timeout: retransmits single unacked pkt associated with timeout
  - maintains (conceptually) window over n consecutive seq nums
    - limits pipelined, "in flight" pkts to be within this window

### selective repeat

- sender logic
  - data from above
    - if next available seq num in window, send pkt
  - timeout (n)
    - resend pkt n, restart timer
  - ack(n) in [sendbase, sendbase - n - 1]
    - mark pkt n as received
    - if n smallest unacked pkt, advance window base to next unacked seq num
- receiver logic
  - pkt n in [sendbase, sendbase - n - 1]
    - send ack(n)
    - out of order: buffer
    - in order: deliver (also deliver buffered, in order pkts), advance window to next pkt not yet received
  - pkt n in [rcvbase, rcvbase - n - 1]
    - ack(n)
  - otherwise, ignore

### selective repeat dilemma

- what relationship is needed between seq num size and window size to deal with receiver not being able to see sender side?

## tcp

### tcp overview

- p2p: one sender, one receiver
- reliable, in-order byte stream
  - no message boundaries
- full duplex data
  - bidirectional data flow in same conn
  - mss: maximum segment size
- cumulative acks
- pipelining
  - tcp congestion & flow control set window size
- conn-oriented
  - handshaking initializes sender & receiver before data exchange
- flow controlled
- sender will not overwhelm receiver

### segment structure

- 32 bit width
- source port, dest port
- seq num
- ack num
- header length
- congestion notification
- conn mgmt - rst, syn, fin
- flow control: num bytes receiver willing to accept
- tcp options (variable length)
- app data (variable length)

### seq nums, acks

- seq nums
  - byte stream num of first byte in segment's data
- acks
  - seq num of next byte expeced from other side
  - cumulative ack
- out of order segments handled by implementor

### rtt, timeout

- how to set up timeout value?
  - longer than rtt, but rtt varies
  - too short: premature timeout, unnecessary retransmissions
  - too long: slow reaction to segment loss
- how to estimate rtt?
  - samplertt: measured time from segment transmission until ack receipt
    - ignore retransmissions
  - samplertt will vary, want smoother estimated rtt
  - average several recent measurements, not just current samplertt
- timeout interval: estimatedrtt + safety margin
  - (alpha typically 0.125) $ estimatedrtt = (1 - alpha) \times estimatedrtt + alpha \times samplertt $
  - large variation in estimatedrtt -> need larger safety margin
  - $ timeout interval = estimatedrtt + 4 \times devrtt $
- devrtt: ewma of samplertt deviation from estimatedrtt
  - devrtt = $ (1 - beta) \times devrtt + beta \times |samplertt - estimatedrtt| $ (beta usually 0.25)

### sender events

- data received from app
  - create segment with seq num
  - seq num is byte-stream num of first data byte in segment
  - start timer if not already running
    - timer is for oldest unacked segment
    - expiration interval: timeoutinterval
- timeout
  - retransmit segment that caused timeout
  - restart timer
- ack received
  - if ack acknowledges previously unacked segments
    - update what is known to be acked
    - start timer if still have unacked segments

### receiver events

- arrival of in-order segment with expected seq num. all data up to expected seq num already acked
  - delayed ack. wait up to 500 ms for next segment. if no next segment, send ack
- arrival of in-order segment with expected seq num. one other segment has ack pending
  - immediately send single cumulative ack, acking both in-order segments
- arrival of segment out of order higher than expected seq num. gap detected
  - send duplicate ack (acking last correctly received in order byte), indicating seq num of next expected byte
- arrival of segment that partially or completely fills gap
  - immediately send ack, provided segment starts at lower end of gap

### retransmission scenarios

- lost ack
  - sender just resends last seq num
- premature timeout - sender sends multiple pkts, receiver sends acks, but sender resends since ack arrived later than window
  - receiver sends cumulative ack
- sender sends several segments, but one ack lost, so receiver resends cumulative ack to cover for it

### fast retransmit

- if sender receives 3 additional acks for same data (triple duplicate acks), resend unacked segment with smallest seg num
  - likely that unacked segment lost, don't wait for timeout

### flow control

- network layer delivers data faster than app layer removes data from socket buffers -> overflow
- necessary to add flow control info to pkt
- receiver advertises free buffer space in rwnd field in tcp header
  - rcvbuffer size set via socket options (typically 4096 bytes)
  - many operating systems auto adjust rcvbuffer
- sender limits amount of in-flight data to received rwnd
- guarantees receive buffer will not overflow

### conn mgmt

- before exchanging data, sender/receiver handshake
  - agree to establish conn (each knowing other willing to establish conn)
  - agree on conn params (e.g. starting seq nums)

### agreeing to establish conn

- 2-way handshake
  - client: `req_conn(x)`
  - server: estab, `acc_conn(x)`
  - client: estab
- will this always work in network?
  - variable delays
  - retransmitted messages (e.g. `req_conn(x)`) due to message loss
  - message reordering
  - can't see other side

### 2-way handshake scenarios

- normal
  - client `req_conn(x)` hits server timely
  - server `acc_conn(x)` hits client timely
  - client `data(x + 1)` hits server timely
  - server `ack(x + 1)` hits client timely
  - conn complete, server & client forget each other
- weird
  - client `req_conn(x)` hits server timely
  - server `acc_conn(x)` hits client not timely
  - client retransmit `req_conn(x)`
  - server `acc_conn(x)` hits client
  - conn closes, server & client forget each other
  - client retransmitted `req_conn(x)` hits -> half open conn
  - client `data(x + 1)` accepted -> duplicate data accepted

### 3-way handshake

| client state                        | server state       |
| ----------------------------------- | ------------------ |
| choose init seq num x, send tcp syn | wait               |
| wait                                | receive ack(y)     |
| receives syn-ack, estab, send ack   | wait               |
| wait                                | receive ack, estab |

### closing tcp conn

- client & server close their side of conn
  - send tcp segment with fin bit = 1
- respond to received fin with ack
  - on receiving fin, ack can be combined with own fin
- can hold simultaneous fin exchanges

## principles of congestion control

### principles of congestion control

- congestion: too many sources sending too much data too fast for network to handle
- manifestations
  - long delays (queuing in router buffers)
  - pkt loss (buffer overflow)
- different from flow control
- top-10 problem

### causes/costs of congestion

- scenario 1
  - one router, infinite buffers
  - input & output link cap: R
  - 2 flows
  - no need for retransmission
  - as arrival rate approaches R/2, arrival rate gets capped at R/2, but delay exponentially increases
- scenario 2
  - one router, finite buffers
  - sender retransmits lost, timed-out pkt
    - app layer in = app layer out
    - transport layer input includes transmissions -> in >= out
  - idealization: perfect knowledge
    - sender sends only when router buffers available
  - idealization: some perfect knowledge
    - pkts can be dropped at router due to full buffers
    - sender knows when pkt has been dropped; only resends if pkt known to be lost
    - can manifest in either some or no buffer space
  - realistic: unnecessary duplicates
    - pkts can be dropped at router due to full buffers -> retransmit dropped pkts
    - sender times can time out prematurely, sending 2 copies, both of which are delivered
    - costs of congestion
      - more work for given receiver throughput
      - unnecessary retransmissions: link carries multiple copies of pkt
        - decreasing max achievable throughput
- scenario 3
  - 4 senders, multi hop paths, timeout/retransmit
    - what happens as app layer in & rate of app layer in increase?
    - as rate of app layer in increases, all arriving pkts at upper queue are dropped, throughput -> 0
- insights
  - throughput can never exceed capacity
  - delay increases as capacity approached
  - loss/retransmission decreases effective throughput
  - unnecessary duplicates further decrease effective throughput
  - upstream transmission capacity/buffering wasted for pkts lost downstream

### approaches toward congestion control

- e2e congestion control
  - no explicit feedback from network
  - congestion inferred from observed loss & delay
  - approach taken by tcp
- network assisted congestion control
  - routers provide direct feedback to sending/receiving hosts with flows passing through congested router
  - may indicate congestion level or explicitly set sending rate
  - tcp, ecn, atm, decbit protocols

## congestion control

### aimd

- approach: senders can increase sending rate until congestion occurs, then decrease sending rate on loss event
- additive increase
  - increase sending rate by 1 max seg size every rtt until loss detected
- multiplicative decrease
  - cut sending rate in half at each loss event
  - cut in half on loss detected by triple duplicate ack (tcp reno)
  - cut to 1 mss when loss detected by timeout (tcp tahoe)
- distributed, async algorithm shown to optimize congested flow rates network wide & have desirable stability

### congestion control details

- tcp sending behavior
  - roughly: send cwnd bytes, wait rtt for acks, then send more bytes (rate = cwnd/rtt bytes/second)
- sender limits transmission: last byte sent - last byte acked <= cwnd
- cwnd dynamically adjusted in response to observed network congestion (implementing congestion control)

### slow start

- when conn begins, increase rate exponentially until first loss event
  - initially cwnd = 1 mss
  - double cwnd every every rtt
  - done by incrementing cwnd for every ack received
- initial rate slow but increases exponentially

### slow start -> congestion avoidance

- when should exponential increase switch to linear?
  - when cwnd gets to 1/2 value before timeout
- implementation
  - variable ssthresh
  - on loss event, ssthresh set to cwnd/2 just before loss event

### tcp cubic

- is there a better way than aimd to probe for usable bandwidth?
- insight/intuition
  - wmax: sending rate at which congestion loss was detected
  - congestion state of bottleneck link probably (?) hasn't changed much
  - after cutting rate/window in half on loss, iniitally increase to wmax faster, but then approach more slowly
- k: point in time when tcp widow size will reach wmax
  - k itself is tunable
- increase w as a function of the cube of the distance between current time & k
  - larger increases when further away from k
  - smaller increases when nearer to k
- tcp cubic default in linux, is most popular tcp for web servers until ~2024

### bottleneck link

- tcp (classic, cubic) increase sending rate until pkt loss occurs at some router's output: bottleneck link
- understanding congestion: useful to focus on congested bottleneck link
- multiple flows collectively congest bottleneck link
  - each executes their own congestion control
  - each of n flow should ideally receive throuhgput of r/n

### keeping pipe just full enough

- keep bottleneck link busy transmitting, but avoid high delays/buffering
- intuition
  - ideal amount of inflight data for a conn (ninflight) = conn's share of bottleneck bandwidth \* minrtt
- increasing ninflight while it is below bottleneck bandwidth will not increase rtt, since arrival rate to queue < transmission rate
- when we hit bandwidth-delay product, arrival rate of pkt data to bottleneck link = link bandwidth
- any higher than bandwidth-delay product will increase rtt
- throughput will increase until we hit bandwidth-delay product, then plateau
- loss-based tcp operates after we hit bandwidth-delay product, bbr tcp operates when we hit product

### bbr (bottleneck bandwidth & rtt)

- regulates ninflight
- at longer time intervals, reduces ninfligt to lower bandwidth, measure new minrtt
- at shorter time intervals
  - acceleration: increases ninflight until reaches throughput plateau
  - cruising: sends at rate that network delivers data as evidenced through received acks
  - deceleration: reduces ninflight, decreasing queue pressure, looking for lower minrtt

### explicit congestion notification (ecn)

- tcp deployments often implement network assisted congestion control
  - 2 bits in ip header (tos field) marked by router to indicate congestion
    - policy to determine marking chosen by network operator
  - congestion indication carried to destination
  - destination sets ece bit on ack segment to notify sender of congestion
  - involves both ip (ip header ecn bit marking) & tcp (tcp header c, e bit marking)

### tcp fairness

- if k tcp sessions share same bottleneck link of bandwidth r, each should have avg rate of r/k
- ideally, tcp is fair, assuming same rtt & fixed num sessions only in congestion avoidance

### must all network apps be fair?

- udp
  - multimedia apps often don't use tcp
    - don't want rate throttled by congestion control
  - instead use udp
    - send audio/video at constant rate, tolerate loss
  - no policing use of congestion control
- tcp
  - app can open multiple parallel conns between 2 hosts
  - web browsers do this, e.g. link of rate r with 9 existing conns
    - new app asks for 1 tcp, gets rate r/10
    - new app asks for 11 tcps, gets r/2
