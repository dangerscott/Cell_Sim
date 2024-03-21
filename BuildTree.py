from scipy.spatial import cKDTree

import numpy as np

from ScreenInfo import screen_w, screen_h


# Build the cKD tree
def build_ckd(list):
    positions = [object.position for object in list]
    kdtree = cKDTree(positions)
    return kdtree, list

# Function to find the nearest cell to a query point
def find_nearest_cell(kdtree, cell_list, query_point):
    # Query the existing cKD tree to find the nearest neighbor
    distance, index = kdtree.query(query_point)
    
    # Get the position of the query point
    query_position = cell_list[index].position
    
    # Filter out the query point from the list of cells
    filtered_cells = [cell for cell in cell_list if cell.position != query_position]
    
    # Find the nearest neighbor to the query point among the filtered cells
    filtered_positions = [cell.position for cell in filtered_cells]
    filtered_kdtree = cKDTree(filtered_positions)
    distance, index = filtered_kdtree.query(query_point)
    nearest_cell = filtered_cells[index]
    
    return nearest_cell
