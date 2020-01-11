from test.api.test_api import SolvedExercise
import json

def load_exercises(exercises_path):
    with open(exercises_path, 'r') as exercises_file:
        exercises_json = json.load(exercises_file)
        exercises = []
        for exercise_json in exercises_json:
            exercise = SolvedExercise(name=exercise_json["name"], steps=exercise_json["steps"],
                                      result=exercise_json["result"])
            exercises.append(exercise)
        return exercises



