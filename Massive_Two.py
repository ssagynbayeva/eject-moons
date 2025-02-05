import rebound
import numpy as np
import matplotlib.pyplot as plt
import sys

#Important physical constants from the solar system
mJ = 1898.19/1988500        #Jupiter mass
m_moon = 0.07346/1988500    #Moon mass
au = 1.5e8                  #Astronomical Unit
rJ = 70000/au               #Jupiter radius (AU)

def RemoveParticles(sim, center="Star", massless=[]):
    #List of main particles. Removes the center particle from the list.
    hashes = ["Star", "Planet 1", "Planet 2", "Planet 3"]
    hashes.remove(center)
    
    #Removes all remaining particles in the list from the simulation and re-centers the frame.
    for i in range(len(hashes)):
        if hashes[i] in massless:
            sim.particles[hashes[i]].m=0
        else:
            sim.remove(hash=hashes[i])
        
    sim.move_to_com()  


#Initializes a simulation snapshot up to 10 million days back in time.
sa = rebound.SimulationArchive("Archives/sa_escape_151.bin")
sim = (sa[-1001] if len(sa)>1001 else sa[0])
tf = sim.t + (365*100000)    #Final time, set at 100,000 years after the current time

#Add 3 moons in the Laplace resonance.
P = sim.particles["Planet 2"]
sim.add(m=m_moon, primary=P, a=421769/au, e=0.0041, inc=0.036*np.pi/180, l=np.pi/180, hash="Moon 1")
sim.add(m=m_moon, primary=P, a=671079/au, e=0.0101, inc=0.464*np.pi/180, pomega=np.pi, hash="Moon 2")
sim.add(m=m_moon, primary=P, a=1070042/au, e=0.0006, inc=0.186*np.pi/180, l=np.pi, hash="Moon 3")
sim.move_to_com()

#Important simulation settings
sim.integrator = 'ias15'     #Uses IAS15 integrator
sim.ri_ias15.min_dt = 0.01   #Sets minimum timestep
sim.exit_max_distance = 0    #Removes maximum distance limit
sim.initSimulationArchive("Archives/sa_massive_{}.bin".format(151), interval=1000)

# Output coordinates of the moons.
m1 = sim.particles["Moon 1"]
m2 = sim.particles["Moon 2"]
m3 = sim.particles["Moon 3"]
print("Moon 1: {:8.5}, {:8.5}, {:8.5}".format(m1.x, m1.y, m1.z))
print("Moon 2: {:8.5}, {:8.5}, {:8.5}".format(m2.x, m2.y, m2.z))
print("Moon 3: {:8.5}, {:8.5}, {:8.5}".format(m3.x, m3.y, m3.z))


try:
    while(sim.t<=tf):
        #Integrate one shapshot at a time, checking for escapes.
        sim.integrate(sim.t+10000)
        if(P.d >100):
            raise rebound.Escape

    # End of try block. Executes if a planet doesn't escape.
    print(sys.argv[1])
    print(sys.argv[2])
    print("False")

# Except block. Executes if a planet escapes.
except rebound.Escape as error:
    print(sys.argv[1])
    print(sys.argv[2])
    print("True")
