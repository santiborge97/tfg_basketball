//GRÁFICO OFF, DEF, NET RATING
var ctxGames = document.getElementById("bar-chart-games").getContext("2d");
            var myChartGames = new Chart(ctxGames,{
                type:"pie",
                data:{
                    labels:['Victorias','Derrotas'],
                    datasets:[{
                            label: "Num partidos",
                            data:[{{ object.w }},{{ object.l }}],
                            fill:false,
                            backgroundColor:[
                                "rgba(75, 192, 192, 0.2)",
                                "rgba(255, 99, 132, 0.2)"
                            ],
                            borderColor:[
                                "rgb(75, 192, 192)",
                                "rgb(255, 99, 132)"
                            ],
                            borderWidth:1
                    }]
                },
                options:{
                    scales:{
                        yAxes:[{
                                ticks:{
                                    beginAtZero:true
                                    }
                        }]
                    }
                }
            });


//GRÁFICO OFF, DEF, NET RATING
var ctxRating =document.getElementById("bar-chart-rating").getContext("2d");
            var myChartRating = new Chart(ctxRating ,{
                type:"bar",
                data:{
                    labels:['{{player1.player_name}}','{{player2.player_name}}','{{player3.player_name}}','{{player4.player_name}}','{{player5.player_name}}','Quinteto'],
                    datasets:[{
                            label: "Offensive Rating",
                            data:[{{ player1.off_rating }},{{ player2.off_rating }},{{ player3.off_rating }},{{ player4.off_rating }},{{ player5.off_rating }},{{ object.off_rating }},],
                            fill:false,
                            backgroundColor:[
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235)"
                            ],
                            borderColor:[
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)"
                            ],
                            borderWidth:1
                    },
                    {
                            label: "Defensive Rating",
                            data:[{{ player1.def_rating }},{{ player2.def_rating }},{{ player3.def_rating }},{{ player4.def_rating }},{{ player5.def_rating }},{{ object.def_rating }},],
                            fill:false,
                            backgroundColor:[
                                "rgba(255, 99, 132, 0.2)",
                                "rgba(255, 99, 132, 0.2)",
                                "rgba(255, 99, 132, 0.2)",
                                "rgba(255, 99, 132, 0.2)",
                                "rgba(255, 99, 132, 0.2)",
                                "rgba(255, 99, 132)"
                            ],
                            borderColor:[
                                "rgb(255, 99, 132)",
                                "rgb(255, 99, 132)",
                                "rgb(255, 99, 132)",
                                "rgb(255, 99, 132)",
                                "rgb(255, 99, 132)",
                                "rgb(255, 99, 132)"
                            ],
                            borderWidth:1
                    },
                    {
                            label: "Net Rating",
                            data:[{{ player1.net_rating }},{{ player2.net_rating }},{{ player3.net_rating }},{{ player4.net_rating }},{{ player5.net_rating }},{{ object.net_rating }},],
                            fill:false,
                            backgroundColor:[
                                "rgba(255, 205, 86, 0.2)",
                                "rgba(255, 205, 86, 0.2)",
                                "rgba(255, 205, 86, 0.2)",
                                "rgba(255, 205, 86, 0.2)",
                                "rgba(255, 205, 86, 0.2)",
                                "rgba(255, 205, 86)"
                            ],
                            borderColor:[
                                "rgb(255, 205, 86)",
                                "rgb(255, 205, 86)",
                                "rgb(255, 205, 86)",
                                "rgb(255, 205, 86)",
                                "rgb(255, 205, 86)",
                                "rgb(255, 205, 86)"
                            ],
                            borderWidth:1
                    }]
                },
                options:{
                    scales:{
                        yAxes:[{
                                ticks:{
                                    beginAtZero:true
                                    }
                        }]
                    }
                }
            });



//GRÁFICO EFG
var ctxEfg =document.getElementById("bar-chart-efg").getContext("2d");
            var myChartEfg = new Chart(ctxEfg ,{
                type:"bar",
                data:{
                    labels:['{{player1.player_name}}','{{player2.player_name}}','{{player3.player_name}}','{{player4.player_name}}','{{player5.player_name}}','Quinteto'],
                    datasets:[{
                            label: "Effective Field Goal %",
                            data:[{{ player1.efg_pct }},{{ player2.efg_pct }},{{ player3.efg_pct }},{{ player4.efg_pct }},{{ player5.efg_pct }},{{ object.efg_pct }},],
                            fill:false,
                            backgroundColor:[
                                "rgba(73, 240, 81, 0.2)",
                                "rgba(73, 240, 81, 0.2)",
                                "rgba(73, 240, 81, 0.2)",
                                "rgba(73, 240, 81, 0.2)",
                                "rgba(73, 240, 81, 0.2)",
                                "rgba(73, 240, 81, 0.7)"
                            ],
                            borderColor:[
                                "rgb(73, 240, 81)",
                                "rgb(73, 240, 81)",
                                "rgb(73, 240, 81)",
                                "rgb(73, 240, 81)",
                                "rgb(73, 240, 81)",
                                "rgb(73, 240, 81)"
                            ],
                            borderWidth:1
                    }]
                },
                options:{
                    scales:{
                        yAxes:[{
                                ticks:{
                                    beginAtZero:true
                                    }
                        }]
                    }
                }
            });


//GRÁFICO PIE
var ctxPie =document.getElementById("bar-chart-pie").getContext("2d");
            var myChartPie = new Chart(ctxPie ,{
                type:"bar",
                data:{
                    labels:['{{player1.player_name}}','{{player2.player_name}}','{{player3.player_name}}','{{player4.player_name}}','{{player5.player_name}}','Quinteto'],
                    datasets:[{
                            label: "Player Impact Estimate",
                            data:[{{ player1.pie }},{{ player2.pie }},{{ player3.pie }},{{ player4.pie }},{{ player5.pie }},{{ object.pie }},],
                            fill:false,
                            backgroundColor:[
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235, 0.2)",
                                "rgba(54, 162, 235)"
                            ],
                            borderColor:[
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)",
                                "rgb(54, 162, 235)"
                            ],
                            borderWidth:1
                    }]
                },
                options:{
                    scales:{
                        yAxes:[{
                                ticks:{
                                    beginAtZero:true
                                    }
                        }]
                    }
                }
            });