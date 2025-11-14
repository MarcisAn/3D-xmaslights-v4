from AnimationBuilder import AnimationBuilder

builder = AnimationBuilder()

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
for i in range(400):
    builder.light(i, 255, 0, 0)
    builder.update()

builder.done()
