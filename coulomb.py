import numpy as np

class coulomb:

	def __init__(self, N=10, C=1, sigma=1):
		self.N = N
		self.positions = np.random.randn(self.N,2)



		self.C = C
		self.sigma =sigma
		#self.beta_closed = 2/3*(sigma ** 2 + np.sqrt(sigma **4+6*C))
		#self.beta_open = sigma ** 2 + np.sqrt(sigma **4+4*C)
		self.beta_global = np.sqrt(8*C) #check this
		self.cost = np.zeros(N)

		self.circumcircles=False

	def reinit(self, N=10, C=1, sigma=1):
		self.N = N
		self.positions = np.random.randn(self.N,2)



		self.C = C
		self.sigma =sigma
		#self.beta_closed = 2/3*(sigma ** 2 + np.sqrt(sigma **4+6*C))
		#self.beta_open = sigma ** 2 + np.sqrt(sigma **4+4*C)
		self.beta_global = np.sqrt(8*C) #check this
		self.cost = np.zeros(N)
		self.circumcircles=False

	def update_closed(self, delta_t,time_steps):

		self.update_control()


		r = np.random.normal(0,self.sigma/np.sqrt(self.N-1),[self.N,2])

		self.positions=self.positions + delta_t*(self.alpha+r)

	def update_control(self):

		self.J_potential = np.sum(self.positions*self.positions)/8

		self.alpha = -self.positions/2

		self.J_interaction = 0

		for i in range(0,self.N):
			mask = np.ones(self.N,dtype=bool)
			mask[i]=0
			gaps = self.positions[i]-self.positions[mask]
			gaps_norm = np.zeros([self.N-1,1])
			gaps_norm[:,0] = np.sum(gaps*gaps,1)

			self.alpha[i] = self.alpha[i]+self.beta_global/2*np.sum(gaps/gaps_norm/(self.N-1),0)
			self.J_interaction = self.J_interaction+ self.C/(self.N-1)/(self.N-1)*np.sum(1/gaps_norm)

		self.J_control = 0.5*np.sum(self.alpha*self.alpha)

	def get_circumcircles(self, ii):
		t=np.zeros((2,3))

		t[:,0]=self.positions[ii,:]

		radii = []
		x_center = []
		y_center = []

		for j in range(0,self.N):
			if j!=ii:
				t[:,1]=self.positions[j,:]
				for k in range(j+1,self.N):
					if k!=ii:
						t[:,2]=self.positions[k,:]
						[r,center]=coulomb.triangle_circumcircle ( t )
						radii = radii + [r]
						x_center = x_center + [center[0]]
						y_center = y_center + [center[1]]

		return radii, x_center, y_center


	def triangle_circumcircle ( t ):

#*****************************************************************************80
#
## TRIANGLE_CIRCUMCIRCLE computes the circumcircle of a triangle in 2D.
#
#  Discussion:
#
#    The circumcenter of a triangle is the center of the circumcircle, the
#    circle that passes through the three vertices of the triangle.
#
#    The circumcircle contains the triangle, but it is not necessarily the
#    smallest triangle to do so.
#
#    If all angles of the triangle are no greater than 90 degrees, then
#    the center of the circumscribed circle will lie inside the triangle.
#    Otherwise, the center will lie outside the triangle.
#
#    The circumcenter is the intersection of the perpendicular bisectors
#    of the sides of the triangle.
#
#    In geometry, the circumcenter of a triangle is often symbolized by "O".
#
#    Thanks to Chenguang Zhang for pointing out a mistake in the formula
#    for the center, 02 December 2016.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    02 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real T(2,3), the triangle vertices.
#
#    Output, real R, CENTER(2,1), the circumradius and circumcenter
#    of the triangle.
#

		center = np.zeros ( 2 )
#
#  Circumradius.
#
		a = np.sqrt((t[0,0] - t[0,1])**2 + (t[1,0] - t[1,1])** 2)
		b = np.sqrt((t[0,1] - t[0,2])**2 + (t[1,1] - t[1,2])**2)
		c = np.sqrt((t[0,2] - t[0,0])**2 + (t[1,2] - t[1,0])**2)

		bot = ( a + b + c ) * ( - a + b + c ) * (   a - b + c ) * (   a + b - c )

		if ( bot <= 0.0 ):
			r = - 1.0
			return r, center

		r = a * b * c / np.sqrt(bot)

		#
		#  Circumcenter.
		#

		f=np.zeros(2) 

		f[0] = ( t[0,1] - t[0,0] ) ** 2 + ( t[1,1] - t[1,0] ) ** 2
		f[1] = ( t[0,2] - t[0,0] ) ** 2 + ( t[1,2] - t[1,0] ) ** 2

		top = np.zeros ( 2 )

		top[0] =    ( t[1,2] - t[1,0] ) * f[0] - ( t[1,1] - t[1,0] ) * f[1]
		top[1] =  - ( t[0,2] - t[0,0] ) * f[0] + ( t[0,1] - t[0,0] ) * f[1]

		det  =    ( t[1,2] - t[1,0] ) * ( t[0,1] - t[0,0] ) - ( t[1,1] - t[1,0] ) * ( t[0,2] - t[0,0] ) 

		center[0] = t[0,0] + 0.5 * top[0] / det
		center[1] = t[1,0] + 0.5 * top[1] / det

		return r, center
				


