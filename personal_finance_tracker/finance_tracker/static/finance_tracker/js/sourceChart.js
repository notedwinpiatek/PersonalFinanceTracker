import { cirleChart } from "./cirleChart.js";

const sourceEl = document.getElementById('sourceChart');
const sourceCtx = sourceEl.getContext('2d');
const sourceLabels = JSON.parse(sourceEl.getAttribute("data-source-labels"));
const sourceTotals = JSON.parse(sourceEl.getAttribute("data-source-totals"));
const currencySign = sourceEl.getAttribute("data-currency-sign");

cirleChart(sourceLabels, sourceTotals, sourceCtx, currencySign);