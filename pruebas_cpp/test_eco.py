import time
import eco

start = time.time()
e = eco.Ecosystem()
for i in range(300):
    e.evolve()
    print("---")
    print(e.get_num_organisms())
    print(e.get_num_free_locations())
    print(e.get_num_organisms() + e.get_num_free_locations())
    print(time.time() - start)
