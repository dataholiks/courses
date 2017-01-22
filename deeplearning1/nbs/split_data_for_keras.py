import glob
import os
import numpy as np
import zipfile

# Global control params
DOWNLOAD_PATH = "data/statefarm/"
VALIDATION_PERCENT = 0.15
NUM_SAMPLE_FILES = 10

# Input =  kaggle image zip file 'imgs.zip'
# Everytime we start fresh from unzipping. 
# WARNING: First removes train/ and test/ if they already exist.
IMAGE_ZIP = DOWNLOAD_PATH+'imgs.zip'

# output:
#Following new files will be created after splitting
#for each cx in [c0,c1,c2.....cn]
#data/statefarm/valid/cx/   (15% random images from train/cx/ are moved here)
#data/statefarm/sample/train/cx/ (10 random images from ../train/cx are *copied* here)
#data/statefarm/sample/valid/cx/  (10 random images from ../valid/cx are *copied* here)
#data/statefarm/sample/test/   (10 random images from ../test are *copied* here)


def clean_directory(directory):
    if not os.path.exists(directory):
        os.system('mkdir {}'.format(directory))
    else:
        os.system('rm -rf {}*'.format(directory))

def create_class_x_valid_from_training(training_class_path):
    training_class_files = glob.glob(training_class_path+'/*')
    
    num_training_files = len(training_class_files)
    num_valid_files = np.floor(VALIDATION_PERCENT*num_training_files)
    
    files_idxs_to_move = np.random.randint(0, num_training_files, num_valid_files)
    
    for training_idx in files_idxs_to_move:
        training_file = training_class_files[training_idx]
        valid_file = training_file.replace('train','valid')
        os.system('mv -f ' + training_file + ' ' + valid_file)

def create_class_x_sample(class_path, sub_type):
    class_files = glob.glob(class_path+'/*')
    num_files = len(class_files)
    files_idxs_to_move = np.random.randint(0, num_files, NUM_SAMPLE_FILES)
    for idx in files_idxs_to_move:
        source_file = class_files[idx]
        dest_file = source_file.replace(sub_type, 'sample/' + sub_type)
        os.system('cp -f ' + source_file + ' ' + dest_file)

def main():
    # These will be created by unzipping
    # These usually doesn't require changes.
    train_dir = DOWNLOAD_PATH + 'train/'
    test_dir = DOWNLOAD_PATH + 'test/'

    # keras requires a direc to read images. create dummy for test files.
    test_unknown_dir = test_dir + 'unknown/'

    # Following are for validation and "small sample testing" 
    val_dir = DOWNLOAD_PATH + 'valid/'
    sample_dir = DOWNLOAD_PATH + 'sample/'
    sample_train_dir = sample_dir + 'train/'
    sample_valid_dir = sample_dir + 'valid/'
    sample_test_dir = sample_dir + 'test/'
    sample_test_unknown_dir = sample_test_dir + 'unknown/'
    directories_to_create = [val_dir, sample_dir, sample_train_dir, sample_valid_dir, sample_test_dir,
                             sample_test_unknown_dir]

    # Input =  kaggle image zip file 'imgs.zip'
    # Everytime this cell is run, we start fresh from unzipping. 
    # First remove train and test if they exist.
    print('Removing any existing train/ and test/ directories')
    os.system('rm -f -r ' + train_dir)
    os.system('rm -f -r ' + test_dir)

    print('Unzipping image files ...')
    # Extract images from zip file
    with zipfile.ZipFile(IMAGE_ZIP, "r") as zip_ref:
        zip_ref.extractall(DOWNLOAD_PATH)

    # Read class labels
    training_class_paths = glob.glob(train_dir + '*')
    class_labels = [x.split('/')[-1] for x in training_class_paths]
    # Create/Clean directories

    print('Creating or cleaning all necessary directories')
    # Create directories from top level to bottom
    for directory in directories_to_create:
        clean_directory(directory)

    # Create a directory for each class label in valid/ , sample/train/ sample/valid
    for label in class_labels:
        valid_cx = val_dir + label + '/'
        sample_train_cx = sample_train_dir + label + '/'
        sample_valid_cx = sample_valid_dir + label + '/'
        
        clean_directory(valid_cx)
        clean_directory(sample_train_cx)
        clean_directory(sample_valid_cx)

    # Move test files to under 'unknown' directory
    # There are 80K test files. Too slow to move one at a time. 
    # first move test/ to unknown/ 
    # then recreate empty test/
    # move unknown into test/
    temp_unknown = [x + '/' for x in test_dir.split('/')[0:-2]]
    temp_unknown = ''.join(temp_unknown)+'unknown'
    os.system('mv {} {}'.format(test_dir, temp_unkown))
    os.system('mkdir {}'.format(test_dir))
    os.system('mv {} {}'.format(temp_unkown, test_dir))

    print('Moving files ...')
    # Move a fraction of training files to valid direc. 
    # replicate a fraction of train/ and valid/ test/ file structure under sample/
    for training_class_path in training_class_paths:
        
        valid_class_path = training_class_path.replace('train','valid')
        
        create_class_x_valid_from_training(training_class_path)
        
        # for this class, move from train/cx to sample/train/cx .
        # from valid/cx to sample/valid/cx.
        create_class_x_sample(training_class_path, 'train')
        create_class_x_sample(valid_class_path, 'valid')

    # Move some images to sample/test
    create_class_x_sample(test_unknown_dir, 'test')
    # Done restructuring the data.

if __name__ == '__main__':
    main()

