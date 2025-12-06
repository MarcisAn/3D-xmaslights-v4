from AnimationBuilder import AnimationBuilder

builder = AnimationBuilder(30)

# Piekļuve koordinātām
# builder.cords[led_index][0] # X koordināta
# builder.cords[led_index][1] # Y koordināta
# builder.cords[led_index][2] # Z koordināta


# Iedegt lampiņu
# RGB vērtības ir skaitļi no 0 līdz 255
# builder.light(led_index, red, green, blue)

# Saglabāt animācijas kadru
# builder.update()

# Pabeigt animāciju
# builder.done()


# Zemāk esošais kods pakāpeniski iededzina visas lampiņas sarkanā krāsā
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
