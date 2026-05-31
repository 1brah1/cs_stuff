(function () {
  const config = window.DASHBOARD_CONFIG;
  const refreshMs = config.refreshSeconds * 1000;

  const colors = {
    text: "#e7edf6",
    grid: "rgba(148, 164, 184, 0.2)",
    blue: "#59a6ff",
    mint: "#24c8a5",
    yellow: "#ffd166",
    red: "#ff6565",
    green: "#4fe07a",
    orange: "#ff9f43",
    violet: "#c681ff"
  };

  const state = {
    seriesBySymbol: {},
    symbols: config.symbols || [],
    charts: {}
  };

  function setStatus(message) {
    document.getElementById("etlStatus").textContent = message;
  }

  function setLastUpdate(value) {
    document.getElementById("lastUpdate").textContent = value || "-";
  }

  async function fetchJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error("Request failed: " + response.status);
    }
    return response.json();
  }

  function applyDarkScales() {
    return {
      x: {
        ticks: { color: colors.text, maxRotation: 0 },
        grid: { color: colors.grid }
      },
      y: {
        ticks: { color: colors.text },
        grid: { color: colors.grid }
      }
    };
  }

  function destroyChart(name) {
    if (state.charts[name]) {
      state.charts[name].destroy();
      state.charts[name] = null;
    }
  }

  function updateSummaryCards(summaryRows) {
    const container = document.getElementById("summaryCards");
    container.innerHTML = "";

    summaryRows.forEach((row) => {
      const card = document.createElement("article");
      card.className = "summary-card";
      card.innerHTML =
        "<h3>" + row.symbol + "</h3>" +
        "<p class=\"summary-price\">$" + Number(row.close || 0).toFixed(2) + "</p>" +
        "<p class=\"summary-meta\">Range: $" + Number(row.range || 0).toFixed(2) + "</p>" +
        "<p class=\"summary-meta\">Avg Vol: " + Number(row.avg_volume_m || 0).toFixed(2) + "M</p>";
      container.appendChild(card);
    });
  }

  function buildComparisonChart() {
    destroyChart("comparison");
    const ctx = document.getElementById("comparisonChart").getContext("2d");

    const datasets = state.symbols.map((symbol, idx) => {
      const palette = [colors.blue, colors.mint, colors.yellow, colors.violet, colors.orange];
      const series = state.seriesBySymbol[symbol] || { normalized: [], dates: [] };
      return {
        label: symbol,
        data: series.normalized,
        borderColor: palette[idx % palette.length],
        borderWidth: 2,
        tension: 0.2,
        pointRadius: 0
      };
    });

    const labels = (state.seriesBySymbol[state.symbols[0]] || {}).dates || [];

    state.charts.comparison = new Chart(ctx, {
      type: "line",
      data: { labels, datasets },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: colors.text } }
        },
        scales: applyDarkScales()
      }
    });
  }

  function buildDailyChangeChart(symbol) {
    destroyChart("daily");
    const series = state.seriesBySymbol[symbol];
    if (!series) return;

    const ctx = document.getElementById("dailyChangeChart").getContext("2d");
    const barColors = series.daily_change.map((v) => (v >= 0 ? colors.green : colors.red));

    state.charts.daily = new Chart(ctx, {
      type: "bar",
      data: {
        labels: series.dates,
        datasets: [{
          label: symbol + " Daily Change %",
          data: series.daily_change,
          backgroundColor: barColors,
          borderWidth: 0
        }]
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: colors.text } }
        },
        scales: applyDarkScales()
      }
    });
  }

  function buildVolumeChart(symbol) {
    destroyChart("volume");
    const series = state.seriesBySymbol[symbol];
    if (!series) return;

    const ctx = document.getElementById("volumeChart").getContext("2d");

    state.charts.volume = new Chart(ctx, {
      type: "bar",
      data: {
        labels: series.dates,
        datasets: [{
          label: symbol + " Volume (M)",
          data: series.volume.map((v) => v / 1000000),
          backgroundColor: "rgba(36, 200, 165, 0.75)",
          borderColor: colors.mint,
          borderWidth: 1
        }]
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: colors.text } }
        },
        scales: applyDarkScales()
      }
    });
  }

  function buildTrendChart(symbol) {
    destroyChart("trend");
    const series = state.seriesBySymbol[symbol];
    if (!series) return;

    const ctx = document.getElementById("trendChart").getContext("2d");

    state.charts.trend = new Chart(ctx, {
      type: "line",
      data: {
        labels: series.dates,
        datasets: [
          {
            label: symbol + " High",
            data: series.high,
            borderColor: "rgba(89, 166, 255, 0.0)",
            backgroundColor: "rgba(89, 166, 255, 0.16)",
            pointRadius: 0,
            fill: false
          },
          {
            label: symbol + " Low",
            data: series.low,
            borderColor: "rgba(89, 166, 255, 0.0)",
            backgroundColor: "rgba(89, 166, 255, 0.16)",
            pointRadius: 0,
            fill: "-1"
          },
          {
            label: symbol + " Close",
            data: series.close,
            borderColor: colors.blue,
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: colors.text } }
        },
        scales: applyDarkScales()
      }
    });
  }

  async function updateHealth() {
    const health = await fetchJson("/api/health");
    setLastUpdate(health.last_db_update || health.last_success);
    if (health.last_error) {
      setStatus("Error");
    } else if (health.is_running) {
      setStatus("Refreshing");
    } else {
      setStatus("Ready");
    }
  }

  async function loadDataAndRender() {
    setStatus("Loading");

    const [seriesRes, summaryRes] = await Promise.all([
      fetchJson("/api/timeseries"),
      fetchJson("/api/summary")
    ]);

    state.seriesBySymbol = {};
    state.symbols = seriesRes.symbols || state.symbols;
    (seriesRes.series || []).forEach((row) => {
      state.seriesBySymbol[row.symbol] = row;
    });

    updateSummaryCards(summaryRes.summary || []);
    buildComparisonChart();

    const dailySymbol = document.getElementById("dailySymbolSelect").value;
    const volumeSymbol = document.getElementById("volumeSymbolSelect").value;
    const trendSymbol = document.getElementById("trendSymbolSelect").value;

    buildDailyChangeChart(dailySymbol);
    buildVolumeChart(volumeSymbol);
    buildTrendChart(trendSymbol);

    await updateHealth();
  }

  function wireEvents() {
    document.getElementById("dailySymbolSelect").addEventListener("change", (e) => {
      buildDailyChangeChart(e.target.value);
    });

    document.getElementById("volumeSymbolSelect").addEventListener("change", (e) => {
      buildVolumeChart(e.target.value);
    });

    document.getElementById("trendSymbolSelect").addEventListener("change", (e) => {
      buildTrendChart(e.target.value);
    });

    document.getElementById("refreshNowButton").addEventListener("click", async () => {
      setStatus("Refreshing");
      await fetchJson("/api/refresh", { method: "POST" });
      setTimeout(loadDataAndRender, 1500);
    });
  }

  async function bootstrap() {
    document.getElementById("refreshInterval").textContent = config.refreshSeconds;
    wireEvents();
    await loadDataAndRender();
    setInterval(loadDataAndRender, refreshMs);
  }

  bootstrap().catch((err) => {
    setStatus("Error");
    console.error(err);
  });
})();
