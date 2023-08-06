from __future__ import print_function
from __future__ import absolute_import
import os,sys
import numpy as np
import subprocess
import mpi4py
from pyvtk import *
from pyvtk import *
from .GenerateSquareLatticePoresSmooth import *
from .GenerateSquareLatticePores import *
from .ComputeStructuredMesh import *
from .GenerateHexagonalLatticePores import *
from .GenerateStaggeredLatticePores import *
from .GenerateCustomPores import *
from .Generate2DInterface import *
from .GenerateRandomPoresOverlap import *
from .GenerateRandomPoresGrid import *
from . import GenerateMesh2D
from . import GenerateBulk2D
from . import GenerateBulk3D
from . import porous

import matplotlib
be = matplotlib.get_backend()
if not be=='nbAgg' and not be=='module://ipykernel.pylab.backend_inline':
 if not be == 'Qt5Agg': matplotlib.use('Qt5Agg')



import matplotlib.patches as patches
from .fig_maker import *
from matplotlib.path import Path
from IPython.display import display, HTML
from shapely.geometry import LineString
import shapely
import pickle
import sparse

#import GenerateInterface2D
#from nanowire import *
import deepdish as dd
from scipy.sparse import csc_matrix
from matplotlib.pylab import *
from shapely.geometry import MultiPoint,Point,Polygon,LineString
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def create_path(obj):

   codes = [Path.MOVETO]
   for n in list(range(len(obj)-1)):
    codes.append(Path.LINETO)
   codes.append(Path.CLOSEPOLY)

   verts = []
   for tmp in obj:
     verts.append(tmp)
   verts.append(verts[0])

   path = Path(verts,codes)
   return path

class Geometry(object):

 def __init__(self,**argv):

  self.structured = False
  direction = argv.setdefault('direction','x')
  if direction == 'x':
     self.direction = 0
     self.applied_grad = [1,0,0]
  if direction == 'y': 
     self.direction = 1
     self.applied_grad = [0,1,0]
  if direction == 'z':
     self.direction = 2
     self.applied_grad = [0,0,1]
  
  self.argv = argv.copy()
  #argv.setdefault('shape','square')
  geo_type = argv.setdefault('model','porous/square_lattice')

  if geo_type == 'geo':
   if mpi4py.MPI.COMM_WORLD.Get_rank() == 0:
    self.dim = 3   
    self.frame=[]
    self.polygons=[]
    state = self.compute_mesh_data()
    data = {'state':state}
    if self.argv.setdefault('save',True):
      pickle.dump(state,open('geometry.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    return
   else: data = None
   data = mpi4py.MPI.COMM_WORLD.bcast(data,root=0)
   self.state = data['state']

  if geo_type == 'load':
  # if MPI.COMM_WORLD.Get_rank() == 0:
    self.state = pickle.load(open(argv.setdefault('filename','geometry.p'),'rb'))
    self._update_data()

  else:
   if mpi4py.MPI.COMM_WORLD.Get_rank() == 0:
    #porous-----
    #if geo_type == 'porous/random' or \
    polygons = []

    self.porous = False
    if  geo_type == 'porous/square_lattice' or\
        geo_type == 'porous/square_lattice_smooth' or\
        geo_type == 'porous/hexagonal_lattice' or\
        geo_type == 'porous/staggered_lattice' or\
        geo_type == 'porous/random_over_grid' or\
        geo_type == 'porous/random' or\
        geo_type == 'porous/custom':

     self.porous = True
     if geo_type == 'porous/square_lattice':
      self.frame,self.polygons = GenerateSquareLatticePores(argv)
     
     if geo_type == 'porous/square_lattice_smooth':
      self.frame,self.polygons = GenerateSquareLatticePoresSmooth(argv)

     if geo_type == 'porous/hexagonal_lattice':
      self.frame,self.polygons = GenerateHexagonalLatticePores(argv)

     if geo_type == 'porous/staggered_lattice':
      self.frame,self.polygons = GenerateStaggeredLatticePores(argv)

     if geo_type == 'porous/custom':
      self.frame,self.polygons = GenerateCustomPores(argv)

     if geo_type == 'porous/random':
      self.frame,self.polygons,tt,mind = GenerateRandomPoresOverlap(argv)
      self.tt = tt
      self.mind = mind

     if geo_type == 'porous/random_over_grid':
      x,polygons = GenerateRandomPoresGrid(**argv)
      self.x = x

      argv['polygons'] = polygons
      argv['automatic_periodic'] = False
      self.frame,self.polygons = GenerateCustomPores(argv)


    self.Lz = float(argv.setdefault('lz',0.0))
    if geo_type == 'bulk':
      self.porous = True
      self.polygons = []
      Lx = float(argv['lx'])
      Ly = float(argv['ly'])

      self.frame = []
      self.frame.append([-Lx/2,Ly/2])
      self.frame.append([Lx/2,Ly/2])
      self.frame.append([Lx/2,-Ly/2])
      self.frame.append([-Lx/2,-Ly/2])

    if argv.setdefault('mesh',True):
     state = self.mesh(**argv)
     data = {'state':state}
   else: data = None
   data= mpi4py.MPI.COMM_WORLD.bcast(data,root=0)
   self.state = data['state']

   mpi4py.MPI.COMM_WORLD.Barrier()
  if argv.setdefault('savefig',False) or argv.setdefault('show',False) or argv.setdefault('store_rgb',False) :
   self.plot_polygons(**argv)

 def mesh(self,**argv):


   if self.Lz > 0.0:
    self.dim = 3
   else:
    self.dim = 2
   argv.update({'lz':self.Lz})
  
   if self.porous:
     
    if len(self.polygons) > 0 and self.dim == 3:
     #GenerateMesh3D.mesh(self.polygons,self.frame,argv)
     argv['polygons'] = self.polygons
     argv['frame'] = self.frame
     porous.Porous(**argv)

    if len(self.polygons) > 0 and self.dim == 2:
     GenerateMesh2D.mesh(self.polygons,self.frame,argv)
    if len(self.polygons) == 0 and self.dim == 2:
     GenerateBulk2D.mesh(argv)
    if len(self.polygons) == 0 and self.dim == 3:
     GenerateBulk3D.mesh(argv)
     #-----------------------------------

   
   if argv['model'] == '2DInterface':
       Generate2DInterface(argv)
       Lx = float(argv['lx'])
       Ly = float(argv['ly'])
       self.frame = []
       self.frame.append([-Lx/2,Ly/2])
       self.frame.append([Lx/2,Ly/2])
       self.frame.append([Lx/2,-Ly/2])
       self.frame.append([-Lx/2,-Ly/2])
       self.polygons = []



   if not argv.setdefault('only_geo',False):
    if argv['model'] == 'structured':
     self.compute_structured_mesh(**argv)   
    else:
     #Create mesh---
     subprocess.check_output(['gmsh','-format','msh2','-' + str(self.dim),'mesh.geo','-o','mesh.msh'])
     self.import_mesh()

    state = self.compute_mesh_data()
    if self.argv.setdefault('save',True):
     pickle.dump(state,open('geometry.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)



     return state


 # MPI.COMM_WORLD.Barrier()

 def get_repeated_size(self,argv):
    Nx = argv.setdefault('repeat_x',1)
    Ny = argv.setdefault('repeat_y',1)
    size = self.size
    Lx = size[0]*Nx
    Ly = size[1]*Ny
    return Lx,Ly

 def get_repeated(self,Nx,Ny):
    size = self.size
    Lx = size[0]*Nx
    Ly = size[1]*Ny
    return Lx,Ly

 def get_interface_point_couples(self,argv):

   Nx = argv.setdefault('repeat_x',1)
   Ny = argv.setdefault('repeat_y',1)


   for ll in self.side_list['Interface']:
    p1 = self.nodes[self.sides[ll][0]][:2]
    p2 = self.nodes[self.sides[ll][1]][:2]
    for nx in range(Nx):
      for ny in range(Ny):
       P = np.array([self.size[0]*(nx-(Nx-1)*0.5),\
                     self.size[1]*(ny-(Ny-1)*0.5)])
       p1 = np.array(p1) + P
       p2 = np.array(p2) + P
       plot([p1[0],p2[0]],[p1[1],p2[1]],color='w',ls='--',zorder=1)




 def plot_polygons(self,**argv):

   if mpi4py.MPI.COMM_WORLD.Get_rank() == 0:

    lx = abs(self.frame[0][0])*2
    ly = abs(self.frame[0][1])*2

    #init_plotting()
    close()
    #fig = figure(num=" ", figsize=(8*lx/ly, 4), dpi=80, facecolor='w', edgecolor='k')
    fig = figure(num=" ", figsize=(4*lx/ly, 4), dpi=80, facecolor='w', edgecolor='k')
    axes([0,0,1.0,1.0])
    #axes([0,0,0.5,1.0])


    xlim([-lx/2.0,lx/2.0])
    ylim([-ly/2.0,ly/2.0])

    path = create_path(self.frame)
    patch = patches.PathPatch(path,linestyle=None,linewidth=0.1,color='gray',zorder=1,joinstyle='miter')
    gca().add_patch(patch);

    if self.argv.setdefault('inclusion',False):
     color='g'
    else:
     color='white'

    for poly in self.polygons:
     path = create_path(poly)
     patch = patches.PathPatch(path,linestyle=None,linewidth=0.1,color=color,zorder=2,joinstyle='miter')
     gca().add_patch(patch);
     
    
    #plot Boundary Conditions-----
    if argv.setdefault('plot_boundary',False):
     for side in self.side_list['Boundary'] + self.side_list['Interface'] :
      p1 = self.sides[side][0]
      p2 = self.sides[side][1]
      n1 = self.nodes[p1]
      n2 = self.nodes[p2]
      plot([n1[0],n2[0]],[n1[1],n2[1]],color='#f77f0e',lw=6)
     
     
      #plot Periodic Conditions-----
    if argv.setdefault('plot_boundary',False):
     for side in self.side_list['Periodic'] + self.side_list['Inactive']  :
      p1 = self.sides[side][0]
      p2 = self.sides[side][1]
      n1 = self.nodes[p1]
      n2 = self.nodes[p2]
      plot([n1[0],n2[0]],[n1[1],n2[1]],color='#1f77b4',lw=12,zorder=3)
       
    
    #----------------------------
    axis('off')
    data = {}
    if self.argv.setdefault('show',False):
     show()
    if self.argv.setdefault('savefig',False) :
     savefig(argv.setdefault('fig_file','geometry.png'))

    if self.argv.setdefault('store_rgb',False):
     fig.canvas.draw()   
     rgb = np.array(fig.canvas.renderer._renderer)
     data = {'rgb':rgb}
     clf()
   else: data = None
   data =  mpi4py.MPI.COMM_WORLD.bcast(data,root=0)

   if self.argv.setdefault('store_rgb',False):
    self.rgb = data['rgb']



 def compute_triangle_area(self,p1,p2,p):
   p = Polygon([(p1[0],p1[1]),(p2[0],p2[1]),(p[0],p[1])])
   return p.area

 def point_in_elem(self,elem,p):

  poly = []
  for n in self.elems[elem]:
   t1 = self.nodes[n][0]
   t2 = self.nodes[n][1]
   poly.append((t1,t2))
  polygon = Polygon(poly)
  if polygon.contains(Point(p[0],p[1])):
   return True
  else:
   return False


 def compute_line_data(self,p1,p2,data):

    #get the first element---
    x = [0]
    elem = self.get_elem_from_point(p1) 
    value = self.compute_2D_interpolation(data,p1,elem)
    line_data = [value]

    int_points = []
    N = 100
    delta = np.linalg.norm(p2-p1)/N
    gamma = 1e-4
    r_old = p1
    for n in range(1,N+1):
     neighbors = self.get_elem_extended_neighbors(elem)  
     r = p1 + n*(p2-p1)/N
     tmp = self.cross_interface(r_old,r)
     if len(tmp) > 0:
       #print(tmp) 
       x.append(n*delta-np.linalg.norm(r-tmp)-gamma)
       x.append(n*delta-np.linalg.norm(r-tmp)+gamma)
       int_points.append(n*delta-np.linalg.norm(r-tmp))
       versor = r - r_old;versor /= np.linalg.norm(versor)
       elem = self.get_elem_from_point(tmp-gamma*versor,guess = neighbors) 
       value = self.compute_2D_interpolation(data,tmp-gamma*versor,elem)
       elem = self.get_elem_from_point(tmp+gamma*versor,guess = neighbors) 
       value = self.compute_2D_interpolation(data,tmp+gamma*versor,elem)
       line_data.append(value)
       line_data.append(value)
       neighbors = self.get_elem_extended_neighbors(elem)  
     else:
      elem = self.get_elem_from_point(r,guess = neighbors) 
      #print(elem)
      value = self.compute_2D_interpolation(data,r,elem)
      line_data.append(value)
      x.append(n*delta)
     r_old = r

    
    return x,line_data,int_points 


 def get_elem_from_point(self,r,guess = []): 
   
    for elem in guess:
     if self.point_in_elem(elem,r) :
       return elem
   
    for elem in range(len(self.elems)):
     if self.point_in_elem(elem,r) :
       #print('no guess')  
       return elem


 def compute_2D_interpolation(self,data,p,elem):

    if self.point_in_elem(elem,p) :
       
      nodes = self.elems[elem]
      p1 = self.nodes[nodes[0]]
      p2 = self.nodes[nodes[1]]
      p3 = self.nodes[nodes[2]]

      v1 = data[nodes[0]]
      v2 = data[nodes[1]]
      v3 = data[nodes[2]]

      area_1 = self.compute_triangle_area(p2,p3,p)
      area_2 = self.compute_triangle_area(p1,p3,p)
      area_3 = self.compute_triangle_area(p1,p2,p)
      area = area_1 + area_2 + area_3
      v = v1*area_1 + v2*area_2 + v3*area_3
      v /= area

      return v
   
    print('ERROR: no elem found')
    quit()



 def adjust_boundary_elements(self):

  for side in self.side_list['Boundary']:
   self.side_elem_map[side].append(self.side_elem_map[side][0])


 def plot_elem(self,ne,color='gray') :

     elem = self.elems[ne]
     pp = []
     for e in elem:
      pp.append(self.nodes[e][:2])
     path = create_path(pp)
     patch = patches.PathPatch(path,linestyle=None,linewidth=0.1,color=color,zorder=1,joinstyle='miter',alpha=0.7)
     gca().add_patch(patch);
     ave = np.sum(np.array(pp),axis=0)/4
     return ave


 def compute_structured_mesh(self,**argv):

    #self.structured = True 
    l = argv['l']
    self.frame = [[-l/2,-l/2],[-l/2,l/2],[l/2,l/2],[l/2,-l/2]]
    self.polygons = []
    self.size = [l,l,0]

    n = argv['n']

    delta = l/n
    #generate points---
    self.nodes = []
    for y in range(n+1):
     for x in range(n+1):
       self.nodes.append([-l/2 + delta*x,l/2 - delta*y,0])
    self.nodes = np.array(self.nodes)   

    #Build Periodic Nodes----
    self.periodic_nodes = []
    for x in range(n+1):
     self.periodic_nodes.append([x,n*(n+1) + x])
    #-----------------------

    for y in range(n+1):
     self.periodic_nodes.append([y*(n+1),y*(n+1) + n])
    #-----------------------

    #generate sides---
    #horizontal
    self.sides = []
    for y in range(n):
     for x in range(n): #the lower is periodic
       self.sides.append([y*(n+1)+x,y*(n+1)+x+1])
   
    #vertical
    for y in range(n):
     for x in range(n): #the lower is periodic
       self.sides.append([x*(n+1)+y,(x+1)*(n+1)+y])

    #elements---
    self.elems = []
    for y in range(n):
     for x in range(n):
      self.elems.append([y*(n+1)+x,y*(n+1)+x+1,(y+1)*(n+1)+x+1,(y+1)*(n+1)+x])
    #------------------------

    #side_elem_map
    #lower elements 
    self.side_elem_map = {}
    for x in range(n):
     for y in range(n):
       self.side_elem_map.setdefault(y*n+x,[]).append(y*n+x)

    #upper elements   
    for x in range(n):
     for y in range(1,n):
       self.side_elem_map.setdefault(y*n+x,[]).append((y-1)*n+x) 
  
    #right elements   
    for x in range(n-1):
     for y in range(n):
        self.side_elem_map.setdefault(n*n + n*(x+1) + y,[]).append(y*n+x) 

    #left elements   
    for y in range(n):
     for x in range(n):
        self.side_elem_map.setdefault(n*n + n*x + y,[]).append(y*n+x) 

    #border sides---
    for x in range(n):
      self.side_elem_map.setdefault(x,[]).append(n*n-n+x) 
      #self.elem_side_map.setdefault(n*n-n+x,[]).append(x) 

    for y in range(n):
      self.side_elem_map.setdefault(n*n+y,[]).append(n*y+n-1) 
      #self.elem_side_map.setdefault(n*y+n-1,[]).append(n*n+y) 


    #---------------------------------------------------
    self.elem_side_map = {}
    for side in self.side_elem_map.keys():
     for elem in self.side_elem_map[side]:   
      self.elem_side_map.setdefault(elem,[]).append(side)

    #------------------------------------------------------
    self.node_side_map = {}
    for ns,side in enumerate(self.sides):
     for node in side:   
      self.node_side_map.setdefault(node,[]).append(ns)
    for node in range(len(self.nodes)):
      self.node_side_map.setdefault(node,[])  
    #------------------------------------------------------

    
    #-------------------
    node_elem_map = {}
    for node in self.node_side_map.keys():
      for side in self.node_side_map[node]:
        for elem in self.side_elem_map[side]:
          node_elem_map.setdefault(node,set()).add(elem)

    #------------------------------------------------

    self.node_elem_map = {}
    for node in node_elem_map.keys():
        self.node_elem_map.update({node:list(node_elem_map[node])})  
    self.side_node_map = self.sides

    #ad-hoc hacking for connection of nodes on the periodic elements
    self.node_elem_map[0].append(n*n-1)
    self.node_elem_map[n].append(0)
    self.node_elem_map[n].append(n*n-n)
    for y in range(n-1):
      self.node_elem_map[(y+1)*(n+1)+n].append(y*n)
      self.node_elem_map[(y+1)*(n+1)+n].append((y+1)*n)
    
    self.node_elem_map[(n+1)*n].append(0)
    self.node_elem_map[(n+1)*n].append(n-1)
        
    for x in range(n-1):
      self.node_elem_map[(n+1)*n+x+1].append(x)
      self.node_elem_map[(n+1)*n+x+1].append(x+1)

    #last node
    self.node_elem_map[(n+1)*(n+1)-1] = []
    self.node_elem_map[(n+1)*(n+1)-1].append(0)
    self.node_elem_map[(n+1)*(n+1)-1].append(n*n-1)
    self.node_elem_map[(n+1)*(n+1)-1].append(n-1)
    self.node_elem_map[(n+1)*(n+1)-1].append(n*(n-1))


    #Periodic sides-----
    self.side_list = {'Boundary':[],'Interface':[]}
    p_sides = []
    for x in range(n):
      p_sides.append(x)   
      p_sides.append(n*n+x)   
    self.side_list.update({'Periodic':p_sides})

    #------------------------------------------------
    self.side_list.setdefault('Hot',[])
    self.side_list.setdefault('Cold',[])
    #-----------------------------------

    #Interface nodes---
    self.node_list = {}
    tmp = set()
    for side in self.side_list['Interface']:
     tmp.add(self.sides[side][0])
     tmp.add(self.sides[side][1])
    self.node_list.update({'Interface':list(tmp)})

    #region elem map
    self.region_elem_map = {'Matrix':range(len(self.elems))}
    self.elem_region_map = {i:'Matrix' for i in range(len(self.elems)) }


    #create inactive sides---- (for back-compatibility)

    #right sides
    self.side_periodicity = np.zeros((len(self.sides)+n*n,2,3))
    for x in range(n):
      self.side_periodicity[x,1] = [0,l,0] 
      self.side_periodicity[n*n+x,1] = [-l,0,0] 

    self.pairs = []
    self.exlude = []
    for y in range(n): 
      self.sides.append([y*(n+1)+n,(y+1)*(n+1)+n])
      self.pairs.append([n*n+y,len(self.sides)-1])
      self.side_elem_map[len(self.sides)-1]=[n*y+n-1,n*y] 
      self.side_periodicity[len(self.sides)-1,1] = [l,0,0] 
      self.exlude.append(len(self.sides)-1)

    #lower sides
    for x in range(n): 
      self.sides.append([(n+1)*n+x,(n+1)*n +x +1])
      self.pairs.append([x,len(self.sides)-1])
      self.side_elem_map[len(self.sides)-1]=[n*n-n+x,x] 
      self.side_periodicity[len(self.sides)-1,1] = [0,-l,0] 
      self.exlude.append(len(self.sides)-1)
    #--------------------------
    self.side_list.update({'active':range(len(self.sides)-2*n)})
    self.side_list.update({'active_global':range(len(self.sides)-2*n)})
    #self.elem_list = {'active':range(len(self.elems))}

    #select active sides and active nodes---
    #We substract 2*n because we don't want to include the inactive periodic sides
    #create local_global_map
    self.l2g = range(len(self.elems))
    self.g2l = range(len(self.elems))

    #---------------------

   
   #self.add_patterning(**argv)


 def add_patterning(self,**argv):

  if mpi4py.MPI.COMM_WORLD.Get_rank() == 0:
    grid = argv['grid']
    n = int(sqrt(len(self.nodes)))-1
    inclusion = argv.setdefault('inclusion',False)

    self.elem_region_map = {}
    self.region_elem_map = {'Inclusion':[],'Matrix':[]}
    for g in np.array(grid).T:
     ne = g[1]*n + g[0]
     self.region_elem_map['Inclusion'].append(ne)
     self.elem_region_map[ne] = 'Inclusion'
      
    for elem in range(len(self.elems)):
     if not elem in self.elem_region_map.keys():
      self.elem_region_map[elem] = 'Matrix'
      self.region_elem_map['Matrix'].append(elem)
   
    if not inclusion:
     active_sides = set()
     for side in self.side_list['active_global']:
      #is_in = False
      elems = self.side_elem_map[side]
      for elem in elems:   
       if self.elem_region_map[elem] == 'Matrix':  #at least one element is connected with one side
        active_sides.add(side)
        #is_in = True
      #if is_in == False:
        #delete connection on the connection matrix
       # self.A[elems[0],elems[1]] = 0
       # self.A[elems[1],elems[0]] = 0

     self.side_list.update({'active':list(active_sides)})
     #self.elem_list = {'active':self.region_elem_map['Matrix']}
    #---------------------

    #Interfacial sides---------------------------
    if inclusion:
     tmp = set()
     for g in np.array(grid).T:
      ne = g[1]*n + g[0]
      for side in self.elem_side_map[ne]:
        tmp.add(side)
     self.side_list.update({'Interface':list(tmp)})
    else:
     tmp = set()
     for g in np.array(grid).T:
      ne = g[1]*n + g[0]
      for side in self.elem_side_map[ne]:
        tmp.add(side)
     self.side_list.update({'Boundary':list(tmp)})

    #adjust side_elem_map to make it sure Matrix comes first

    for ll in self.side_list['Boundary'] :
      i,j  = self.side_elem_map[ll]
      if i in self.region_elem_map['Inclusion']:
        self.side_elem_map[ll] = [j,i]

    #we need to change this--
    #make weigths smaller
    #--------------------------

    if not inclusion:
     self.l2g = []
     self.g2l = np.zeros(len(self.elems),dtype=int)
     for i in range(len(self.elems)):
       if i in self.region_elem_map['Matrix']:
         self.l2g.append(i)
         self.g2l[i] = len(self.l2g)-1


    #print(len(self.side_list['active']))
    self.compute_connecting_matrix()
    #print(np.shape(self.A))

    
    data = {'nle':len(self.l2g),'g2l':self.g2l,'l2g':self.l2g,'side_elem_map':self.side_elem_map,'elem_side_map':self.elem_side_map,\
            'side_list':self.side_list,'region_elem_map':self.region_elem_map,\
            'elem_region_map':self.elem_region_map,'A':self.A}

  else: data = None


  self.state.update(mpi4py.MPI.COMM_WORLD.bcast(data,root=0))



 def plot_structured_mesh(self,**argv):


    ptext = argv.setdefault('text',False)

    if ss:
     axis('equal')
     axis('off')
     for node in self.nodes:
       scatter(node[0],node[1],color='r')
 
     for y in range(n+1):
      for x in range(n+1):
       if ptext:
        text(-l/2 + delta*x,l/2 - delta*y+0.15,str(y*(n+1)+x),color='r',ha='center')


     for n_side,side in enumerate(self.sides):
      p0 = self.nodes[side[0]]
      p1 = self.nodes[side[1]]
      m = (np.array(p0) + np.array(p1))/2
      plot([p0[0],p1[0]],[p0[1],p1[1]],color='b')
      if ptext:
       text(m[0],m[1],str(n_side),color='b')

     for ne in range(len(self.elems)):
      ave = self.plot_elem(ne,color='gray')

      if ptext:
       text(ave[0],ave[1],str(ne),color='black')
     
     #for g in np.array(grid).T:
     # ne = g[1]*n + g[0]
     # self.plot_elem(ne,color='green')

     #s = 23
     #for elem in self.side_elem_map[s]:    
     # self.plot_elem(elem,color='red')
     #p = 15
     #for elem in self.node_elem_map[p]:    
     # self.plot_elem(elem,color='red')

     show()

 def compute_mesh_data(self):


    #self.import_mesh()

    #self.compute_elem_map()
    #print(self.side_elem_map)
    #self.adjust_boundary_elements()


    self.compute_elem_volumes()
    self.compute_side_areas()
    self.compute_side_normals()
    self.compute_elem_centroids()
    self.compute_side_centroids()
    self.compute_least_square_weigths()
    self.compute_connecting_matrix()
    self.compute_connecting_matrix_new()
    self.compute_interpolation_weigths()
    self.compute_contact_areas()
    self.compute_boundary_condition_data()
    self.n_elems = len(self.elems)
    self.nle = len(self.l2g)

    data = {'side_list':self.side_list,\
          'node_list':self.node_list,\
          #'elem_list':self.elem_list,\
          'exlude':self.exlude,\
          'n_elems':self.n_elems,\
          'elem_side_map':self.elem_side_map,\
          'elem_region_map':self.elem_region_map,\
          'side_elem_map':self.side_elem_map,\
          'side_node_map':self.side_node_map,\
          'node_elem_map':self.node_elem_map,\
          #'elem_map':self.elem_map,\
          'nodes':self.nodes,\
          'N_new':self.N_new,\
          'N':self.N,\
          'sides':self.sides,\
          'elems':self.elems,\
          'A':self.A,\
          'side_periodicity':self.side_periodicity,\
          'dim':self.dim,\
          'weigths':self.weigths,\
          'region_elem_map':self.region_elem_map,\
          'size':self.size,\
          'c_areas':self.c_areas,\
          'interp_weigths':self.interp_weigths,\
          'elem_centroids':self.elem_centroids,\
          'side_centroids':self.side_centroids,\
          'elem_volumes':self.elem_volumes,\
          'periodic_nodes':self.periodic_nodes,\
          'side_areas':self.side_areas,\
          'pairs':self.pairs,\
          'B':self.B,\
          'node_side_map':self.node_side_map,\
          'B_with_area':self.B_with_area,\
          'B_with_area_old':self.B_with_area_old,\
          'CM':self.CM,\
          'CP':self.CP,\
          'CPB':self.CPB,\
          #'periodic_sides':self.periodic_sides,\
          #'boundary_elements':self.boundary_elements,\
          #'interface_elements':self.interface_elements,\
          'side_normals':self.side_normals,\
          'grad_direction':self.direction,\
          'l2g':self.l2g,\
          'g2l':self.g2l,\
          'nle':self.nle,\
          'area_flux':self.area_flux,\
          'flux_sides':self.flux_sides,\
          #'labels':self.blabels,\
          'frame':self.frame,\
          'polygons':self.polygons,\
          'applied_grad':self.applied_grad,\
          'argv':self.argv,\
          'side_periodic_value':self.side_periodic_value}

    return data


 def compute_connecting_matrix(self):

   nc = len(self.elems)
   row_tmp = []
   col_tmp = []
   data_tmp = []

   for ll in self.side_list['active'] :
    if not ll in self.side_list['Hot'] and\
     not ll in self.side_list['Cold'] and not ll in self.side_list['Boundary']:
         
     elems = self.get_elems_from_side(ll)
     kc1 = elems[0]
     kc2 = elems[1]
     row_tmp.append(kc1)
     col_tmp.append(kc2)
     data_tmp.append(1)
     row_tmp.append(kc2)
     col_tmp.append(kc1)
     data_tmp.append(1)
    
   self.A = csc_matrix( (np.array(data_tmp),(np.array(row_tmp),np.array(col_tmp))), shape=(nc,nc) ).todense()

 def compute_connecting_matrix_new(self):

   nc = len(self.elems)
   N  = sparse.DOK((nc,nc,3), dtype=float32)

   ns = len(self.elem_side_map[0])
   CP  = sparse.DOK((nc,ns,3), dtype=float32) #this is a elem X n_side map of normal
   CM  = sparse.DOK((nc,ns,3), dtype=float32) #this is a elem X n_side map of normal

   N_new = sparse.DOK((nc,nc,3), dtype=float32)
   #self.CM = np.zeros((nc,ns,3))

   self.CPB = np.zeros((nc,3))
   i = [];j = [];k = []
   data = []
   for ll in self.side_list['active'] :
     elems = self.get_elems_from_side(ll)
     kc1 = elems[0]
     kc2 = elems[1]
     vol1 = self.get_elem_volume(kc1)
     vol2 = self.get_elem_volume(kc2)
     area = self.compute_side_area(ll)
     normal = self.compute_side_normal(kc1,ll)
     #normal = np.array([round(n,7) for n in normal])
     if not kc1 == kc2:
       N[kc1,kc2] = normal*area/vol1
       N[kc2,kc1] = -normal*area/vol2
       N_new[kc1,kc2] = normal
       N_new[kc2,kc1] = -normal
     else:  
       s = np.where(np.array(self.elem_side_map[kc1])==ll)[0][0]
       CM[kc1,s]  = normal*area/vol1
       CP[kc1,s] = normal



   self.CP = CP.to_coo()
   self.CM = CM.to_coo()
   self.N = N.to_coo()
   self.N_new = N_new.to_coo()




 #def compute_elem_map(self):

 # self.elem_map = {}
 # for elem1 in self.elem_side_map:
 #   for side in self.elem_side_map[elem1]:
 #    elem2 = self.get_neighbor_elem(elem1,side)
 #    self.elem_map.setdefault(elem1,[]).append(elem2)


 def get_side_orthognal_direction(self,side):

   elem = self.side_elem_map[side][0]
   c1 = self.get_elem_centroid(elem)
   c2 = self.get_side_centroid(side)
   normal = self.compute_side_normal(elem,side)
   area = self.compute_side_area(side)
   Af = area*normal
   dist = c2-c1
   v_orth = np.dot(Af,Af)/np.dot(Af,dist)
   return v_orth


 def get_distance_between_centroids_of_two_elements_from_side(self,ll):


   (elem_1,elem_2) = self.side_elem_map[ll]
   c1 = self.get_elem_centroid(elem_1)
   c2 = self.get_next_elem_centroid(elem_1,ll)
   dist = np.linalg.norm(c2-c1)

   return dist

 def get_decomposed_directions(self,elem_1,elem_2,rot = np.eye(3)):

   #if elem_1 == elem_2:
   # return 0.0,0.0
   #else:
    side = self.get_side_between_two_elements(elem_1,elem_2)
    normal = self.compute_side_normal(elem_1,side)
    area = self.compute_side_area(side)
    Af = area*normal
    c1 = self.get_elem_centroid(elem_1)

    if elem_1 == elem_2:
     c2 = self.get_side_centroid(side)
    else:    
     c2 = self.get_next_elem_centroid(elem_1,side)

    dist = c2 - c1

    v_orth = np.dot(normal,np.dot(rot,normal))/np.dot(normal,dist)
    v_non_orth = np.dot(rot,normal) - dist*v_orth
    return area*v_orth,area*v_non_orth


 def get_side_coeff(self,side):

  elem = self.side_elem_map[side][0]
  vol = self.get_elem_volume(elem)
  normal = self.compute_side_normal(elem,side)
  area = self.get_side_area(side)
  return normal*area/vol #This is specific to boundaries

 #def get_coeff(self,elem_1,elem_2):

 #  side = self.get_side_between_two_elements(elem_1,elem_2)
 #  vol = self.get_elem_volume(elem_1)
 #  normal = self.compute_side_normal(elem_1,side)
 #  area = self.compute_side_area(side)

 #  return normal*area/vol

 def compute_2D_adjusment(self,normal,phi_s,dphi):

  tmp =  np.arctan2(normal[1],normal[0])
  if not tmp == 0.0:
   tmp = (tmp + np.pi*(1.0-np.sign(tmp)))%(2.0*np.pi)

  phi_normal = (np.pi/2.0-tmp)%(2.0*np.pi)

  phi_right = (phi_normal+np.pi/2.0)%(2.0*np.pi)
  phi_left = (phi_normal-np.pi/2.0)%(2.0*np.pi)

  phi_1 = 0.0
  phi_2 = 0.0
  phi_left = round(phi_left,8)
  phi_right = round(phi_right,8)
  phi_normal = round(phi_normal,8)
  phi_s = round(phi_s,8)


  delta = 1e-7
  case = 0
  if phi_s <= phi_right +delta and phi_s > (phi_right - dphi/2.0)%(2.0*np.pi):
   phi_1 = phi_right
   phi_2 = (phi_s + dphi/2.0)%(2.0*np.pi)
   case = 1

  elif phi_s > phi_right + delta and phi_s < (phi_right + dphi/2.0)%(2.0*np.pi):
   phi_1 = (phi_s-dphi/2.0)%(2.0*np.pi)
   phi_2 = phi_right
   case = 2

  elif phi_s < phi_left - delta and phi_s > (phi_left - dphi/2.0)%(2.0*np.pi):
   phi_1 = phi_left
   phi_2 = (phi_s + dphi/2.0)%(2.0*np.pi)
   case = 3
   #print(phi_1 * 180.0/np.pi)
   #print(phi_2 * 180.0/np.pi)
   #print(phi_normal * 180.0/np.pi)
   #print(phi_s * 180.0/np.pi)



  elif phi_s >= phi_left - delta and phi_s < (phi_left + dphi/2.0)%(2.0*np.pi):
   phi_1 = (phi_s-dphi/2.0)%(2.0*np.pi)
   phi_2 = phi_left
   case = 4


  phi_dir_adj = [np.cos(phi_1) - np.cos(phi_2),np.sin(phi_2) - np.sin(phi_1),0.0]
  return np.array(phi_dir_adj),case


 def get_angular_coeff_old(self,elem_1,elem_2,angle):

  vol = self.get_elem_volume(elem_1)
  side = self.get_side_between_two_elements(elem_1,elem_2)
  normal = self.compute_side_normal(elem_1,side)
  area = self.compute_side_area(side)
  tmp = np.dot(angle,normal)
  cm = 0
  cp = 0
  cmb = 0
  cpb = 0

   
  if tmp < 0:
   if elem_1 == elem_2:  
    cmb = tmp*area/vol
   else:
    cm = tmp*area/vol
  else:
   cp = tmp*area/vol
   if elem_1 == elem_2:  
    cpb = tmp
  

  return cm,cp,cmb,cpb


 def get_angular_coeff(self,elem_1,elem_2,index):

  side = self.get_side_between_two_elements(elem_1,elem_2)
  vol = self.get_elem_volume(elem_1)
  normal = self.compute_side_normal(elem_1,side)
  for i in range(3):
   normal[i] = round(normal[i],8)
  area = self.compute_side_area(side)


  if self.dim == 2:
      
   p = index
   
   polar_int = self.dom['polar_dir'][p]*self.dom['polar_factor']
   tmp = np.dot(polar_int,normal)
   coeff  = tmp*area/vol
   #coeff = np.dot(angle_factor,normal)*area/vol
   #control  = np.dot(self.dom['polar_dir'][p],normal)
  else :
   t = int(index/self.dom['self.n_phi'])
   p = index%self.dom['n_phi']
   angle_factor = self.dom['S'][t][p]/self.dom['d_omega'][t][p]
   coeff = np.dot(angle_factor,normal)*area/vol

  #coeff = round(coeff,8)
  #anti aliasing---
  extra_coeff = 0.0
  extra_angle = 0.0
  case = 0
  if self.dim == 2:
   (phi_dir_adj,case) = self.compute_2D_adjusment(normal,round(self.dom['phi_vec'][p],8),self.dom['d_phi'])
   #extra_coeff = np.dot(phi_dir_adj,normal)*area/vol/self.dom['d_phi_vec'][p]
   #extra_angle = np.dot(phi_dir_adj,normal)*self.dom['d_phi']

  cm = 0.0
  cp = 0.0
  cmb = 0.0
  cpb = 0.0
  if coeff >= 0:
   cp = coeff - extra_coeff
   if not elem_1 == elem_2:
    cm = extra_coeff
   else:
    cpb = tmp*self.dom['d_phi'] - extra_angle
    cmb = extra_coeff
  else :
   cp = extra_coeff
   if not elem_1 == elem_2: #In this case the incoming part is from the boundary
    cm = coeff  - extra_coeff
   else:
    cmb = coeff - extra_coeff
    cpb = extra_angle


  if cpb < 0.0:
   print('cpb')
   print(cpb)

  if cmb > 0.0:
   print('cmb')
   print(cmb)

  if cm > 0.0:
   print('cm')
   print(cm)

  if cp < 0.0:#
     print('cp')
     print(cp)
     print(extra_coeff)
     print(case)
     print(coeff)
#     quit()

  return cm,cp,cmb,cpb


# def get_aa(self,elem_1,elem_2,phi_dir,dphi):

#   side = self.get_side_between_two_elements(elem_1,elem_2)
#   vol = self.get_elem_volume(elem_1)
#   normal = self.compute_side_normal(elem_1,side)

#   gamma = arcsin(np.dot(phi_dir,normal[0:2]))

#   if gamma >= 0.0:
     #p_plus = 0.5 + min([gamma,dphi/2.0])/dphi
     #p_minus = 1.0-p_plus


   #if gamma < 0.0:
#     p_minus = 0.5 + min([-gamma,dphi/2.0])/dphi
     #p_plus = 1.0-p_minus

  # return p_minus,p_plus



 def get_af(self,elem_1,elem_2):

   side = self.get_side_between_two_elements(elem_1,elem_2)
   normal = self.compute_side_normal(elem_1,side)
   area = self.compute_side_area(side)
   return normal*area


 def get_normal_between_elems(self,elem_1,elem_2):

   side = self.get_side_between_two_elements(elem_1,elem_2)
   normal = self.compute_side_normal(elem_1,side)
   return normal


 def get_side_between_two_elements(self,elem_1,elem_2):

   if elem_1 == elem_2: #Boundary side
    for side in self.elem_side_map[elem_1]:
     if side in self.side_list['Boundary']:
      return side
    print('No boundary side')
    quit()
   else:

    for side_1 in self.elem_side_map[elem_1]:
     for side_2 in self.elem_side_map[elem_2]:
      if side_1 == side_2:
       return side_1

    print('no adjacents elems')
    assert(1==0)
    quit()



 def compute_gradient_on_side(self,x,ll,side_periodic_value):

   #Diff in the temp
  
   elems = self.side_elem_map[ll]
   kc1 = elems[0]
   temp_1 = x[kc1]
   #Build tempreature matrix--------------------------
   diff_temp = np.zeros(self.dim + 1)
   grad = np.zeros(3)
   for s in self.elem_side_map[kc1]:
    if s in self.side_list['Boundary']:
     temp_2 = temp_1
    else:
     kc2 = self.get_neighbor_elem(kc1,s)
     temp_2 = x[kc2] + self.get_side_periodic_value(s,kc2,side_periodic_value)

    ind1 = self.elem_side_map[kc1].index(s)
    diff_t = temp_2 - temp_1
    diff_temp[ind1] = diff_t
    #-----------------------------------------------
    #COMPUTE GRADIENT
   tmp = np.dot(self.weigths[kc1],diff_temp)
   grad[0] = tmp[0] #THESE HAS TO BE POSITIVE
   grad[1] = tmp[1]
   if self.dim == 3:
    grad[2] = 0.0

   return grad



 def compute_thermal_conductivity_from_scalar(self,x,flux_sides,side_periodic_value,factor = np.eye(3)):

   #Diff in the temp
   kappa = 0.0
   for ll in flux_sides :
    normal = self.get_side_normal(0,ll)
    area_loc = self.get_side_area(ll)
    elems = self.side_elem_map[ll]
    kc1 = elems[0]
    temp_1 = x[kc1]
    #Build tempreature matrix--------------------------
    diff_temp = np.zeros(self.dim + 1)
    grad = np.zeros(self.dim)
    for s in self.elem_side_map[kc1]:
     if s in self.side_list['Boundary']:
      temp_2 = temp_1
     else:
      kc2 = self.get_neighbor_elem(kc1,s)
      temp_2 = x[kc2] + self.get_side_periodic_value(s,kc2,side_periodic_value)

     ind1 = self.elem_side_map[kc1].index(s)
     diff_t = temp_2 - temp_1
     diff_temp[ind1] = diff_t
    #-----------------------------------------------
    #COMPUTE GRADIENT
    tmp = np.dot(self.weigths[kc1],diff_temp)
    grad[0] = tmp[0] #THESE HAS TO BE POSITIVE
    grad[1] = tmp[1]
    if self.dim == 3:
     grad[2] = tmp[2]

    #COMPUTE THERMAL CONDUCTIVITY------------------
    for i in range(self.dim):
     for j in range(self.dim):
      kappa -= normal[i]*factor[i][j]*grad[j]*area_loc

   return kappa


 def compute_thermal_conductivity_outer(self,vector,scalar,flux_sides):

   #Here we simply invert Fourier's law
   factor = np.eye(3)
   power = 0.0
   for ns in flux_sides:
    ne = self.side_elem_map[ns][0]
    normal = self.get_side_normal(0,ns)
    area_loc = self.get_side_area(ns)
    power_loc = 0.0
    for i in range(self.dim):
     for j in range(self.dim):
      power_loc -= normal[i]*factor[i][j]*vector[j]*scalar[ne]*area_loc
    power += power_loc
   return power

 def compute_thermal_conductivity(self,grad,flux_sides,factor=np.eye(3)):

   #Here we simply invert Fourier's law
   power = 0.0
   for ns in flux_sides:
    ne = self.side_elem_map[ns][0]
    normal = self.get_side_normal(0,ns)
    area_loc = self.get_side_area(ns)
    power_loc = 0.0
    for i in range(3):
     for j in range(3):
      power_loc -= normal[i]* factor[i][j] * grad[ne][j]*area_loc
    power += power_loc

   return power



 def compute_average_temperature(self,x,flux_sides):

   #Here we simply invert Fourier's law
   temp = 0.0
   for ns in flux_sides:
    ne = self.side_elem_map[ns][0]
    area_loc = self.get_side_area(ns)
    temp += area_loc * x[ne]

   return temp


 def compute_contact_areas(self):

  self.c_areas = np.zeros(3)

  nodesT = self.nodes.copy().T

  minx = min(nodesT[0])
  maxx = max(nodesT[0])
  miny = min(nodesT[1])
  maxy = max(nodesT[1])
  minz = min(nodesT[2])
  maxz = max(nodesT[2])
  if self.dim == 3:
   self.c_areas[0] = (maxy - miny) * (maxz - minz)
   self.c_areas[1] = (maxz - minz) * (maxx - minx)
   self.c_areas[2] = (maxy - miny) * (maxx - minx)
  else :
   self.c_areas[0] = maxy - miny
   self.c_areas[1] = maxx - minx
   self.c_areas[2] = 0


 def get_side_area(self,side):
  return self.side_areas[side]

 def get_elem_volume(self,elem):
  return self.elem_volumes[elem]

 def compute_elem_volumes(self):

  self.elem_volumes = np.zeros(len(self.elems))
  for k in range(len(self.elems)):
   self.elem_volumes[k] = self.compute_elem_volume(k)




 def compute_side_areas(self):
  self.side_areas = np.zeros(len(self.sides))
  for k in range(len(self.sides)):
   self.side_areas[k] = self.compute_side_area(k)


 def get_dim(self):
   return self.dim

 def _update_data(self):
    self.nodes = self.state['nodes']
    #self.elem_list = self.state['elem_list']
    self.dim = self.state['dim']
    self.n_elems = self.state['n_elems']
    self.A = self.state['A']
    self.sides = self.state['sides']
    self.elems = self.state['elems']
    self.side_periodicity = self.state['side_periodicity']
    self.region_elem_map = self.state['region_elem_map']
    self.size = self.state['size']
    self.dim = self.state['dim']
    self.weigths = self.state['weigths']
    self.elem_region_map = self.state['elem_region_map']
    self.elem_side_map = self.state['elem_side_map']
    self.side_node_map = self.state['side_node_map']
    self.node_elem_map = self.state['node_elem_map']
    self.node_side_map = self.state['node_side_map']
    self.side_elem_map = self.state['side_elem_map']
    self.side_list = self.state['side_list']
    self.interp_weigths = self.state['interp_weigths']
    self.elem_centroids = self.state['elem_centroids']
    self.c_areas = self.state['c_areas']
    self.side_centroids = self.state['side_centroids']
    self.periodic_nodes = self.state['periodic_nodes']
    self.elem_volumes = self.state['elem_volumes']
    #self.boundary_elements = self.state['boundary_elements']
    #self.interface_elements = self.state['interface_elements']
    self.side_normals = self.state['side_normals']
    self.side_areas = self.state['side_areas']
    self.exlude = self.state['exlude']
    self.pairs = self.state['pairs']
    self.direction = self.state['grad_direction']
    self.area_flux = self.state['area_flux']
    self.node_list = self.state['node_list']
    self.flux_sides = self.state['flux_sides']
    self.l2g = self.state['l2g']
    self.g2l = self.state['g2l']
    self.nle = self.state['nle']
    self.frame = self.state['frame']
    self.argv = self.state['argv']
    self.polygons = self.state['polygons']
    self.N = self.state['N']
    self.N_new = self.state['N_new']
    self.CM = self.state['CM']
    self.applied_grad = self.state['applied_grad']
    self.CP = self.state['CP']
    #self.periodic_sides = self.state['periodic_sides']
    self.CPB = self.state['CPB']
    self.B = self.state['B']
    #self.labels = self.state['labels']
    self.B_with_area = self.state['B_with_area']
    self.B_with_area_old = self.state['B_with_area_old']
    self.side_periodic_value = self.state['side_periodic_value']
    self.kappa_factor = self.size[self.direction]/self.area_flux



 def import_mesh(self):


  #-------------

  f = open('mesh.msh','r')
  #Read boundary conditions------------------
  f.readline()
  f.readline()
  f.readline()
  f.readline()
  self.blabels = {}
  nb =  int(f.readline())
  for n in range(nb):
   tmp = f.readline().split()
   l = tmp[2].replace('"',r'')
   self.blabels.update({int(tmp[1]):l})

  #------------------------------------------
  self.elem_region_map = {}
  self.region_elem_map = {}


  


  #import nodes------------------------
  #f.readline()
  f.readline()
  f.readline()
  n_nodes = int(f.readline())
  nodes = []
  for n in range(n_nodes):
   tmp = f.readline().split()
   nodes.append([float(tmp[1]),float(tmp[2]),float(tmp[3])])

  nodes = np.array(nodes)

  if self.dim == 3:
   self.size = np.array([ max(nodes[:,0]) - min(nodes[:,0]),\
                  max(nodes[:,1]) - min(nodes[:,1]),\
                  max(nodes[:,2]) - min(nodes[:,2])])
  else:
   self.size = np.array([ max(nodes[:,0]) - min(nodes[:,0]),\
                  max(nodes[:,1]) - min(nodes[:,1]),0])

  self.nodes = nodes
  #import elements and create map
  self.side_elem_map = {}
  self.elem_side_map = {}
  f.readline()
  f.readline()
  n_tot = int(f.readline())
  self.sides = []
  self.elems = []
  b_sides = []
  nr = []

  self.node_side_map = {}
  self.side_node_map = {}
  self.node_elem_map = {}
  self.side_list = {}

  for n in range(n_tot):
   tmp = f.readline().split()

   #Get sides------------------------------------------------------------
   if self.dim == 3 and int(tmp[1]) == 2: #2D area
     n = sorted([int(tmp[5])-1,int(tmp[6])-1,int(tmp[7])-1])

   if self.dim == 2 and int(tmp[1]) == 1: #1D area
     n = sorted([int(tmp[5])-1,int(tmp[6])-1])

   b_sides.append(n)
   nr.append(int(tmp[3]))

   if self.dim == 3 and int(tmp[1]) == 4: #3D Elem
     node_indexes = [int(tmp[5])-1,int(tmp[6])-1,int(tmp[7])-1,int(tmp[8])-1]
     n = sorted(node_indexes)
     self.elems.append(n)
     perm_n =[[n[0],n[1],n[2]],\
             [n[0],n[1],n[3]],\
             [n[1],n[2],n[3]],\
             [n[0],n[2],n[3]]]
     self._update_map(perm_n,b_sides,nr,node_indexes)
     self.elem_region_map.update({len(self.elems)-1:self.blabels[int(tmp[3])]})
     self.region_elem_map.setdefault(self.blabels[int(tmp[3])],[]).append(len(self.elems)-1)

   if self.dim == 2 and int(tmp[1]) == 2: #2D Elem (triangle)
     node_indexes = [int(tmp[5])-1,int(tmp[6])-1,int(tmp[7])-1]
     n = sorted(node_indexes)
     self.elems.append(n)
     perm_n =[[n[0],n[1]],\
             [n[0],n[2]],\
             [n[1],n[2]]]
     self.elem_region_map.update({len(self.elems)-1:self.blabels[int(tmp[3])]})
     self.region_elem_map.setdefault(self.blabels[int(tmp[3])],[]).append(len(self.elems)-1)

     self._update_map(perm_n,b_sides,nr,node_indexes)

   if self.dim == 2 and int(tmp[1]) == 3: #2D Elem (quadrangle)
     n = [int(tmp[5])-1,int(tmp[6])-1,int(tmp[7])-1,int(tmp[8])-1]

     #n = sorted(node_indexes)
     self.elems.append(n)
     perm_n =[ sorted([n[0],n[1]]),\
              sorted([n[1],n[2]]),\
              sorted([n[2],n[3]]),\
              sorted([n[3],n[0]])]
     self._update_map(perm_n,b_sides,nr,n)

     self.elem_region_map.update({len(self.elems)-1:self.blabels[int(tmp[3])]})
     self.region_elem_map.setdefault(self.blabels[int(tmp[3])],[]).append(len(self.elems)-1)

  #------------------------------------------------------------
  #Set default for hot and cold
  self.side_list.setdefault('Hot',[])
  self.side_list.setdefault('Cold',[])


  #Apply Periodic Boundary Conditions
  self.side_list.update({'active':list(range(len(self.sides)))})
  self.side_periodicity = np.zeros((len(self.sides),2,3))
  group_1 = []
  group_2 = []
  self.exlude = []

  self.pairs = [] #global (all periodic pairs)

  self.side_list.setdefault('Boundary',[])
  self.side_list.setdefault('Interface',[])
  #self.node_list.setdefault('Interface',[])
  self.periodic_nodes = []
  #self.periodic_sides = {}

  if self.argv.setdefault('delete_gmsh_files',False):
    os.remove(os.getcwd() + '/mesh.msh')
    os.remove(os.getcwd() + '/mesh.geo')

  for label in list(self.side_list.keys()):

   #Add Cold and Hot to Boundary
   #if label == "Hot" or label == "Cold":
   # tmp = self.side_list.setdefault('Boundary',[])+self.side_list[label]
   # self.side_list['Boundary'] = tmp

   if str(label.split('_')[0]) == 'Periodic':
    if not int(label.split('_')[1])%2==0:
     contact_1 = label
     contact_2 = 'Periodic_' + str(int(label.split('_')[1])+1)
     group_1 = self.side_list[contact_1]
     group_2 = self.side_list[contact_2]
     pairs = []

     #compute tangential unity vector
     tmp = self.nodes[self.sides[group_2[0]][0]] - self.nodes[self.sides[group_2[0]][1]]
     t = tmp/np.linalg.norm(tmp)
     n = len(group_1)
     for s1 in group_1:
      d_min = 1e6
      for s in group_2:
       c1 = self.compute_side_centroid(s1)
       c2 = self.compute_side_centroid(s)
       d = np.linalg.norm(c2-c1)
       if d < d_min:
        d_min = d
        pp = c1-c2
        s2 = s

      #if abs(np.dot(pp,self.nodes[self.sides[s1][0]]-self.nodes[self.sides[s1][1]]))>1e-4:
      pairs.append([s1,s2])
      self.side_periodicity[s1][1] = pp
      self.side_periodicity[s2][1] = -pp

      #self.periodic_sides[s1] = s2 
      #self.periodic_sides[s2] = s1
      if np.linalg.norm(self.nodes[self.sides[s1][0]] - self.nodes[self.sides[s2][0]]) == np.linalg.norm(pp):
       self.periodic_nodes.append([self.sides[s1][0],self.sides[s2][0]])
       self.periodic_nodes.append([self.sides[s1][1],self.sides[s2][1]])
      else:
       self.periodic_nodes.append([self.sides[s1][0],self.sides[s2][1]])
       self.periodic_nodes.append([self.sides[s1][1],self.sides[s2][0]])


     plot_sides = False
     if plot_sides:
      for s in pairs:
       c1 = self.compute_side_centroid(s[0])
       c2 = self.compute_side_centroid(s[1])
       #plot([c1[0],c2[0]],[c1[1],c2[1]],color='r')
      #show()
     #Amend map
     for s in pairs:
      s1 = s[0]
      s2 = s[1]

      #Change side in elem 2
      elem2 = self.side_elem_map[s2][0]
      index = self.elem_side_map[elem2].index(s2)
      self.elem_side_map[elem2][index] = s1
      self.side_elem_map[s1].append(elem2)

      #To get hflux sides right-----
      self.side_elem_map[s2].append(self.side_elem_map[s1][0])

      #-------------------------

      #Delete s2 from active list
      self.side_list['active'].remove(s2)


      self.exlude.append(s2)
      tmp = self.side_list.setdefault('Inactive',[]) + [s2]
      self.side_list['Inactive'] = tmp

     #Polish sides
     tmp = self.side_list.setdefault('Periodic',[])+self.side_list[contact_1]
     self.side_list['Periodic'] = tmp


     del self.side_list[contact_1]
     del self.side_list[contact_2]
     self.pairs += pairs

  #Create boundary_elements--------------------

  #self.boundary_elements = []
  #self.interface_elements = []

  self.node_list = {}
  boundary_nodes = []
  for ll in self.side_list['Boundary']:
   #self.boundary_elements.append(self.side_elem_map[ll][0])
   for node in self.sides[ll]:
    if not node in boundary_nodes:
     boundary_nodes.append(node)
  self.node_list.update({'Boundary':boundary_nodes})

  interface_nodes = []
  #self.interface_elements = []
  for ll in self.side_list['Interface']:
   #self.interface_elements.append(self.side_elem_map[ll][0])
   #self.interface_elements.append(self.side_elem_map[ll][1])
   for node in self.sides[ll]:
    if not node in interface_nodes:
     interface_nodes.append(node)
  self.node_list.update({'Interface':interface_nodes})

  self.side_list.update({'active_global':self.side_list['active']})
  self.adjust_boundary_elements()

  self.l2g=range(len(self.elems))
  self.g2l=range(len(self.elems))
  self.nle = len(self.elems)

  #print(self.node_list['Interface'])


  #delete MESH-----
  #a=subprocess.check_output(['rm','-f','mesh.geo'])
  #a=subprocess.check_output(['rm','-f','mesh.msh'])

  #----------------


 def get_elems_from_side(self,ll):

  return self.side_elem_map[ll]


 def _update_map(self,perm_n,b_sides,nr,node_indexes):


    #UPDATE NODE_ELEM_MAP-------------------
    for n in node_indexes:
     self.node_elem_map.setdefault(n,[]).append(len(self.elems)-1)
    #---------------------------------------

    for new_n in perm_n :
     #Use the node_side_map---------
     index = -1
     sides = []
     for k in new_n:
      if index == -1:
       if k in self.node_side_map.keys():
        for s in self.node_side_map[k]:
         if np.allclose(self.sides[s],new_n):
          index = s
          break

     if index == -1:
      self.sides.append(new_n)
      index = len(self.sides)-1

      #add boundary--------------------------------------
      try:
       k = b_sides.index(new_n)

       self.side_list.setdefault(self.blabels[nr[k]],[]).append(index)
      except:
       a = 1
      #------------------------------------------------------
      for i in range(len(new_n)):
       self.node_side_map.setdefault(new_n[i],[]).append(index)
       self.side_node_map.setdefault(index,[]).append(new_n[i])

     #------------------------------------
     self.side_elem_map.setdefault(index,[]).append(len(self.elems)-1)
     self.elem_side_map.setdefault(len(self.elems)-1,[]).append(index)





 def get_elem_boundary_area_normal(self,elem) :

    sides = self.elem_side_map[elem]
    is_here = 0
    for s in sides:
     if s in self.side_list['Boundary'] :
      normal = self.compute_side_normal(elem,s)
      is_here = 1
      break
    if is_here == 0 : print('ERROR: side is not a boundary')
    return normal


 def compute_side_normals(self):

  self.side_normals = np.zeros((len(self.sides),2,3))
  for s in range(len(self.sides)):
   elems = self.side_elem_map[s]
   self.side_normals[s][0] = self.compute_side_normal(elems[0],s)
   if len(elems)>1:
    self.side_normals[s][1] = self.compute_side_normal(elems[1],s)

 def compute_side_normal(self,ne,ns):

  #Get generic normal--------------------
  v1 = self.nodes[self.sides[ns][1]]-self.nodes[self.sides[ns][0]]
  if self.dim == 3:
   v2 = self.nodes[self.sides[ns][2]]-self.nodes[self.sides[ns][1]]
  else :
   v2 = np.array([0,0,1])
  v = np.cross(v1,v2)
  normal = v/np.linalg.norm(v)
  #-------------------------------------

  #Check sign
  ind = self.side_elem_map[ns].index(ne)
  c_el   = self.compute_centroid(self.elems[ne])
  c_side = self.compute_centroid(self.sides[ns]) -  self.side_periodicity[ns][ind]

  c = (c_side - c_el)
  if np.dot(normal,c) < 0: normal = - normal


  return normal

 def get_n_elems(self):
  return len(self.elems)

 def compute_side_area(self,ns):

  p = self.nodes[self.sides[ns]]
  if self.dim == 2:
    return np.linalg.norm(p[1]-p[0])
  else:
   v = np.cross(p[1]-p[0],p[1]-p[2])
   normal = v/np.linalg.norm(v)
   tmp = np.zeros(3)
   for i in range(len(p)):
    vi1 = p[i]
    vi2 = p[(i+1)%len(p)]
    tmp += np.cross(vi1, vi2)

   result = np.dot(tmp,normal)
   return abs(result/2)


 def write_vtk(self,file_name,data) :

   points = self.nodes
   el = self.elems
   cells = []
   for k in range(len(el)):
    if self.dim == 3:
     cells.append(el[k][0:4])
    else:
     cells.append(el[k][0:3])

   if self.dim == 3:
    vtk = VtkData(UnstructuredGrid(points,tetra=cells),data)
   else:
    vtk = VtkData(UnstructuredGrid(points,triangle=cells),data)
   vtk.tofile(file_name,'ascii')


 def get_side_normal(self,ne,ns):
  return self.side_normals[ns,ne]


 def get_elem_centroid(self,ne):
  return self.elem_centroids[ne]

 def get_side_centroid(self,ns):
  return self.side_centroids[ns]



 def compute_side_centroids(self):

  self.side_centroids = np.zeros((len(self.sides),3))
  for s in range(len(self.sides)):
   self.side_centroids[s] = self.compute_side_centroid(s)

 def compute_side_centroid(self,ns):

  nodes = self.nodes[self.sides[ns]]

  centroid = np.zeros(3)
  for p in nodes:
   centroid += p
  return centroid/len(nodes)



 def compute_elem_centroids(self):

  self.elem_centroids = np.zeros((len(self.elems),3))
  for elem in range(len(self.elems)):
   self.elem_centroids[elem] = self.compute_elem_centroid(elem)


 def compute_elem_centroid(self,ne):
  nodes = self.nodes[self.elems[ne]]
  centroid = np.zeros(3)
  for p in nodes:
   centroid += p

  return centroid/len(nodes)

 def compute_elem_volume(self,kc1):

  if self.dim == 3: #Assuming Tetraedron
   ns = self.elems[kc1]
   m = np.ones((4,4))
   m[0,0:3] = self.nodes[ns[0]]
   m[1,0:3] = self.nodes[ns[1]]
   m[2,0:3] = self.nodes[ns[2]]
   m[3,0:3] = self.nodes[ns[3]]
   return abs(1.0/6.0 * np.linalg.det(m))

  if self.dim == 2: #Assuming Tetraedron

    
   points = self.nodes[self.elems[kc1]]
   x = []; y= []
   for p in points:
    x.append(p[0])
    y.append(p[1])

   return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


   return volume


 def get_side_periodic_value(self,elem,elem_p) :

    ll = self.get_side_between_two_elements(elem,elem_p)
    ind = self.side_elem_map[ll].index(elem)
    return self.side_periodic_value[ll][ind]


 def get_next_elem_centroid(self,elem,side):

  centroid1 = self.get_elem_centroid(elem)
  elem2 = self.get_neighbor_elem(elem,side)
  centroid2 = self.get_elem_centroid(elem2)
  ind1 = self.side_elem_map[side].index(elem)
  ind2 = self.side_elem_map[side].index(elem2)
  centroid = centroid2 - self.side_periodicity[side][ind1] + self.side_periodicity[side][ind2]
  return centroid

 def cross_interface(self,p1,p2):

  line1 = LineString([p1,p2])
  for ll in self.side_list['Interface']:
   p3 = self.nodes[self.sides[ll][0]][:2]
   p4 = self.nodes[self.sides[ll][1]][:2]
   line2 = LineString([p3,p4])
   tmp = line1.intersection(line2)
   if isinstance(tmp,shapely.geometry.Point):
     return np.array([tmp.x,tmp.y])
  return []


 def compute_centroid(self,side):

  node = np.zeros(3)
  for p in side:
   node += self.nodes[p]

  return node/len(side)

 def get_elem_extended_neighbors(self,elem):
  #This also includes the element get_distance_between_centroids_of_two_elements_from_side
  neighbors = []
  for n in self.elems[elem]:
   for elem2 in self.node_elem_map[n]:
    if not elem2 in neighbors: neighbors.append(elem2)
    #for m in self.elems[elem2]:
    # for elem3 in self.node_elem_map[m]:
    #    if not elem3 in neighbors: neighbors.append(elem3)

  return neighbors

 def get_elem_neighbors(self,elem):

  neighbors = []
  for ll in self.elem_side_map[elem]:
   neighbors.append(self.get_neighbor_elem(elem,ll))
  return neighbors

 def get_neighbor_elem(self,elem,ll) :

    if not (elem in self.side_elem_map[ll]) : print('error')

    for tmp in self.side_elem_map[ll] :
       if not (tmp == elem) :
         return tmp


 def compute_interpolation_weigths(self):

  self.interp_weigths = {}# np.zeros(len(self.sides))
  for ll in self.side_list['active']:
   if not (ll in (self.side_list['Boundary'] + self.side_list['Hot'] + self.side_list['Cold'])) :
    e0 = self.side_elem_map[ll][0]
    e1 = self.side_elem_map[ll][1]
    P0 = self.get_elem_centroid(e0)
    P1 = self.get_next_elem_centroid(e0,ll)
    #---------------------------------------------------------------
    if self.dim == 3:
     #from here: http://geomalgorithms.com/a05-_intersect-1.html
     u = P1 - P0
     n = self.get_side_normal(1,ll)
     node = self.nodes[self.sides[ll][0]]
     w = P0 - node
     s = -np.dot(n,w)/np.dot(n,u)
    else: #dim = 2
     P2 = self.nodes[self.sides[ll][0]]
     P3 = self.nodes[self.sides[ll][1]]
     den = (P3[1] - P2[1])*(P1[0]-P0[0])-(P3[0]-P2[0])*(P1[1]-P0[1])
     num = (P3[0] - P2[0])*(P0[1]-P2[1])-(P3[1]-P2[1])*(P0[0]-P2[0])
     a = num/den
     P = P0 + a * (P1-P0)
     if a < 0.0 or a > 1.0 :
      print(P0)
      print(P1)
      print('ERROR in the skew parameter')
      return
     dist = np.linalg.norm(P1-P0)
     d = np.linalg.norm(P - P1)
     s = d/dist
     #---------------------------------------------------------------
    self.interp_weigths.update({ll:s})
   else:
    #self.interp_weigths.update({ll:0.0})
    self.interp_weigths.update({ll:1.0})


 def get_region_from_elem(self,elem):
  return self.elem_region_map[elem]


 def get_interpolation_weigths(self,ll,elem):

  #return self.interp_weigths[ll]
  if self.side_elem_map[ll][0] == elem:
   return self.interp_weigths[ll]
  else:
   return 1.0-self.interp_weigths[ll]

 def compute_boundary_condition_data(self):

    gradir = self.direction

    if gradir == 0:
     flux_dir = [1,0,0]
     length = self.size[0]

    if gradir == 1:
     flux_dir = [0,1,0]
     length = self.size[1]

    if gradir == 2:
     flux_dir = [0,0,1]
     length = self.size[2]

    delta = 1e-2
    nsides = len(self.sides)
    flux_sides = [] #where flux goes
    side_value = np.zeros(nsides)

    tmp = self.side_list.setdefault('Periodic',[]) + self.exlude

    for kl,ll in enumerate(tmp) :
     normal = self.compute_side_normal(self.side_elem_map[ll][0],ll)
     tmp = np.dot(normal,flux_dir)
     if tmp > delta : #either negative or positive
      flux_sides.append(ll)

     if tmp < - delta :
        side_value[ll] = -1.0
     if tmp > delta :
        side_value[ll] = +1.0
        
    side_periodic_value = np.zeros((nsides,2))

   
    n_el = len(self.elems)
    B = sparse.DOK((n_el,n_el),dtype=float32)
    B_with_area = sparse.DOK((n_el,n_el,3),dtype=float32)

    B_with_area_old = sparse.DOK((n_el,n_el),dtype=float32)

     
    if len(self.side_list.setdefault('Periodic',[])) > 0:
     for side in self.pairs:
      side_periodic_value[side[0]][0] = side_value[side[0]]
      side_periodic_value[side[0]][1] = side_value[side[1]]

      elem1,elem2 = self.side_elem_map[side[0]]
      B[elem1,elem2] = side_value[side[0]]
      B[elem2,elem1] = side_value[side[1]]


      if np.linalg.norm(np.cross(self.get_side_normal(1,side[0]),self.applied_grad)) < 1e-5:
       B_with_area[elem1,elem2] = abs(side_value[side[0]]*self.get_side_area(side[0]))*self.get_side_normal(0,side[0])
       B_with_area_old[elem1,elem2] = abs(side_value[side[0]]*self.get_side_area(side[0]))
      
    self.area_flux = abs(np.dot(flux_dir,self.c_areas))
    self.flux_sides = flux_sides
    self.side_periodic_value = side_periodic_value
    self.B = B.to_coo()
    self.B_with_area = B_with_area.to_coo()
    self.B_with_area_old = B_with_area_old.to_coo()#.to_scipy_sparse()



 def compute_least_square_weigths(self):

   nd = len(self.elems[0])
   diff_dist = np.zeros((len(self.elems),nd,self.dim))


   for ll in self.side_list['active_global'] :
    elems = self.side_elem_map[ll]
    kc1 = elems[0]
    c1 = self.compute_elem_centroid(kc1)
    ind1 = self.elem_side_map[kc1].index(ll)
    if not ll in (self.side_list['Boundary'] + self.side_list['Hot'] + self.side_list['Cold'] + self.side_list['Interface']):
     #Diff in the distance
     kc2 = elems[1]
     c2 = self.get_next_elem_centroid(kc1,ll)
     ind2 = self.elem_side_map[kc2].index(ll)
     dist = c2-c1

     for i in range(self.dim):
      diff_dist[kc1][ind1][i] = dist[i]
      diff_dist[kc2][ind2][i] = -dist[i]
    else :
     dist = self.compute_side_centroid(ll) - c1
     for i in range(self.dim):
      diff_dist[kc1][ind1][i] = dist[i]
      

     if ll in self.side_list['Interface']:# or self.side_list['Boundary']:
      kc2 = elems[1]
      c2 = self.get_next_elem_centroid(kc1,ll)
      dist = self.compute_side_centroid(ll) - c2
      ind2 = self.elem_side_map[kc2].index(ll)
      for i in range(self.dim):
        diff_dist[kc2][ind2][i] = dist[i]



   #Compute weights
   self.weigths = []
   for tmp in diff_dist :
    self.weigths.append(np.dot(np.linalg.inv(np.dot(np.transpose(tmp),tmp)),np.transpose(tmp)  ))


 def compute_interfacial_node_temperature(self,temp,kappa):
     
     int_temp_matrix = {}
     int_temp_inclusion = {}
     for ll in self.side_list['Interface'] :

       (i,j) = self.side_elem_map[ll]
       w = self.get_interpolation_weigths(ll,i)
       Ti = temp[i]
       Tj = temp[j]
       ki = kappa[i]
       kj = kappa[j]
       Tb = (kj*w*Tj + ki*(1-w)*Ti)/(kj*w + ki*(1-w))

       (n1,n2) = self.side_node_map[ll]

       int_temp_matrix[n1] = int_temp_matrix.setdefault(n1,0) + Tb/2
       int_temp_matrix[n2] = int_temp_matrix.setdefault(n2,0) + Tb/2

       int_temp_inclusion[n1] = int_temp_inclusion.setdefault(n1,0) + Tb/2
       int_temp_inclusion[n2] = int_temp_inclusion.setdefault(n2,0) + Tb/2

     return {'inclusion':int_temp_inclusion,'matrix':int_temp_matrix}

 def compute_interfacial_temperature_side(self,temp,kappa):
     
     int_temp = {}
     
     for ll in self.side_list['Interface'] :

       (i,j) = self.side_elem_map[ll]
       w = self.get_interpolation_weigths(ll,i)
       Ti = temp[i]
       Tj = temp[j]
       ki = kappa[i]
       kj = kappa[j]
       Tb = (kj*w*Tj + ki*(1-w)*Ti)/(kj*w + ki*(1-w))

       int_temp[ll] = Tb

     return int_temp


 def compute_divergence(self,data,add_jump=True,verbose=0) :

  div = np.zeros(len(self.elems))     
  for n,d in enumerate(data.T):
    div += self.compute_grad(d,add_jump = add_jump,verbose=verbose).T[n]

  return div


 def compute_grad(self,temp,lattice_temp =[],add_jump=True,verbose=0,pbcs=None,interfacial_temperature = None) :

   if len(lattice_temp) == 0: lattice_temp = temp

   nd = len(self.elems[0])

   if self.dim == 2:
    diff_temp = np.zeros((self.nle,nd))
   else:
    diff_temp = np.zeros((self.nle,4))

   gradT = np.zeros((self.nle,3))

   #Diff in the temp
   for ll in self.side_list['active'] :
   #for ll in range(len(self.sides))  :

    elems = self.side_elem_map[ll]
    kc1 = elems[0]
    c1 = self.get_elem_centroid(kc1)
    ind1 = self.elem_side_map[kc1].index(ll)

    if not ll in (self.side_list['Boundary'] + self.side_list['Hot'] + self.side_list['Cold'] + self.side_list['Interface']) :
     kc2 = elems[1]
     ind2 = self.elem_side_map[kc2].index(ll)

     temp_1 = temp[self.g2l[kc1]]
     temp_2 = temp[self.g2l[kc2]]
     if add_jump: 
       temp_2 += self.get_side_periodic_value(kc2,kc1) 
     else:
       temp_2 += pbcs[kc1,kc2]        

     diff_t = temp_2 - temp_1

     diff_temp[self.g2l[kc1]][ind1]  = diff_t
     diff_temp[self.g2l[kc2]][ind2]  = -diff_t
    else :
     if ll in self.side_list['Hot'] :
      diff_temp[kc1][ind1]  = 0.5-temp[kc1]

     if ll in self.side_list['Cold'] :
      diff_temp[kc1][ind1]  = -0.5-temp[kc1]

     if ll in self.side_list['Boundary'] : 
      diff_temp[self.g2l[kc1]][ind1]  = lattice_temp[self.g2l[kc1]]-temp[self.g2l[kc1]]

     if ll in self.side_list['Interface'] : 
      kc2 = elems[1]
      ind2 = self.elem_side_map[kc2].index(ll)
      if interfacial_temperature == None:
       Tb1 = temp[kc1]
       Tb2 = temp[kc2]
      else:    
       Tb1 = interfacial_temperature[ll][0]
       Tb2 = interfacial_temperature[ll][1]

      diff_temp[self.g2l[kc1]][ind1]  = Tb1 - temp[self.g2l[kc1]]
      diff_temp[self.g2l[kc2]][ind2]  = Tb2 - temp[self.g2l[kc2]]

   for k in range(self.nle) :
       
    tmp = np.dot(self.weigths[self.l2g[k]],diff_temp[k])
    gradT[k][0] = tmp[0] #THESE HAS TO BE POSITIVE
    gradT[k][1] = tmp[1]
    if self.dim == 3:
     gradT[k][2] = tmp[2]

   return gradT
