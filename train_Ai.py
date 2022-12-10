from prepare_data import *
from sklearn.model_selection import train_test_split as tts
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from nets.MLP import mlp
from nets.conv import conv
from random import randint

# define some constants
N_FRUITS = 29
FRUITS ={0: 'anvil', 1: 'apple', 2: 'axe', 3: 'banana', 4: 'bed', 5: 'bicycle', 6: 'bird', 7: 'birthday cake', 8: 'book', 9: 'cactus', 10: 'cake', 11: 'camel', 12: 'camera', 13: 'donut', 14: 'giraffe', 15: 'guitar', 16: 'jail', 17: 'motorbike', 18: 'mouse', 19: 'mug', 20: 'mushroom', 21: 'pineapple', 22: 'pizza', 23: 'scorpion', 24: 'snowman', 25: 'The Eiffel Tower', 26: 'The Mona Lisa', 27: 'tree', 28: 'whale'} 

# number of samples to take in each class
N = 3000

# some other constants
N_EPOCHS = 50

# data files in the same order as defined in FRUITS
files =['anvil.npy', 'apple.npy', 'axe.npy', 'banana.npy', 'bed.npy', 'bicycle.npy', 'bird.npy', 'birthday cake.npy', 'book.npy', 'cactus.npy', 'cake.npy', 'camel.npy', 'camera.npy', 'donut.npy', 'giraffe.npy', 'guitar.npy', 'jail.npy', 'motorbike.npy', 'mouse.npy', 'mug.npy', 'mushroom.npy', 'pineapple.npy', 'pizza.npy', 'scorpion.npy', 'snowman.npy', 'The Eiffel Tower.npy', 'The Mona Lisa.npy', 'tree.npy', 'whale.npy']



# images need to be 28x28 for training with a ConvNet
fruits = load("data/", files, reshaped=True)
# images need to be flattened for training with an MLP
# fruits = load("data/", files, reshaped=False)


# limit no of samples in each class to N
fruits = set_limit(fruits, N)
# normalize the values
fruits = map(normalize, fruits)

# define the labels
labels = make_labels(N_FRUITS, N)


# prepare the data
x_train, x_test, y_train, y_test =tts(list(fruits), labels, test_size=0.05)
Y_train = np_utils.to_categorical(y_train, N_FRUITS)
Y_test = np_utils.to_categorical(y_test, N_FRUITS)

############################start train########################
# one hot encoding

# use our custom designed ConvNet model

# model = conv(classes=N_FRUITS, input_shape=(28, 28, 1))

# # use our custom designed MLP model
# # model = mlp(classes=N_FRUITS)


# model.compile(loss='categorical_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])

# input("Type 'train' to start training: ")
# print ("Training commenced")

# model.fit(np.array(x_train), np.array(Y_train), batch_size=32, epochs=N_EPOCHS, verbose=1)  # type: ignore

# print ("Training complete")

# print ("Evaluating model")
# preds = model.predict(np.array(x_test))

# score = 0
# for i in range(len(preds)):
#     if np.argmax(preds[i]) == y_test[i]:
#         score += 1

# print ("Accuracy: ", ((score + 0.0) / len(preds)) * 100)

# name = input(">Enter name to save trained model: ")
# model.save(name + ".h5")
# print ("Model saved")

############end train#########################

model = load_model(f"./models/last_model.h5")

def visualize_and_predict():
    "selects a random test case and shows the object, the prediction and the expected result"
    # img = Image.open('samples/apple_3.png')
    # img = img.convert("L")
    # img = img.resize((28,28))
    # img = np.expand_dims(img, axis=0)
    # img = np.reshape(img, (28, 28, 1))
    # # invert the colors
    # img = np.invert(img)
    # # brighten the image by 60%
    # for i in range(len(img)):
    #     for j in range(len(img)):
    #         if img[i][j] > 50:
    #             img[i][j] = min(255, img[i][j] + img[i][j] * 0.60)
    # img = normalize(img)
    # val = model.predict(np.array([img]))
    # pred = FRUITS[np.argmax(val)]
    # print (pred)

    # # print(FRUITS[y_test[n]])
    n = randint(0, len(x_test))
    print(len(x_test))
    visualize(denormalize(np.reshape(x_test[n], (28, 28))))
    predict = model.predict(np.array([x_test[n]]))# type: ignore
    print(np.argmax(predict))
    pred = FRUITS[np.argmax(predict)]# type: ignore
    actual = FRUITS[y_test[n]]
    print ("Actual:", actual)
    print ("Predicted:", pred)
    visualize(denormalize(np.reshape(x_test[n], (28, 28))))


print ("Testing mode")
visualize_and_predict()
