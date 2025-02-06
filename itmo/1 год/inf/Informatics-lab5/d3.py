import pandas
import matplotlib.pyplot
import matplotlib.patches

data = pandas.read_csv("Data.csv")
date1 = "18/09/18"
date2 = "16/10/18"
date3 = "16/11/18"
date4 = "18/12/18"
data_date1 = data[data["<DATE>"] == date1]
data_date2 = data[data["<DATE>"] == date2]
data_date3 = data[data["<DATE>"] == date3]
data_date4 = data[data["<DATE>"] == date4]

data_for_plot = {
    '18/09/18 - Открытие': data_date1['<OPEN>'],
    '18/09/18 - Макс': data_date1['<HIGH>'],
    '18/09/18 - Мин': data_date1['<LOW>'],
    '18/09/18 - Закрытие': data_date1['<CLOSE>'],
    '16/10/18 - Открытие': data_date2['<OPEN>'],
    '16/10/18 - Макс': data_date2['<HIGH>'],
    '16/10/18 - Мин': data_date2['<LOW>'],
    '16/10/18 - Закрытие': data_date2['<CLOSE>'],
    '16/11/18 - Открытие': data_date3['<OPEN>'],
    '16/11/18 - Макс': data_date3['<HIGH>'],
    '16/11/18 - Мин': data_date3['<LOW>'],
    '16/11/18 - Закрытие': data_date3['<CLOSE>'],
    '18/12/18 - Открытие': data_date4['<OPEN>'],
    '18/12/18 - Макс': data_date4['<HIGH>'],
    '18/12/18 - Мин': data_date4['<LOW>'],
    '18/12/18 - Закрытие': data_date4['<CLOSE>']
}

matplotlib.pyplot.figure(figsize=(10, 6))
box = matplotlib.pyplot.boxplot(data_for_plot.values(), patch_artist=True, widths=0.5)

colors = ['royalblue', 'honeydew', 'gray', 'gold',
          'cornflowerblue', 'green', 'navy', 'chocolate',
          'dodgerblue', 'firebrick', 'darkgreen','indigo',
          'indianred', 'khaki', 'lightgoldenrodyellow', 'greenyellow']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

matplotlib.pyplot.legend(["18/09/18 - Открытие", "18/09/18 - Макс", "18/09/18 - Мин", "18/09/18 - Закрытие", "16/10/18 - Открытие", "16/10/18 - Макс", "16/10/18 - Мин", "16/10/18 - Закрытие", "16/11/18 - Открытие", "16/11/18 - Макс", "16/11/18 - Мин", "16/11/18 - Закрытие", "18/12/18 - Открытие", "18/12/18 - Макс", "18/12/18 - Мин", "18/12/18 - Закрытие"], loc='upper left', bbox_to_anchor=(1, 1))
matplotlib.pyplot.xticks(range(len(data_for_plot)), data_for_plot.keys(), rotation=45)
matplotlib.pyplot.grid(True)
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()