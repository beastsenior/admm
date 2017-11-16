import data
import globle as g
import admm as ad
import topology as tp

tp.topology()
for problem in g.L_PROBLEM:
	data.data(problem)
	for mode in g.L_MODE:
		ad.admm(problem, mode)
	ad.result(problem)

	