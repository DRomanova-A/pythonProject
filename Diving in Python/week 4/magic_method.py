import os.path
import tempfile
import uuid


class File:
    def __init__(self, path ='example.txt'):
      self.path = path
      self.current_position = 0

      if not os.path.exists(path):
        open(self.path, 'w').close()

    def write(self, text):
        with open(self.path, 'w') as f:
            return f.write(text)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __add__(self, other):
        result_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4())) #str (uuid.uuid4 ()) - генерация случайного имени файла
        result = File(result_path)
        result.write(self.read() + other.read())
        return result

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)
            line = f.readline()

            if line:
                self.current_position = f.tell()
                return  line
            else:
                self.current_position = 0
                raise StopIteration('EOF')


def main():
    f = File('test.txt')
    print(f.write('test1'))
    print(f.read())
    file1 = File('test2.txt')
    print(file1.write('test2'))
    print(file1.read())
    new_file_obj = f + file1
    isinstance(new_file_obj, File)

    print(new_file_obj)
    for line in new_file_obj:
       print(ascii(line))


if __name__ == '__main__':
    main()