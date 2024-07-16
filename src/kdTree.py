import statistics, math
from binaryTree import Node as BT


def build_kdtree(particles):
    if not particles:
        return None

    median_index = len(particles) // 2
    median_point = sorted(particles, key=lambda p: p[0])[median_index]
    left_points = [p for p in particles if p[0] < median_point[0]]
    right_points = [p for p in particles if p[0] > median_point[0]]
    return BT(median_point, build_kdtree(left_points), build_kdtree(right_points))







    return initial_y_split

