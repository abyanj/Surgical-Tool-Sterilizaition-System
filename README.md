# Surgical-Tool-Sterilizaition-System
by: Abyan Jaigirdar


# Executive Summary
The aim of the project was to design a system which included a container and a computer program which would enable the sterilization of a
surgical tool. In order to effectively accomplish each task, the project was divided and tackled by two sub
teams. Each sub team was responsible for a part in the project. The modeling sub team was responsible for the
apparatus which would hold the tool while it is being sterilized . The computing sub team was responsible
for creating a computer program for the robotic arm to move the container to the autoclave for sterilization .
In order to design an appropriate container, it had to fulfill specific requirements, such as: it had to allow
for sterilization, hold the tool in place within the container and allow the container to be easily picked up by QArm. The problem was approached by designing a series
of containers and making slight improvements to each one, until the desired container was finally achieved. The container was designed in such a way that it imitated
the shape of the tool, as well it had a fitted shape; this prevented the tool from moving and rattling while it was
being transported to the autoclave. Additionally, the container has a lid that is held down by two clips. The clips
ensure that the lid will remain attached to the container during transportation and sterilization. Furthermore, the
container has no holes that are large enough for the tool to fall through when the lid is closed. However, there is
a sufficient number of holes which would allow the tool to be successfully sterilized. Since this is the case, the
tool is effectively secured in the container for transportation and is able to undergo sterilization.

In order to operate said robotic arm, a computer program was to be designed. The program utilizes
muscle sensors that emulate each mechanism of the arm (such as its gripper, waist, base and so on) in order to
transfer the container containing the surgical instrument. The intricacies of the program needed to contain
functions that individually controlled the gripper, moving to the desired drop-off location given a random
container, opening/closing the autoclave bin drawer and a method in which the inventory was evaluated to
determine whether the program should terminate. By using the built-in functions given from the python library,
the computing sub-team was able to identify the locations of each autoclave and write the coordinates into
functions which can be called. The inventory evaluation was done by a means of evaluating a Boolean list, each
index corresponding to a specific container. If all index's in the list were True, the program would exit
