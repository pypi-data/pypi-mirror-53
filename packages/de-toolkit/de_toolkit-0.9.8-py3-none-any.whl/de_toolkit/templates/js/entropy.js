var data = d.properties.entropies,
                    slider = $(elem).find(".percentile_slider"),
                    entropy_chart,
                    counts_chart,
                    update_counts,
                    tot_features,
                    exemplar_name, exemplar_entropy,
                    sum = function(l) { return l.reduce(function(a,b) { return a+b },0) };

                exemplar_name = function(i) {
                    if(data.exemplar_features[i] === null) {
                        return 'No exemplar genes';
                    }
                    return data.exemplar_features[i].name;
                }

                exemplar_entropy = function(i) {
                    if(data.exemplar_features[i] === null) {
                        return 'NA';
                    }
                    return data.exemplar_features[i].entropy.toFixed(2);
                }

                tot_features = sum(data.num_features);
                update_counts = function(i) {
                        var sorted_counts,
                            exemplar = data.exemplar_features[i];

                        sorted_counts = _.sortBy(
                                exemplar.counts,
                                function(x) { return x[1] }
                            );

                        counts_chart.subtitle.update({
                            text: 'Feature: '+exemplar_name(i)+
                                  ' | Entropy: '+exemplar_entropy(i)+
                                  ' | Entropy Percentile: '+i
                        });
                        counts_chart.xAxis[0].update({categories: sorted_counts.map(
                            function(x) { return x[0]; }
                        )});
                        counts_chart.series[0].setData(sorted_counts);
                };

                slider.slider({
                    value: 0,
                    min: 0,
                    max: data.exemplar_features.length-1,
                    step: 1,
                    slide: function(event, ui) {
                        update_counts(ui.value);
                    }
                });

                entropy_chart = Highcharts.chart(elem.querySelector(".entropy"), {
                    title: { text: 'Sample Entropy' },
                    xAxis: [
                        {
                            title: { text: 'Percentile' },
                            crosshair: true,
                            categories: data.pct
                        }
                    ],
                    yAxis: [
                        {
                            title: { text: 'Entropy' },
                            crosshair: true
                        },
                        {
                            title: { text: 'Number of Features' },
                            crosshair: true,
                            opposite: true
                        }

                    ],
                    series: [
                        {
                            name: 'Sample Entropy',
                            data: data.pctVal,
                            yAxis: 0,
                            events: {
                                click: function(e) {
                                    $(slider).slider("value",e.point.x);
                                    update_counts(e.point.x);
                                }
                            }
                        },
                        {
                            type: 'line',
                            name: 'Maximum Entropy',
                            data: Array(data.pct.length).fill(-Math.log(1/data.exemplar_features[0].counts.length)),
                            dashStyle: 'ShortDash',
                            marker: { enabled: false },
                            yAxis: 0
                        },
                        {
                            name: 'Number of Features',
                            data: data.num_features.map(function(a,i) {
                                return tot_features - sum(data.num_features.slice(0,i));
                            }),
                            yAxis: 1,
                            events: {
                                click: function(e) {
                                    $(slider).slider("value",e.point.x);
                                    update_counts(e.point.x);
                                }
                            }
                        }
                    ],
                });
                addFullscreenButton(
                    elem.querySelector("#entropy-card-fullscreen"),
                    entropy_chart
                );


                counts_chart = Highcharts.chart(elem.querySelector(".entropy_counts"), {
                    chart: { },
                    title: { text: 'Exemplar Entropy Counts'},
                    subtitle: {
                            text: 'Feature: '+exemplar_name(0)+
                                ' | Entropy: '+exemplar_entropy(0)+
                                ' | Entropy Percentile: 0'
                    },
                    xAxis: {
                        title: { text: 'Sample' },
                        categories: _.sortBy(
                            data.exemplar_features[0].counts,
                            function(x) { return x[1] }
                        ).map(
                            function(x) { return x[0]; }
                        )
                    },
                    yAxis: {
                        title: { text: 'Counts' }
                    },
                    series: [{
                        type: 'column',
                        name: 'Counts',
                        data: _.sortBy(
                            data.exemplar_features[0].counts,
                            function(x) { return x[1] }
                        )
                    }],
                    updateCounts: function(i) {
                    }
                });

                addFullscreenButton(
                    elem.querySelector("#exemplar-card-fullscreen"),
                    counts_chart
                );

