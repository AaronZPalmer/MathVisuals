import numpy as np

class buses:

	def __init__(self, N, C=0, sigma=1):
		self.N = N
		self.positions = np.arange(0,N)/2
		self.C = C
		self.sigma =sigma
		self.beta_closed = 2/3*(sigma ** 2 + np.sqrt(sigma **4+6*C))
		self.beta_open = sigma ** 2 + np.sqrt(sigma **4+4*C)
		self.beta_global = sigma ** 2 + np.sqrt(sigma **4+8*C)

	def reinit(self, N, C=0, sigma=1):
		self.N = N
		self.positions = np.arange(0,N)/2
		self.C = C
		self.sigma =sigma
		self.beta_closed = 2/3*(sigma ** 2 + np.sqrt(sigma **4+6*C))
		self.beta_open = sigma ** 2 + np.sqrt(sigma **4+4*C)
		self.beta_global = sigma ** 2 + np.sqrt(sigma **4+8*C)

	def update_closed(self, delta_t,time_steps):

		alpha = np.zeros(self.N)

		alpha = -self.positions/2
		for i in range(0,self.N):
			mask = np.ones(self.positions.shape,dtype=bool)
			mask[i]=0
			alpha[i] = alpha[i]+self.beta_closed/2*np.sum(1/(self.positions[i]-self.positions[mask])/(self.N-1))


		r = np.random.normal(0,self.sigma/np.sqrt(self.N-1),self.N)
		alpha = alpha+r

		self.positions=self.positions + delta_t*alpha

