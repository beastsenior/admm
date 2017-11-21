import data
import globle as g
import admm as ad
import topology as tp

tp.init_topology()
data.init_data('Lasso')
for mode_i in range(len(g.L_MODE)):
	tp.topology(mode_i)
	data.data(mode_i)
	ad.admm(mode_i)
	ad.get_min(mode_i)
ad.result('Lasso')

	