import math

class three_vector(object):
    def f(self):
        data = {
            'x': 0,
            '$x': lambda x: data.update({'x': x}),
            'y': 0,
            '$y': lambda x: data.update({'y': x}),
            'z': 0,
            '$z': lambda x: data.update({'z': x})
        }
        #def magnitude(self):
        #   m = pow((pow(data.get('x'), 2) + pow(data.get('y'), 2) + pow(data.get('z'), 2)), (1/2))
        #   return m

        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return None
        return cf
    def magnitude(self):
        x_squared = pow(self.run('x'), 2)
        y_squared = pow(self.run('y'), 2)
        z_squared = pow(self.run('z'), 2)
        squares_sum = x_squared + y_squared + z_squared
        m = round(math.sqrt(squares_sum), 2)
        return m
    run = f(1)

# print s1.data

