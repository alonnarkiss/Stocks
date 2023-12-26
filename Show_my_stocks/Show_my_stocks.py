import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

stocks = ["TSLA", "MSFT", "NVDA", "INTC", "AAPL", "META"]
start_date = "2018-01-01"
ma = 50

def download_data(stock):
    df = yf.download(stock, start=start_date, period='1d')
    df[f"Sma_{ma}"] = df['Close'].rolling(window=ma).mean()
    return df

fig, axs = plt.subplots(3, 2, figsize=(12, 8))
axs = axs.flatten()

def update_plot(i):
    for j, stock in enumerate(stocks):
        df = download_data(stock)

        close_value = np.array(df['Close'])
        price = (close_value[-1])
        sma_value = np.array(df[f"Sma_{ma}"])
        the_dates = np.array(df.index)
        ax = axs[j]
        ax.clear()

        ax.plot(the_dates, close_value, label='Close')
        ax.plot(the_dates, sma_value, label=f'{ma}-day SMA | Price = {price:.2f}')
        ax.annotate(f'Current Price: ${price:.2f}', xy=(the_dates[-1], close_value[-1]),
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="-|>", color='red'),
                    fontsize=12, fontname='Arial', color='black',
                    bbox=dict(facecolor='grey', edgecolor='black'))
        # at = AnchoredText("Figure 1a",
        #                   prop=dict(size=15), frameon=True, loc='lower left')
        # at.patch.set_boxstyle("round,pad=0.,rounding_0size=0.2")
        # ax.add_artist(at)


        ax.set_title(f'{stock} Closing Price and {ma}-day SMA')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.legend()
        ax.grid(True)

ani = animation.FuncAnimation(fig, update_plot, interval=60000)  # Update every 60 seconds

plt.tight_layout()
plt.show()
