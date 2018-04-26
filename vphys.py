# ------------------------------- Information ------------------------------- #
# Author:       Joey Dumont                    <joey.dumont@gmail.com>        #
# Created       Mar. 1st, 2018                                                #
# Description:  Misc configuration for NumPy, SciPy and matplotlib.           #
# Dependencies: - NumPy                                                       #
#               - Scipy                                                       #
#               - Matplotlib                                                  #
# --------------------------------------------------------------------------- #

# ----------------------------- Misc. Functions ----------------------------- #
def mkdir_p(mypath):
  """
  Creates a directory. equivalent to using mkdir -p on the command line
  """

  from errno import EEXIST
  from os import makedirs,path

  try:
      makedirs(mypath)
  except OSError as exc: # Python >2.5
      if exc.errno == EEXIST and path.isdir(mypath):
          pass
      else: raise


# --------------------------- matplotlib Functions -------------------------- #
def adjust_spines(ax, spines, points_outward=10):
  """
  Helps in re-creating the spartan style of Jean-luc Doumont's graphs.

  Removes the spines that are not specified in spines, and colours the specified
  ones in gray, and pushes them outside the graph area.
  """
  for loc, spine in ax.spines.items():
      if loc in spines:
          spine.set_position(('outward', points_outward))  # outward by 10 points
          #spine.set_smart_bounds(True)
          spine.set_color('gray')
      else:
          spine.set_color('none')  # don't draw spine

  # turn off ticks where there is no spine
  if 'left' in spines:
      ax.yaxis.set_ticks_position('left')
  else:
      # no yaxis ticks
      ax.yaxis.set_ticks([])

  if 'bottom' in spines:
      ax.xaxis.set_ticks_position('bottom')
  else:
      # no xaxis ticks
      ax.xaxis.set_ticks([])


def default_pgf_configuration():
  """
  Defines a default configuration for the pgf engine of matplotlib, with
  LaTeX support.
  """
  pgf_with_pdflatex = {
   		"font.family": "serif", # use serif/main font for text elements
   		"text.usetex": True,    # use inline math for ticks
   		"pgf.rcfonts": False,   # don't setup fonts from rc parameters
   		"pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{siunitx}",
        #r"\usepackage{mathspec}",
        r"\usepackage[charter]{mathdesign}",
        r"\usepackage{fontspec}",
        #r"\setmathfont{Fira Sans}",
        r"\setmainfont{Oswald}",
        ]
  }

  return pgf_with_pdflatex

def BarPlotWithLogAxes(ax_handle,x,y,width, xdelta=0.0, **plot_kwargs):
    """
    This plots a bar graph with a log-scaled x axis by manually filling rectangles.
    We use the
    """
    import matplotlib.pyplot as plt
    import numpy as np
    for i in range(len(x)):
        artist, = ax_handle.fill([10**(np.log10(x[i])-width-xdelta), 10**(np.log10(x[i])-width-xdelta), 10**(np.log10(x[i])+width-xdelta),10**(np.log10(x[i])+width-xdelta)], [0, y[i], y[i], 0],**plot_kwargs)

    return artist

# ------------------------------ MPI Functions ------------------------------ #
def GenerateIndicesForDifferentProcs(nprocs, loopsize):
  """
  Generates a list that contains the elements of the loops that each
  rank will process. In the case that the number of processors does not divide
  the loop size, We divide the rest of the work amongst the first (loopsize % nprocs)
  processors.
  """
  rank = MPI.COMM_WORLD.Get_rank()
  if (nprocs <= loopsize):
    sizes        = divmod(loopsize,nprocs)
    indices_rank = np.empty((sizes[0]), dtype=int)

    for i in range(sizes[0]):
      indices_rank[i] = rank*sizes[0]+i

    if MPI.COMM_WORLD.Get_rank() < sizes[1]:
      indices_rank = np.append(indices_rank, nprocs+MPI.COMM_WORLD.Get_rank())

  elif (nprocs > loopsize):
    indices_rank = None

    if rank < loopsize:
      indices_rank = np.array([rank])

  return indices_rank

# ------------------------ Cluster-Related Functions ------------------------ #

def ListSimulationDirectories(bin_dir):
  """
  We count the number of directory that end in \d{5}.BQ. This gives us the
  number of simulation that we ran, and also their names.
  """
  import os
  import re
  dirList = [f for f in os.listdir(bin_dir) if re.search(r'(.*\d{5}.BQ)', f)]

  sortedList = sorted(dirList, key=str.lower)

  for i in range(len(sortedList)):
    sortedList[i] += "/{:05g}.BQ/".format(i+1)

  return sortedList

# -------------------------- matplotlib variables --------------------------- #

# -- morgenstemning colormap
# https://www.osapublishing.org/DirectPDFAccess/1A428D10-90A3-7D1F-A46F3712F727F357_252779/oe-21-8-9862.pdf
import matplotlib as mpl
morgen_colors=[[0.0, 0.0, 0.0],
               [0.0003007843137254902, 0.004015294117647059, 0.005722352941176471],
               [0.0005015686274509805, 0.007930588235294118, 0.011444705882352942],
               [0.0007035294117647059, 0.011845882352941177, 0.017168235294117647],
               [0.0010047058823529412, 0.015759607843137256, 0.022989411764705883],
               [0.0013058823529411765, 0.019576470588235292, 0.028713725490196077],
               [0.0016094117647058822, 0.023491764705882354, 0.034534117647058826],
               [0.002010980392156863, 0.027404313725490195, 0.04025921568627451],
               [0.002412549019607843, 0.031219215686274508, 0.04608196078431372],
               [0.0028141176470588237, 0.03503411764705883, 0.051904705882352936],
               [0.0032196078431372547, 0.038849019607843135, 0.057727450980392156],
               [0.0037215686274509802, 0.04266392156862745, 0.06355019607843138],
               [0.004223529411764706, 0.04647411764705882, 0.0693729411764706],
               [0.0047305882352941175, 0.05018862745098039, 0.0751956862745098],
               [0.005332941176470589, 0.053903137254901964, 0.08102392156862745],
               [0.0059352941176470594, 0.05761764705882353, 0.08694705882352942],
               [0.006543921568627451, 0.061325882352941175, 0.09287019607843137],
               [0.007246666666666667, 0.06494, 0.09879333333333333],
               [0.007949411764705882, 0.06854705882352942, 0.1047164705882353],
               [0.008659607843137256, 0.07206823529411766, 0.11063960784313726],
               [0.009462745098039215, 0.07568235294117646, 0.11656274509803922],
               [0.010274117647058822, 0.07928823529411765, 0.12248588235294117],
               [0.011177647058823528, 0.08280196078431372, 0.12840901960784315],
               [0.012081176470588236, 0.0863156862745098, 0.1343411764705882],
               [0.012994117647058823, 0.0898294117647059, 0.14035529411764705],
               [0.013998039215686275, 0.09333333333333334, 0.14627843137254903],
               [0.015001960784313725, 0.09675686274509804, 0.15221176470588235],
               [0.016016470588235295, 0.10025999999999999, 0.15822470588235293],
               [0.01712078431372549, 0.1036843137254902, 0.16415882352941177],
               [0.01823647058823529, 0.10718666666666667, 0.17017098039215686],
               [0.019441176470588233, 0.1106, 0.17609411764705885],
               [0.020645882352941177, 0.11401333333333333, 0.18201725490196077],
               [0.021850588235294118, 0.11743921568627451, 0.18794039215686273],
               [0.023068235294117646, 0.12095294117647058, 0.1938505882352941],
               [0.024373333333333334, 0.12446666666666667, 0.19968666666666665],
               [0.02567843137254902, 0.12798039215686274, 0.20559607843137254],
               [0.02699764705882353, 0.13149411764705882, 0.21143294117647057],
               [0.02840313725490196, 0.13499333333333333, 0.217341568627451],
               [0.029808627450980393, 0.13840666666666668, 0.2231792156862745],
               [0.03122941176470588, 0.14182, 0.22908705882352942],
               [0.03275098039215686, 0.14521764705882353, 0.23492549019607842],
               [0.03437333333333333, 0.14853058823529414, 0.2408486274509804],
               [0.03608, 0.1518435294117647, 0.24677176470588236],
               [0.03780352941176471, 0.15513960784313727, 0.25271176470588236],
               [0.039627843137254905, 0.1583349019607843, 0.25871803921568626],
               [0.04153529411764706, 0.16146470588235293, 0.26464117647058827],
               [0.043460784313725485, 0.16465921568627453, 0.27056431372549017],
               [0.04548705882352941, 0.16778980392156864, 0.2764874509803922],
               [0.047595294117647055, 0.1710023529411765, 0.28239176470588234],
               [0.049722745098039214, 0.1742149019607843, 0.28821450980392155],
               [0.05195098039215686, 0.17740784313725488, 0.2940372549019608],
               [0.05428, 0.18052, 0.29985999999999996],
               [0.05670980392156863, 0.1835913725490196, 0.3056827450980392],
               [0.059261176470588234, 0.1865027450980392, 0.3115262745098039],
               [0.061992941176470584, 0.18937176470588235, 0.3174494117647059],
               [0.06482549019607843, 0.19208235294117648, 0.3233725490196078],
               [0.06778078431372549, 0.19479294117647059, 0.3292956862745098],
               [0.07091529411764706, 0.19745882352941174, 0.33519647058823526],
               [0.07419607843137256, 0.19994588235294117, 0.341064705882353],
               [0.07775607843137256, 0.20228588235294118, 0.34706509803921565],
               [0.08154117647058823, 0.2043705882352941, 0.35301176470588236],
               [0.08562862745098039, 0.20630666666666667, 0.35903529411764706],
               [0.09004274509803921, 0.20791607843137255, 0.36505882352941177],
               [0.09490941176470588, 0.20909764705882353, 0.3711317647058823],
               [0.10045607843137254, 0.20972509803921568, 0.3773560784313726],
               [0.1068843137254902, 0.20980000000000001, 0.3835294117647059],
               [0.11404117647058824, 0.20977411764705883, 0.3894494117647059],
               [0.12172823529411765, 0.20967372549019608, 0.39501882352941176],
               [0.12996666666666667, 0.20954666666666666, 0.40036000000000005],
               [0.13860823529411764, 0.20931882352941178, 0.40539882352941176],
               [0.14768039215686274, 0.20899019607843136, 0.4101352941176471],
               [0.15720078431372547, 0.2085886274509804, 0.4145972549019608],
               [0.1670235294117647, 0.20815882352941176, 0.4188294117647059],
               [0.17712, 0.20765686274509804, 0.4227878431372549],
               [0.1874470588235294, 0.2071258823529412, 0.4264866666666666],
               [0.1980764705882353, 0.20649411764705883, 0.4298411764705882],
               [0.20900823529411766, 0.20576156862745099, 0.4329643137254902],
               [0.2202121568627451, 0.20492823529411766, 0.4358152941176471],
               [0.2315870588235294, 0.20399411764705883, 0.43843411764705886],
               [0.2430937254901961, 0.20295921568627454, 0.440781568627451],
               [0.2547392156862745, 0.2018235294117647, 0.44292745098039216],
               [0.26638470588235297, 0.20061882352941177, 0.4449035294117647],
               [0.2780945098039216, 0.19934980392156865, 0.4467145098039216],
               [0.2899407843137255, 0.1979443137254902, 0.44828823529411765],
               [0.30182000000000003, 0.1965058823529412, 0.4496952941176471],
               [0.31376666666666664, 0.19493333333333332, 0.4508666666666667],
               [0.3257470588235294, 0.1931929411764706, 0.4519035294117647],
               [0.33779411764705886, 0.19135176470588236, 0.4527729411764706],
               [0.3498756862745098, 0.18940980392156864, 0.45350705882352943],
               [0.36198823529411767, 0.1873321568627451, 0.45407450980392156],
               [0.3740352941176471, 0.1851235294117647, 0.4545411764705882],
               [0.3860466666666667, 0.1828435294117647, 0.4549070588235294],
               [0.3979572549019608, 0.18039803921568628, 0.4551721568627451],
               [0.4098035294117647, 0.17788823529411765, 0.45537294117647054],
               [0.42161294117647063, 0.17537843137254902, 0.455536862745098],
               [0.4332843137254902, 0.17283137254901962, 0.4556],
               [0.44479176470588233, 0.17025882352941174, 0.4556],
               [0.45619843137254906, 0.1677870588235294, 0.4555619607843137],
               [0.4675043137254902, 0.16537764705882355, 0.455461568627451],
               [0.4787094117647059, 0.16296823529411764, 0.4553223529411765],
               [0.4898137254901961, 0.16055882352941178, 0.45512156862745096],
               [0.5007776470588235, 0.15810980392156862, 0.4549207843137255],
               [0.51162, 0.15564, 0.45471999999999996],
               [0.5224219607843137, 0.15323058823529412, 0.45447882352941177],
               [0.533123137254902, 0.15082117647058824, 0.4541776470588235],
               [0.5437235294117647, 0.14841176470588235, 0.45383529411764706],
               [0.554264705882353, 0.14600235294117647, 0.4534337254901961],
               [0.5647639215686275, 0.1435929411764706, 0.4530321568627451],
               [0.5751623529411765, 0.14122588235294117, 0.4525882352941176],
               [0.5854600000000001, 0.13891686274509804, 0.45208627450980393],
               [0.5957, 0.1366078431372549, 0.4515843137254902],
               [0.6058529411764706, 0.13429882352941178, 0.45108235294117643],
               [0.6158921568627451, 0.13198980392156864, 0.45062431372549017],
               [0.6258870588235295, 0.1296807843137255, 0.45017843137254904],
               [0.6357811764705883, 0.12737176470588235, 0.44972117647058824],
               [0.6455745098039215, 0.1251078431372549, 0.4492745098039216],
               [0.6553125490196079, 0.12294470588235294, 0.44877254901960784],
               [0.6650047058823529, 0.12088235294117647, 0.4482705882352941],
               [0.6745960784313725, 0.11896705882352941, 0.4477686274509804],
               [0.6840866666666667, 0.11716, 0.44722],
               [0.6935235294117648, 0.1154, 0.44666470588235296],
               [0.7029129411764705, 0.1137407843137255, 0.44611529411764705],
               [0.7122494117647059, 0.11223019607843138, 0.4455129411764706],
               [0.7215376470588235, 0.11092117647058823, 0.4449105882352941],
               [0.7307250980392157, 0.10976509803921569, 0.4442596078431372],
               [0.7399098039215686, 0.10875882352941177, 0.4435078431372549],
               [0.7490964705882353, 0.10795411764705883, 0.44265529411764704],
               [0.7582819607843136, 0.10745058823529412, 0.4416521568627451],
               [0.7675180392156862, 0.10830392156862745, 0.44009607843137255],
               [0.7767035294117648, 0.11127294117647059, 0.4377847058823529],
               [0.7858901960784314, 0.11585098039215687, 0.43491960784313727],
               [0.7950235294117647, 0.12173921568627452, 0.43149921568627453],
               [0.8040070588235294, 0.12862705882352943, 0.42768117647058823],
               [0.8129419607843137, 0.13637686274509803, 0.4235572549019608],
               [0.8217192156862745, 0.14518705882352942, 0.4189776470588235],
               [0.8302999999999999, 0.15489411764705882, 0.41405294117647057],
               [0.8386733333333334, 0.16509333333333331, 0.4089266666666667],
               [0.8468517647058824, 0.17570235294117648, 0.40359882352941173],
               [0.8548211764705882, 0.1869235294117647, 0.398015294117647],
               [0.8625427450980392, 0.19885019607843138, 0.39212941176470584],
               [0.8699529411764706, 0.2115372549019608, 0.3858862745098039],
               [0.877070588235294, 0.22486470588235294, 0.3793505882352941],
               [0.8839309803921569, 0.23864039215686272, 0.37255764705882355],
               [0.8904890196078432, 0.2527070588235294, 0.365518431372549],
               [0.8968011764705882, 0.26680588235294117, 0.3583905882352941],
               [0.9029117647058824, 0.28091764705882355, 0.3512058823529412],
               [0.9087635294117647, 0.2951874509803922, 0.343863137254902],
               [0.9143129411764706, 0.30965882352941176, 0.3363764705882353],
               [0.9195599999999999, 0.324389803921569, 0.32867294117647056],
               [0.924504705882353, 0.3394231372549019, 0.32078392156862745],
               [0.9291470588235294, 0.35469999999999996, 0.31273529411764706],
               [0.9334278431372549, 0.370178431372549, 0.3044850980392157],
               [0.9373650980392156, 0.38591803921568624, 0.29597372549019607],
               [0.9410000000000001, 0.4019, 0.28728],
               [0.9443325490196078, 0.4179627450980392, 0.2784250980392157],
               [0.9474235294117647, 0.4340862745098039, 0.26942941176470586],
               [0.9502517647058824, 0.45024941176470584, 0.2602717647058823],
               [0.9527776470588235, 0.46635098039215683, 0.2510356862745098],
               [0.955063137254902, 0.48235176470588237, 0.24173764705882353],
               [0.9572094117647059, 0.49818941176470594, 0.23240117647058825],
               [0.9591921568627451, 0.5137627450980392, 0.22300196078431372],
               [0.9610364705882353, 0.529096862745098, 0.2135650980392157],
               [0.9627164705882354, 0.544229411764706, 0.20412823529411767],
               [0.9642588235294117, 0.5592243137254902, 0.19475529411764705],
               [0.9656360784313726, 0.5739898039215686, 0.18541882352941175],
               [0.9668764705882353, 0.5885823529411766, 0.1760823529411765],
               [0.9679509803921568, 0.6030090196078431, 0.16681098039215686],
               [0.9688894117647059, 0.6172341176470588, 0.15764039215686276],
               [0.9697270588235294, 0.6312576470588235, 0.1486364705882353],
               [0.9704639215686275, 0.6450796078431372, 0.1397678431372549],
               [0.9710333333333333, 0.6587000000000001, 0.131],
               [0.971535294117647, 0.6720517647058823, 0.1224],
               [0.9720372549019607, 0.6851686274509804, 0.11393411764705882],
               [0.9724713725490196, 0.6980839215686275, 0.10563686274509804],
               [0.9728729411764706, 0.7107294117647058, 0.09747294117647058],
               [0.9732745098039216, 0.7231411764705883, 0.08940980392156862],
               [0.9736760784313725, 0.7353513725490196, 0.08130941176470588],
               [0.9741470588235294, 0.7472905882352942, 0.07324705882352942],
               [0.9745792156862745, 0.7589274509803922, 0.06535529411764707],
               [0.9749807843137255, 0.7704023529411764, 0.057805490196078425],
               [0.9753823529411765, 0.7816352941176471, 0.05065882352941176],
               [0.9757839215686275, 0.792636862745098, 0.04391529411764706],
               [0.976256862745098, 0.803436862745098, 0.03757490196078427],
               [0.9767588235294118, 0.8140352941176471, 0.03156588235294118],
               [0.9773329411764705, 0.8243600000000001, 0.02571490196078431],
               [0.9780078431372549, 0.8344549019607843, 0.020254901960784354],
               [0.9787105882352941, 0.8443482352941176, 0.015371764705882392],
               [0.9794866666666667, 0.8541133333333334, 0.011093333333333372],
               [0.9803635294117647, 0.8636301960784313, 0.007272156862745059],
               [0.9812670588235294, 0.8729929411764706, 0.004076470588235255],
               [0.9822450980392157, 0.8822549019607843, 0.0016607843137254822],
               [0.9832490196078432, 0.8914160784313726, 0.0002760784313725482],
               [0.9841776470588236, 0.9006270588235293, 0.0024094117647058743],
               [0.9850811764705882, 0.9097874509803922, 0.008119607843137215],
               [0.9859847058823529, 0.9186949019607843, 0.01624274509803914],
               [0.9869647058823529, 0.9273, 0.026558823529411607],
               [0.9879686274509804, 0.9354490196078431, 0.03824666666666679],
               [0.9889725490196078, 0.9432486274509804, 0.05142941176470588],
               [0.9899764705882352, 0.9506682352941177, 0.06630235294117647],
               [0.9909023529411765, 0.9576066666666666, 0.08242039215686274],
               [0.9917274509803922, 0.9642764705882353, 0.0987843137254902],
               [0.9925305882352942, 0.9705082352941177, 0.1157],
               [0.9934129411764706, 0.9761568627450979, 0.13355882352941176],
               [0.994236862745098, 0.9812007843137255, 0.15242549019607804],
               [0.99496, 0.9857199999999999, 0.17238000000000037],
               [0.9956627450980392, 0.9894941176470589, 0.19328235294117646],
               [0.9963654901960785, 0.9925427450980392, 0.21509176470588234],
               [0.9971494117647058, 0.9948047058823529, 0.23780823529411765],
               [0.9979525490196078, 0.9961788235294118, 0.26159490196078433],
               [0.9985917647058823, 0.9968917647058824, 0.28608039215686276],
               [0.9988647058823529, 0.9972470588235294, 0.31084117647058784],
               [0.9989, 0.9973, 0.33563803921568586],
               [0.9986505882352942, 0.997050588235294, 0.36035176470588276],
               [0.9981823529411764, 0.9966658823529412, 0.3845470588235298],
               [0.9975964705882353, 0.9962643137254903, 0.4080537254901961],
               [0.9971627450980393, 0.9958627450980392, 0.43034901960784316],
               [0.9970152941176471, 0.9958, 0.45057176470588234],
               [0.9970850980392156, 0.9959701960784313, 0.46942823529411765],
               [0.9971854901960784, 0.9961709803921568, 0.4875027450980392],
               [0.9972858823529411, 0.9964576470588236, 0.5049576470588235],
               [0.9974725490196079, 0.9967588235294117, 0.5220666666666667],
               [0.9975866666666667, 0.9969733333333333, 0.5387866666666666],
               [0.9977741176470588, 0.9972611764705883, 0.5551035294117647],
               [0.9978874509803921, 0.9974749019607843, 0.5712796078431372],
               [0.9978999999999999, 0.9975878431372549, 0.5874427450980392],
               [0.9978999999999999, 0.9976, 0.6034294117647059],
               [0.9978999999999999, 0.9976886274509803, 0.6192145098039216],
               [0.9978999999999999, 0.9977, 0.6347090196078431],
               [0.9978999999999999, 0.9977894117647058, 0.6499011764705882],
               [0.9978999999999999, 0.9978, 0.6648807843137255],
               [0.9979901960784314, 0.9978901960784313, 0.6796588235294118],
               [0.998, 0.9978999999999999, 0.694144705882353],
               [0.9980909803921569, 0.9979909803921568, 0.7083282352941177],
               [0.9981913725490197, 0.9981827450980392, 0.7223007843137255],
               [0.9982917647058823, 0.9982917647058823, 0.7360717647058823],
               [0.9984843137254902, 0.9984843137254902, 0.7496411764705883],
               [0.9986850980392157, 0.9986850980392157, 0.7630090196078431],
               [0.9987929411764707, 0.9987929411764707, 0.7762682352941176],
               [0.9989866666666667, 0.9988933333333334, 0.7894266666666666],
               [0.999093725490196, 0.9989937254901962, 0.8025780392156863],
               [0.9991941176470588, 0.9990941176470588, 0.8157294117647058],
               [0.9992, 0.9991, 0.8287862745098039],
               [0.9992, 0.9991, 0.8417423529411764],
               [0.9992, 0.9991, 0.8546929411764705],
               [0.9992, 0.9991, 0.8674521568627451],
               [0.9992, 0.9991, 0.8801058823529412],
               [0.9992, 0.9991, 0.8926588235294117],
               [0.9992, 0.999196862745098, 0.9050141176470589],
               [0.9992972549019608, 0.9992972549019608, 0.9172650980392157],
               [0.9993, 0.9993, 0.9294152941176471],
               [0.9993980392156863, 0.9993980392156863, 0.9414647058823529],
               [0.999498431372549, 0.999498431372549, 0.9534133333333333],
               [0.9995988235294118, 0.9995988235294118, 0.9651623529411765],
               [0.9996992156862745, 0.9996992156862745, 0.9769082352941176],
               [0.9997996078431373, 0.9997996078431373, 0.9885545098039216],
               [1.0, 1.0, 1.0]]

morgen_colors_r = morgen_colors[::-1]

morgenstemning_cmap   = mpl.colors.ListedColormap(morgen_colors,  'morgenstemning')
morgenstemning_r_cmap = mpl.colors.ListedColormap(morgen_colors_r,'inv_morgenstemning')