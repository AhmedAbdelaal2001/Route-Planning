# Route-Planning
## Description
Creating a route planning system is akin to Google Maps; the objective is to find the optimal path between two locations, and to allow for more complex queries. For instance, not only can you find the shortest path from the Psychiatry Parking Lot to the Stadium, but you can also ask to stop by a bookstore and a restaurant along the way, allowing for some very interesting results. Answers can be found in **submission.py**

## Shortest Paths
Uniform Cost Search (UCS) is used to find the compute the optimal path between the start and end tags. The realization of this problem can be found in the **ShortestPathProblem** class. To see the results, follow the following procedure:
- Run **python mapUtil.py > readableStanfordMap.txt** to generate a text file of the possible locations and their tags.
- Choose a starting location and an end tag, and implement the **getStanfordShortestPathProblem** function accordingly.
- Run **python grader.py 1b-custom** to generate path.json.
- Run **python visualization.py**.
A sample of the results is shown below:

![image](https://github.com/AhmedAbdelaal2001/Route-Planning/assets/101427765/1b6c20a2-942d-46a5-84b5-2a43ac0560c6)

## Unordered Waypoints
The state definition is adjusted to allow for unordered waypoints, which can be seen in the **WaypointsShortestPathProblem** class. To see the results, follow the following procedure:
- Choose a starting location, an end tag, and a set of intermediary stops, then implement the **getStanfordWaypointsShortestPathProblem** function accordingly.
- Run **python grader.py 2c-custom** to generate path.json.
- Run **python visualization.py**.
A sample of the results is shown below:
![image](https://github.com/AhmedAbdelaal2001/Route-Planning/assets/101427765/3e986dfd-5143-4129-8f45-ba3e6a6ada61)

## Speeding up With A*
Two heuristics are implemented for use in the A* algorithm to speed up the process and allow for extremely quick queries. The heuristics are as follows:
- **StraightLineHeuristic** computes the straight line distance between the startTag and closest location having the endTag.
- **NoWaypointsHeuristic** computes the shortest path while ignoring the intermediary waypoints, akin to the first part.
The **NoWaypointsHeuristic**, in particular, seems to speed up the computation significantly.




