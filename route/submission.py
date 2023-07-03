from typing import List, Tuple

from mapUtil import (
    CityMap,
    computeDistance,
    createStanfordMap,
    locationFromTag,
    makeTag,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch


# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Check out the docstring for `State` in `util.py` for more details and code.

########################################################################################
# Problem 1a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `startLocation` to any location with the specified `endTag`.
    """

    def __init__(self, startLocation: str, endTag: str, cityMap: CityMap):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return State(self.startLocation, None)
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.endTag in self.cityMap.tags[state.location]
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        return [[nextLocation, State(nextLocation, None), distance] for nextLocation, distance in self.cityMap.distances[state.location].items()]
        # END_YOUR_CODE


########################################################################################
# Problem 1b: Custom -- Plan a Route through Stanford


def getStanfordShortestPathProblem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `startLocation`/`endTag`. If you prefer, you may create a new map using via
    `createCustomMap()`.

    Run `python mapUtil.py > readableStanfordMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/stanford-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "park", "food")
        - `parking=`  - Assorted parking options (e.g., "underground")
    """
    cityMap = createStanfordMap()

    # Or, if you would rather use a custom map, you can uncomment the following!
    # cityMap = createCustomMap("data/custom.pbf", "data/custom-landmarks".json")

    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    startLocation = str(1757902279)
    endTag = "entrance=yes"
    return ShortestPathProblem(startLocation, endTag, cityMap)


########################################################################################
# Problem 2a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `startLocation` to any location with the specified `endTag` such that the path also
    traverses locations that cover the set of tags in `waypointTags`.

    Think carefully about what `memory` representation your States should have!
    """
    def __init__(
        self, startLocation: str, waypointTags: List[str], endTag: str, cityMap: CityMap
    ):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

        # We want waypointTags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypointTags = tuple(sorted(waypointTags))

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        startingMemory = []
        for i in range(len(self.waypointTags)):
            if self.waypointTags[i] in self.cityMap.tags[self.startLocation]: startingMemory.append(1)
            else: startingMemory.append(0)
        startingMemory = tuple(startingMemory)
        return State(self.startLocation, startingMemory)
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        endReached = self.endTag in self.cityMap.tags[state.location]
        #print(f"Start Location: {self.startLocation}")
        #print(f"End Tag: {self.endTag}")
        #print(f"Waypoint Tags: {self.waypointTags}")
        #print(f"Current State: {state}")
        #print("--------------------------------------------------------------")
        if not endReached: return False
        for element in state.memory:
            if element==0: return False
        return True
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 17 lines of code, but don't worry if you deviate from this)
        returnedArr = []
        for nextLocation, distance in self.cityMap.distances[state.location].items():
            nextState_memory = list(state.memory)
            for i in range(len(self.waypointTags)):
                if self.waypointTags[i] in self.cityMap.tags[nextLocation]: nextState_memory[i] = 1
            nextState_memory = tuple(nextState_memory)
            returnedArr.append((nextLocation, State(nextLocation, nextState_memory + tuple()), distance))
        return returnedArr
        # END_YOUR_CODE


########################################################################################
# Problem 2b: Custom -- Plan a Route with Unordered Waypoints through Stanford


def getStanfordWaypointsShortestPathProblem() -> WaypointsShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `startLocation`/`waypointTags`/`endTag`.

    Similar to Problem 1b, use `readableStanfordMap.txt` to identify potential
    locations and tags.
    """
    cityMap = createStanfordMap()
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    startLocation = "540510207"
    waypointTags = ["amenity=food", "landmark=bookstore", "landmark=evgr_a", "bicycle=yes", "barrier=gate"]
    endTag = "landmark=stanford_stadium"
    # END_YOUR_CODE
    return WaypointsShortestPathProblem(startLocation, waypointTags, endTag, cityMap)


########################################################################################
# Problem 3a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.


def aStarReduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        def startState(self) -> State:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return problem.startState()
            # END_YOUR_CODE

        def isEnd(self, state: State) -> bool:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return problem.isEnd(state)
            # END_YOUR_CODE

        def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
            # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
            succList = problem.successorsAndCosts(state)
            for element in succList:
                element = list(element)
                element[2] += heuristic.evaluate(element[1]) - heuristic.evaluate(state)
                element = tuple(element)
            # END_YOUR_CODE
            return succList
    
    return NewSearchProblem()


########################################################################################
# Problem 3b: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `computeDistance` defined in `mapUtil.py`
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap

        # Precompute
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        self.endLocations = [location for location in self.cityMap.geoLocations.keys() if endTag in self.cityMap.tags[location]]
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        return max([computeDistance(self.cityMap.geoLocations[state.location], self.cityMap.geoLocations[endLocation]) for endLocation in self.endLocations])
        # END_YOUR_CODE


########################################################################################
# Problem 3c: "no waypoints" heuristic for A*


class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `startLocation` to any location with `endTag`,
    ignoring all waypoints.
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        """
        Precompute cost of shortest path from each location to a location with the desired endTag
        """
        # Define a reversed shortest path problem from a special END state
        # (which connects via 0 cost to all end locations) to `startLocation`.
        class ReverseShortestPathProblem(SearchProblem):
            def startState(self) -> State:
                """
                Return special "END" state
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return State("Special END State", None)
                # END_YOUR_CODE

            def isEnd(self, state: State) -> bool:
                """
                Return False for each state.
                Because there is *not* a valid end state (`isEnd` always returns False), 
                UCS will exhaustively compute costs to *all* other states.
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return False
                # END_YOUR_CODE

            def successorsAndCosts(
                self, state: State
            ) -> List[Tuple[str, State, float]]:
                # If current location is the special "END" state, 
                # return all the locations with the desired endTag and cost 0 
                # (i.e, we connect the special location "END" with cost 0 to all locations with endTag)
                # Else, return all the successors of current location and their corresponding distances according to the cityMap
                # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
                returnedArr = []
                if state.location == "Special END State":
                    for endLocation in cityMap.geoLocations.keys():
                        if endTag in cityMap.tags[endLocation]: returnedArr.append((endLocation, State(endLocation, None), 0))
                else:
                    for nextLocation, distance in cityMap.distances[state.location].items(): returnedArr.append((nextLocation, State(nextLocation, None), distance))
                
                return returnedArr
                # END_YOUR_CODE

        # Call UCS.solve on our `ReverseShortestPathProblem` instance. Because there is
        # *not* a valid end state (`isEnd` always returns False), will exhaustively
        # compute costs to *all* other states.
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        ucs = UniformCostSearch(verbose=0)
        problem = ReverseShortestPathProblem()
        ucs.solve(problem)
        # END_YOUR_CODE

        # Now that we've exhaustively computed costs from any valid "end" location
        # (any location with `endTag`), we can retrieve `ucs.pastCosts`; this stores
        # the minimum cost path to each state in our state space.
        #   > Note that we're making a critical assumption here: costs are symmetric!
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        self.heuristicFunction = ucs.pastCosts
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.heuristicFunction[state.location]
        # END_YOUR_CODE
