import redis
from collections import namedtuple


REQUEST_KEY = "findpath"
RESPONSE_KEY = "path"
DYNAMIC_OBSTACLES_KEY = "dynamic_obstacles"


CircleObstacles = namedtuple("CircleObstacles", ["xcenter", "ycenter", "radius"])


class NoWay:

    def __init__(self, redis_host="127.0.0.1", redis_port=6379):
        self.redis = redis.Redis(redis_host, redis_port, db=0, decode_responses=True)

    def send_obstacles(self, obstacles):
        """
        Sets the dynamic obstacles for the path finding.
        This function removes all the previously send obstacles and set those new ones.
        Only circles obstacles are supported.
        :param obstacles:The list of dynamic obstacles to consider
        :type obstacles: list[CircleObstacles]
        :return: None
        """
        self.redis.delete(DYNAMIC_OBSTACLES_KEY)
        ser = [",".join([o.xcenter, o.ycenter, o.radius]) for o in obstacles]
        self.redis.rpush(DYNAMIC_OBSTACLES_KEY, *ser)

    def plan(self, xstart, ystart, xgoal, ygoal):
        """
        Send a planning request from `xstart,ystart` to `xgoal,ygoal` taking the latest dynamic obstacles set
        with `send_obstacles`. This remove any previous solution found from the buffer (and won't be accessible anymore
        through the `get_path` function.
        :param xstart: x coordinate of the start point of the request
        :param ystart: y coordinate of the start point of the request
        :param xgoal: x coordinate of the goal point of the request
        :param ygoal: y coordinate of the goal point of the request
        :return: None
        """
        self.redis.delete(RESPONSE_KEY)
        clients = self.redis.publish(REQUEST_KEY, f"{xstart},{ystart};{xgoal},{ygoal}")
        if clients == 0:
            print("[NoWay] Plan request sent, but no client received it. Are you sure NoWay is currently started and "
                  "the redis databases are the same?")

    def is_planning_finished(self):
        """
        Checks if the planning task has ended. Returns True if no planning task is running, even if no path has been
        found. Returns False if a planning task is running or if no request has been sent on the current redis instance.
        :return: True if no planning task is running, False otherwise
        """
        return self.redis.get(RESPONSE_KEY) is not None

    def get_path(self):
        """
        Returns the path found for the last request sent. Returned list will be empty if no path has been found.
        Returns None if the planning task is not finished.
        :return: The list of points linking the two points sent in the request avoiding both static and dynamic
        obstacles.
        :rtype: list[tuple[int, int]] | None
        """
        path = self.redis.get(RESPONSE_KEY)
        if path is None:
            return None
        if path == '':
            return []
        p = path.strip(';').split(';')
        # Converts "x1,y1;x2,y2;..." -> [(int(x&), int(y1)), (int(x2), int(y2)), ...]
        p = list(map(lambda pt: tuple(map(int, pt.split(','))), p))
        return p
