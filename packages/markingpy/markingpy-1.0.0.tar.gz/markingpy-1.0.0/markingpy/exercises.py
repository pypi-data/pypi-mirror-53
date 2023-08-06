#      Markingpy automatic grading tool for Python code.
#      Copyright (C) 2019 University of East Anglia
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
"""
Exercise building utilities.
"""
import logging
import weakref
from collections import namedtuple
from functools import wraps
from contextlib import contextmanager
from inspect import isfunction
from typing import ( Union, Dict, Any, Type, Callable, Optional, Tuple, Iterable)


from .cases import Test, TimingTest, CallTest, Call
from .utils import log_calls
from .import cases

ARGS = Tuple[Any, ...]
KWARGS = Dict[str, Any]
logger = logging.getLogger(__name__)
INDENT = " " * 4
__all__ = [
    'Exercise',
    'ExerciseFunctionProxy',
    'ExerciseInstance',
    'ExerciseError',
    'ExerciseFeedback',
    'ClassExercise',
    'FunctionExercise',
    'InteractionExercise',
]
_EXERCISES = weakref.WeakKeyDictionary()


class ExerciseBase:

    def __init__(self):
        ex_no = min(
            i for i in range(1, len(_EXERCISES) + 2) if i not in _EXERCISES.values()
        )
        _EXERCISES[self] = ex_no

    def get_number(self) -> int:
        return _EXERCISES[self]


class ExerciseError(Exception):
    pass


ExerciseFeedback = namedtuple(
    "ExerciseFeedback", ("marks", "total_marks", "feedback", "per_test")
)


def record_call(*args: Any, **kwargs: Any) -> Call:
    """
    Record the arguments of a function call.

    :return: Call namedtuple (args, kwargs)
    """
    return Call(args, kwargs)


class Exercise(ExerciseBase):
    """
    Exercises are the main objects in a marking scheme file. These will be used
    to test each submission to construct the final mark and feedback. Each
    exercise object holds a number of tests to be run, which constitute the
    grading criteria for the exercise.

    This class is intended to provide the core functionality for exercise
    objects, and it is not intended for this class to be instantiated
    directly. For exercises involving functions, use the subclass
    :class:`markingpy.FunctionExercise`, and for exercises involving classes
    use the subclass :class:`markingpy.ClassExercise`.

    The :func:`markingpy.exercise` decorator is the preferred method for
    creating Exercise instances. This decorator will select the most
    appropriate Exercise subclass for the decorated type.

    :param function_or_class: Function or class to be wrapped.
    :param name: Name of the test. Defaults to the name of *function_or_class*.
    :param descr: Short description of the test to be printed in the feedback.
    """

    def __init__(
        self,
        function_or_class: Union[Callable, Type],
        name: Optional[str] = None,
        descr: Optional[str] = None,
        marks: Optional[int] = None,
        submission_name: Optional[str] = None,
        **args: Any,
    ):
        super().__init__()
        self.number = self.get_number()
        wraps(function_or_class)(self)
        self.tests = []
        self.num_tests = 0
        self.func = function_or_class
        if submission_name is None:
            submission_name = function_or_class.__name__
        self.submission_name = submission_name
        self.exc_func = record_call
        self.name = name if name else self.get_name()
        self.descr = descr
        self.marks = marks

    def lock(self):
        """
        Lock the function into testing mode.

        The execution function is changed to the model function ready to be used
        for grading submissions.
        """
        # TODO: fix the tests at this point so no more can be added.
        self.exc_func = self.func

    def validate(self):
        """
        Check that the exercise is valid.

        :raises ExerciseError: If the exercise fails to validate.
        """
        logger.info(f'Validating exercise: {self.name}')
        self.lock()
        total_marks = self.total_marks
        if self.marks is not None:
            if not self.marks == total_marks:
                raise ExerciseError(
                    f'{self.name} Error:\n'
                    f"Total marks ({total_marks}) from tests does not match "
                    f"marks ({self.marks}) allocated to exercise."
                )

        self.marks = total_marks
        ns = {self.submission_name: self.func}
        result = self.run(ns)
        if not result.total_marks == self.marks:
            raise ExerciseError(
                f'{self.name} Error:\n'
                f'Total marks allocated in result ({result.total_marks}) does '
                f'not match the total marks available for the exercise '
                f'({self.marks}).'
            )

        if not result.marks == result.total_marks:
            raise ExerciseError(
                f'{self.name} Error:\n'
                f'Model solution for exercise {self.name} does not receive '
                f'full marks.\n\n{result.feedback}'
            )

        logger.info(f'Validation: Passed')

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.func.__name__})"

    def get_name(self) -> str:
        return f"Exercise {self.number}: {self.func.__name__}"

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call the exercise function or submission function.

        For functions, this is the same as invoking the function.
        For classes, this function instantiates the exercise class
        or the submission class.
        """
        return self.exc_func(*args, **kwargs)

    @contextmanager
    def set_to_submission(self, submission_func: Union[Callable, Type]):
        """
        Set the execution function to the submission function or class
        :param submission_func: Function or class to set
        """
        self.exc_func = submission_func
        try:
            yield

        finally:
            self.exc_func = self.func

    @property
    def total_marks(self) -> int:
        return sum(t.marks for t in self.tests)

    def add_test(
        self,
        *args,
        name: Optional[str] = None,
        cls: Type[cases.BaseTest] = None,
        **params: Any,
    ) -> cases.BaseTest:
        """
        Add a new test to the exercise.

        This method should usually not be called directly. It is better to
        use one of the specific test creator methods.

        Keyword parameters are passed to the Test instance.

        :param name: Name for the test. Defaults to name of the function.
        :param cls: Class to instantiate. Defaults to :class:`markingpy.Test`
        :return: Test instance
        """
        if cls is None:
            cls = Test
        test = cls(*args, exercise=self, name=name, **params)
        self.tests.append(test)
        return test

    @log_calls("info")
    def test(
        self,
        name: Optional[str] = None,
        cls: Optional[Type[cases.BaseTest]] = None,
        **kwargs: Any,
    ) -> cases.BaseTest:
        """
        Add a new test to the exercise by decorating a function. The function
        should return `True` for a successful test and `False` for a failed
        test. Printed statements used in the function will be added to the
        feedback for the submission.

        Equivalent to creating a function `func` and running
        `ex.add_test(func)`.

        :param name: Name for the test. Defaults to name of the function.
        :param cls: Class to instantiate.
            Defaults to :class:`Test`.
        """
        if cls is None:
            cls = Test
        if isinstance(name, str):
            kwargs["name"] = name
            name = None

        def decorator(func):
            return self.add_test(func, cls=cls, **kwargs)

        if name is None:
            return decorator

        elif isfunction(name):
            return decorator(name)

        raise TypeError('Custom test must decorate a function.')

    def get_submission_function(
        self, namespace: Dict[str, Any]
    ) -> Union[Callable, Type]:
        return namespace.get(self.submission_name, None)

    def format_feedback(self, results: Any) -> ExerciseFeedback:
        if not results:
            msg = (f"Function {self.submission_name} was not found in " "submission.")
            return ExerciseFeedback(0, self.total_marks, msg, [])

        feedback = [self.name]
        if self.descr:
            feedback.append(self.descr)
        feedback.extend(r.feedback for r in results)
        score = sum(r.mark for r in results)
        feedback.append(f"Score for {self.name}: {score} / {self.total_marks}")
        return ExerciseFeedback(score, self.total_marks, "\n".join(feedback), results)

    def run(self, namespace: Dict[str, Any]) -> ExerciseFeedback:
        """
        Run the test suite on submission.

        :param namespace: submission namespace
        :return: namedtuple containing marks, total_marks, feedback
        """
        submission_fun = self.get_submission_function(namespace)
        if submission_fun is None:
            return self.format_feedback([])

        results = [test(submission_fun) for test in self.tests]
        return self.format_feedback(results)


class ExerciseFunctionProxy:

    def add_test(self, *args: Any, **kwargs: Any) -> cases.BaseTest:
        raise NotImplementedError

    @log_calls("info")
    def add_test_call(
        self, call_params: ARGS = None, call_kwparams: KWARGS = None, **kwargs: Any
    ) -> cases.BaseTest:
        """
        Add a call test to the exercise.

        Submission function is evaluated against the model solution, and is
        successful if both functions return the same value.

        :param call_params:
        :param call_kwparams:
        """
        if isinstance(call_params, Call):
            call_params, call_kwparams = call_params
        return self.add_test(call_params, call_kwparams, cls=CallTest, **kwargs)

    @log_calls("info")
    def timing_test(
        self,
        timing_cases: Union[Dict[Call, float], Iterable[Call]],
        tolerance: float = 0.2,
        **kwargs: Any,
    ) -> cases.BaseTest:
        """
        Test the timing of a submission against the model solution.

        :param timing_cases:
        :param tolerance:
        """
        return self.add_test(timing_cases, tolerance, cls=TimingTest, **kwargs)


class FunctionExercise(Exercise, ExerciseFunctionProxy):
    """
    Subclass of :class:`Exercise` with test methods for functions.

    Calling objects of this class within test functions will return the
    result of running either the model solution or the submission function

    Calling objects of this class in the body of the the marking scheme file
    will return a named tuple ``Call(args, kwargs)``, which holds the
    arguments *args* and keyword arguments *kwargs* for the call. These can
    be passed to test calls or timing tests.
    """
    set_function = Exercise.set_to_submission




# noinspection PyProtectedMember
class ExerciseInstance:

    def __init__(self, parent: 'ClassExercise', cls: Type, *args: Any, **kwargs: Any):
        self.__call_args = Call(args, kwargs)
        self.__parent = parent
        self.__cls = cls

    def __getattr__(self, item: str) -> Any:
        if not hasattr(self.__cls, item):
            raise AttributeError(f"{self.__cls} does not have attribute {item}")

        cls_attr = getattr(self.__cls, item)
        if isfunction(cls_attr):
            return ExerciseMethodProxy(
                self.__cls, self.__parent, self.__call_args, item
            )


class ExerciseMethodProxy(ExerciseFunctionProxy):

    def __init__(self, cls: Type, parent: 'ClassExercise', inst_call: Call, name: str):
        wraps(getattr(cls, name))(self)
        self.name = name
        self.parent = parent
        self.cls = cls
        self.inst_call = inst_call

    def add_test(
        self, *args: Any, cls: Optional[Type] = None, **kwargs: Any
    ) -> cases.BaseTest:
        if cls is cases.CallTest:
            return self.parent.method_test_call(
                self.name,
                *args,
                inst_with_args=self.inst_call.args,
                inst_with_kwargs=self.inst_call.kwargs,
                **kwargs,
            )

        elif cls is cases.TimingTest:
            return self.parent.method_timing_test(
                self.name,
                *args,
                inst_with_args=self.inst_call.args,
                isnt_with_kwargs=self.inst_call.kwargs,
                **kwargs,
            )

        raise TypeError

    def __call__(self, *args, **kwargs):
        return record_call(*args, **kwargs)


class ClassExercise(Exercise):
    """
    Subclass of :class:`Exercise` with test methods for classes.

    This class provides two test methods specifically for testing instance
    methods for the class. The first is a method analogue for a call test on
    the :class:`FunctionExercise` class. The second is an analogue
    of a timing test.

    Calling objects of this class within test functions will return an
    instance of the model solution class or the submission class, depending
    on where this function is used.

    Calling objects of this class in the body of the the marking scheme file
    will return an instance of :class:`ExerciseInstance`,
    which provides an easier method for adding for adding method test calls and
    timing test calls to the parent exercise. Each method attached to this
    :class:`ExerciseInstance` object provides an interface similar to that of
    :class:`FunctionExercise` for adding method call tests and
    method timing tests. The arguments used to instantiate the object will
    automatically be added to the test metadata.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        def wrapper(*iargs, **ikwargs):
            return ExerciseInstance(self, self.func, *iargs, **ikwargs)

        self.exc_func = wrapper

    @log_calls("info")
    def method_test_call(
        self,
        method: str,
        call_params: Optional[ARGS] = None,
        call_kwparams: Optional[KWARGS] = None,
        inst_with_args: Optional[ARGS] = None,
        inst_with_kwargs: Optional[KWARGS] = None,
        **kwargs: Any,
    ) -> cases.MethodTest:
        """
        Test the call of a method on the exercise class. This will create a new
        instance with the provided arguments, and then run the named method with
        the provided arguments.

        :param method: Name of method to be called. Attribute error raised if
            the method does not exist.
        :param call_params: Parameters with which to call the method
        :type call_params: tuple, None or :class:`Call`
        :param call_kwparams: Keyword parameters with which to call the method
        :type call_kwparams: dict or None
        :param inst_with_args: Parameters for instance creation
        :type inst_with_kwargs: dict or None
        :param inst_with_kwargs: Keyword parameters for instance creation
        :return: :class:`MethodTest` object
        """
        return self.add_test(
            method,
            call_params,
            call_kwparams,
            inst_with_args,
            inst_with_kwargs,
            cls=cases.MethodTest,
            **kwargs,
        )

    def method_timing_test(
        self,
        timing_cases: Union[Dict[Call, float], Iterable[Call]],
        tolerance: float = 0.2,
        inst_with_args: Optional[ARGS] = None,
        inst_with_kwargs: Optional[KWARGS] = None,
        **kwargs: Any,
    ) -> cases.MethodTimingTest:
        return self.add_test(
            timing_cases,
            tolerance,
            inst_with_args,
            inst_with_kwargs,
            cls=cases.MethodTimingTest,
            **kwargs,
        )


class InteractionExercise(Exercise):
    """
    Exercise class for testing interaction with some preset object.

    Construct exercises based on principle success criteria, rather than
    knowing a model solution and testing output against one another.

    For example, finding solutions to a maze. There are algorithms that
    can be used to find a solution, but many possible solutions.
    The principle success criteria is exiting the maze. Secondary success
    criteria could be the number of dead-ends met during the solution.
    (The implementation of randomly generated mazes is itself an interesting
    challenge.)

    The syntax for this exercise is different from other exercises. The
    exercise wraps an environment object that determines the parameters for
    the test. In the example above, this would be the maze. The submission
    can interact with the object using its methods. For instance,
    these could be moving in each direction, or looking ahead. The submission
    function must use only the functions provided by the environment object to
    solve the problem.
    """

    def __init__(self, environment: Type, **kwargs: Any):
        super().__init__(environment, **kwargs)

    def new_test(
        self, instantiation_call: Call, **kwargs: Any
    ) -> cases.InteractionTest:
        """
        Create a new interaction test. Tests of this kind revolve around the
        state object, as defined by class wrapped by the exercise. A test
        gives arguments to create the state object. The submission should
        define a function that manipulates the state object to achieve the
        success criteria added to the test.

        :param instantiation_call: Arguments to be used to create the state
            object.
        :param kwargs: Configuration arguments for the test object.
        :return: :class:`cases.InterctationTest`
        """
        return self.add_test(
            self.func, instantiation_call, cls=cases.InteractionTest, **kwargs
        )
