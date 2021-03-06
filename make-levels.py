import pickle

levels = []

levels.append([{"x": 700, "y": 300, "signals": [[0,0],[0,1],[0,2]]}])

levels.append([{"x": 700, "y": 300, "signals": [[0,2],[0,3],[0,4]]},
            {"x": 800, "y": 200, "signals": [[0,0],[0,2],[0,4]]},
            {"x": 800, "y": 400, "signals": [[0,5],[0,6],[0,7]]}])

levels.append([{"x": 700, "y": 300, "signals": [[0,1],[0,2],[0,3]]},
            {"x": 800, "y": 200, "signals": [[1,1],[1,2],[1,3]]},
            {"x": 800, "y": 300, "signals": [[1,2],[1,4],[1,7]]},
            {"x": 800, "y": 400, "signals": [[1,2],[1,3],[0,4]]},
            {"x": 900, "y": 300, "signals": [[2,2],[2,3],[2,4]]}])

levels.append([{"x": 700, "y": 300, "signals": [[0,3],[1,4],[2,5]]},
            {"x": 800, "y": 300, "signals": [[0,2],[0,3],[0,4]], "disrupt": True},
            {"x": 900, "y": 300, "signals": [[3,7],[4,7],[5,7]]}])

levels.append([{"x": 700, "y": 200, "signals": [[1,4],[2,5],[3,6]]},
            {"x": 700, "y": 400, "signals": [[3,4],[2,5],[1,6]]},
            {"x": 800, "y": 300, "signals": [[0,1],[0,2],[0,3]], "broken": {0}}])


pickle.dump(levels, open("JOCProject\spacegem-python\levels", "wb"))
