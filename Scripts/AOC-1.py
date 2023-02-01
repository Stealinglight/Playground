from AOC_1_list import calories as elf_calories

current_elf = 0

max_calories = max(elf_calories)
max_elf = elf_calories.index(max_calories)

print("The Elf carrying the most calories is Elf", max_elf + 1, "with a total of", max_calories, "calories.")
