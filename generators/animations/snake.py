from AnimationBuilder import AnimationBuilder
import random
builder = AnimationBuilder(40)

head_position = 1
apple_position = 0
snake_length = 1

LED_COUNT = 400

while True:
    apple_position = random.randrange(0,LED_COUNT)
    builder.light(apple_position, 230,0,0)
    while head_position != apple_position:
        if head_position < apple_position:
            builder.light(head_position, 230,255,0)
            builder.light(head_position-snake_length-1, 0,0,0)
            head_position += 1
        else:
            builder.light(head_position, 230, 255, 0)
            builder.light(head_position + snake_length + 1, 0, 0, 0)
            head_position -= 1
        builder.update()
    snake_length += 1
    builder.wait(25)

    if snake_length > 11:
        break

builder.done()
