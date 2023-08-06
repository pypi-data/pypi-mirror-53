from ethics.plans.semantics import *

a = Action("test1", dict(), [{"condition":dict(), "effect":{"eff":True}}], "neutral")
b = Action("test2", dict(), [{"condition":dict(), "effect":{"duh":False}}], "neutral")

p = Plan([a, b])
print(p)

print("*"*20)
e = p.compute_all_epsilon_alternatives()
print(e)
for pp in e:
    print("original", p)
    print(type(pp), pp)
    
print("*"*20)

e = p.compute_all_effect_alternatives({"eff": True})
print(e)
for pp in e:
    print([a.eff for a in pp.endoActions])
    
print("*"*20)


