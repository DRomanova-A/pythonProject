import os
import csv
import re


class CarBase:
    photo_file_names = ['.jpg', '.jpeg', '.gif', '.png']

    def get_photo_file_ext(self):
        """
        Get photo file extension ('.png', '.jpeg', etc).
        :return: str, file extension
        """
        if os.path.splitext(self.photo_file_name)[1] in self.photo_file_names:
            return os.path.splitext(self.photo_file_name)[1]
        else:
            return False

    def __init__(self, brand, photo_file_name, carrying):
        if not brand:
            raise ValueError('brand обязательный атрибут!')
        #регулярное выражение
        if not re.findall(r'^\S+.jpeg$|^\S+.jpg$|^\S+.png$|^\S+.gif$', photo_file_name):
            raise ValueError('photo_file_name обязательный атрибут!')
        if not carrying:
            raise ValueError('carrying обязательный атрибут!')

        self.brand = brand

        self.photo_file_name = photo_file_name

        try:
            self.carrying = float(carrying)
        except TypeError as err:
            print(err)
        else:
            self.carrying = float(carrying)

    @property
    def car_type(self):
        raise NotImplementedError


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        try:
            if not passenger_seats_count:
                raise ValueError('passenger_seats_count обязательный атрибут!')
            self.passenger_seats_count = int(passenger_seats_count)
        except TypeError as error:
            print(error)
        else:
            self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.__body_whl = body_whl
        try:
            if self.__body_whl == "":
                self.body_length = self.body_width = self.body_height = float(0)
            else:
                self.body_length, self.body_width, self.body_height = map(float, self.__body_whl.split("x"))
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        try:
            if not extra:
                raise ValueError('extra обязательный атрибут!')
            self.extra = extra
        except TypeError as error:
            print(error)
        else:
            self.extra = extra


def get_car_list(csv_fd):
    car_list = []
    try:
        with open(csv_fd) as csv_f:
            reader = csv.reader(csv_f, delimiter=';')
            next(reader)

            for row in reader:
                length = len(row)

                if length >= 6:
                    try:
                        type = row[0]
                        if type == 'car':
                            car_list.append(Car(
                                brand=row[1], photo_file_name=row[3], carrying=row[5],
                                passenger_seats_count=row[2]
                            ))
                        elif type == 'truck':
                            car_list.append(Truck(
                                brand=row[1], photo_file_name=row[3], carrying=row[5],
                                body_whl=row[4]
                            ))
                        elif type == 'spec_machine':
                            car_list.append(SpecMachine(
                                brand=row[1], photo_file_name=row[3], carrying=row[5],
                                extra=row[6]
                            ))
                    except KeyError:
                        # если car_type не извесен, просто игнорируем csv-строку
                        continue
                    except (ValueError, IndexError):
                        pass

    except IOError as err:
        print(f'Ошибка! #{err.errno} {err.strerror} {err.filename}')

    return car_list


if __name__ == '__main__':
    csv_filename = "coursera_week3_cars.csv"
    cars = get_car_list(csv_filename)
    print(cars)
