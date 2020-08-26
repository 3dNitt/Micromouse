# Micromouse
#### Table of Contents:
1. [Introduction](#about)
2. [Algorithm](#algorithm)
		* Modified flodd algo(#modified-floodfill-algorithm)
3. [Simulator](#Micromouse-Maze-Simulator)

# About
Micromouse is an event where small robot mice solve a 16×16 maze. It began in the late 1970s.[1] Events are held worldwide, and are most popular in the UK, U.S., Japan, Singapore, India, South Korea and becoming popular in subcontinent countries such as Sri Lanka.

The maze is made up of a 16×16 grid of cells, each 180 mm square with walls 50 mm high.[2] The mice are completely autonomous robots that must find their way from a predetermined starting position to the central area of the maze unaided. The mouse needs to keep track of where it is, discover walls as it explores, map out the maze and detect when it has reached the goal. Having reached the goal, the mouse will typically perform additional searches of the maze until it has found an optimal route from the start to the finish. Once the optimal route has been found, the mouse will run that route in the shortest possible time.

We participated in the competition in __Dec2019-Jan2020__ at 2 places:
  * Techfest, IITB.
  * IITM.
## Modified Floodfill Algorithm
Download [this pdf](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjemOqZpbjrAhW94HMBHVcxDhQQFjABegQICxAD&url=http%3A%2F%2Fijcte.org%2Fpapers%2F738-T012.pdf&usg=AOvVaw2uW4zsDibyeHgYuILskI9J) to get insight of the algorithm.

# Algorithms
We used following things in our programming:
	* Flood fill algorithm
	* Bit masking
	* PID control
## Micromouse Maze Simulator
You can find about the simulator [here](https://mmsim.readthedocs.io/en/stable/).
