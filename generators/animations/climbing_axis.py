from AnimationBuilder import AnimationBuilder

builder = AnimationBuilder(30)


for slider in range(-50,110, 5):
    for i in range(400):
        if builder.cords[i][0] < slider:
            builder.light(i, 255, 0, 0)
        if builder.cords[i][0] < slider - 20:
            builder.light(i, 0, 0, 0)
    builder.update()

for slider in range(-50, 100, 5):
    for i in range(400):
        if builder.cords[i][1] < slider:
            builder.light(i, 0, 255, 0)
        if builder.cords[i][1] < slider - 20:
            builder.light(i, 0, 0, 0)
    builder.update()

for slider in range(0, 200, 5):
    for i in range(400):
        if builder.cords[i][2] < slider:
            builder.light(i, 0, 0, 255)
        if builder.cords[i][2] < slider - 20:
            builder.light(i, 0, 0, 0)
    builder.update()
builder.done()
