import ACO
import Functions

colony = ACO.ACO()
ranges = [[-5,5],
          [-5,5],
          [-5,5]]

colony.cost(Functions.Sphere)
colony.variables(3, ranges)
colony.parameters(50, 5, 50, 0.01, 0.85)
solution = colony.optimize()

print "Optimized solution is"
print solution
