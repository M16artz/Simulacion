'use strict';
const elementoPorId = identificador => document.getElementById(identificador);
let datos = null, tiempoSimulado = 0, indiceEvento = 0, reproduciendo = true,
    tiempoUltimoFotograma = 0, tiempoUltimoDibujo = 0;
const nombresEventos = {
  arrival: 'Llegada',
  service_start: 'Comienza servicio',
  departure: 'Salida',
  end: 'Fin de simulación'
};
const formatearNumero = (numero, decimales = 3) =>
    numero == null || !Number.isFinite(numero) ? '—' : Number(numero).toFixed(decimales);
const formatearPorcentaje = numero => formatearNumero(numero * 100, 1) + '%';

function leerConfiguracion() {
  return {
    arrival_rate: Number(elementoPorId('lambda').value),
        service_rate: Number(elementoPorId('mu').value),
        duration: Number(elementoPorId('duration').value), seed: Number(elementoPorId('seed').value)
  }
}
async function cargarSimulacion() {
  elementoPorId('alert').textContent = '';
  if (elementoPorId('seedMode').value === 'random') {
    generarSemilla();
  } else if (!elementoPorId('seed').reportValidity()) {
    return;
  }
  elementoPorId('run').disabled = true;
  try {
    const respuesta = await fetch('/api/simulate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(leerConfiguracion())
    });
    const resultado = await respuesta.json();
    if (!respuesta.ok) throw Error(resultado.error || 'Error inesperado');
    datos = resultado;
    tiempoSimulado = 0;
    indiceEvento = 0;
    reproduciendo = true;
    tiempoUltimoFotograma = 0;
    elementoPorId('timeline').max = datos.config.duration;
    elementoPorId('timeline').value = 0;
    elementoPorId('durationText').textContent = '/ ' + datos.config.duration;
    elementoPorId('play').textContent = '❚❚ Pausar';
    elementoPorId('conveyor').classList.remove('paused');
    dibujar(true);
  } catch (error) {
    elementoPorId('alert').textContent = error.message
  } finally {
    elementoPorId('run').disabled = false
  }
}
function obtenerEstado() {
  if (!datos) return null;
  while (indiceEvento < datos.events.length &&
         datos.events[indiceEvento].t <= tiempoSimulado + 0.00000001)
    indiceEvento++;
  return datos.events[Math.max(0, indiceEvento - 1)] || {
    t: 0,
    queue: 0,
    system: 0,
    busy: 0,
    arrived: 0,
    completed: 0,
    mean_wait: 0,
    mean_system: 0,
    avg_queue: 0,
    avg_system: 0,
    utilization: 0
  };
}
function calcularMetricasActuales(estado) {
  // Integración exacta por tramos constantes desde el último evento hasta el reloj de animación.
  const intervaloTranscurrido = Math.max(0, tiempoSimulado - estado.t),
        tiempoObservacion = Math.max(tiempoSimulado, 0.00000001);
  const longitudMediaCola =
      (estado.avg_queue * estado.t + intervaloTranscurrido * estado.queue) / tiempoObservacion;
  const paquetesMediosSistema =
      (estado.avg_system * estado.t + intervaloTranscurrido * estado.system) / tiempoObservacion;
  const utilizacion =
      (estado.utilization * estado.t + intervaloTranscurrido * estado.busy) / tiempoObservacion;
  return {
    Lq: longitudMediaCola,
    L: paquetesMediosSistema,
    rho: utilizacion,
    Wq: estado.mean_wait,
    W: estado.mean_system
  };
}
function dibujar(forzar = false) {
  if (!datos) return;
  const estado = obtenerEstado(), metricasActuales = calcularMetricasActuales(estado);
  elementoPorId('clock').textContent = formatearNumero(tiempoSimulado, 1);
  elementoPorId('timeline').value = tiempoSimulado;
  elementoPorId('arrived').textContent = estado.arrived;
  elementoPorId('completed').textContent = estado.completed;
  elementoPorId('queue').textContent = estado.queue;
  elementoPorId('util').textContent = formatearPorcentaje(metricasActuales.rho);
  elementoPorId('queueCount').textContent = estado.queue;
  elementoPorId('processing').textContent = estado.busy ? 'SÍ' : 'NO';
  elementoPorId('finished').textContent = estado.completed;
  elementoPorId('workState').textContent = estado.busy ? '● EN SERVICIO' : '○ SERVIDOR LIBRE';
  elementoPorId('status').textContent = tiempoSimulado >= datos.config.duration ? '● FINALIZADO' :
      reproduciendo                                                             ? '● EJECUTANDO' :
                                                                                  '● PAUSADO';
  elementoPorId('status').style.color =
      tiempoSimulado >= datos.config.duration ? '#ffc368' : '#58dab0';
  elementoPorId('stationBody').parentElement.classList.toggle('active', Boolean(estado.busy));
  const inicioServicio = [...datos.events.slice(0, indiceEvento)].reverse().find(
      evento => evento.type === 'service_start' &&
          !datos.events.slice(datos.events.indexOf(evento) + 1, indiceEvento)
               .some(salida => salida.type === 'departure' && salida.id === evento.id));
  elementoPorId('stationJob').textContent =
      estado.busy && inicioServicio ? 'PKG-' + String(inicioServicio.id).padStart(3, '0') : 'LIBRE';
  const paquetesEnCola = [];
  // Orden FIFO reconstruido desde el registro; se limita la representación a 9 cajas.
  for (let indiceEventoCola = 0; indiceEventoCola < indiceEvento; indiceEventoCola++) {
    const evento = datos.events[indiceEventoCola];
    if (evento.type === 'arrival') paquetesEnCola.push(evento.id);
    if (evento.type === 'service_start') {
      const indicePaquete = paquetesEnCola.indexOf(evento.id);
      if (indicePaquete >= 0) paquetesEnCola.splice(indicePaquete, 1)
    }
  }
  const contenedor = elementoPorId('queuePacks');
  contenedor.replaceChildren();
  paquetesEnCola.slice(0, 9).forEach((identificador, indice) => {
    const caja = document.createElement('div');
    caja.className = 'package';
    caja.style.left = `${Math.max(0, 61 - (Math.min(paquetesEnCola.length, 9) - indice) * 7.4)}%`;
    const etiquetaPaquete = document.createElement('small');
    etiquetaPaquete.textContent = '#' + identificador;
    caja.append(etiquetaPaquete);
    contenedor.append(caja)
  });
  if (paquetesEnCola.length > 9) {
    const indicadorAdicional = document.createElement('div');
    indicadorAdicional.className = 'package';
    indicadorAdicional.style.left = '1%';
    indicadorAdicional.textContent = '+' + (paquetesEnCola.length - 9);
    contenedor.append(indicadorAdicional)
  }
  const definicionesMetricas = [
    ['ρ · utilización', 'rho', 'rho'], ['L · número medio en sistema', 'L', 'L'],
    ['Lq · longitud media de cola', 'Lq', 'Lq'], ['W · permanencia media', 'W', 'W'],
    ['Wq · espera media', 'Wq', 'Wq']
  ];
  elementoPorId('metrics').innerHTML =
      definicionesMetricas
          .map(([etiqueta, claveTeorica, claveMetrica]) => {
            const valorTeorico = datos.theory[claveTeorica],
                  valorSimulado = metricasActuales[claveMetrica];
            return `<tr><td>${etiqueta}</td><td>${formatearNumero(valorTeorico)}</td><td>${
                formatearNumero(valorSimulado)}</td><td>${
                valorTeorico == null ? '—' :
                                       formatearNumero(valorSimulado - valorTeorico)}</td></tr>`
          })
          .join('');
  const eventosRecientes =
      datos.events.slice(Math.max(0, indiceEvento - 8), indiceEvento).reverse();
  elementoPorId('log').innerHTML =
      eventosRecientes
          .map(
              evento => `<div class="logline"><b>${formatearNumero(evento.t, 2)}</b> ${
                  nombresEventos[evento.type]} ${
                  evento.id != null ? '· Paquete #' + evento.id : ''}${
                  evento.type === 'service_start' ? ' · espera ' + formatearNumero(evento.wait, 2) :
                                                    ''}</div>`)
          .join('');
  const tiempoActual = performance.now();
  if (forzar || tiempoActual - tiempoUltimoDibujo > 90) {
    dibujarGrafico(elementoPorId('queueChart'), 'queue', '#42d3d8', tiempoSimulado);
    dibujarGrafico(
        elementoPorId('waitChart'), 'mean_wait', '#ffc368', tiempoSimulado, 'Espera promedio');
    tiempoUltimoDibujo = tiempoActual
  }
}
function dibujarGrafico(lienzo, campo, color, tiempoLimite, titulo) {
  const rectangulo = lienzo.getBoundingClientRect(),
        proporcionPixeles = window.devicePixelRatio || 1;
  const anchoLienzo = Math.max(180, rectangulo.width), altoLienzo = 210;
  lienzo.width = anchoLienzo * proporcionPixeles;
  lienzo.height = altoLienzo * proporcionPixeles;
  const contexto = lienzo.getContext('2d');
  contexto.scale(proporcionPixeles, proporcionPixeles);
  contexto.clearRect(0, 0, anchoLienzo, altoLienzo);
  let eventos = datos.events.filter(evento => evento.t <= tiempoLimite),
      serie = eventos.map(evento => ({x: evento.t, y: evento[campo]}));
  let ultimoPunto = serie.at(-1);
  serie.push({x: tiempoLimite, y: ultimoPunto ? ultimoPunto.y : 0});
  let valorMaximo = Math.max(1, ...serie.map(punto => punto.y));
  valorMaximo *= 1.15;
  const margenIzquierdo = 35, limiteDerecho = anchoLienzo - 10, margenSuperior = 20,
        limiteInferior = altoLienzo - 27, anchoGrafico = limiteDerecho - margenIzquierdo,
        altoGrafico = limiteInferior - margenSuperior;
  contexto.font = '11px ui-sans-serif,system-ui';
  contexto.textAlign = 'right';
  contexto.strokeStyle = '#27384c';
  contexto.fillStyle = '#8c9eb2';
  contexto.lineWidth = 1;
  for (let indice = 0; indice <= 4; indice++) {
    const y = limiteInferior - (indice / 4) * altoGrafico;
    contexto.beginPath();
    contexto.moveTo(margenIzquierdo, y);
    contexto.lineTo(limiteDerecho, y);
    contexto.stroke();
    contexto.fillText(formatearNumero(valorMaximo * indice / 4, 1), margenIzquierdo - 8, y + 4)
  }
  contexto.textAlign = 'center';
  for (let indice = 0; indice <= 4; indice++) {
    let x = margenIzquierdo + indice * anchoGrafico / 4;
    contexto.fillText(formatearNumero(tiempoLimite * indice / 4, 0), x, limiteInferior + 17)
  }
  contexto.beginPath();
  contexto.lineWidth = 2;
  contexto.strokeStyle = color;
  serie.forEach((punto, indice) => {
    let x = margenIzquierdo + anchoGrafico * (tiempoLimite ? punto.x / tiempoLimite : 0),
        y = limiteInferior - altoGrafico * punto.y / valorMaximo;
    if (!indice)
      contexto.moveTo(x, y);
    else if (campo === 'queue') {
      let puntoAnterior = serie[indice - 1];
      contexto.lineTo(x, limiteInferior - altoGrafico * puntoAnterior.y / valorMaximo);
      contexto.lineTo(x, y)
    } else
      contexto.lineTo(x, y)
  });
  contexto.stroke();
  let degradado = contexto.createLinearGradient(0, margenSuperior, 0, limiteInferior);
  degradado.addColorStop(0, color + '33');
  degradado.addColorStop(1, color + '02');
  contexto.lineTo(limiteDerecho, limiteInferior);
  contexto.lineTo(margenIzquierdo, limiteInferior);
  contexto.closePath();
  contexto.fillStyle = degradado;
  contexto.fill();
}
function animar(tiempoActual) {
  if (!tiempoUltimoFotograma) tiempoUltimoFotograma = tiempoActual;
  const tiempoTranscurrido = Math.min((tiempoActual - tiempoUltimoFotograma) / 1000, .1);
  tiempoUltimoFotograma = tiempoActual;
  if (datos && reproduciendo && tiempoSimulado < datos.config.duration) {
    tiempoSimulado = Math.min(
        datos.config.duration,
        tiempoSimulado + tiempoTranscurrido * Number(elementoPorId('speed').value));
    if (tiempoSimulado === datos.config.duration) {
      reproduciendo = false;
      elementoPorId('play').textContent = '▶ Reproducir';
      elementoPorId('conveyor').classList.add('paused')
    }
    dibujar()
  }
  requestAnimationFrame(animar);
}
// En modo aleatorio, evita repetir la semilla que muestra el campo.
let ultimaSemilla = Number(elementoPorId('seed').value);
function generarSemilla() {
  ultimaSemilla = Number(elementoPorId('seed').value);
  let nuevaSemilla = ultimaSemilla;
  const valoresAleatorios = new Uint32Array(1);
  while (nuevaSemilla === ultimaSemilla) {
    (window.crypto || self.crypto).getRandomValues(valoresAleatorios);
    nuevaSemilla = valoresAleatorios[0]
  }
  ultimaSemilla = nuevaSemilla;
  elementoPorId('seed').value = nuevaSemilla;
  return nuevaSemilla;
}
elementoPorId('seedMode').addEventListener('change', () => {
  const semillaFija = elementoPorId('seedMode').value === 'fixed';
  elementoPorId('seed').readOnly = !semillaFija;
  elementoPorId('seedHelp').textContent = semillaFija
      ? 'Introduce un entero entre 0 y 4294967295. Con los mismos parámetros y semilla obtendrás la misma simulación.'
      : 'Se genera una nueva semilla al simular. Copia su valor y elige una semilla específica para repetirla con los mismos parámetros.';
});
elementoPorId('run').addEventListener('click', cargarSimulacion);
elementoPorId('scenario').addEventListener('change', evento => {
  if (evento.target.value !== 'custom') {
    elementoPorId('lambda').value = evento.target.value;
    elementoPorId('mu').value = 3;
    cargarSimulacion()
  }
});
for (const identificador of ['lambda', 'mu'])
  elementoPorId(identificador)
      .addEventListener('input', () => {elementoPorId('scenario').value = 'custom'});
elementoPorId('play').addEventListener('click', () => {
  if (!datos) return;
  if (tiempoSimulado >= datos.config.duration) {
    tiempoSimulado = 0;
    indiceEvento = 0
  }
  reproduciendo = !reproduciendo;
  elementoPorId('play').textContent = reproduciendo ? '❚❚ Pausar' : '▶ Reproducir';
  elementoPorId('conveyor').classList.toggle('paused', !reproduciendo);
  dibujar(true)
});
elementoPorId('restart').addEventListener('click', () => {
  tiempoSimulado = 0;
  indiceEvento = 0;
  reproduciendo = true;
  elementoPorId('play').textContent = '❚❚ Pausar';
  elementoPorId('conveyor').classList.remove('paused');
  dibujar(true)
});
elementoPorId('timeline').addEventListener('input', evento => {
  tiempoSimulado = Number(evento.target.value);
  indiceEvento = 0;
  dibujar(true)
});
elementoPorId('export').addEventListener('click', () => {
  if (!datos) return;
  const columnas = ['id', 'arrival', 'start', 'departure', 'wait', 'service', 'system'];
  let filas = [
    columnas.join(';'),
    ...datos.jobs.map(
        paquete => columnas
                       .map(
                           columna => Number.isFinite(paquete[columna]) ?
                               String(paquete[columna]).replace('.', ',') :
                               paquete[columna])
                       .join(';'))
  ];
  let archivoCsv = new Blob(['\ufeff' + filas.join('\n')], {type: 'text/csv;charset=utf-8'});
  let urlDescarga = URL.createObjectURL(archivoCsv), enlaceDescarga = document.createElement('a');
  enlaceDescarga.href = urlDescarga;
  enlaceDescarga.download = 'simulacion_mm1_paquetes.csv';
  enlaceDescarga.click();
  setTimeout(() => URL.revokeObjectURL(urlDescarga), 1000)
});
elementoPorId('compare').addEventListener('click', async () => {
  const botonComparar = elementoPorId('compare');
  botonComparar.disabled = true;
  elementoPorId('comparisonResults').textContent = 'Calculando los tres escenarios…';
  try {
    const respuesta = await fetch('/api/scenarios'), escenarios = await respuesta.json();
    if (!respuesta.ok) throw Error('Error en comparación');
    elementoPorId('comparisonResults').innerHTML =
        `<table><thead><tr><th>Escenario</th><th>λ</th><th>μ</th><th>ρ teórico</th><th>Lq teórico</th><th>Lq simulado</th><th>Wq teórico</th><th>Wq simulado</th></tr></thead><tbody>${
            escenarios
                .map(
                    escenario => `<tr><td>${escenario.scenario}</td><td>${
                        formatearNumero(
                            escenario.arrival_rate,
                            1)}</td><td>${formatearNumero(escenario.service_rate, 1)}</td><td>${
                        formatearPorcentaje(escenario.theory.rho)}</td><td>${
                        formatearNumero(escenario.theory.Lq)}</td><td>${
                        formatearNumero(escenario.simulated.avg_queue)}</td><td>${
                        formatearNumero(escenario.theory.Wq)}</td><td>${
                        formatearNumero(escenario.simulated.mean_wait)}</td></tr>`)
                .join(
                    '')}</tbody></table><p class="footnote">Los valores simulados varían con la duración y la semilla. El escenario próximo a saturación requiere horizontes mayores para converger.</p>`
  } catch (error) {
    elementoPorId('comparisonResults').textContent = error.message
  } finally {
    botonComparar.disabled = false
  }
});
window.addEventListener('resize', () => dibujar(true));
requestAnimationFrame(animar);
cargarSimulacion();
