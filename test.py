import utils
import numpy as np
import hexy as hx

start1 = hx.axial_to_cube(utils.offset_to_axial(np.array([[0,6]])))
start2 = hx.axial_to_cube(utils.offset_to_axial(np.array([[2,2]])))

end1 = hx.axial_to_cube(utils.offset_to_axial(np.array([[6,6]])))
end2 = hx.axial_to_cube(utils.offset_to_axial(np.array([[5,2]])))

dist1  = utils.distance_wraparound(start1, end1, (6,6))
dist2 = utils.distance_wraparound(start2, end2, (6,6))

print(f"{dist1}, {dist2}")