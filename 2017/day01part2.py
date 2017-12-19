def rcaptcha(number):
  snumber = str(number)
  lhalf = len(snumber)/2
  return sum([int(a) for a,b in zip(snumber, snumber[lhalf:]+snumber[:lhalf]) if a==b])

