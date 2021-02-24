def generate_paranthesis(oB, cB, n, s=[]):
    if(cB == n):
        print(''.join(s))
        return
    if(oB < n):
        s.append('(')
        generate_paranthesis(oB+1, cB, n, s)
        s.pop()
    if(cB < oB):
        s.append(')')
        generate_paranthesis(oB, cB+1, n, s)
        s.pop()
    return


generate_paranthesis(0, 0, 3)
