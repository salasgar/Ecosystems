import time
import eco

start = time.time()
e = eco.Ecosystem()
e.initialize()
e.create_new_organisms(eco.OrganismType.PLANT_A, 5000);
e.create_new_organisms(eco.OrganismType.PLANT_B, 5000);
e.create_new_organisms(eco.OrganismType.HERBIVORE, 5000);
e.create_new_organisms(eco.OrganismType.CARNIVORE, 5000);
print("init time: {:.2f}ms".format(1000 * (time.time() - start)))
num_iters = 1000
for i in range(num_iters):
    start = time.time()
    print("cycle: {0}".format(i))
    e.evolve()
    print("num_organisms: {0}".format(e.get_num_organisms()))
    iteration_time_ms = 1000 * (time.time() - start)
    print("iteration time: {:.2f}ms".format(iteration_time_ms))
