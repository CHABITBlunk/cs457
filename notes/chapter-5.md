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
- messages
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
