Run on cloud with me

import pegasi
import requests, time, math

dash=pegasi.Dash("PASSWORD","HOST")
def test():
	return requests.get("https://ident.me").text
dash.run(test)

#let's do heavy lifting
math.factorial(10000)


d.map(math.factorial,50*[10000])

def pause(x):
	time.sleep(x)
	return time.time()
Yest, you actually run 50 parallel computations in cloud for a moment

d.map(test,50*[1])

