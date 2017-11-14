import data
import globle as g
import admm as ad
import topology as tp

tp.topology()
for problem in g.PROBLEM:
	data.data(problem)
	for mode in g.MOA:
		ad.admm(mode,problem)
	ad.result(g.MOA, problem)

	