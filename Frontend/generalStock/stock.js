$().ready(function(){
    // REST API GET
    async function getData(url) {                    
      return await fetch(url).then(res => res.json());
    }

    getData("https://greenstock.pl/api/publicStock/fullHistory") 
    .then((responseJSON) => {
      size = responseJSON.ResourcePrices[0].prices.length

      for (var i = 0; i < size; i++) {

        // Consider only indices where R value changes
        if ((i/2) + 1 == Math.floor(i/2) + 1) {
          $("#stocks-box").append('<div class="row"></div>')
        }

        var base = '<div class="col my-card" style="max-width: 300px"> \
                    <div class="card"> \
                      <div class="card-body"> \
                        <h4 class="card-title text-center"><b>' + responseJSON.ResourcePrices[0].prices[i].resource + '</b></h4> \
                        <canvas id="chart-' + (i + 1) + '"></canvas> \
                      </div> \
                    </div> \
                 </div>'

        // ----------------------- Divide area by X skip title ----------
        $("#stocks-box .row").eq(Math.floor(i/2) + 1).append(base);

        const ctx = document.getElementById('chart-' + (i + 1));

        const data = [];
        responseJSON.ResourcePrices.forEach(element => {
          var point = {}
          
          point.x = element.time;
          point.y = element.prices[i].price

          data.push(point)
        });
    
        const totalDuration = 1000;
        const delayBetweenPoints = totalDuration / data.length;
        const previousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(100) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;
        const animation = {
          x: {
            type: 'number',
            easing: 'linear',
            duration: delayBetweenPoints,
            from: NaN, // the point is initially skipped
            delay(ctx) {
              if (ctx.type !== 'data' || ctx.xStarted) {
                return 0;
              }
              ctx.xStarted = true;
              return ctx.index * delayBetweenPoints;
            }
          },
          y: {
            type: 'number',
            easing: 'linear',
            duration: delayBetweenPoints,
            from: previousY,
            delay(ctx) {
                if (ctx.type !== 'data' || ctx.yStarted) {
                    return 0;
                }
                ctx.yStarted = true;
                return ctx.index * delayBetweenPoints;
            }
        }
        };

        var lineColor = {}
        if (responseJSON.Trends[i].Trend == "green") {
          lineColor = {
            borderColor: '#00FF00',
            borderWidth: 1,
            radius: 0,
            data: data,
          }
        } else {
          lineColor = {
            borderColor: '#FF0000',
            borderWidth: 1,
            radius: 0,
            data: data,
          }
        }

        new Chart(ctx, {
            type: 'line',
            data: {
              datasets: [lineColor]
            },
            options: {
              animation,
              interaction: {
                intersect: false
              },
              plugins: {
                legend: false
              },
              scales: {
                x: {
                  display: true,
                  title: {
                    display: true,
                    text: 'Time'
                  },
                  type: 'linear'
                },
                y: {
                  display: true,
                  title: {
                    display: true,
                    text: 'Min. price'
                  },
                  type: 'linear'
                }
              }
            }                
        });    
      }
    })
    .catch(error => {
      console.error(error);
    });
});