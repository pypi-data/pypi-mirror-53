import traitlets

class default(traitlets.BaseDescriptor):
    def __init__(self, f, cls, name):
        self.func = f
        self.class_init(cls, name)
    
    # def __call__(self, *Args):
    #     print('YEARH')
    #     fds
    #     return self.func(*args)
class connector(traitlets.BaseDescriptor):
    def __init__(self, input, output, **kwargs):
        print('Connector.__init__', input, output, kwargs)
        self.input = input
        self.output = output
    def class_init(self, cls, name):
        print('Connector.class_init', cls, name)
        super(connector, self).class_init(cls, name)
        # self.compute.this_class = cls
        cls._trait_default_generators[self.output] = default(self.compute_and_observe, cls, self.output)
    
    def compute_and_observe(self, obj):
        print("compute and observe")
        dsa
        def update(change):
            setattr(obj, self.output, self.compute(obj))
        obj.observe(update, self.input)
        return self.compute(obj)

    def compute(self, obj):
        values = [getattr(obj, k) for k in self.input]
        result = self.func(self, *values)
        return result
    
    def instance_init(self, obj):
        print('Connector.instance_init', obj)
    def __call__(self, func):
        print('Connector.__call__', func)
        self.func = func
        return self


# def connect(input, output):
#     def decorator(f):
#         import pdb; pdb.set_trace()
#     return Connector()

class Spam(traitlets.HasTraits):
    min = traitlets.Float(0)
    max = traitlets.Float(1)
    value = traitlets.Float(0.2)
    normalized_value = traitlets.Float()

    @connector(input=['min', 'max', 'value'], output='normalized_value')
    def _calc(self, min, max, value):
        print('calc', min, max)
        return (value - min) / (max - min)


if __name__ == '__main__':
    spam = Spam(min=5, max=10, value=3)
    spam.value = 1
    print(spam.normalized_value)
    spam.value = 9
    print(spam.normalized_value)
    spam.value = 5
    print(spam.normalized_value)
    spam.value = 10
    print(spam.normalized_value)
    spam.value = 7.5
    print(spam.normalized_value)

