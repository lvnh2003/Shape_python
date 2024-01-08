import pygame
import numpy as np
from math import * 
WHITE = (255,255,255)
RED  = (255,0,0)
BLACK = (0,0,0)
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("Cube Rectangle")
screen = pygame.display.set_mode((WIDTH,HEIGHT))
points = []
angle = 0
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])
projected_points = [
    [n, n] for n in range(len(points))
]
clock = pygame.time.Clock()
def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.01
    screen.fill(WHITE)
    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z,point.reshape((3,1)))
        rotated2d = np.dot(rotation_y,rotated2d)
        rotated2d = np.dot(rotation_x,rotated2d)
        projected2d = np.dot(projection_matrix,rotated2d)
        x = int(projected2d[0][0] * 100) + WIDTH/2
        y = int(projected2d[1][0] * 100) + HEIGHT/2

        projected_points[i] = [x,y]
        pygame.draw.circle(screen, BLACK, (x,y), 5)
        i +=1
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    pygame.display.update()