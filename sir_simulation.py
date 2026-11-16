import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# total number of S and I people
N = 300
NN = 1

# number of days or frames to simulate
T = 150

# length and width of domain
l = 100
w = 3

gamma = 0.1  # rate of recovery
beta = 0.2  # rate of infection

# contact / infection radius
delta = 3

Dh = 0.5  # rate of movement of healthy
Di = 0  # rate of movement of infected

# intitalize position of susceptible individuals
x = l * np.random.rand(N)
y = w * np.random.rand(N)

# initial xy coords of Infected
ix = np.array([1.0])
iy = np.array([1.0])

# initial xy coords of Recovered
rx = np.array([], dtype=float)
ry = np.array([], dtype=float)

# counting over time
NS = np.zeros(T, dtype=int)
NI = np.zeros(T, dtype=int)
NR = np.zeros(T, dtype=int)

# animation and line plot plotting
fig, (ax_anim, ax_plot) = plt.subplots(2, 1, figsize=(8, 6), height_ratios=[3, 2])
ax_anim.set_xlim(-1, l+1)
ax_anim.set_ylim(-1, w+1)
ax_anim.set_aspect("auto")
ax_anim.set_xlabel("x")
ax_anim.set_ylabel("y")
sus_artist, = ax_anim.plot([], [], '.b', label="Susceptible")
inf_artist, = ax_anim.plot([], [], '*r', label="Infected")
rec_artist, = ax_anim.plot([], [], 'og', label="Recovered")
ax_anim.legend()

time = np.arange(1, T + 1)
line_s, = ax_plot.plot([], [], 'b', linewidth=2, label='Susceptible')
line_i, = ax_plot.plot([], [], 'r', linewidth=2, label='Infected')
line_r, = ax_plot.plot([], [], 'g', linewidth=2, label='Recovered')
ax_plot.set_xlim(0, T)
ax_plot.set_ylim(0, N + 10)
ax_plot.set_ylabel('Number of individuals')
ax_plot.set_xlabel('Time')
ax_plot.legend()

# dictionary to map the array variables to labels
state = {
    "x": x,
    "y": y,
    "ix": ix,
    "iy": iy,
    "rx": rx,
    "ry": ry,
    "NS": NS,
    "NI": NI,
    "NR": NR
}

# define a step function
def step():
    x = state["x"]  # pulls in the global array variable
    y = state["y"]
    ix = state["ix"]
    iy = state["iy"]
    rx = state["rx"]
    ry = state["ry"]

    rec_idx = [] # recovery event vector
    for k in range(len(ix)):  # for each infected
        if np.random.rand() < gamma:  # recovery as a random event 
            rec_idx.append(k)  # adding a Recovered if random num less than rate of gamma

    if len(rec_idx) > 0: # if someone is added to recovered, we need to update the coordinates of Recovered and Infected individuals 
        # update the coordinates of Recovered and infected individuals
        rx = np.concatenate((rx, ix[rec_idx]))  # add to recovered
        ry = np.concatenate((ry, iy[rec_idx]))
        ix = np.delete(ix, rec_idx)  # and remove from infected
        iy = np.delete(iy, rec_idx)

    inf_idx = []
    for kk in range(len(x)):  # for each susceptible person
        if len(ix) == 0:  # if there are no infected individuals, then break the loop
            break

        dists = np.sqrt((ix - x[kk]) ** 2 + (iy - y[kk]) ** 2)  # compute dist from the susceptible person to all infected individuals
        d = np.min(dists)  # take the minimum distance of these dists
        if d < delta and np.random.rand() < beta:  # check if its less than the threshold distance AND if a random number is less than the infection rate
            inf_idx.append(kk)  # if both pass then an infection event occurs

    if len(inf_idx) > 0:  # if someone gets infected then we need to update that data
        # update the coordinates of Infected and Susceptible individuals
        ix = np.concatenate((ix, x[inf_idx]))
        iy = np.concatenate((iy, y[inf_idx]))
        x = np.delete(x, inf_idx)
        y = np.delete(y, inf_idx)

    # movement of S -- each takes a random step in x and y direction
    for k in range(len(x)):
        if x[k] < 0:  # if less than 0 in either direction then set equal to 0
            x[k] = 0
        elif x[k] > l:
            x[k] = l  # if greater than the boundaries then set equal to the boundary
        elif y[k] < 0:
            y[k] = 0
        elif y[k] > w:
            y[k] = w
        else:
            x[k] += Dh * np.random.randn()
            y[k] += Dh * np.random.randn()

    # add random step for I movement
    for k in range(len(ix)):  # movement of I
        if ix[k] < 0:
            ix[k] = 0
        elif ix[k] > l:
            ix[k] = l  # boundary conditions
        elif iy[k] < 0:
            iy[k] = 0
        elif iy[k] > w:
            iy[k] = w
        else:
            ix[k] += Di * np.random.randn()  # here, Di controls how much they move
            iy[k] += Di * np.random.randn()

    # add random step for R movement
    for k in range(len(rx)):  # movement of R
        if rx[k] < 0:
            rx[k] = 0
        elif rx[k] > l:
            rx[k] = l  # boundary conditions
        elif ry[k] < 0:
            ry[k] = 0
        elif ry[k] > w:
            ry[k] = w
        else:
            rx[k] += Dh * np.random.randn()
            ry[k] += Dh * np.random.randn()

    # update the dictionary variables with the new values at each step
    state["x"] = x
    state["y"] = y
    state["ix"] = ix
    state["iy"] = iy
    state["rx"] = rx
    state["ry"] = ry

    return x, y, ix, iy, rx, ry


def update(frame):
    x, y, ix, iy, rx, ry = step()

    state["NS"][frame] = len(x)
    state["NI"][frame] = len(ix)
    state["NR"][frame] = len(rx)

    sus_artist.set_data(x, y)
    inf_artist.set_data(ix, iy)
    rec_artist.set_data(rx, ry)

    line_s.set_data(np.arange(frame + 1), state["NS"][:frame + 1])
    line_i.set_data(np.arange(frame + 1), state["NI"][:frame + 1])
    line_r.set_data(np.arange(frame + 1), state["NR"][:frame + 1])

    return sus_artist, inf_artist, rec_artist, line_s, line_i, line_r

ani = FuncAnimation(fig, update, frames=T, interval=50, blit=False, repeat=False)
plt.show()
