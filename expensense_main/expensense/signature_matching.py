"""
The below code is the combination of two code bases taken from
https://github.com/ahmetozlu/signature_extractor
https://github.com/omrawal/Signature-Matching/blob/main/signature.py

"""

import cv2
import numpy as np
from skimage import measure, morphology
from skimage.measure import regionprops
from skimage.metrics import structural_similarity as ssim
import os

def calculate_similarity(receipt_path, signature_path):
    """ 
    Method to calculate the signature similarity between receipt submitted and
    signature stored of the employee
    """

    # Read the input receipt image
    receipt_img = cv2.imread(receipt_path, 0)
    receipt_img = cv2.threshold(receipt_img, 127, 255, cv2.THRESH_BINARY)[1]  # Ensure binary
    
    # Connected component analysis by scikit-learn framework
    blobs = receipt_img > receipt_img.mean()
    blobs_labels = measure.label(blobs, background=1)
    
    the_biggest_component = 0
    total_area = 0
    counter = 0
    for region in regionprops(blobs_labels):
        if region.area > 10:
            total_area += region.area
            counter += 1
        if region.area >= 250:
            if region.area > the_biggest_component:
                the_biggest_component = region.area
    
    # the parameters are used to remove small size connected pixels outliar 
    constant_parameter_1 = 8
    constant_parameter_2 = 25
    constant_parameter_3 = 10

    # the parameter is used to remove big size connected pixels outliar
    constant_parameter_4 = 9

    # experimental-based ratio calculation
    # a4_small_size_outliar_constant is used as a threshold value to remove connected outliar connected pixels

    average = total_area / counter
    a4_small_size_outliar_constant = ((average / constant_parameter_1) * constant_parameter_2) + constant_parameter_3
    
    # experimental-based ratio calculation, modify it for your cases
    # a4_big_size_outliar_constant is used as a threshold value to remove outliar connected pixels
    a4_big_size_outliar_constant = a4_small_size_outliar_constant * constant_parameter_4
    
    # remove the connected pixels are smaller than a4_small_size_outliar_constant
    pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
    component_sizes = np.bincount(pre_version.ravel())
    too_small = component_sizes > a4_big_size_outliar_constant
    too_small_mask = too_small[pre_version]
    pre_version[too_small_mask] = 0
    cv2.imwrite('pre_version.png', pre_version)
    
    # Read the pre-version
    pre_version_img = cv2.imread('pre_version.png', 0)
    pre_version_img = cv2.threshold(pre_version_img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imwrite("output.png", pre_version_img)
    
    # Read the signature image
    signature_img = cv2.imread(signature_path)
    signature_img = cv2.cvtColor(signature_img, cv2.COLOR_BGR2GRAY)
    signature_img = cv2.resize(signature_img, (300, 300))
    
    # Read the pre-processed receipt image
    processed_receipt_img = cv2.imread('output.png')
    # processed_receipt_img = cv2.imread(receipt_path)
    processed_receipt_img = cv2.cvtColor(processed_receipt_img, cv2.COLOR_BGR2GRAY)
    processed_receipt_img = cv2.resize(processed_receipt_img, (300, 300))
    
    # show images for debugging
    # cv2.imshow('Signature Image', signature_img)
    # cv2.imshow('Receipt Image', receipt_img)
    # cv2.imshow('Processed Receipt Image', processed_receipt_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Run structural similarity algorithm to find to similarity value
    similarity_value = ssim(signature_img, processed_receipt_img) * 100
    # Clean up by deleting the temporary files
    if os.path.exists('pre_version.png'):
        os.remove('pre_version.png')
    if os.path.exists('output.png'):
        os.remove('output.png')

    return similarity_value

# Debug
# if __name__ == '__main__':
#     receipt_path = '../media/signature_test/signature_receipt_3.png'
#     signature_path = '../media/signatures/Company1/Team1/Test1Employee2/signature.jpg'

#     similarity_index = calculate_similarity(receipt_path, signature_path)
#     print('Similarity Index:', similarity_index)
