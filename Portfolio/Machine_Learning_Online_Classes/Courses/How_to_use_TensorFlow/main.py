##################################################################
#Description:
#      Neural network that tells you if a house is a good buy
#      from Siraj Raval 
#      Raval's github: https://github.com/llSourcell/How_to_use_Tensorflow_for_classification-LIVE
#
# Author: Jean-Simon Marrocco
# Date: 02-12-2017
##################################################################
# coding: utf-8

# In[2]:


import pandas as pd # work with data as tables
import numpy as np # use number matrices
import matplotlib.pyplot as plt
import tensorflow as tf


# In[5]:


#step 1 load data
dataframe = pd.read_csv('data.csv') #dataframe
#removd the feature we dont care about
dataframe = dataframe.drop(['index','price', 'sq_price'], axis =1)
#we only use the first 10 rows
dataframe = dataframe[0:10]
dataframe


# In[8]:


#step 2 - add labels
# 1 is good buy and 0 os bad buy
dataframe.loc[:, ('y1')] = [1,1,1,0,0,1,0,1,1,1]
#y2 is a negation of y1, opposite
dataframe.loc[:, ('y2')] = dataframe['y1'] == 0
#turn TRUE/FALSE values to 1 and 0
dataframe.loc[:, ('y2')] = dataframe['y2'].astype(int)
dataframe


# In[16]:


#Step3 - prepare data for tensorflow
#tensor are a generic version of vectors and matrices
#vector - is a list of numbers
#matrix - is a list of list of numbers (2D tensor)
#list of list of list of numbers (3D Tensor)
#...

#convert features to input tensor
inputX = dataframe.loc[:, ['area', 'bathrooms']].as_matrix()
#convert labels to input tensor
inputY = dataframe.loc[:,['y1', 'y2']].as_matrix()


# In[19]:


#step4 - write out our hyperparameters
learning_rate = 0.000001
training_epochs = 2000

display_step = 50
n_samples = inputY.size


# In[47]:


#Step 5 - creat our computation graph/neural network
#for feature input tensors, none means any numbers of examples
#placeholers are gateways for data into our compulations graph
x = tf.placeholder(tf.float32, [None,2])

#creat weighs
#2x2 float matrix, that we'll keep updating through the training process
#variables in tf hold and update parameters
#in memory buffers containing tensors
w = tf.Variable(tf.zeros([2,2]))

#add biases (ex: is b in y = mx + b is the bias, like that)
b = tf.Variable(tf.zeros([2]))

#multply our weights by our inputs, first calculation
#weights are how we govern how data flows in our neural net
#multiply input by weights and add biases
y_values =tf.add(tf.matmul(x,w), b)

#apply osftmax to values we just created (solfmax =sigmoid)
#sofmax is our activation function
y = tf.nn.softmax(y_values)

#feed in a matrix of lables
y_ = tf.placeholder(tf.float32, [None, 2] )


# In[48]:


#Step6 - perform training

#creat our cost function, mean squared error
#reduce sum computes the sum of element across dimensions of tensor
cost = tf.reduce_sum(tf.pow(y_ - y, 2))/(2*n_samples)

#Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

#init variables and tensorflow session
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)


# In[54]:


#training loop
for i in range(training_epochs):
    sess.run(optimizer, feed_dict={x: inputX, y_: inputY})
    
    #write out logs of training
    if (i) % display_step == 0:
        cc = sess.run(cost, feed_dict={x: inputX, y_:inputY})
        print('training step:', '%04d' % (i), "cost=", '{:.9f}'.format(cc))
        
print("Optimization Finished!")
training_cost = sess.run(cost, feed_dict={x: inputX, y_: inputY})
print("Training cost=", training_cost, "w=", sess.run(w), "b=", sess.run(b), '\n') 


# In[57]:


sess.run(y, feed_dict={x:inputX})


# In[ ]:


#its saying all house are a good buy! but only 7/10 are really
#solution : add extrat layer

