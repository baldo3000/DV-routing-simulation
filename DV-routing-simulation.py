class Router:
    def __init__(self, name):
        self.name = name
        self.routing_table = {} # destination: (distance, next hop)
        self.routing_table[self.name] = (0, self.name)
        
    def add_neighbour(self, neighbour, distance):
        self.routing_table[neighbour] = (distance, neighbour)
        
    def update_table(self, neighbour, neighbour_table):
        neighbour_distance = self.routing_table.get(neighbour, (999, None))[0]
        for destination, (distance, _) in neighbour_table.items():
            new_distance = neighbour_distance + distance
            if destination not in self.routing_table or new_distance < self.routing_table[destination][0]:
                self.routing_table[destination] = (new_distance, neighbour)
                
    def print_table(self):
        print(f"Routing table for node {self.name}:")
        for destination, (distance, next_hop) in self.routing_table.items():
            print(f"  Destination: {destination}, Distance: {distance}, Next Hop: {next_hop}")
               
 
 
if __name__ == "__main__":
    A = Router("A")
    B = Router("B")
    
    A.print_table()
    B.print_table()
    
    A.add_neighbour(B.name, 2)
    B.add_neighbour(A.name, 2)
    
    A.print_table()
    B.print_table()
    
    B.add_neighbour("C", 3)
    A.update_table(B.name, B.routing_table)
    
    A.print_table()
    B.print_table()