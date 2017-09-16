import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def add_layer(inputs, in_size, out_size, activeation_funtion=None):
    with tf.name_scope('layer'):
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='Weight')
        with tf.name_scope('biase'):
            biases  = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='biase')
        Wx_plus_b = tf.matmul(inputs, Weights) + biases
        if activeation_funtion is None:
            outputs = Wx_plus_b
        else:
            outputs = activeation_funtion(Wx_plus_b)
        return outputs

x_data = np.linspace(-1,1,300)[:, np.newaxis]
noise  = np.random.normal(0,0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32, [None, 1], name='x_input')
    ys = tf.placeholder(tf.float32, [None, 1], name='y_input')

l1 = add_layer(xs,1,10,activeation_funtion=tf.nn.relu)
prediction = add_layer(l1, 10, 1, activeation_funtion=None)

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]), name='loss')
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
init = tf.global_variables_initializer()
sess = tf.Session()
writer=tf.summary.FileWriter("logs/", sess.graph)
sess.run(init)

#fig = plt.figure()
#ax  = fig.add_subplot(1,1,1)
#ax.scatter(x_data, y_data)
#plt.ion()
#plt.show(block=False)
#
#for i in range(1000):
#    sess.run(train_step, feed_dict={xs:x_data, ys:y_data})
#    if i % 50 == 0:
##        print(sess.run(loss, feed_dict={xs:x_data, ys:y_data}))
#        try:
#            ax.lines.remove(lines[0])
#        except Exception:
#            pass
#        prediction_value = sess.run(prediction, feed_dict={xs:x_data})
#        lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
#        plt.pause(1)
#
