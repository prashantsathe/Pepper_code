import os
import glob
import numpy as np
import cv2
from sklearn.utils import shuffle


def load_train(train_path, image_size):
    images = []
    x = []
    y = []
    theta = []

    #files = glob.glob(train_path+'*')
    files  = os.listdir(train_path)
    for fl in files:
        print ("hello "+fl)
        image = cv2.imread(train_path+fl)
        image = cv2.resize(image, (image_size, image_size), cv2.INTER_LINEAR)
        images.append(image)
        param = fl.split('_')
        #print ("param", param)
        x.append(param[1])
        y.append(param[2])
        theta.append(param[3][:-5])


    images = np.array(images)
    print (images.shape)
    x = np.array(x)
    y = np.array(y)
    theta = np.array(theta)
    
    return images, x, y, theta


def load_test(test_path, image_size):
    path = test_path
    files = sorted(glob.glob(path+'/*'))
    image_test = []
    x_test = []
    y_test = []
    theta_test = []
    print("Reading test images")
    for fl in files:
        #print (fl)
        param = os.path.basename(fl).split('_')

        #print "hello"+flbase
        img = cv2.imread(fl)
        img = cv2.resize(img, (image_size, image_size), cv2.INTER_LINEAR)
        image_test.append(img)
        x_test.append(param[1])
        y_test.append(param[2])
        theta_test.append(param[3][:-5])

    
    ### because we're not creating a DataSet object for the test images,normalization happens here
    image_test = np.array(image_test, dtype=np.uint8)
    image_test = image_test.astype('float32')
    image_test = image_test / 255
    print (image_test.shape)
    return image_test, x_test, y_test, theta_test



class DataSet(object):

  def __init__(self, images, x, y, theta):
    """Construct a DataSet. one_hot arg is used only if fake_data is true."""

    self._num_examples = images.shape[0]


    # Convert shape from [num examples, rows, columns, depth]
    # to [num examples, rows*columns] (assuming depth == 1)
    # Convert from [0, 255] -> [0.0, 1.0].

    images = images.astype(np.float32)
    images = np.multiply(images, 1.0 / 255.0)

    self._images = images
    self._x = x
    self._y = y
    self._theta = theta
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def theta(self):
    return self._theta

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size

    if self._index_in_epoch > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1

      # # Shuffle the data (maybe)
      # perm = np.arange(self._num_examples)
      # np.random.shuffle(perm)
      # self._images = self._images[perm]
      # self._labels = self._labels[perm]
      # Start next epoch

      start = 0
      self._index_in_epoch = batch_size
      #print(batch_size, self._num_examples)
      assert batch_size <= self._num_examples
    end = self._index_in_epoch

    return self._images[start:end], self._x[start:end], self._y[start:end], self._theta[start:end]


def read_train_sets(train_path, image_size, validation_size=0):
  class DataSets(object):
    pass
  data_sets = DataSets()

  images, x, y, theta = load_train(train_path, image_size)
  images, x, y, theta = shuffle(images, x, y, theta)  # shuffle the data

  if isinstance(validation_size, float):
    validation_size = int(validation_size * images.shape[0])

  validation_images = images[:validation_size]
  validation_x = x[:validation_size]
  validation_y = y[:validation_size]
  validation_theta = theta[:validation_size]

  train_images = images[validation_size:]
  train_labels = x[validation_size:]
  train_ids = y[validation_size:]
  train_cls = theta[validation_size:]

  data_sets.train = DataSet(train_images, train_labels, train_ids, train_cls)
  data_sets.valid = DataSet(validation_images, validation_x, validation_y, validation_theta)

  return data_sets


def read_test_set(test_path, image_size):
  images, x, y, theta  = load_test(test_path, image_size)
  return images, x, y, theta
