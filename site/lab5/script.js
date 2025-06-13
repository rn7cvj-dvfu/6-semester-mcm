// --- DOM ссылки ---
const L_slider = document.getElementById("L");
const nx_slider = document.getElementById("nx");
const c_slider = document.getElementById("c");
const CFL_slider = document.getElementById("CFL");
const T_slider = document.getElementById("T");
const initialConditionSelect = document.getElementById("initialCondition");
const customFunctionGroup = document.getElementById("custom-function-group");
const customFunctionInput = document.getElementById("customFunctionInput");
const runButton = document.getElementById("runButton");
const statusDiv = document.getElementById("status");
const charts = {};
let animationFrameId;

// --- Обновление значений слайдеров ---
const sliders = ["L", "nx", "c", "CFL", "T"];
sliders.forEach((id) => {
  const slider = document.getElementById(id);
  const display = document.getElementById(`${id}-value`);
  display.textContent = slider.value;
  slider.addEventListener("input", (e) => {
    display.textContent = e.target.value;
  });
});

// --- Предустановленные начальные функции ---
const initialConditions = {
  box: (x, L) => (x >= L / 4 && x <= L / 2 ? 2.0 : 1.0),
  gaussian: (x, L) => Math.exp(-Math.pow((x - L / 2) / (L / 10), 2)),
  sine: (x, L) => 1.5 + 0.5 * Math.sin((2 * Math.PI * x) / L),
};

// --- Логика отображения поля для своей функции ---
initialConditionSelect.addEventListener("change", () => {
  if (initialConditionSelect.value === "custom") {
    customFunctionGroup.style.display = "block";
  } else {
    customFunctionGroup.style.display = "none";
  }
});

// --- Основная логика симуляции ---
function runSimulation() {
  // Остановка предыдущей анимации, если она была
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }

  statusDiv.textContent = "Подготовка...";
  statusDiv.classList.remove("status-error");

  // --- 1. Получение параметров из UI ---
  const L = parseFloat(L_slider.value);
  const nx = parseInt(nx_slider.value);
  const c = parseFloat(c_slider.value);
  const CFL = parseFloat(CFL_slider.value);
  const T = parseFloat(T_slider.value);

  let ic_func;
  if (initialConditionSelect.value === "custom") {
    try {
      // ВНИМАНИЕ: new Function() похож на eval(). Безопасно только потому,
      // что код выполняется локально в вашем браузере.
      ic_func = new Function("x", "L", `return ${customFunctionInput.value}`);
      // Пробный вызов для проверки синтаксиса
      ic_func(0, L);
    } catch (e) {
      statusDiv.textContent = "Ошибка в пользовательской функции!";
      statusDiv.classList.add("status-error");
      console.error("Custom function error:", e);
      return;
    }
  } else {
    ic_func = initialConditions[initialConditionSelect.value];
  }

  // --- 2. Настройка переменных симуляции ---
  const dx = L / (nx - 1);
  const dt = (CFL * dx) / c;
  const nt = Math.floor(T / dt);
  const nu = (c * dt) / dx;

  const x_space = Array.from({ length: nx }, (_, i) => i * dx);
  const u0 = x_space.map((x) => ic_func(x, L));

  let u_exp = [...u0];
  let u_imp = [...u0];

  // Проверка на некорректные значения (NaN) после вычисления u0
  if (u0.some(isNaN)) {
    statusDiv.textContent = "Ошибка: функция вернула NaN!";
    statusDiv.classList.add("status-error");
    return;
  }

  // --- 3. Настройка матрицы для неявного метода (A) ---
  const A = Array.from({ length: nx }, () => Array(nx).fill(0));
  const nu_half = nu / 2;
  for (let i = 0; i < nx; i++) {
    A[i][i] = 1;
    if (i < nx - 1) A[i][i + 1] = nu_half;
    if (i > 0) A[i][i - 1] = -nu_half;
  }
  A[0][nx - 1] = -nu_half; // Периодические граничные условия
  A[nx - 1][0] = nu_half;

  // --- 4. Настройка графиков ---
  ["explicit", "implicit"].forEach((type) => {
    if (charts[type]) charts[type].destroy();
    const ctx = document.getElementById(`${type}Chart`).getContext("2d");
    charts[type] = new Chart(ctx, {
      type: "line",
      data: {
        labels: x_space.map((x) => x.toFixed(2)),
        datasets: [
          {
            label: `u(x, t)`,
            data: [...u0],
            borderColor:
              type === "explicit"
                ? "rgba(26, 115, 232, 1)"
                : "rgba(211, 47, 47, 1)",
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.1,
          },
        ],
      },
      options: {
        animation: false,
        scales: {
          y: { min: -1, max: 2.5 },
          x: {},
        },
      },
    });
  });

  // --- 5. Цикл анимации ---
  let n = 0; // счетчик шагов по времени
  function animate() {
    if (n >= nt) {
      statusDiv.textContent = "Симуляция завершена!";
      return;
    }

    // --- Шаг явного метода ---
    const un_exp = [...u_exp];
    for (let i = 0; i < nx; i++) {
      const i_minus_1 = i === 0 ? nx - 1 : i - 1;
      u_exp[i] = un_exp[i] - nu * (un_exp[i] - un_exp[i_minus_1]);
    }

    // --- Шаг неявного метода ---
    try {
      u_imp = numeric.solve(A, u_imp);
    } catch (e) {
      console.error("Ошибка решения СЛАУ:", e);
      statusDiv.textContent = "Ошибка: неявный метод не сошелся!";
      statusDiv.classList.add("status-error");
      cancelAnimationFrame(animationFrameId);
      return;
    }

    // Обновляем график не на каждом шаге для производительности
    if (n % 5 === 0) {
      charts.explicit.data.datasets[0].data = u_exp;
      charts.implicit.data.datasets[0].data = u_imp;
      charts.explicit.update();
      charts.implicit.update();
      statusDiv.textContent = `Симуляция... Время: ${(n * dt).toFixed(
        2
      )} / ${T.toFixed(2)}c`;
    }

    n++;
    animationFrameId = requestAnimationFrame(animate);
  }

  animate();
}

// --- Обработчики событий ---
runButton.addEventListener("click", runSimulation);

// Запустить симуляцию с параметрами по умолчанию при загрузке страницы
window.addEventListener("load", () => {
  runButton.click();
});
