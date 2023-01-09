$().ready(function(){
    const ctx = document.getElementById('air-chart');

    const data = [];
    let prev = 100;
    for (let i = 1930; i < 2030; i++) {
      prev += 5 - Math.random() * 10;
      data.push({x: i, y: prev});
    }

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