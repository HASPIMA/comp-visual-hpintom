# Three.js
In this implementation, we populate the scene with three geometric objects which are grouped together as meshes in a group. We apply rotation and translation transformations through a slider UI made with Leva on this group (the parent) which, by the hierarchy, also afffects the meshes (the children).

## GIF
![hierarchy](https://github.com/user-attachments/assets/50ab7e85-80aa-47b6-8f03-b9e3c0084697)

## Learning comments
- Having hierarchical tree structures for objects allows us to greatly simplify the process of applying transformations to groups of objects; it allows us to organize them in an intuitive manner and save time by allowing the use of relative coordinates and saving us the need to manually apply the same transformations to different objects.

- Using Leva to include a slider UI presented some problems when we tried to add it directly to the ParentGroup module. We had to include it as a separate module in order for it to work.
