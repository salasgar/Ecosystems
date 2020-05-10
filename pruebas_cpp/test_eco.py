import time
import eco

start = time.time()
e = eco.Ecosystem()
print("init time: {:.2f}ms".format(1000 * (time.time() - start)))
start = time.time()
num_iters = 1000
for i in range(num_iters):
    e.evolve()
print(e.get_num_organisms())
iteration_time_ms = 1000 * (time.time() - start) / num_iters
print("avg iteration time: {:.2f}ms".format(iteration_time_ms))
