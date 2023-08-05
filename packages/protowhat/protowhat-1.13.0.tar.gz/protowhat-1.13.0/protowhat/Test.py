from protowhat.Feedback import Feedback


class TestFail(Exception):
    def __init__(self, feedback, payload):
        super().__init__(feedback.message)
        self.feedback = feedback
        self.payload = payload


class Test:
    """
    The basic Test. It should only contain a failure message, as all tests should result in
    a failure message when they fail.

    Note:
        This test should not be used by itself, subclasses should be used.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, feedback):
        """
        Initialize the standard test.

        Args:
            feedback: string or Feedback object
        """
        if issubclass(type(feedback), Feedback):
            self.feedback = feedback
        elif issubclass(type(feedback), str):
            self.feedback = Feedback(feedback)
        else:
            raise TypeError(
                "When creating a test, specify either a string or a Feedback object"
            )

        self.result = None

    def __call__(self):
        """
        Wrapper around specific tests. Tests only get one chance.
        """
        if self.result is None:
            try:
                self.test()
                self.result = bool(self.result)
            except:
                self.result = False

    def test(self):
        """
        Perform the actual test.
        """
        raise NotImplementedError

    def get_feedback(self):
        return self.feedback

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, repr(vars(self)))


class Fail(Test):
    def test(self):
        self.result = False
