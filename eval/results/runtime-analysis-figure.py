#!/usr/bin/python
import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

mpl.font_manager.USE_FONTCONFIG=True

# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['ps.fonttype'] = 42
# mpl.rcParams['text.usetex'] = True
# from matplotlib import font_manager
# font_manager.USE_FONTCONFIG = True

# flist = mpl.font_manager.get_fontconfig_fonts()
# print flist
# names = [(fname, mpl.font_manager.FontProperties(fname=fname).get_name()) for fname in flist]
# print names


# font = matplotlib.font_manager.FontProperties(family='Fira Sans')
# file = matplotlib.font_manager.findfont(font)
# print file

# print pd.__version__

df = pd.read_csv("runtime-analysis.csv", skipinitialspace=True)

# drop some columns and rows that add clutter
df = df.drop(["comment", "analysis", "browser"], axis=1)

# add Program column that combines all polybench programs into one and gives more readable names
df.loc[df.program == "pspdfkit", "program_group"] = "PSPDFKit"
df.loc[df.program == "UE4Game-HTML5-Shipping", "program_group"] = "Unreal Engine 4"
df.loc[(df.program != "pspdfkit") & (df.program != "UE4Game-HTML5-Shipping"), "program_group"] = "PolyBench (median)"

# add overhead column that is relative to the none execution
for i, row in df.iterrows():
	none_seconds = df[(df.hooks == "none") & (df.program == row.program)].seconds.median()
	df.ix[i, "overhead"] = row.seconds / float(none_seconds)

# df.replace("br_table","   br_table",inplace=True)

# print df[df.hooks == "all"].groupby("program").median()

# or geo mean
# df_ = df.groupby(["hooks", "program"]).median()
# print df_

# custom hooks sort order
df.hooks = pd.Categorical(df.hooks, [
	"none",
	"start",
	"nop",
	"unreachable",	
	"memory_size",
	"memory_grow",
	"select",
	"drop",
	"load",
	"store",
	"call",
	"return",
	"const",
	"unary",
	"binary",
	"global",
	"local",
	"begin",
	"end",
	"if",
	"br",
	"br_if",
	"br_table",
	"all",
])

# print df
# print df.dtypes

sns.set_style("ticks")
sns.set_palette(
	sns.xkcd_palette(["pale red", "medium green", "denim blue"])
	# sns.color_palette("Set1", n_colors=3)
)

fp = mpl.font_manager.FontProperties(fname="/usr/share/fonts/truetype/fira/FiraSans-Regular.ttf")
# print fp
print mpl.font_manager.findfont("Fira Sans")

g = sns.factorplot(x="hooks", y="overhead", hue="program_group", kind="bar", aspect=4, size=4, data=df, legend=False, estimator=sp.stats.gmean,
	errwidth=.5,
	# capsize=.1,
)
g.ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
g.despine(offset=4,bottom=True)
plt.xlabel("Instrumented Hooks", fontproperties=fp, fontsize=11)
plt.ylabel("Relative Runtime", fontproperties=fp, fontsize=11,
#	position=(0,.3)
)
# legend = plt.legend(loc="upper right",bbox_to_anchor=(1.04, 1.07),frameon=1,framealpha=1,prop=fp, fontsize=11)
# legend.get_frame().set_linewidth(0)
plt.tick_params(axis='x', 
	bottom=False, # ticks along the bottom edge are off
	labelbottom=True)
g.ax.yaxis.grid(b=True,which="major",color=".7",linewidth=.5)
g.ax.yaxis.grid(b=True,which="minor",color=".85",linewidth=.5,linestyle="--")
# g.set_xticklabels(rotation=45, ha="center", position=(0,-.02), fontproperties="Inconsolata",fontsize="11", rotation_mode="anchor")
g.set_xticklabels(fontproperties="Inconsolata",fontsize="10",
	rotation=45,
	position=(0,0.05)
)
g.set_yticklabels(g.ax.get_yticks(), fontproperties=fp)

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

# change_width(g.ax, .25)

g.savefig("runtime-analyis.pdf")