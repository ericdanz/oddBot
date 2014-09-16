ff#devices have device IDs and components
class device(object):
	def __init__(self):
		self.comps = []
		self.id = 0
	def addcomp(self, comp):
		self.comps.append(comp)
			
#components have inputs/outputs (ios) and component IDs
class component(object):
	def __init__(self):
		self.ios = []
	def setcompnum(self, compno):
		self.compid = compno
	def setport(self, portname):
		self.port = portname
	def addio(self, io):
		self.ios.append(io)
	def setclass(self, compclass):
		self.classOf = compclass
			
#input/output
class inout(object):
	def __init__(self):
		self.isInput = ""
		self.classOf = ""
		self.typeOf = ""
		self.lowerBound = ""
		self.upperBound = ""
		self.granularity = ""
		self.state = ""
		
	'''def setio(self,isinput, classof, typeof, lowerbound, upperbound, granularity):
		self.isinput = isinput
		self.classof = classof
		self.typeof = typeof
		self.lowerbound = lowerbound
		self.upperbound = upperbound
		self.granularity = granularity'''
			
			
#generic class
class thing(object):
	def __init__(self):
		self.subs = []
	def addsub(self,sub):
		self.subs.append(sub)
			
