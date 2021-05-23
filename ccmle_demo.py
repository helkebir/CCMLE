from bvls import BVLS, np
from matplotlib import pyplot as plt

# EXAMPLE

# Set seed for reproducibility
np.random.seed(5)
# Sample size
n = 5000
# Number of oscillations
N = 10

# Standard deviation
sigma = 3

# Ground truth vector
# yt = np.zeros(n)
yt = np.sin(np.linspace(0, N*2*np.pi, n)) + np.sin(np.linspace(0, (N/2)*2*np.pi, n))

# Observation vector
# y = np.random.normal(0,sigma,n)
y = yt + np.random.normal(0,sigma,n)
y = y.reshape((len(y),1))

print("Relative change bound observed in in ground truth: ", np.max(np.abs(np.diff(yt))))
yt = yt.reshape((len(yt),1))

# Universal relative bound
eps = 0.01
# Create bounds vector of suitable size
eps *= np.ones((2*len(y)-2,1))

# Solve CCMLE (or bounded variable least squares, BVLS)
x,res = BVLS(y, eps)
x = x.value

print("Commanded standard deviation:", sigma)
print("Computed standard deviation of measurement signal:", np.std((y - yt).flatten()))
print("Computed standard deviation after CCMLE:", np.std((x - yt).flatten()))

# Plot results
figure, ax = plt.subplots(2,1)

ax[0].set_title('Signal')
ax[0].set_ylabel('Value')
ax[0].plot(y, marker='o', markersize=3, label=r"Observations ($\sigma = "+str(sigma)+"$)")
ax[0].plot(yt, marker='o', markersize=3, label='Truth')
ax[0].plot(x, label='BVLS')
ax[0].legend()

ax[1].set_title('Noise/Error')
ax[1].set_xlabel('Sample number')
ax[1].set_ylabel('Value')
ax[1].plot(y-x, linestyle='-.', label='Deviation (obs - BVLS)')
ax[1].plot(yt-x, linestyle='-.', label='Deviation (truth - BVLS)')
ax[1].legend()

plt.tight_layout()
plt.savefig('res.png')
plt.show(block=True)