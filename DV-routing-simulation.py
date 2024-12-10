import sys
class Router:
    """Simulated router with DV
    """
    def __init__(self, name: str):
        """Creates a router with the given name

        Args:
            name (str): name of the router
        """
        self.name = name
        self.routing_table: dict[str, tuple[int, str]] = {} # destination: (distance, next hop)
        self.routing_table[self.name] = (0, self.name)
        
    def add_neighbour(self, neighbour: str, distance: int):
        """Add a new neighbour

        Args:
            neighbour (str): neighbour router
            distance (int): distance between the two routers
        """
        self.routing_table[neighbour] = (distance, neighbour)
        
    def update_table(self, neighbour: str, neighbour_table: dict[str, tuple[int, str]]):
        """Updates the router distance vector with the one from provided router

        Args:
            neighbour (str): name of the router that provides the DV
            neighbour_table (dict[str, tuple[int, str]]): DV of the router
        """
        neighbour_distance = self.routing_table.get(neighbour, (sys.maxsize, None))[0]
        for destination, (distance, _) in neighbour_table.items():
            new_distance = neighbour_distance + distance
            if destination not in self.routing_table or new_distance < self.routing_table[destination][0]:
                self.routing_table[destination] = (new_distance, neighbour)
                
    def print_table(self):
        """Prints DV
        """
        print(f"Routing table for node {self.name}:")
        for destination, (distance, next_hop) in self.routing_table.items():
            print(f"  Destination: {destination}, Distance: {distance}, Next Hop: {next_hop}")
               
class Network:
    """Simulated network of routers with DVs
    """
    def __init__(self):
        """Creates a new network
        """
        self.routers: dict[str, Router] = {} # router: Router
        self.edges: dict[tuple[str, str], int] = {} # (router1, router2): distance
        
    def add_router(self, name: str):
        """Add a new router to the network

        Args:
            name (str): name of the router to add
        """
        self.routers[name] = Router(name)
        
    def add_edge(self, router1: str, router2: str, distance: int):
        """Add a new edge between two routers. 
        If they are not in the network already, new ones will be created with the given names

        Args:
            router1 (str): name of the first router
            router2 (str): name of the second router
            distance (int): distance between the routers
        """
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
        
    def update_tables(self, steps=None):
        """Makes all routers in the network exchange their DVs to their neighbours

        Args:
            n (_type_, optional): Number of exchange steps. Defaults to the number of routers in the network.
        """
        if steps is None:
            steps = len(self.routers)
        for _ in range(steps):
            for (router1, router2) in self.edges:
                self.routers[router1].update_table(router2, self.routers[router2].routing_table)
                self.routers[router2].update_table(router1, self.routers[router1].routing_table)
        
    def print_tables(self):
        """Prints DVs from all routers in the network
        """
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
    print("\n")
    # edge cost change test
    net.add_edge("C", "D", 1)
    net.update_tables()
    net.print_tables()