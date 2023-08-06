Run on cloud with me


```
import pegasi
import time, math, requests


pwd="eat those french fries and drink cola"
api="https://pcze5.azurewebsites.net/cloudpickle"
api_load="https://pcze5.azurewebsites.net/load"
hash=pegasi.hash(pwd)

dash = pegasi.Dash(pwd,api)

def hello_world(x="world"):
	return "Hello {}!".format(x)




print(dash.run(hello_world))

def timey_wimey(x):
	time.sleep(x)
	return time.time()
print(dash.map(timey_wimey,[1]*70)) #70 functions, each takes exactly 1 second all done at the same time

print(dash.map(timey_wimey,args=[1]*70)) 
print(dash.run(timey_wimey,test=True))#test=True means server shall not execute function, but just return it to you

print(dash.run(timey_wimey,args=[1],save="timey_wimey")) #execute and save
print(dash.run(hello_world,save="hello_world",test=True)) #save without executing

print(dash.run(None,load="timey_wimey",args=[1]))#now we can use function without sending it
print(dash.map(None,load="timey_wimey",args=[1]*70))#weven map

print(dash.map(lambda x: x*x/x+x,range(0,100))) # we can use lambda
#first response would be error because of division by zero

print(dash.filter(lambda t: t % 1 > 0.5,dash.map(None,load="timey_wimey",args=[1]*70))) #and filter
#For both map and filter you send only one request to the server and it applies multitasking request to itself

print(dash.map(lambda a,b: "{} and {}".format(a,b),[["A","B"],["R","B"],["R","D"]],star=True))

#if you have function that accepts more than one argument use star=True

print(requests.get(api_load,params={"hash":hash,"load":"hello_world"}).text)
#you can send get requests to trigger function from anywhere
#TODO: sending args through get requests
```