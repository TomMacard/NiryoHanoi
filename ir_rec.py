
liste_action = []

def ia_rec(l, n, d, i, a):

    if n == 1 :
        l.append((d,a))
    else:
        ia_rec(l, n-1, d, a, i)
        ia_rec(l, 1, d, i, a)
        ia_rec(l, n - 1, i, d, a)

ia_rec(liste_action, 4, 1,2,3)

print(liste_action)