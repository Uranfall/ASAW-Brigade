
# General Information About the Project
## README.md
Here we can add info about the project, like notes about how to use our code.
Feel free to add stuff here.

# Debugging
## How to Use Debug Entities
You can find the code for debug entities in: [graphics/Debug_Entities.py](graphics/Debug_Entities.py).
To show the debug entity, you should add it to ```ui_data.ui_entities```. This will make sure that the entity is deleted after some time.
When you want to visualize something, you can access [ui_data](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/main.py#L17) through ```DebugGlobal.ui_data```.
```
DebugGlobal.ui_data.ui_entities.append(DebugBox([YOUR_BOX_DATA], stay_alive_for=1))
```
This example will create a box that will be deleted after about a second.
If you want the object to stay for longer/shorter period of time, you can change the ```stay_alive_for``` setting.
**If you don't set ```stay_alive_for```, the object will stay on screen forever.**

# Shared Utility
## [```sign(num: float)```](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/shared_utility.py#L5)
### General
This function returns the sign of the number it is given.
### Input
```a number```
### Output
```1 if the number is positive, -1 if negative, and 0 if the number is 0.```

## [```angle_to_vector(angle: float, distance=1.0)```](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/shared_utility.py#L9)
### General
The function turns any angle you give it into a direction.
### Input
```
angle (degrees)
distance (set to 1 by default)
```
### Output
```direction (offset_x, offset_y).```

## [```vector_to_angle(vector: list[float, float] | tuple[float, float])```](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/shared_utility.py#L17)
### General
The function gets a direction and turns it into an angle.
### Input
```Direction (offset_x, offset_y)```
### Output
```angle (degrees)```

## [```lerp(start: float | Sequence[float], end: float | Sequence[float], factor: float)```](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/shared_utility.py#L60)
### General
"lerp" is short for [linear interpolation](https://en.wikipedia.org/wiki/Linear_interpolation).
This function helps you smoothly transition between numbers, positions, colors, and anything else that is a number or an array of them.
### Input
```
number\array A
number\array B
factor (how much B you want in A. 0 is 100% A and 1 is 100% B while 0.5 is inbetween).
```
### Output
```
number\array
```

## [```ValueCurve```](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/shared_utility.py#L66)
### General
It is simmilar to lerp, but you are allowed to have as many points as you want.
It is useful if you want to make an animation.
### How to Use
You first have to create the curve.
```
curve = ValueCurve((0, 0), (1, 0.5), (0, 1))  # This curve will go from 0 to 1 and then to 0 again.
curve2d = ValueCurve(((0, 0), 0), ((1, 0), 1), ((1, 1), 2), ((0, 1), 1))  # This curve will go along a 1x1 square.
```
After you create the curve, you call it and give it the distance you want to advance along it.
```
t = 0.25
output = curve(t)  # the output is 0.5.
```


# UI & Graphics
## [Camera](https://github.com/Uranfall/ASAW-Brigade/blob/5b21f7d9e2bb3996ee56261182602a147fca1666/graphics/graphics_utility.py#L10)
The camera helps convert coordinates on the map to coordinates on the screen, and the other way too.
### Accessing Camera
You can access camera from ```ui_data.camera```, or as input for ```Entity.draw```.
### Map Coordinates vs Screen Coordinates
In pygame, when you increase the y-position of the object, the object moves down. The coordinates (0, 0) are at the top-left of the screen.
This is very inconvinient, so the camera flips the y axis and moves all the objects by half the screen size, so they appear at the center.
The camera can also move, when that happens, all the objects are moved to the opposite direction.
### Converting to screen from map
To convert map coordinates to screen, you can call camera directly.
```
camera(x, y)
```
or
```
camera(*coordinates)
```
If you input only one number, the camera will just resize the number.
```
real_scale = 30.0
screen_scale = camera(real_scale)
```
### Converting to map from screen
Conversion from screen coordinates to map works the same as map to screen, except you should use ```camera.screen_to_global```.

### A little drawing of camera converting map coordinates into screen coordinates
<img width="554" height="275" alt="image" src="https://github.com/user-attachments/assets/fd1a8b96-eaeb-48af-b7cc-1639b8663060" />
