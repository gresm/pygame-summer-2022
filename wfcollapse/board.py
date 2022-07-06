class Board2d:
    """
    2 dimensional board with size.
    """
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.board = [[0 for x in range(width)] for y in range(height)]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def get_at(self, x, y):
        """
        Get value at position.
        :param x:
        :param y:
        :return:
        """
        return self.board[x][y]

    def set_at(self, x, y, value):
        """
        Set value at position.
        :param x:
        :param y:
        :param value:
        :return:
        """
        self.board[x][y] = value
