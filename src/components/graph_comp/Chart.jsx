import React, { useEffect, useContext, useState } from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import moment from 'moment';
import GraphContext from '../../context/Graph';
import Spinner from './Loading';
import millify from 'millify';

function MyChart() {
  const { Prices, TimeLabel, Fetching } = useContext(GraphContext);

  // Prices.map((price) => {
  //   price = millify(price);
  // });

  const chartData = {
    type: 'line',
    labels: TimeLabel,
    datasets: [
      {
        data: Prices,
        label: 'Real Price',
        borderColor: 'rgb(60,186,159)',
        backgroundColor: 'rgb(60,186,159,0.1)',

        pointRadius: 0,
        fill: true,
        clip: { left: false, top: 5, right: 5, bottom: 10 },
        spanGaps: true,

        borderWidth: 1,
      },
    ],
    options: {
      interaction: {
        mode: 'index',
      },
      plugins: {
        display: true,
        text: 'chart',
      },
      layout: {
        padding: 20,
      },
      tension: 2,
    },
    backgroundColor: 'rgb(10,60,210)',
  };
  if (Fetching || !TimeLabel) {
    return (
      <div className='p-5'>
        <Spinner />
      </div>
    );
  }
  return (
    <div className='App p-5'>
      <Line data={chartData} />
    </div>
  );
}

export default MyChart;
