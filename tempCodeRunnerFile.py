def draw_cubes(cube_list,water_list):
    for cube in cube_list:
        cube.gravity(screen)
        if cube.pos.y>=710:
            cube_list.pop(cube_list.index(cube))
        for waters in water_list:
            if cube.rect.colliderect(waters.rect):
                waters.speed+=cube.speed*0.1