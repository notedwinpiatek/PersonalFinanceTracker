import { cirleChart } from "./cirleChart.js";

const categoryEl = document.getElementById('categoryChart');
const categoryCtx = categoryEl.getContext('2d');
const categoryLabels = JSON.parse(categoryEl.getAttribute("data-category-labels"));
const categoryTotals = JSON.parse(categoryEl.getAttribute("data-category-totals"));

cirleChart(categoryLabels, categoryTotals, categoryCtx);