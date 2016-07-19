def menu(menu_points):

    print ('please choose from the following options:')

    for point in menu_points:
        print ("%i.: %s" % (menu_points.index(point)+1, point) )
    print ("press 'x' to exit")

    user_input = int(input())
    return user_input