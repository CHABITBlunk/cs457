# network layer - control plane

### toc

- intro
- routing protocols
  - link state
  - distance vector
- intra-isp routing: ospf
- routing among isps: bgp
- sdn control plane
- icmp
- network mgmt, config
  - snmp
  - netconf/yang

## intro

### network layer functions

- forwarding: move pkts from router's input to appropriate router output (data plane)
- routing: determine route taken by pkts from src to dst (control plane)
- 2 approaches to structuring network control plane
  - per router control (traditional)
    - individual routing algorithm components in each & every router interact in control plane
  - logically centralized control (sdn)
    - remote controller computes & installs forwarding tables in routers

## routing protocols

### routing protocols

- goal: determine good routes from sending host to receiving host through network of routers
  - path: sequence of routers pkts traverse from src to dst
  - good: least cost, fastest, least congested
  - routing: top 10 networking challenge

### graph abstraction: link costs

- cost defined by network operator: could always be 1, or inversely related to bandwidth, or inversely related to congestion

### routing algorithm classification

- routes change slowly over time (static) vs routes changing more quickly (dynamic)
- all routers have complete topology, link cost info, link state algorithms (global) vs iterative process of computation & exchange of info with neighbors, distance vector algorithms (decentralized)

## routing protocols - link state

### dijkstra's link state routing algorithm

- centralized: network topology & link costs known to all nodes
  - accomplished via link state broadcast
  - all nodes have same info
- computes least cost paths from 1 node (source) to all other nodes
  - gives forwarding table for that node
- iterative: after k iterations, know least cost path to k dsts
- notation
  - c_x,y: direct link cost from node x to y, infinity if not direct neighbors
  - D(v): current estimate of cost of least cost path to from src to dst v
  - p(v) predecessor node along path from src to v
  - N': set of nodes whose least cost path definitively known
- algorithm
  - initialization
    - N' = {u}
    - for all nodes v: if v adjacent to u; then D(v) = c_u,v; else D(v) = infinity
  - loop until all nodes in N'
    - find w not in N' such that D(w) is a min
    - add w to N'
    - update D(v) for all v adjacent to w and not in N':
      - D(v) = min(D(v), D(w) + c_w,v)
  - discussion
    - algorithm complexity: n nodes
      - each of n iteration: need to check all nodes not in N'
      - n(n + 1) / 2 comparisons: O(n^2) complexity
      - more efficient implementations possible that have O(n log n)
    - msg complexity
      - each router must broadcast link state info to other n routers
      - efficient broadcast algorithms: O(n) link crossings to disseminate a broadcast msg from one src
      - each router's msg crosses O(n) links: overall msg complexity: O(n^2)
  - oscillations possible when link costs depend on traffic volume

## routing protocols - distance vector

### distance algorithm

- based on bellman-ford (bf) equation (dynamic programming)
- let D_x(y): cost of least cost path from x to y - D_x(y) = min_v {c_x,v + D_v(y)}
- key idea
  - from time to time, each node sends its own distance vector estimate to neighbors
  - when x receives new dv estimate from any neighbor, updates its own dv using bf equation
    - D_x(y) <- min_v {c_x,v + D_v(y)} for each node y element of N
  - under minor, natural conditions, estimates converge to actual least cost
- algorithm
  - each node
    - wait for change in local link cost or msg from neighbor
    - recompute dv estimates using dv received from neighbor
    - if dv to any dst has changed, notify neighbors
  - iterative, async
    - each local iteration caused by local link cost change or dv update msg from neighbor
  - distributed, self stopping
    - each node notifies neighbors only when its dv changes
- bad news travels slow because it is distributed
  - count to infinity problem

### compared with ls algorithm

- msg complexity
  - ls: n routers, O(n^2 msgs sent)
  - dv: exchange between neighbors; convergence time varies
- speed of convergence
  - LS: O(n^2) algorithms, O(n^2) msgs - may have oscillations
  - DV: convergence time varies, may have routing loops, count to infinity problem
- robustness
  - ls
    - router can advertise incorrect link cost
    - each router computes only its own table
  - dv
    - router can advertise incorrect path cost: black holing
    - each router's dv used by others: errors propagate through network

## intra-isp routing: ospf

### make routing scalable

- how to scale billions of dsts?
  - can't store all dsts in routing tables
  - routing table exchange would swamp links
- administrative autonomy
  - each network admin may want to control routing in its own network

### internet approach to scalable routing

- aggregate routers into regions called autonomous systems (as, domains)
- intra-as (intra-domain)
  - routing among routers within same network
  - all routers in as must run same intra-domain protocol
  - routers in different as can run different intra-domain routing protocols
  - gateway router: at edge of its own as, has links to routers in other as's
- inter-as (inter-domain)
  - routing among as's
  - gateways perform inter-domain routing as well as intra-domain routing

### interconnected as's

- forwarding table configured by intra and inter-as routing algorithms
  - intra-as routing determine entries for dsts within as
  - inter-as & intra-as determine entries for external dsts

### inter-as routing: a role in intra-domain forwarding

- suppose router as1 receives datagram (dst outside as1)
  - to which gateway should the router forward pkt?
  - as1 inter-domain routing must
    - learn which dsts are reachable through as2 and which through as3
    - propagate this reachability info to all routers in as1

### intra-as routing: routing within an as

- most common intra-as routing protocols
  - rip (routing info protocol)
    - classic dv: dvs exchanged every 30s
    - no longer widely used
  - eigrp (enhanced interior gateway routing protocol)
    - dv based
    - formerly cisco proprietary for decades, became open in 2013
  - ospf (open shortest path first)
    - link state routing
    - is-is protocol (iso standard) essentially the same as ospf

### ospf routing

- open: publicly available
- classic link state
  - each router floods ospf link state advertisements (directly over ip rather than using tcp/udp) to all other routers in entire as
  - multiple link costs metrics possible: bandwidth, delay
  - each router has full topology, uses dijkstra's algorithm to compute forwarding table
- security: all ospf msgs authenticated to prevent malicious intrusion

### hierarchical ospf

- 2 level hierarchy: local area, backbone
  - link state advertisements flooded only in area or backbone
  - each node has detailed area topology, only konws direction to reach other dsts
- backbone components
  - boundary router
    - connects to other as's
  - backbone router
    - runs ospf limited to backbone
- local area components
  - area border routers
    - summarize distances to dsts in own area, advertise in backbone
  - local routers
    - flood ls in area only
    - compute routing within area
    - forward pkts to outside via area border router
  - internal routers

## routing among isps: bgp

### internet inter-as routing: bgp

- border gateway protocol - de facto inter-domain routing protocol
  - glue that holds internet together
- allows subnet to advertise its existence & dsts it can reach to internet
- bgp provides each as a means to
  - obtain dst network reachability info from neighboring as's (ebgp)
  - determine routes to other networks based on reachability info & policy
  - propagate reachability info to all as internal routers (ibgp)
  - advertise dst reachability info to neighboring networks

### bgp basics

- bgp session: 2 bgp routers (peers) exchange bgp msgs over semi permanent tcp conns
  - advertise paths to different dst network prefixes (bgp is a path vector protocol)
- when as3 gateway 3a advertises path as3,x to as2 gateway 2c, as3 promises as2 it will forward datagrams to x

### bgp msgs

- bgp msgs exchanged between peers over tcp conn
- msgs
  - open: opens tcp conn to remote bgp peer & authenticates sending bgp peer
  - update: advertises new path (or withdraws old)
  - keepalive: keeps conn alive in absence of updates, also acks open request
  - notification: reports errors in previous msg, also used to close conn

### path attrs & bgp routes

- bgp advertised route: prefix + attrs
  - prefix: dst being advertised
  - 2 important attrs
    - as path: list of as's through which prefix advertisement has passed
    - next hop: indicates specific internal as router to next hop as
- policy based routing
  - gateway receiving route advertisement uses import policy to accept/decline path
  - as policy also determines whether to advertise path to other neighboring as's

### bgp path advertisement

- single path
  - as2 router 2c receives path advertisement as3,x from as3 router 3a via ebgp
  - based on as2 policy, as2 router 2c accepts path as3,x & propagates to all as2 routers via ibgp
  - based on as2 policy, as2 router 2a advertises path as2,as3,x to as1 router 1c via ebgp
- multiple paths
  - gateway router may learn about multiple paths to dst
  - as1 gateway router 1c learns path as2,as3,x from 2a
  - as1 gateway router learns path as3,x from 3a
  - based on policy, as1 gateway router 1c chooses path as3,x & advertises path within as1 via ibgp

### bgp populate forwarding tables

- recall: 1a, 1b, 1d learn via ibgp from 1c: "path to x goes through 1c"
- at 1d: ospf intra-domain routing: to get to 1c, use interface 1
- at 1d: to get to x, use interface 1
- at 1a: ospf intra-domain routing: to get to 1c, use interface 2
- at 1a: to get to x, use interface 2

### hot potato routing

- 2d learns via ibgp it can route to x via 2a or 2c
- hot potato routing: choose local gateway that has least intra-domain cost (e.g. 2d chooses 2a even though more as hops to x) - don't worry about inter-domain cost

### bgp: achieving policy via advertisements

- isp only wants to route traffic to/from its customer networks (doesn't want to carry transit traffic between other isps)
  - a, b, c are provider networks
  - x, w, y are customers
  - x is dual-homed: attached to 2 other networks
  - policy to enforce: x doesn't want to route from b to c via x, so x will not advertise to b a route to c
  - a advertises path aw to b & c
  - b chooses not to advertise baw to c
    - b gets no revenue for routing cbaw since none of c, a, or w are b's customers
    - c doesn't learn about cbaw path
  - c will route caw (not using b) to get to w

### bgp route selection

- router may learn about more than one route to dst as, selects route based on
  1. local preference value attr: policy decision
  2. shortest as path
  3. closest next hop router: hot potato routing
  4. additional criteria

### why different intra-as & inter-as routing?

- policy
  - inter-as: admin wants control over how its traffic is routed, who routes through its network
  - intra-as: single admin, so policy less of an issue
- scale
  - hierarchical routing saves table size, reduced update traffic
- performance
  - intra-as: can focus on performance
  - inter-as: policy dominates over performance

## sdn control plane

### sdn

- internet network layer: historically implemented via distributed, per-router control approach
  - monolithic router contains switching hardware, runs proprietary implementation of internet standard protocols (ip, rip, is-is, ospf, bgp) in proprietary router os
  - different middleboxes for different layer functions: firewalls, load balancers, nat boxes, etc.
- ~2005: renewed interest in rethinking network control plane

### per-router control plane

- individual routing algorithm components in each router interact in the control plane to compute forwarding tables

### sdn control plane

- remote controller computes & installs forwarding tables in routers

### sdn

- why a logically centralized control plane?
  - easier network mgmt: avoid router misconfigurations, greater flexibility of traffic flows
  - table based forwarding (openflow api) allows programming routers
    - centralized programming easier: compute tables centrally & distribute
    - distributed programming more difficult: compute tables as result of distributed algorithm implemented in each router
  - open implementation of control plane
    - foster innovation: let 1000 flowers bloom

### sdn analogy: mainframe to pc

- mainframe
  - vertically integrated
  - closed, proprietary
  - slow innovation
  - small industry
- pc
  - horizontal
  - open interfaces
  - rapid innovation
  - huge industry

### traffic engineering: difficult with traditional routing

- what if network operator wants u to z traffic to flow along uvwz rather than uxyz?
  - need to redefine link weights so traffic routing algorithm computes routes accordingly (or need a new algorithm)
  - link weights only considered knobs: not much control
- what if network operator wants to split u to z traffic along uvwz & uxyz (load balancing)?
  - can't do it (or need new routing algorithm)
- what if w wants to route blue & red traffic differently from w to z?
  - can't do it with dst-based forwarding & ls or dv routing
  - generalized forwarding & sdn can achieve any desired routing

### sdn

1. generalized "flow-based" forwarding
2. control & data plane separation
3. control plane functions external to data plane switches
4. programmable control apps

- data plane switches
  - fast, simple, commodity switches implementing generalized data plane forwarding in hardware
  - flow (forwarding) table computed & installed under controller supervision
  - api for table-based switch control (e.g. openflow)
    - defines what is controllable & what is not
  - protocol for communicating with controller (e.g. openflow)
- sdn controller (network os)
  - maintain network state info
  - interacts with network control apps above via northbound api
  - interacts with network switches below via southbound api
  - implemented as distributed system for performance, scalability, fault tolerance, robustness
- network control apps
  - brains of control: implement control functions using lower level services, api provided by sdn controller
  - unbundled: can be provided by 3rd party: distinct from routing vendor or sdn controller

### sdn controller components

- interface layer to network control apps: abstractions api
- network wide state mgmt: state of network links, switches, & services: distributed database
- communication: communicate between sdn controller & controlled switches

### openflow: key msgs from controller to switch

- features: controller queries switch features, switch replies
- configure: controller queries/sets switch config params
- modify-state: add, delete, modify flow entries in openflow tables
- pkt-out: controller can send this pkt out of specific switch port

### openflow: key msgs from switch to controller

- pkt-in: transfer pkt & its control to controller. see pkt-out msg from controller
- flow-removed: flow table entry deleted at switch
- port status: inform controller of a change on a port

### sdn control/data plane interaction example

1. s1, experiencing link failure, uses openflow port status msg to notify controller
2. sdn controller receives openflow msg, updates link status info
3. dijkstra's routing algorithm application called
4. dijkstra's routing algorithm access network graph info & link state info in controller, then computes new routes
5. link state routing app interacts with flow table computation component in sdn controller, which computes new flow tables needed
6. controller uses openflow to install new tables in switches that need updating

### onos sdn controller

- control apps separate from controller
- intent framework: high level spec of service: what rather than how
- considerable emphasis on distributed core: service reliability, replication performance scaling

### google orion sdn control plane

- orion: google's sdn control plane: control plane for google's data center (jupiter) & wide area (b4) networks
  - routing (intradomain, ibgp), traffic engineering: implemented in apps on top of orion core
  - edge-edge flow-based controls (e.g. coflow scheduling) to meet contract slas
  - mgmt: pub-sub distributed microservices in orion core, openflow for switch signaling/monitoring

### google & sdn: value of logically centralized abstraction

- new opportunities to more formally & intentionally manage config

### sdn: selected challenges

- hardening control plane: dependable, reliable, performance scalable, secure distributed system
  - robustness to failures: leverage strong theory of reliable distributed system for control plane
  - dependability, security: baked in from day 1?
- networks & protocols meeting mission specific requirements
  - e.g. real-time, ultra-reliable, ultra-secure
- internet scaling: beyond a single as
- sdn critical in 5g networks
