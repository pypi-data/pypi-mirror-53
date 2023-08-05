import torch
import math
import logging

class NumericEncoder:

    def __init__(self, data_type = None, is_target = False):
        self._is_target = True
        self._trained = False
        self._min_value = None
        self._max_value = None
        self._type = data_type
        self._mean = None
        self._pytorch_wrapper = torch.FloatTensor

    def encode(self, data):

        if self._trained == False:
            count = 0
            value_type = 'int'
            for number in data:
                try:
                    number = float(number)
                except:
                    continue

                if number is None or math.isnan(number):
                    logging.error('Lightwood does not support working with NaN values !')
                    exit()

                self._min_value = number if self._min_value is None or self._min_value > number else self._min_value
                self._max_value = number if self._max_value is None or self._max_value < number else self._max_value
                count += number

                if int(number) != number:
                    value_type = 'float'

            self._type = value_type if self._type is None else self._type
            self._mean = count / len(data)

            self._trained = True

        ret = []

        for number in data:

            vector_len = 3 if self._is_target else 4
            vector = [0]*vector_len


            if number is None:
                ret += [vector]
                continue

            try:
                number = float(number)
            except:
                logging.warning('It is assuming that  "{what}" is a number but cannot cast to float'.format(what=number))
                ret += [vector]
                continue

            if number < 0:
                vector[0] = 1

            if number == 0:
                vector[1] = 1

            else:
                vector[2] = math.log(abs(number))

            if not self._is_target:
                vector[-1] = 1 # is not null


            ret += [vector]


        return self._pytorch_wrapper(ret)


    def decode(self, encoded_values):
        ret = []
        for vector in encoded_values.tolist():
            if vector[-1] == 0 and self._is_target == False: # is not null = false
                ret += [None]
                continue

            if math.isnan(vector[1]):
                abs_rounded_first = 0
            else:
                abs_rounded_first = abs(round(vector[1]))


            if abs_rounded_first == 1:
                real_value = 0
            else:
                if math.isnan(vector[0]):
                    abs_rounded_zero = 0
                else:
                    abs_rounded_zero = abs(round(vector[0]))

                is_negative = True if abs_rounded_zero == 1 else False
                encoded_value = vector[2]
                try:
                    real_value = -math.exp(encoded_value) if is_negative else math.exp(encoded_value) #(self._max_value-self._min_value)*encoded_value + self._mean
                except:
                    if self._type == 'int':
                        real_value = pow(2,63)
                    else:
                        real_value = float('inf')

            if self._type == 'int':
                real_value = round(real_value)

            ret += [real_value]

        return ret



if __name__ == "__main__":

    encoder = NumericEncoder(data_type='int')

    print(encoder.encode([1,2,2,2,2,2,8.6]))

    print(encoder.decode(encoder.encode([1, 2, 2, 2, 2, 2, 8.7, 800, None])))

    encoder = NumericEncoder()

    print(encoder.encode([1, 2, 2, 2, 2, 2, 8.6]))

    print(encoder.decode(encoder.encode([1, 2, 2, 2, 2, 2, 8.7, None])))
