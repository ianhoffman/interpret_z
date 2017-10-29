class TokenZ:
    def __init__(self, z_type, value):
        self.z_type = z_type
        self.value = value

    def __str__(self):
        return '{class_name}({z_type}, {value})'.format(
            class_name=self.__class__.__name__,
            z_type=self.z_type,
            value=self.value
        )

    def __eq__(self, other):
        return self.z_type == other
