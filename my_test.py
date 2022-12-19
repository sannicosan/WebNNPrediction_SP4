import os
import hashlib
import ast
import json
import numpy as np

# dir = 'D:\ProgramFiles\Anaconda3\envs\sprint4\lib\os.py'
# print(dir.split('.')[-1] in {'png','py', 'txt'}) 

path = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(path,'tests/dog.jpeg')

with open(filepath,'rb') as f:
    data = f.read()
    name_md5 = hashlib.md5(data).hexdigest()   # Example:  "0b3f45b266a97d7029dde7c2ba372093" + ".png"
    
print(name_md5)

path = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(path,'tests/dog.jpeg')
f = {'file': (open(filepath,'rb'), 'dog.jpeg')}
print(f['file'][0].read())

# ar = np.array([[('n02108551', 'Tibetan_mastiff', 0.9666902),(('n02108551', 'Tibetan_mastiff', 0.9666902))]])
# id, clase, prob = ar[0][0]
# print(id,clase,prob)

# dic = '{"filename": "q\x9dH\xdb\xaa\xc79\xa2=\xc7\xa7\xcf\x17#\x9d\x0e.jpeg", "prediction": "Eskimo_dog", "score": 0.9345518946647644 }'
# print(ast.literal_eval(dic))

# dic = {"filename": "q\x9dH\xdb\xaa\xc79\xa2=\xc7\xa7\xcf\x17#\x9d\x0e.jpeg", "prediction": "Eskimo_dog", "score": 0.9345518946647644}
# print(dic.filename)

exit()