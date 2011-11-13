# =============================================================================
# MODULE IMPORTS
# =============================================================================
import es
import gamethread


# =============================================================================
# MODULE INFORMATION
# =============================================================================
info = es.AddonInfo()
info.name = "Repeat2 - EventScripts python library"
info.version = "sushi01"
info.url = "http://www.eventscripts.com/pages/Repeat2/"
info.basename = "repeat2"
info.author = "SumGuy14 (Aka SoccerDude) & XE_ManUp"


# =============================================================================
# MODULE GLOBAL VARIABLES
# =============================================================================
STATUS_STOPPED = 1
STATUS_RUNNING = 2
STATUS_PAUSED = 3


# =============================================================================
# MODULE CLASSES
# =============================================================================
class RepeatError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class RepeatContainer(dict):
    """Dictionary object that contains all repeat instances. The keys of the
    dictionary are the repeat names and the Repeat() instances are the values
    of the keys.

    """
    def add(self, name, instance):
        """Adds a repeat instance by name to the dictionary."""
        if not name in self:
            # Add the repeat instance to the dictionary
            self[name] = instance
        else:
            raise RepeatError('The repeat name "%s" already exists! ' % name +
                'If you are creating a new repeat, please use a different ' +
                'name. If you are updating the repeat, please use ' +
                'repeat.find("%s").' % name)

    def delete(self, name):
        """Deletes a repeat instance by name from the container."""
        try:
            # Delete the repeat instance from the dictionary
            del self[name]
        except KeyError:
            # Do not raise an exception if the repeat does not exist
            pass


repeatContainer = RepeatContainer()


class RepeatManager(object):
    """Class that controls interaction with the repeat such as starting,
    stopping, pausing, resuming, etc.

    Arguments:
        instance_or_name: This can be either a Repeat() instance, or the name
                          given to the instance.

    """
    # =========================================================================
    #   RepeatManager class instance special methods
    # =========================================================================
    def __init__(self, instance_or_name):
        # Public variables
        if not isinstance(instance_or_name, Repeat):
            # Find the instance
            instance = find(str(instance_or_name))

            if instance is None:
                raise RepeatError(
                    'The repeat name "%s" can not be found' % instance_or_name)
            self.repeat = find(instance_or_name)
        else:
            self.repeat = instance_or_name

        # Private variables
        self._adjusted = 0
        self._count = 0
        self._interval = 0
        self._limit = 0
        self._status = STATUS_STOPPED

    def __getitem__(self, name):
        # Return using getattr
        return getattr(self, str(name).lower())

    def __setitem__(self, name, value):
        #Forward to __setattr__
        self.__setattr__(name, value)

    # =========================================================================
    #   RepeatManager class instance read-only properties
    # =========================================================================
    @property
    def timeleft(self):
        """Returns the amount of time (in seconds) remaining in the repeat."""
        return self.remaining * self._interval

    @property
    def elapsed(self):
        """Returns the amount of time (in seconds) that has elapsed."""
        if not self._adjusted:
            return self._count * self._interval

        # Return adjusted value
        return (self._count * self._interval) + self._adjusted

    @property
    def time(self):
        """Returns the total amount of time (in seconds) it will take to
        complete the repeat.

        """
        if not self._adjusted:
            return self._interval * self._limit

        # Return the adjusted value
        return ((self._interval * self._limit) +
            (self._adjusted * self._interval))

    @property
    def remaining(self):
        """Returns the number of loops remaining in the repeat."""
        return self._limit - self._count

    @property
    def count(self):
        """Returns the number of loops that the repeat has fired."""
        if not self._adjusted:
            return self._count

        # Return the adjusted value
        return self._count + self._adjusted

    @property
    def status(self):
        """Returns the status of the repeat:

        STATUS_STOPPED == 1
        STATUS_RUNNING == 2
        STATUS_PAUSED == 3
        """
        return RepeatManager.status
        return self._status

    @property
    def interval(self):
        """Returns the delay between each time the repeat is fired."""
        return self._interval

    @property
    def limit(self):
        """Returns the number of times the repeat will run/loop."""
        return self._limit

    # =========================================================================
    #   RepeatManager class instance methods
    # =========================================================================
    def start(self, interval, limit):
        """Starts the repeatable command.

        Arguments:
            interval: Float value which represents the delay between each time
                      the repeat is fired.
            limit: Integer value which represents the number of times to loop.
                   If 0, the repeat will continue to loop indefinately until
                   stopped.

        Note:
            * If starting an already running repeat, this will stop the
              currently running repeat, and restart with the newly passed
              values.
            * If starting a paused repeat, this restart the repeat with the
              newly passed values.
        """
        # If the repeat is currently running, no action is needed
        if self.status == STATUS_RUNNING:
            self.stop()

        # Set up initial repeat starting values
        self._adjusted = 0
        self._count = 0
        self._interval = float(interval)
        self._limit = int(limit)
        self._status = STATUS_RUNNING

        # Begin execution of the repeat
        self._fire()

    def restart(self):
        """Restarts the repeat based on the stored interval and limit
        arguments.

        Note:
            * It is assumed that the start() method was used prior to utilizing
              this method. If both the interval and limit have values of 0,
              this method will not restart the repeat.

        """
        # Set up initial repeat starting values
        self._adjusted = 0
        self._count = 0
        self._status = STATUS_RUNNING

        # Fire the repeat
        self._fire()

    def stop(self):
        """Stops the execution of the repeat.

        Note:
            * By stopping the repeat, it effectly cancels all pending actions.
            * Once stopped, the repeat must be started using the start() or
              restart() methods.
            * Use the pause() method if needing to resume the repeat from
              where it was left off.

        """
        # Cancel the delay
        gamethread.cancelDelayed(self.repeat.name)

        # Set the repeat status to stopped
        self._status = STATUS_STOPPED

        # Set the adjusted time back to default
        self._adjusted = 0

    def pause(self):
        """Pauses a repeat for continued execution at a later time.

        Note:
            * Repeat must be running (status == 2) to pause.
            * To resume paused repeat, use the resume() method.

        """
        # If the repeat is already running, do nothing
        if self._status != STATUS_RUNNING:
            return

        # Set the status to "paused"
        self._status = STATUS_PAUSED

        # Cancel the delay
        gamethread.cancelDelayed(self.repeat.name)

    def resume(self):
        """Resumes a paused repeat.

        Note:
            * Only to be used for resuming a paused repeat.
            * If needing to restart a repeat from the beginning, use the
              start() method.
            * A paused repeat will show a status of 3 (PAUSE).

        """
        # If the repeat is already running, do nothing
        if self._status == STATUS_RUNNING:
            return

        # Make sure that we can resume the repeat
        if ((self._interval != 0 and self.remaining > 0) or
            self._interval == 0):

            # Set the status to "running"
            self._status = STATUS_RUNNING

            # Begin the execution of repeat
            self._fire()

    def delete(self):
        """Deletes the repeat from its stored location in the container. When
        deleting the repeat, the repeat is stopped. The intention of this
        method is that it is to be used for cleanup purposes. Since the repeat
        instance is saved in a container, it is pertinent that you delete your
        created repeat when your script/addon is unloaded.

        """
        # If the repeat is running, stop it
        if self._status == STATUS_RUNNING:
            self.stop()

        # Delete the repeat from the container
        repeatContainer.delete(self.repeat.name)

    def extend(self, seconds):
        """Extends the amount of time (in seconds) that the repeat will run.

        Note:
            * Time can not be extended if limit is set to 0.

        """
        # Check the limit
        if self._limit == 0:
            return

        # Calculate the adjusted count needed
        count = int(int(seconds) / self._interval)
        #print "count:", count

        # Set the adjusted time to the current count for improved calculations
        if not self._adjusted:
            self._adjusted += count
        else:
            self._adjusted += count - self._count

        # Reduce the count
        self._count -= count

    def reduce(self, seconds):
        """Reduces the amount of time (in seconds) that the repeat will run.

        Note:
            * Time can not be extended if limit is set to 0.

        """
        # Check the limit
        if self._limit == 0:
            return

        # Calculate the adjusted count needed
        count = int(int(seconds) / self._interval)

        # Set the adjusted time to the current count for improved calculations
        if not self._adjusted:
            self._adjusted += count
        else:
            self._adjusted += count - self._count

        # Increment the count
        self._count += count

    def _fire(self):
        # Make sure the amount of times fired is under its limit or infinite
        if self._count < self._limit or self._limit == 0:
            # Increment loop counter
            self._count += 1

            if callable(self.repeat.command):
                # Python function
                gamethread.delayedname(self._interval, self.repeat.name,
                                       self.repeat.command, self.repeat.args,
                                       self.repeat.kwargs)
            else:
                # Console command
                gamethread.delayedname(self._interval, self.repeat.name,
                                       es.server.queuecmd, self.repeat.command)

            # Re-call the self._fire() loop
            gamethread.delayedname(
                self._interval, self.repeat.name, self._fire)
        else:
            self.stop()


class Repeat(RepeatManager):
    """Class that contains the intial repeat object."""
    # =========================================================================
    #   Repeat class instance special methods
    # =========================================================================
    def __init__(self, name, command, *args, **kwargs):
        # Public variables
        self.name = str(name)
        self.command = command
        self.args = args
        self.kwargs = kwargs

        # Instantiate the RepeatManager
        RepeatManager.__init__(self, self)

        # Store the repeat in the repeat container
        repeatContainer.add(self.name, self)

    def __getitem__(self, name):
        # Return using getattr
        return getattr(self, str(name).lower())

    def __setitem__(self, name, value):
        #Forward to __setattr__
        self.__setattr__(name, value)

    def __setattr__(self, name, value):
        if name == 'name':
            if hasattr(self, name):
                # Since the name changed, update the repeat container
                repeatContainer.add(str(value), self)
                repeatContainer.delete(self.name)

        # Set the attribute
        object.__setattr__(self, name, value)

    def __str__(self):
        return repr(self.name)


# =============================================================================
# MODULE FUNCTIONS
# =============================================================================
def find(name):
    """Finds and returns a repeat by its name.

    Note:
        * Returns a Repeat() class instance if the name is found.
        * Returns None if a Repeat() class instance is not found.

    """
    if name in repeatContainer:
        return repeatContainer[name]

    return None


def delete(name):
    """Deletes a repeat by name."""
    repeatContainer.delete(name)


def get_repeat_names():
    """Returns a list of all existing/stored repeat names."""
    return repeatContainer.keys()
