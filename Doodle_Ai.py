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

conv = load_model("./models/last_model.h5")
DOODLES ={0: 'anvil', 1: 'apple', 2: 'axe', 3: 'banana', 4: 'bed', 5: 'bicycle', 6: 'bird', 7: 'birthday cake', 8: 'book', 9: 'cactus', 10: 'cake', 11: 'camel', 12: 'camera', 13: 'donut', 14: 'giraffe', 15: 'guitar', 16: 'jail', 17: 'motorbike', 18: 'mouse', 19: 'mug', 20: 'mushroom', 21: 'pineapple', 22: 'pizza', 23: 'scorpion', 24: 'snowman', 25: 'the eiffel Tower', 26: 'the mona lisa', 27: 'tree', 28: 'whale'} 
N_DOODLES = 29


def detect_sketch(name,doodle_name):
    try:
        x = Image.open(f'server_images/{name}.png')
        x = x.convert("L")
        # resize input image to 28x28
        x = x.resize((28, 28))
        model = conv
        x = np.expand_dims(x, axis=0)  # type: ignore
        x = np.reshape(x, (28, 28, 1))
        # invert the colors
        x = np.invert(x)
        # brighten the image by 60%
        for i in range(len(x)):
            for j in range(len(x)):
                if x[i][j] > 50:
                    x[i][j] = min(255, x[i][j] + x[i][j] * 0.60)

        # normalize the values between -1 and 1
        x = normalize(x)
        val = model.predict(np.array([x]))# type: ignore
        pred = DOODLES[np.argmax(val)]
        print(pred)        
        return val[0][np.argmax(val)],pred
    except Exception as ex:
        print(ex,"in doodle_Ai")