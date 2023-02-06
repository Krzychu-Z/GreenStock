$().ready(function(){
    const ctx = document.getElementById('air-chart');

    const data = [{
      x: 1920,
      y: 3.52
    },
    {
      x: 1930,
      y: 3.93
    },
    {
      x: 1940,
      y: 4.85
    },
    {
      x: 1950,
      y: 6.00
    },
    {
      x: 1960,
      y: 9.39
    },
    {
      x: 1970,
      y: 14.9
    },
    {
      x: 1980,
      y: 19.5
    },
    {
      x: 1990,
      y: 22.76
    },
    {
      x: 2000,
      y: 25.45
    },
    {
      x: 2010,
      y: 33.36
    },
    {
      x: 2020,
      y: 35.26
    }
    ];

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

    var inView = false;

    function isScrolledIntoView(elem){
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();

        var elemTop = $(elem).offset().top;
        var elemBottom = elemTop + $(elem).height();

        return ((elemTop <= docViewBottom) && (elemBottom >= docViewTop));
    }

    $(window).scroll(function() {
        if (isScrolledIntoView('#air-chart')) {
            if (inView) { return; }
            inView = true;
            new Chart(ctx, {
                type: 'line',
                data: {
                  datasets: [{
                    borderColor: '#FF0000',
                    borderWidth: 1,
                    radius: 0,
                    data: data,
                  }]
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
                        text: 'Years'
                      },
                      type: 'linear'
                    },
                    y: {
                      display: true,
                      title: {
                        display: true,
                        text: 'Billion tonnes'
                      },
                      type: 'linear'
                    }
                  }
                }                
            });
        } else {
            inView = false;  
        }
    });
})