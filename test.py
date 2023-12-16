with open('map40', 'w') as file:
    for i in range(40):
        for j in range(40):
            file.write('.')
        file.write('\n')