import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date 
import io 
import base64

def autopct_format(pct):
    return ('%1.1f%%' % pct) if pct >= 1 else ''

def make_donut_chart(data_list, label_list, ):
  x = data_list
  colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
  fig, ax = plt.subplots(figsize=(4.5,4))
  def sort(list):
    for item in list: 
      return item 
  ax.pie(x, 
          colors=colors,
          radius=1.5, 
          labels =label_list,
          labeldistance = 0.8,
          startangle= 0,
          autopct= autopct_format,
          pctdistance= 0.55,
          wedgeprops={'linewidth':3,'edgecolor':'w', 'width':0.5},
          )

  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format="png")
  plt.close()
  img_buffer.seek(0)
  img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
  img_buffer.closed
  return img_base64

def make_grouped_bar_chart(time_list, value_list ):
  time_line = tuple(time_list)
  category_count = value_list
  print(time_line)
  print(category_count)
  colors = plt.get_cmap('Blues')
  x = np.arange(len(time_line))
  width = 0.2
  multiplier = 0

  fig, ax = plt.subplots(layout='constrained')
  
  for attribute, measurement in category_count.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label = attribute)
    multiplier += 1
  ax.set_ylabel('Length (mm)')
  # ax.set_title('Penguin attributes by species')
  ax.set_xticks(x + width, time_line)
  ax.legend(loc='upper left', ncols=3)
  ax.set_ylim(0, 250)
  
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format="png")
  plt.close()
  img_buffer.seek(0)
  img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
  img_buffer.closed
  return img_base64

def make_one_line_chart(time_list, value_list ):
  time_line = time_list
  category_count = value_list
  colors = plt.get_cmap('Blues')
  x = time_line
  y = category_count
  fig, axs = plt.subplots(figsize=(5, 4))
  axs.plot(x, y,  linewidth=1, markersize=0, )

  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format="png")
  plt.close()
  img_buffer.seek(0)
  img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
  img_buffer.closed
  return img_base64