import rebound
import numpy as np

#Uniform Distribution with low and high adjustable.
def U(l, h):
    return np.random.uniform(low = l, high = h)

#Rayleigh Distribution. Uses the Uniform Distribution.
def Rayleigh (l):
    X = l*np.sqrt(-2*np.log(1-U(0, 1) ))
    return X
    
R = 2*np.pi                     #Radian measures
mjup = 1898.19/1988500          #Mass of Jupiter, in solar masses

#Create a simulation
sim = rebound.Simulation()
sim.units = ('AU', 'day', 'msun')
sim.exit_max_distance = 100.0
sim.initSimulationArchive('escape_sa.bin', interval=1e4)

#Add sun and Jupiters, with randomized orbital elements, move of COM reference frame.
sim.add(m=1.0)
sim.add(m=mjup, a=3.0, e=Rayleigh(0.01), inc=Rayleigh(0.01), omega=U(0,R), Omega=U(0,R), M=U(0,R))
sim.add(m=mjup, P=sim.particles[1].P*U(1.2,1.4), e=Rayleigh(0.01), inc=Rayleigh(0.01), omega=U(0,R), Omega=U(0,R), M=U(0,R))
sim.add(m=mjup, P=sim.particles[2].P*U(1.2,1.4), e=Rayleigh(0.01), inc=Rayleigh(0.01), omega=U(0,R), Omega=U(0,R), M=U(0,R))
sim.move_to_com()

#Try to integrate, raise exception if escape is detected.
try:    
    sim.integrate(365)
    print ('Simulation integrated to {} days'.format(sim.t))
    sim.status()
    #rebound.OrbitPlot(sim, slices=True, limz=5)
except rebound.Escape as error:
    print (error)
    sim.status()
    #rebound.OrbitPlot(sim, slices=True, limz=5)
    for i in range(len(sim.particles)):
        if i>0:
            print('Distance of Particle {}: {} AU'.format(i, sim.particles[i].d))
