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

- forwarding: move packets from router's input to appropriate router output (data plane)
- routing: determine route taken by pkts from src to dst (control plane)
- 2 approaches to structuring network control plane
  - per router control (traditional)
    - individual routing algorithm components in each & every router interact in control plane
  - logically centralized control (sdn)
    - remote controller computes & installs forwarding tables in routers

## routing protocols

### routing protocols

- goal: determine good routes from sending host to receiving host through network of routers
  - path: sequence of routers packets traverse from src to dst
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
    - message complexity
      - each router must broadcast link state info to other n routers
      - efficient broadcast algorithms: O(n) link crossings to disseminate a broadcast message from one src
      - each router's message crosses O(n) links: overall message complexity: O(n^2)
