import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date 
import io 
import base64

def autopct_format(pct):
    return ('%1.1f%%' % pct) if pct >= 1 else ''

def make_donut_chart(data_list, label_list, ):
  x = data_list
  today = date.today()
  colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
  fig, ax = plt.subplots(figsize=(4,4))
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

