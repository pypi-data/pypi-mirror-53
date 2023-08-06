class indicators:
    def __init__(self, security):
        self.security = security

    def daily_dips(self, days = None, amount = 0.05):
        """Return the number of $amount (or greater) sized dips in the number of $days"""
        
        total_dips = 0
        data = self.security.load_data(days).values.tolist()
        for n in range(len(data)):

            day = data[n]
            yesterday = data[n - 1]

            if day < yesterday:
                if (yesterday - day) / yesterday >= amount:
                    total_dips += 1

        return total_dips

    def largest_drawdown(self, days = None):
        """Return the largest dip amount"""

        largest = 0
        drawdown = 0
        price_at_start = 0
        data = self.security.load_data(days).values.tolist()
        for n in range(len(data)):
            day = data[n]
            yesterday = data[n - 1]

            if day < yesterday:
                if drawdown is 0:
                    price_at_start = day

                drawdown += yesterday - day
            else:
                if drawdown > 0:
                    if drawdown > largest:
                        largest = drawdown

                    drawdown = 0

        return largest

    def rsi(self, days = None):
        data = self.security.load_data(days=days)
        dx = data.diff()
        
        up,down = dx.copy(), dx.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        up = up.rolling(window=12).mean()
        down = down.rolling(window=12).mean().abs()
        
        print(up / down)
        #up = data.rolling_mean()
        #print(up)
        #print(data)
        exit(-1)