import inspect


class Loggable:

    def __init__(self, class_name):
        """
            :param class_name: The name of the child class. Should be passed using
            the following argument (in the child ctor): self.__class__.__name__
        """
        self.m_class_name = class_name

    def log_me(self):
        """
            This function is used so that every class can be "loggable" easily and with
            consistent manner.
            :return: The full name of the function from which it was called in
            the format: ClassName::CurrentExecutingFunctionName.
        """
        calling_func_name = inspect.stack()[1][3]
        ret_str = self.m_class_name + "::" + calling_func_name + " - "
        return ret_str
