from Esercizi_2set.Es3_1  import *

def main():
    """
     Sappiamo che:
        K1+ = <3,n>  , dunque e1=3
        K2+ = <5,n>  , dunque e2=5
        n è lo stesso per tutti e 2


    """

    c1 = 82819140145469  # primo ciphertext intercettato
    c2 = 157356442552819173976949  # secondo ciphertext intercettato
    e1 = 3
    e2 = 5
    # modulo RSA utilizzato per la creazione di entrembe le coppie di chiavi (cosa da NON fare mai)
    n = 112137763021160565141095447514289188316099305050728548533990009459340088478604617874283528379792371687919406014282922583771903203542840497778554663219496576912001458191643798008255064443259316602248816694007897022508299325243314145599359546048231178850144548579269422836638239848102178140850949393175535681977

    # calcolo i coefficienti x,y tali che d = mcd(d1,d2) = d1*x +d2*y
    _,x,y = egcd(e1,e2)

    # calcolo del plaintext basato sull'identità di Bezout
    m = ((c1 ** x) * (c2 ** y)) % n
    m = int(m)
    print(m)

    # encryption del messaggio con la prima chiave per verifica
    t1 = (m ** 3) % n
    t1 = int(t1)
    print(t1 == c1)

    # encryption del messaggio con la seconda chiave per verifica
    t2 = (m ** 5) % n
    t2 = int(t2)
    print(t2 == c2)


if __name__ == '__main__':
    main()
