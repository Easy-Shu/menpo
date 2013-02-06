from ibugMM.importer.model import ModelImporterFactory
from ibugMM.mesh.face import Face
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from mayavi import mlab
plt.interactive(True)

def print_geodesic_patterns(phi_coords, i):
  distances = distance.pdist(phi_coords[:,0:i], 'cityblock')
  plt.figure()
  fig = plt.gcf()
  plt.hist(distances, bins=1000, histtype='stepfilled', range=(0,500))
  fig.savefig('full_' + `i` + '.pdf')
  plt.figure()
  fig = plt.gcf()
  small_distances = distances[np.where(distances < 5)]
  plt.hist(small_distances, bins=1000, histtype='stepfilled', range=(0,5))
  fig.savefig('near0_' + `i` + '.pdf')

def gen_phi_coords(face, landmarks):
  phi_m = face.calculate_geodesics(landmarks['mouth'])['phi']
  phi_n = face.calculate_geodesics(landmarks['nose'])['phi']
  phi_l = face.calculate_geodesics(landmarks['l_eye'])['phi']
  phi_r = face.calculate_geodesics(landmarks['r_eye'])['phi']
  # ph_coords s.t. phi_coords[0] is the geodesic vector for the first ordinate
  return np.vstack((phi_m, phi_n, phi_l, phi_r)).T

## ioannis face
ioannis_path_1 = '/home/jab08/Dropbox/testData/ioannis_1.obj'
importer = ModelImporterFactory(ioannis_path_1)
o_ioannis_1 = importer.generateFace()
ioannis_path_2 = '/home/jab08/Dropbox/testData/ioannis_2.obj'
importer = ModelImporterFactory(ioannis_path_2)
o_ioannis_2 = importer.generateFace()
# store the landmarks 
# note, l_eye is THEIR l_eye (right as we look at it)
o_ioannis_1.landmarks['nose']  = [46731]
o_ioannis_1.landmarks['l_eye'] = [5695]
o_ioannis_1.landmarks['r_eye'] = [5495]
o_ioannis_1.landmarks['mouth'] = [15461, 18940, 12249, 17473, 36642, 2889, 11560, 10125]
o_ioannis_1.landmarks['cheek_freckle'] = [752]

o_ioannis_2.landmarks['nose']  = [10476]
o_ioannis_2.landmarks['l_eye'] = [40615]
o_ioannis_2.landmarks['r_eye'] = [40526]
o_ioannis_2.landmarks['mouth'] = [41366, 28560, 36719, 17657, 13955, 26988, 6327, 8229]
o_ioannis_1.landmarks['cheek_freckle'] = [32294]
ioannis_1  = o_ioannis_1.new_face_masked_from_nose_landmark()
ioannis_2  = o_ioannis_2.new_face_masked_from_nose_landmark()

# generate the geodesic vectors for face 1 and 2
phi_1 = gen_phi_coords(ioannis_1, ioannis_1.landmarks)
phi_2 = gen_phi_coords(ioannis_2, ioannis_2.landmarks)

# find all distances between the two phi's
distances = distance.cdist(phi_1, phi_2)

# now find the minimum mapping indicies, both for 2 onto 1 and 1 onto 2
mins_2_to_1 = np.argmin(distances, axis=1)
mins_1_to_2 = np.argmin(distances, axis=0)

# and count how many times each vertex is mapped from
count_1_to_2 = np.bincount(mins_1_to_2)
count_2_to_1 = np.bincount(mins_2_to_1)

# calculate the mapping and build a new face using it
full_ioannis_2_coords = np.copy(ioannis_1.coords)
full_ioannis_2_coords[index_map_1] = ioannis_2.coords[mins_2_to_1]

newFace = Face(coords=full_ioannis_2_coords,coordsIndex=ioannis_1.coordsIndex)





def l2_using_only(indexes):
  if len(indexes) > 1:
    return np.sum(delta_phi[:,indexes]**2,1)
  else:
    return delta_phi[:,indexes]**2

#phi_coords_2 = gen_phi_coords(ioannis_2, landmarks_2)
#for i in range(1,5):
#  print_geodesic_patterns(phi_coords_2, i)


#figure = mlab.gcf()
#mlab.clf()
#figure.scene.disable_render = True
#
#self = ioannis_2
#face_coords = mlab.triangular_mesh(self.coords[:,0], self.coords[:,1],
#                                   self.coords[:,2], self.coordsIndex, 
#                                   color=(0.5,0.5,0.5)) 
#figure.scene.disable_render = False
#face_points = face_coords.glyph.glyph_source.glyph_source.output.points.to_array()
#
#
#def picker_callback(picker):
#    """ Picker callback: this get called when on pick events.
#    """
#    if picker.actor in face_coords.actor.actors:
#        # Find which data point corresponds to the point picked:
#        # we have to account for the fact that each data point is
#        # represented by a glyph with several points
#        point_id = picker.point_id/face_points.shape[0]
#        # If the no points have been selected, we have '-1'
#        print point_id
#        if point_id != -1:
#            # Retrieve the coordinnates coorresponding to that data
#            # point
#            x, y, z = self.coords[point_id,0], self.coords[point_id,1], self.coords[point_id,2]
#            # Move the outline to the data point.
#            outline.bounds = (x-0.1, x+0.1,
#                              y-0.1, y+0.1,
#                              z-0.1, z+0.1)
#
#
#picker = figure.on_mouse_pick(picker_callback)
#picker.tolerance = 0.01
#
#
#mlab.show()