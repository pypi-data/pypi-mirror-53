from __future__ import absolute_import
from __future__ import print_function
from timeit import default_timer


class Timer(object):
    timer_stack = []
    max_depth = 0
    timing_enabled = False

    def __init__(self, name=None):
        """
        Create a Timer object. If timing is enabled, the timer starts on instantiation,
        and ends when it goes out of scope.

        Arguments:
            - 'name': Optional name to give the timer.
                    Defaults ot "timer <n>" where this is the nth timer on the stack.
        """
        if not name:
            depth = len(self.timer_stack)
            name = "timer %d" % (depth + 1)
        self.name = name
        self.started = False
        if self.timing_enabled:
            self.start()

    def start(self):
        if self.started:
            return
        depth = len(self.timer_stack)
        if depth >= self.max_depth:
            return
        timer = default_timer()
        name = self.name

        spaces = depth * "    "
        print(spaces + "[%s] start" % name)
        timer = default_timer()
        self.timer_stack.append((timer, name))
        self.started = True

    def stop(self):
        # Not checking if we have any timers,
        # because that's a pretty serious bug we should blow up on
        # if len(self.timers) < 1:
        #     return
        if not self.started:
            return
        start, name = self.timer_stack.pop()
        depth = len(self.timer_stack)
        spaces = depth * "    "
        msg = ""
        end = default_timer()
        msg += spaces
        msg += ("")
        msg += ("[%s] end\t" % name)
        msg += ("Elapsed time: %.3f seconds" % (end - start))
        print(msg)
        print("")
        self.started = False

    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        self.stop()

    def __del__(self):
        self.stop()

    @classmethod
    def enable_timing(cls, do_time, max_depth=10000):
        """
        Enable (or disable) timing for all timers not already started.

        Arguments:
            - 'do_time': Boolean to enable or disable timing.
            - 'max_depth': Maximum depth of the timer stack. Timers beyond max_depth will not start.
                           Defaults to 10000
        """
        cls.timing_enabled = do_time
        if do_time:
            cls.max_depth = max_depth
