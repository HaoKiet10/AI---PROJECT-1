

import pygame


def switchToHome(index, algo):
    temp = index
    from Home import runHome
    runHome(temp, algo)
    
def switchToMove(screen, board, startPos, stonePos, switchPos, path, weight, index, algo):
    from Move import run
    temp = index
    run(screen, board, startPos, stonePos, switchPos ,path, weight, temp, algo)
    