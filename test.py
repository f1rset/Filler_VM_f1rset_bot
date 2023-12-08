with open('map60', 'w') as file:
    for i in range(60):
        for j in range(60):
            file.write('.')
        file.write('\n')