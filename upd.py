import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Начальные параметры
beta_init = 0.3
gamma_init = 0.1
S0_init = 990
I0_init = 10
days_init = 160

# Создание фигуры и осей для графиков
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.4)

# Первоначальный расчет и отрисовка
def update_model(beta, gamma, S0, I0, days):
    N = S0 + I0
    t = np.linspace(0, days, days)
    S = np.zeros(days)
    I = np.zeros(days)
    R = np.zeros(days)
    
    S[0] = S0
    I[0] = I0
    R[0] = 0
    
    for day in range(1, days):
        S[day] = S[day - 1] - (beta * S[day - 1] * I[day - 1] / N)
        I[day] = I[day - 1] + (beta * S[day - 1] * I[day - 1] / N) - (gamma * I[day - 1])
        R[day] = R[day - 1] + (gamma * I[day - 1])
    
    ax.clear()
    ax.plot(t, S, 'b', label='Восприимчивые (S)')
    ax.plot(t, I, 'r', label='Инфицированные (I)')
    ax.plot(t, R, 'g', label='Выздоровевшие (R)')
    ax.set_title('Модель SIR с интерактивными параметрами')
    ax.set_xlabel('Дни')
    ax.set_ylabel('Количество людей')
    ax.legend()
    ax.grid()
    ax.set_ylim(0, N)
    fig.canvas.draw_idle()

# Создание слайдеров
axcolor = 'lightgoldenrodyellow'
ax_beta = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_gamma = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_S0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_I0 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_days = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

slider_beta = Slider(ax_beta, 'β (заражение)', 0.01, 1.0, valinit=beta_init)
slider_gamma = Slider(ax_gamma, 'γ (выздоровление)', 0.01, 0.5, valinit=gamma_init)
slider_S0 = Slider(ax_S0, 'Начальные S', 1, 1000, valinit=S0_init, valstep=1)
slider_I0 = Slider(ax_I0, 'Начальные I', 1, 100, valinit=I0_init, valstep=1)
slider_days = Slider(ax_days, 'Дни моделирования', 10, 365, valinit=days_init, valstep=1)

# Функция обновления при изменении слайдеров
def update(val):
    update_model(
        slider_beta.val,
        slider_gamma.val,
        slider_S0.val,
        slider_I0.val,
        int(slider_days.val)
    )

slider_beta.on_changed(update)
slider_gamma.on_changed(update)
slider_S0.on_changed(update)
slider_I0.on_changed(update)
slider_days.on_changed(update)

# Кнопка сброса
resetax = plt.axes([0.8, 0.02, 0.1, 0.04])
button = Button(resetax, 'Сброс', color=axcolor, hovercolor='0.975')

def reset(event):
    slider_beta.reset()
    slider_gamma.reset()
    slider_S0.reset()
    slider_I0.reset()
    slider_days.reset()

button.on_clicked(reset)

# Первоначальный вызов
update_model(beta_init, gamma_init, S0_init, I0_init, days_init)

plt.show()