module Lib
    ( someFunc
    ) where

someFunc :: IO ()
someFunc = putStrLn "someFunc"

neighbour_one_d lst = [ x | x <- [0..length lst - 1], lst !! x == 1]
neighbours node graph = neighbour_one_d (graph !! node)
neighbours_filtered node graph visited =
    let lst = graph !! node in
    [x | x <- [0..length lst-1], lst !! x == 1, not (elem x visited)] 
