def rcaptcha(number):
  snumber = str(number)
  return sum([int(a) for a,b in zip(snumber, snumber[1:]+snumber[0]) if a==b])

