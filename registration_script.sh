#!/bin/bash

# Path to ANTs binaries
ANTSPATH="/usr/local/ants/bin/"

# Image dimensionality
DIM=3

# Number of threads for multi-threading
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# Input file names for fixed and moving images in HDF5 format
FIXED_IMAGE_HDF5="Flow1.h5"
MOVING_IMAGE_HDF5="Flow2.h5"
OUTPUT_LABEL="output_label"

# Convert HDF5 files to NIfTI
${ANTSPATH}antsH5ToImage 3 /Data/MAG $MOVING_IMAGE_HDF5 MOVING_IMAGE.nii.gz
${ANTSPATH}antsH5ToImage 3 /Data/MAG $FIXED_IMAGE_HDF5 FIXED_IMAGE.nii.gz

# Perform image registration
$ANTSPATHantsRegistration -d $DIM \
    -m MI[FIXED_IMAGE.nii.gz,MOVING_IMAGE.nii.gz,1,32,regular,0.05] \
    -t translation[0.1] \
    -c [10000x111110x11110,1.e-8,20] \
    -s 0x0x0vox \
    -f 4x2x1 -l 1 \
    -o [output_prefix,output_diff.nii.gz,output_inv.nii.gz]

# Apply transformation to moving image
${ANTSPATH}antsApplyTransforms -d $DIM \
    -i MOVING_IMAGE.nii.gz \
    -r FIXED_IMAGE.nii.gz \
    -n linear \
    -t output_prefix0GenericAffine.mat \
    -o def.mha
