class Router:
    def __init__(self, name: str):
        self.name = name
        self.routing_table: dict[str, tuple[int, str]] = {} # destination: (distance, next hop)
        self.routing_table[self.name] = (0, self.name)
        
    def add_neighbour(self, neighbour: str, distance: int):
        self.routing_table[neighbour] = (distance, neighbour)
        
    def update_table(self, neighbour: str, neighbour_table: dict[str, tuple[int, str]]):
        neighbour_distance = self.routing_table.get(neighbour, (999, None))[0]
        for destination, (distance, _) in neighbour_table.items():
            new_distance = neighbour_distance + distance
            if destination not in self.routing_table or new_distance < self.routing_table[destination][0]:
                self.routing_table[destination] = (new_distance, neighbour)
                
    def print_table(self):
        print(f"Routing table for node {self.name}:")
        for destination, (distance, next_hop) in self.routing_table.items():
            print(f"  Destination: {destination}, Distance: {distance}, Next Hop: {next_hop}")
               
class Network:
    def __init__(self):
        self.routers: dict[str, Router] = {} # router: Router
        self.edges: dict[tuple[str, str], int] = {} # (router1, router2): distance
        
    def add_router(self, name: str):
        self.routers[name] = Router(name)
        
    def add_edge(self, router1: str, router2: str, distance: int):
        # creates routers if they don't exist
        if router1 not in self.routers:
            self.add_router(router1)
        if router2 not in self.routers:
            self.add_router(router2)
        # edge from router1 to router2
        self.edges[(router1, router2)] = distance
        self.routers[router1].add_neighbour(router2, distance)
        # edge from router2 to router1
        self.edges[(router2, router1)] = distance
        self.routers[router2].add_neighbour(router1, distance)
        
    def update_tables(self, n=None):
        if n is None:
            n = len(self.routers)
        for _ in range(n):
            for (router1, router2) in self.edges:
                self.routers[router1].update_table(router2, self.routers[router2].routing_table)
                self.routers[router2].update_table(router1, self.routers[router1].routing_table)
        
    def print_tables(self):
        for _, router in self.routers.items():
            router.print_table()
        
        
 
if __name__ == "__main__":
    net = Network()
    
    net.add_edge("A", "B", 7)
    net.add_edge("B", "C", 5)
    net.add_edge("C", "D", 20)
    net.add_edge("A", "D", 2)
    
    net.update_tables()
    net.print_tables()