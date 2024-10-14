
# Read the input
lines = []
while True:
    try:
        line = input()
        if not line:
            # An empty line indicates the end of an Elf's inventory
            lines.append('')
        else:
            # Add the line to the input list
            lines.append(int(line))
    except EOFError:
        # Stop reading input when there is no more input
        break

# Parse the input to create a list of the Calories carried by each Elf
calories = []
current_elf = 0
current_calories = 0
for line in lines:
    if line == '':
        # Add the current Elf's calories to the list and reset the current Elf and calories
        calories.append(current_calories)
        current_elf += 1
        current_calories = 0
    else:
        # Add the line to the current Elf's calories
        current_calories += line

# Sort the list of Elf Calories in descending order
calories.sort(reverse=True)

# Find the top three Elves carrying the most Calories
top_calories = calories[:3]

# Output the total Calories carried by the top three Elves carrying the most Calories
print(sum(top_calories))
