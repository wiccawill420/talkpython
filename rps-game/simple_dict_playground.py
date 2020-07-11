"""
lst = [1, 1, 11, 7]
print(lst)
lst.append(2)
print(lst)
lst.remove(11)
print(lst)
lst.sort()
print(lst)

st = {1, 1, 11, 7}
print(st)
st.add(1)
st.add(1)
st.add(1)
st.add(1)
print(st)

d = {
    'bob': 0,
    'sarah': 0,
    'defeated_by': {'paper', 'wolf'},
    'defeats': {'scissors', 'sponge'}
}
print(f"You are defeated by {d['defeated_by']}")
print(d['bob'])
d['bob'] += 1
print(d['bob'])
print(d)
d['billy'] = 7
print(d)

print(d.get('bob', 40))
print(d.get('oranges', 20))
"""

d = {
    'Sam': 7,
    'rolls': ['rock', 'paper', 'scissors'],
    'done': True
}

print(d["Sam"])          # outputs 7
print(d['rolls'])        # outputs ['rock', 'paper', 'scissors']
print(d.get('Sarah'))    # outputs None
print(d.get('Jeff', -1)) # outputs -1
print(d['done'])         # outputs True
