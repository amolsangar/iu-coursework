#!/usr/local/bin/python3
#
# Authors: [Amol Dattatray Sangar (asangar)]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021

# Reference - https://github.com/Invictus17/FindTheHorizon 
# Referred above link for implementation of Viterbi algorithm

from PIL import Image
from numpy import *
import numpy as np
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image                                                                                                                                      
def calc_edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

#  draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels

def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)


# main program
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = calc_edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # ========================================================================
    def generate_emission_matrix(edge_strength):
        edge_strength.dtype = float64
        edge_strength_col_sum = edge_strength.sum(axis=0)
        edge_strength_normalized = edge_strength / edge_strength_col_sum

        return edge_strength_normalized
    

    # ========================================================================
    # Part 1 - Simple Bayes Net

    # Calculating emissions
    edge_strength_normalized = generate_emission_matrix(edge_strength)
    airice_simple = argmax(edge_strength_normalized, axis=0)
    
    counts = np.bincount(airice_simple)
    max_airiceSimple_rowIndex = np.argmax(counts)
    icerock_simple = argmax(edge_strength_normalized[max_airiceSimple_rowIndex + 15:], axis=0)

    for i in range(0,len(icerock_simple)):
        icerock_simple[i] = icerock_simple[i] + max_airiceSimple_rowIndex + 15

    new_image = draw_boundary(input_image, airice_simple, (255, 255, 0), 3)
    new_image = draw_boundary(new_image, icerock_simple, (255, 255, 0), 3)
    imageio.imwrite("output_simple.jpg", new_image)
    

    # ========================================================================
    # Part 2 - HMM with Viterbi Algorithm

    rows, columns = edge_strength.shape

    def trans_prob_per_cell(fixed_row,fixed_column,viterbi,row_threshold):
        trans_prob = []

        for row in range(rows):
            if abs(fixed_row - row) < 8 and fixed_row > row_threshold:
                trans_prob.append(0.5 * viterbi[row][fixed_column - 1])
            else:
                trans_prob.append(0.001 * viterbi[row][fixed_column - 1])
        
        return trans_prob

    def viterbi_algo(edge_strength, row_threshold=-1):
        emission_prob_matrix = generate_emission_matrix(edge_strength)

        viterbi = emission_prob_matrix * 100    # To make sure that points don't end up with zero after multiplication
        trans_prob_matrix = []

        for column in range(1, columns):
            max_trans_prob_index = []

            for row1 in range(rows):
                trans_prob = trans_prob_per_cell(row1,column,viterbi,row_threshold)
                
                viterbi[row1][column] = viterbi[row1][column] * max(trans_prob)    # emission * max(transition prob)
                max_trans_prob_index.append(trans_prob.index(max(trans_prob)))
                
            trans_prob_matrix.append(max_trans_prob_index)     # Shape - 224 * 175
        
        viterbi_lastCol_index = argmax(viterbi[:, -1], axis=0)
        next_index = viterbi_lastCol_index
        
        trans_prob_matrix = np.array(trans_prob_matrix).T.tolist()    # Shape - 175 * 224

        # Backtracking from end using maximum index
        edge_index = [viterbi_lastCol_index]
        for i in range(columns - 2, -1, -1):
            edge_index.append(trans_prob_matrix[next_index][i])
            next_index = trans_prob_matrix[next_index][i]

        # Reverse the list formed
        edge_index = edge_index[::-1]
        
        return edge_index

    # Calculate UPPER line trace    
    input_image = Image.open(input_filename).convert('RGB')
    edge_strength = calc_edge_strength(input_image)
    airice_hmm = viterbi_algo(edge_strength, -1)
    
    # Draw UPPER edge
    input_image = Image.open(input_filename).convert('RGB')
    new_image = draw_boundary(input_image, airice_hmm, (0, 0, 255), 3)

    # Get the most frequent occuring edge/line pixel row index
    counts = np.bincount(airice_hmm)
    max_airiceHMM_rowIndex = np.argmax(counts)
    
    # Calculate LOWER line trace
    icerock_hmm = viterbi_algo(edge_strength, max_airiceHMM_rowIndex + 12)
    
    # Draw LOWER edge
    new_image = draw_boundary(new_image, icerock_hmm, (0, 0, 255), 3)
    imageio.imwrite("output_hmm.jpg", new_image)


    # ========================================================================
    # Part 3 - HUMAN FEEDBACK
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    input_image = Image.open(input_filename).convert('RGB')
    edge_strength = calc_edge_strength(input_image)

    # Change edge strength values for feedback point
    # Calculate UPPER line trace 
    edge_strength[ : , gt_airice[0] ] = 0
    edge_strength[ gt_airice[1], gt_airice[0] ] = 1
    airice_feedback = viterbi_algo(edge_strength, -1)
    
    # Draw UPPER edge
    input_image = Image.open(input_filename).convert('RGB')
    new_image = draw_boundary(input_image, airice_feedback, (255, 0, 0), 3)
    new_image = draw_asterisk(new_image, gt_airice, (255, 255, 255), 2)
    
    # Get the most frequent occuring edge/line pixel row index
    counts = np.bincount(airice_feedback)
    max_airiceFeedback_rowIndex = np.argmax(counts)

    # Recalculate edge strength on original image
    input_image = Image.open(input_filename).convert('RGB')
    edge_strength_2 = calc_edge_strength(input_image)

    # Calculate LOWER line trace
    edge_strength_2[ : , gt_icerock[0] ] = 0
    edge_strength_2[ gt_icerock[1] , gt_icerock[0] ] = 1
    icerock_feedback = viterbi_algo(edge_strength_2, max_airiceFeedback_rowIndex + 12)
    
    # Draw LOWER edge
    new_image = draw_boundary(new_image, icerock_feedback, (255, 0, 0), 3)
    new_image = draw_asterisk(new_image, gt_icerock, (255, 255, 255), 2)
    imageio.imwrite("output_feedback.jpg", new_image)
    

    # ========================================================================
    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    input_image = Image.open(input_filename).convert('RGB')
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")


    # ========================================================================
    # Test Commands
    # python polar.py test_images\09.png 80 20 60 60
    # python polar.py test_images\30.png 80 20 104 59
    # python polar.py test_images\31.png 80 20 108 60
    # python polar.py test_images\16.png 80 20 30 37
    # python polar.py test_images\23.png 80 33 117 82