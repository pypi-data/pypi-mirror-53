import numpy as np
import cv2
import imutils
import os
from sklearn.utils import shuffle

class GeneratorImage():
    def __init__(self, batch_sizes=4, color_modes='rgb', image_sizes=(512,512,3), rotation_degrees=None, flip_image_horizontal_status=False, flip_image_vertical_status=False, zoom_scales=None):
        """[summary]
        
        Arguments:
            batch_sizes {[type]} -- [description]
        
        Keyword Arguments:
            color_modes {str} -- [description] (default: {'rgb'})
            image_sizes {tuple} -- [description] (default: {(512,512,3)})
            rotation_degrees {[type]} -- [description] (default: {None})
            flip_image_horizontal_status {bool} -- [description] (default: {False})
            flip_image_vertical_status {bool} -- [description] (default: {False})
            zoom_scales {[type]} -- [description] (default: {None})
        """
        self.batch_size = batch_sizes
        self.color_mode = color_modes
        self.image_size = image_sizes
        self.rotation_degree = rotation_degrees
        self.flip_image_horizontal_status = flip_image_horizontal_status
        self.flip_image_vertical_status = flip_image_vertical_status
        self.zoom_scale = zoom_scales 

    def batch_generator(self, list_path_data, list_target_data):
        """[summary]
        
        Arguments:
            list_path_data {[type]} -- [description]
            list_target_data {[type]} -- [description]
        """
        counter_image = 0
        number_class = np.amax(list_target_data)
        while True:
            image_data_batch = []
            image_target_batch = []
            for i in range(self.batch_size):
                try:
                    number_augmentation = 1
                    image_file = list_path_data[counter_image]
                    if self.color_mode == 'grayscale':
                        image = cv2.imread(image_file,0)
                    else:
                        image = cv2.imread(image_file)
                    image = cv2.resize(image, (self.image_size[0], self.image_size[1]))
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = image.astype(np.float32)
                    image = image/255.0

                    image_data_batch.append(image)
                    #image_target_batch.append(list_target_data[counter_image])
                    if self.rotation_degree!=None:
                        number_rotation = int(360/self.rotation_degree)
                        for j in range(number_rotation):
                            radian_rotation = self.rotation_degree
                            image_rotation = self.rotate_image(image, radian_rotation)
                            radian_rotation += self.rotation_degree
                            image_data_batch.append(image_rotation)
                            #image_target_batch.append(list_target_data[counter_image])
                            number_augmentation += 1
                    
                    if self.flip_image_horizontal_status==True:
                        image_flip = self.flip_image_horizontal(image)
                        image_data_batch.append(image_flip)
                        #image_target_batch.append(list_target_data[counter_image])
                        number_augmentation += 1

                    if self.flip_image_vertical_status==True:
                        image_flip = self.flip_image_vertical(image)
                        image_data_batch.append(image_flip)
                        #image_target_batch.append(list_target_data[counter_image])
                        number_augmentation += 1

                    if self.zoom_scale!=None:
                        image_zoom = self.zoom_image(image,self.zoom_scale)
                        image_data_batch.append(image_zoom)
                        #image_target_batch.append(list_target_data[counter_image])
                        number_augmentation += 1
                    
                    for i in range(0,number_augmentation):
                        tmp_target_batch = np.zeros(number_class+1).astype(np.float32)
                        tmp_target_batch[list_target_data[counter_image]-1] = 1
                        image_target_batch.append(tmp_target_batch)
                    
                    counter_image+=1
                    if counter_image >= len(list_path_data):
                        counter_image = 0
                except:
                    print("Failed to open "+str(list_path_data[counter_image]))

            image_data_batch = np.array(image_data_batch)            
            image_data_batch = image_data_batch.reshape((self.batch_size*number_augmentation,self.image_size[0],self.image_size[1],self.image_size[2])).astype(np.float32)
            image_target_batch = np.array(image_target_batch)            
            
            yield(image_data_batch,image_target_batch)

    def generate_from_directory_manual(self, directory):
        """[summary]
        
        Arguments:
            directory {[type]} -- [description]
        """
        list_path_image , list_target_image = self.get_list_image_and_label(path_dataset = directory)
        list_path_image , list_target_image = shuffle(list_path_image, list_target_image, random_state=0)
        return self.batch_generator(list_path_data=list_path_image, list_target_data=list_target_image) , self.get_num_data(list_path_image)

    def generate_from_directory_auto(self, directory, val_ratio=0.2):
        """[summary]
        
        Arguments:
            directory {[type]} -- [description]
        """
        list_path_image , list_target_image = self.get_list_image_and_label(path_dataset = directory)
        list_path_image , list_target_image = shuffle(list_path_image, list_target_image, random_state=0)
        split_size = 1 - val_ratio
        train_data, train_target, val_data, val_target = self.split_dataset(list_path_data=list_path_image, list_target_data=list_target_image, split_sizes=split_size)        
        train_generator = self.batch_generator(list_path_data=train_data, list_target_data=train_target)
        val_generator = self.batch_generator(list_path_data=val_data, list_target_data=val_target)
        num_train_data = self.get_num_data(train_data)
        num_val_data = self.get_num_data(val_data) 
        return train_generator , val_generator , num_train_data , num_val_data
    
    def get_num_data(self, list_path_data):
        """[summary]
        
        Arguments:
            list_path_data {[type]} -- [description]
        """
        return len(list_path_data)
        
    def flip_image_horizontal(self, image):
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
        """
        return cv2.flip(image,0)

    def flip_image_vertical(self, image):
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
        """
        return cv2.flip(image,1)
    
    def flip_image_both(self, image):
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
        """
        return cv2.flip(image, -1)
    
    def get_list_image_and_label(self, path_dataset):
        """[summary]
        
        Arguments:
            path_dataset {[type]} -- [description]
        """
        dataset_path = os.path.join(os.getcwd(), path_dataset)
        list_dir_name = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path,d))]
        list_dir_name.sort()
        list_path_file = []
        list_target_dataset = []
        for i in range(0,len(list_dir_name)):
            full_path_dir = os.path.join(dataset_path,list_dir_name[i])
            file_names = os.listdir(full_path_dir)
            for path_file in file_names:
                list_path_file.append(os.path.join(full_path_dir,path_file))
                list_target_dataset.append(i)
        list_path_dataset = np.array(list_path_file)
        list_target_dataset = np.array(list_target_dataset)
        list_target_dataset = np.reshape(list_target_dataset,len(list_path_dataset))
        return list_path_dataset, list_target_dataset

    def rotate_image(self, image, rotation_degrees=90):
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
        
        Keyword Arguments:
            rotation_degrees {int} -- [description] (default: {90})
        """
        return imutils.rotate(image, rotation_degrees)

    def split_dataset(self, list_path_data, list_target_data, split_sizes=0.8):
        """[summary]
        
        Arguments:
            list_path_data {[type]} -- [description]
            list_target_data {[type]} -- [description]
        
        Keyword Arguments:
            split_sizes {float} -- [description] (default: {0.8})
        """
        limit = int(len(list_path_data) * split_sizes) + 1
        train_list_path_data = list_path_data[:limit]
        val_list_path_data = list_path_data[limit:]
        train_list_target_data = list_target_data[:limit]
        val_list_target_data = list_target_data[limit:]
        return train_list_path_data, train_list_target_data, val_list_path_data, val_list_target_data

    def zoom_image(self, image, zoom_scales=0.3):
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
        
        Keyword Arguments:
            zoom_scales {float} -- [description] (default: {0.3})
        """
        height, width, channels = image.shape
        center_x,center_y=int(height/2),int(width/2)
        radius_x,radius_y= int(zoom_scales*height/100),int(zoom_scales*width/100)
        min_x,max_x=center_x-radius_x,center_x+radius_x
        min_y,max_y=center_y-radius_y,center_y+radius_y
        cropped = image[min_x:max_x, min_y:max_y]
        resized_cropped = cv2.resize(cropped, (width, height))
        return resized_cropped