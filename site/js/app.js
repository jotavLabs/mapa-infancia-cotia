"use strict";

(() => {
  const NUM = new Intl.NumberFormat("pt-BR");
  const fmt = (n) => NUM.format(Math.round(n));
  const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const reduzMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const largo = window.matchMedia("(min-width: 900px)");
  const comMouse = window.matchMedia("(hover: hover) and (pointer: fine)");
  const temaEscuro = window.matchMedia("(prefers-color-scheme: dark)");
  // Prévia hospedada onde a página não pode chamar outros sites (Nominatim) nem baixar arquivos
  const PREVIA = window.MODO_PREVIA === true || new URLSearchParams(location.search).has("previa");
  // Miolo verde-pálido do mapa do PMAS, sem CRAS de referência (scripts/desenhar_territorios.py)
  const CENTRO_RESERVA = [-23.74285, -46.96886];

  // ---------- configuração ----------

  const FAMILIAS = [
    { id: "saude", nome: "Saúde", camadas: ["saude_atencao_basica", "saude_urgencia", "saude_hospital", "saude_mental", "saude_especializada", "reabilitacao"] },
    { id: "educacao", nome: "Educação infantil", camadas: ["educacao_infantil"] },
    { id: "assistencia", nome: "Assistência social", camadas: ["assistencia_social"] },
    { id: "protecao", nome: "Proteção", camadas: ["protecao"] },
  ];
  const CAMADAS = {
    saude_atencao_basica: { rotulo: "UBS (atenção básica)", icone: "ubs" },
    saude_urgencia: { rotulo: "Urgência e emergência", icone: "urgencia" },
    saude_hospital: { rotulo: "Hospital", icone: "hospital" },
    saude_mental: { rotulo: "Saúde mental (CAPS)", icone: "mental" },
    saude_especializada: { rotulo: "Atenção especializada", icone: "especializada" },
    reabilitacao: { rotulo: "Reabilitação", icone: "reabilitacao" },
    educacao_infantil: { rotulo: "Creches e pré-escolas", icone: "educacao" },
    assistencia_social: { rotulo: "CRAS e CREAS", icone: "assistencia" },
    protecao: { rotulo: "Conselhos Tutelares", icone: "protecao" },
  };
  const TODAS_CAMADAS = FAMILIAS.flatMap((f) => f.camadas);
  const FAMILIA_DA_CAMADA = Object.fromEntries(FAMILIAS.flatMap((f) => f.camadas.map((c) => [c, f.id])));
  const ICONES = {
    ubs: "M6.5 2.5h3v4h4v3h-4v4h-3v-4h-4v-3h4z",
    urgencia: "M3.5 12.5V9a4.5 4.5 0 0 1 9 0v3.5zM2 13.5h12V15H2zM7.3.8h1.4V3H7.3zM2.2 3.1l1-1 1.6 1.6-1 1zM13.8 3.1l-1-1-1.6 1.6 1 1z",
    hospital: "M3 2.5h2.5v4.25h5V2.5H13v11h-2.5V9.25h-5v4.25H3z",
    mental: "M7.2 2h1.6v7.1c1.9-.3 3.1-1.7 3.1-4.1V3.2h1.6V5c0 3.3-1.8 5.4-4.7 5.7V14H7.2v-3.3C4.3 10.4 2.5 8.3 2.5 5V3.2h1.6V5c0 2.4 1.2 3.8 3.1 4.1z",
    especializada: "M5.5 3.5V1.8h5v1.7H14V13H2V3.5zM6.8 3.5h2.4v-.5H6.8zM7.25 5.3v2.45H4.8v1.5h2.45v2.45h1.5V9.25h2.45v-1.5H8.75V5.3z",
    reabilitacao: "M8.6 1.3a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM7.4 5.2h1.7v2.9h3.2l1.6 4-1.4.6-1.2-3H7.4zM6 7.6l.5 1.6a2.9 2.9 0 1 0 3.6 3.4l1.5.6A4.5 4.5 0 1 1 6 7.6z",
    educacao: "M2 9h5.5v5H2zM8.5 9H14v5H8.5zM5.25 3h5.5v5h-5.5z",
    assistencia: "M8 1.8 1.4 7.5l1 1.1.9-.8V14h3.8v-3.8h1.8V14h3.8V7.8l.9.8 1-1.1z",
    protecao: "M8 1.5 2.8 3.4v4c0 3.3 2.2 5.8 5.2 7 3-1.2 5.2-3.7 5.2-7v-4z",
  };
  const svg = (icone) => `<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path fill-rule="evenodd" d="${ICONES[icone]}"/></svg>`;
  const amostra = (camada) => `<span class="mk-amostra" style="--cor: var(--${FAMILIA_DA_CAMADA[camada]})">${svg(CAMADAS[camada].icone)}</span>`;
  const corFundo = (numero) => `var(--t${numero}-fundo)`;

  const RAZOES = [
    { id: "ubs", campo: "n_saude_atencao_basica", nome: "UBS", um: "1 UBS", nenhum: "Nenhuma UBS dentro do território." },
    { id: "cras", campo: "n_cras", nome: "CRAS", um: "1 CRAS", nenhum: "Nenhum CRAS dentro do território." },
    { id: "educ", campo: "n_educacao_infantil", nome: "Educação infantil", um: "1 creche ou pré-escola", nenhum: "Nenhuma creche ou pré-escola dentro do território." },
  ];
  const nomeRazao = (r) => (r.id === "educ" ? "creche ou pré-escola" : r.nome);
  const MODOS = [
    { id: "pmas", rotulo: "Cores do PMAS" },
    { id: "ubs", rotulo: "Crianças por UBS" },
    { id: "cras", rotulo: "Crianças por CRAS" },
    { id: "educ", rotulo: "Crianças por educação infantil" },
  ];
  const CLASSES = [
    { id: "abaixo-forte", texto: "20% ou mais abaixo da média", teste: (r) => r < 0.8 },
    { id: "abaixo", texto: "de 5% a 20% abaixo da média", teste: (r) => r < 0.95 },
    { id: "meio", texto: "perto da média (até 5% de diferença)", teste: (r) => r <= 1.05 },
    { id: "acima", texto: "de 5% a 20% acima da média", teste: (r) => r <= 1.2 },
    { id: "acima-forte", texto: "20% ou mais acima da média", teste: () => true },
  ];
  const GRUPOS_PERTO = [
    { rotulo: "UBS", teste: (p) => p.camada === "saude_atencao_basica" },
    { rotulo: "Urgência e emergência", teste: (p) => p.camada === "saude_urgencia" },
    { rotulo: "Creche ou pré-escola", teste: (p) => p.camada === "educacao_infantil" },
    { rotulo: "CRAS", teste: (p) => p.subtipo === "CRAS" },
    { rotulo: "Conselho Tutelar", teste: (p) => p.camada === "protecao" },
  ];
  const ROTULO_VOLTAR = {
    territorio: "Todos os territórios",
    bairro: "Voltar aos bairros",
    endereco: "Voltar à busca",
    comparar: "Voltar à comparação",
  };

  const estado = {
    camadas: new Set(Object.keys(CAMADAS)),
    territorio: null,
    modo: "pmas",
    ordem: { col: "numero", dir: 1 },
    metrica: "criancas",
    aba: "territorio",
  };

  // ---------- utilidades ----------

  const cssVar = (nome) => getComputedStyle(document.documentElement).getPropertyValue(nome).trim();
  const dataBR = (iso) => (iso || "").split("-").reverse().join("/");
  const leve = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  const ABREVIACOES = { jd: "jardim", pq: "parque", vl: "vila", chac: "chacara", res: "residencial", sta: "santa", sto: "santo", cond: "condominio", est: "estrada" };
  const porExtenso = (s) => leve(s).split(" ").map((p) => ABREVIACOES[p] || p).join(" ");

  // mistura duas cores #rrggbb; peso é a fração da primeira
  function misturar(a, b, peso) {
    const rgb = (h) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
    const x = rgb(a), y = rgb(b);
    return `#${x.map((v, i) => Math.round(v * peso + y[i] * (1 - peso)).toString(16).padStart(2, "0")).join("")}`;
  }

  function distanciaM(a, b) {
    const R = 6371000, rad = Math.PI / 180;
    const dLat = (b[0] - a[0]) * rad, dLon = (b[1] - a[1]) * rad;
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(a[0] * rad) * Math.cos(b[0] * rad) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  const textoDistancia = (m) => (m < 1000 ? `${fmt(Math.round(m / 10) * 10)} m` : `${(m / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} km`);

  function dentroDoAnel(lon, lat, anel) {
    let dentro = false;
    for (let i = 0, j = anel.length - 1; i < anel.length; j = i++) {
      const [xi, yi] = anel[i], [xj, yj] = anel[j];
      if ((yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) dentro = !dentro;
    }
    return dentro;
  }
  function dentroDaGeometria(lon, lat, geom) {
    const poligonos = geom.type === "Polygon" ? [geom.coordinates] : geom.coordinates;
    return poligonos.some((p) => dentroDoAnel(lon, lat, p[0]) && !p.slice(1).some((furo) => dentroDoAnel(lon, lat, furo)));
  }

  function linkar(texto) {
    return esc(texto).replace(/https?:\/\/[^\s)<]+/g, (u) => `<a href="${u}" target="_blank" rel="noopener">${u.replace(/^https?:\/\//, "").slice(0, 40)}…</a>`);
  }

  async function carregar(caminho) {
    const r = await fetch(caminho);
    if (!r.ok) throw new Error(`não foi possível ler ${caminho} (${r.status})`);
    return r.json();
  }

  // ---------- dados derivados ----------

  let territorios = [];
  let porNumero = {};
  let equipamentos = [];
  let bairros = [];
  let totais = {};

  function prepararTerritorios(gj) {
    territorios = gj.features.map((f) => {
      const p = { ...f.properties, geometria: f.geometry };
      p.criancas = p.pop_0_4 + p.pop_5_9 + p.pop_10_14;
      p.n_creas = p.n_assistencia_social - p.n_cras;
      p.n_equipamentos = TODAS_CAMADAS.reduce((s, c) => s + (p[`n_${c}`] || 0), 0);
      p.bairros = bairros.filter((b) => b.territorios.includes(p.numero)).sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"));
      return p;
    }).sort((a, b) => a.numero - b.numero);
    porNumero = Object.fromEntries(territorios.map((t) => [t.numero, t]));
    const soma = (campo) => territorios.reduce((s, t) => s + (t[campo] || 0), 0);
    totais = { criancas: soma("criancas") };
    for (const r of RAZOES) totais[r.campo] = soma(r.campo);
  }
  const razao = (t, r) => (t[r.campo] > 0 ? t.criancas / t[r.campo] : null);
  const media = (r) => totais.criancas / totais[r.campo];
  function classeDe(t, r) {
    const v = razao(t, r);
    if (v === null) return { id: "nenhum", texto: "nenhum equipamento deste tipo" };
    const rel = v / media(r);
    return CLASSES.find((c) => c.teste(rel));
  }

  // ---------- elementos ----------

  const app = document.getElementById("app");
  const topo = document.querySelector(".topo");
  const folha = document.getElementById("folha");
  const alca = document.getElementById("folha-alca");
  const vistaAbas = document.getElementById("vista-abas");
  const vistaTerritorio = document.getElementById("vista-territorio");
  const corpoAbas = vistaAbas.querySelector(".folha-corpo");
  const corpoTerritorio = vistaTerritorio.querySelector(".folha-corpo");
  const conteudoPainel = document.getElementById("pt-conteudo");
  const botaoVoltar = document.getElementById("pt-voltar");
  const btnMenu = document.getElementById("btn-menu");
  const menu = document.getElementById("menu");
  const btnCamadas = document.getElementById("btn-camadas");
  const painelCamadas = document.getElementById("painel-camadas");
  const legendaModo = document.getElementById("legenda-modo");
  const resultado = document.getElementById("resultado-busca");

  // ---------- mapa: só Cotia, em formas lisas, sem mapa de ruas ----------

  const mapa = L.map("mapa", {
    zoomControl: false,
    attributionControl: false,
    renderer: L.svg({ padding: 0.6 }),
    zoomSnap: 0.25,
    zoomDelta: 0.5,
    minZoom: 8,
    maxZoom: 17,
    maxBoundsViscosity: 1,
  });
  L.control.zoom({ position: "topright", zoomInTitle: "Aproximar", zoomOutTitle: "Afastar" }).addTo(mapa);
  L.control.scale({ imperial: false, position: "bottomleft" }).addTo(mapa);
  mapa.createPane("rotulos");
  mapa.getPane("rotulos").style.pointerEvents = "none";

  // Afastado, os pontos encolhem e os nomes dos territórios passam para cima deles
  function atualizarZoom() {
    const z = mapa.getZoom();
    mapa.getContainer().classList.toggle("zoom-baixo", z < 13);
    mapa.getContainer().classList.toggle("zoom-minimo", z < 11.5);
    mapa.getPane("rotulos").style.zIndex = z < 13 ? 620 : 450;
  }
  mapa.on("zoomend", atualizarZoom);

  let camadaBase, camadaTerritorios, camadaContorno, limitesCotia;
  const marcadores = [];
  let marcadorBusca = null;

  // Embaixo, Cotia inteira na cor das divisas (fecha as frestas entre setores); por cima, o contorno firme
  const estiloBase = () => ({ stroke: false, fillColor: cssVar("--mapa-divisa"), fillOpacity: 1 });
  const estiloContorno = () => ({ color: cssVar("--mapa-contorno"), weight: 2.5, opacity: 1, fill: false, lineJoin: "round" });

  function corDoTerritorio(t) {
    if (estado.modo === "pmas") return cssVar(`--t${t.numero}-fundo`);
    return cssVar(`--div-${classeDe(t, RAZOES.find((x) => x.id === estado.modo)).id}`);
  }

  function estiloTerritorio(f) {
    const t = porNumero[f.properties.numero];
    const sel = estado.territorio;
    const cor = corDoTerritorio(t);
    return {
      color: sel === t.numero ? cssVar("--mapa-contorno") : cssVar("--mapa-divisa"),
      weight: sel === t.numero ? 3.5 : 1.5,
      opacity: 1,
      lineJoin: "round",
      fillColor: sel && sel !== t.numero ? misturar(cor, cssVar("--mapa-fundo"), 0.4) : cor,
      fillOpacity: 1,
    };
  }

  const camadaDoTerritorio = (num) => camadaTerritorios.getLayers().find((l) => l.feature.properties.numero === num);

  function redesenharMapa() {
    camadaBase.setStyle(estiloBase());
    camadaTerritorios.setStyle(estiloTerritorio);
    if (estado.territorio) camadaDoTerritorio(estado.territorio).bringToFront();
    camadaContorno.setStyle(estiloContorno());
    camadaContorno.bringToFront();
  }

  function desenharTerritorios(gj) {
    camadaTerritorios = L.geoJSON(gj, {
      style: estiloTerritorio,
      onEachFeature: (f, camada) => {
        camada.on("click", (e) => {
          L.DomEvent.stopPropagation(e);
          if (!painelCamadas.hidden) { alternarCamadas(false); return; }
          if (estado.territorio === f.properties.numero) return;
          selecionarTerritorio(f.properties.numero, { enquadrar: !largo.matches });
        });
      },
    }).addTo(mapa);
  }

  // Com o mapa bem afastado, nomes curtos, para os territórios do norte não se atropelarem
  const NOME_CURTO = { 1: "Jd. Japão", 2: "Caucaia do Alto", 3: "Mirizola", 4: "Central", 5: "KM 21", 6: "Arco-Íris", 7: "Caputera" };

  function desenharRotulos() {
    const quebrar = (nome) => esc(nome).replace(" / ", " /<br>").replace(" (", "<br>(");
    for (const t of territorios) {
      L.marker([t.rotulo_lat, t.rotulo_lon], {
        pane: "rotulos", interactive: false, keyboard: false,
        icon: L.divIcon({
          className: "rotulo-territorio", iconSize: [0, 0],
          html: `<span class="longo">${quebrar(t.nome)}</span><span class="curto">${esc(NOME_CURTO[t.numero] || t.nome)}</span>`,
        }),
      }).addTo(mapa);
    }
    L.marker(CENTRO_RESERVA, {
      pane: "rotulos", interactive: false, keyboard: false,
      icon: L.divIcon({ className: "rotulo-reserva", html: "<span>Reserva do<br>Morro Grande</span>", iconSize: [0, 0] }),
    }).addTo(mapa);
  }

  function ficha(p) {
    const linhas = [
      ["Tipo", p.subtipo],
      ["Gestão", { municipal: "Municipal", estadual: "Estadual", conveniada: "Conveniada" }[p.gestao] || p.gestao],
      ["Endereço", [p.endereco, p.bairro].filter(Boolean).join(" — ")],
      ["Telefone", p.telefone],
      ["Território", p.territorio],
      ["Fonte", `<a href="${esc(p.fonte_url)}" target="_blank" rel="noopener">${esc(p.fonte)}</a>`],
      ["Coleta", dataBR(p.data_coleta)],
    ].filter(([, v]) => v);
    const corpo = linhas.map(([k, v]) => `<dt>${k}</dt><dd>${k === "Fonte" ? v : esc(v)}</dd>`).join("");
    const avisos = [];
    if (p.verificacao === "nao_confirmado") avisos.push("Endereço sem confirmação oficial recente.");
    if (p.observacao) avisos.push(linkar(p.observacao));
    return `<div class="ficha" style="--cor: var(--${FAMILIA_DA_CAMADA[p.camada]})">
      <p class="ficha-tipo">${esc(CAMADAS[p.camada].rotulo)}</p>
      <h3>${esc(p.nome)}</h3><dl>${corpo}</dl>
      ${avisos.map((a) => `<p class="aviso">${a}</p>`).join("")}</div>`;
  }

  // No celular, a ficha abre com a folha recolhida e o mapa desvia dela
  function prepararPopup(marcador) {
    const popup = marcador.getPopup();
    if (!popup) return;
    if (!painelCamadas.hidden) alternarCamadas(false);
    if (largo.matches) {
      popup.options.autoPanPaddingBottomRight = L.point(16, 16);
    } else {
      if (posicaoFolha !== "baixo") definirFolha("baixo");
      popup.options.autoPanPaddingBottomRight = L.point(16, alturas().baixo + 16);
    }
  }

  function desenharEquipamentos(gj) {
    for (const f of gj.features) {
      const p = f.properties;
      const [lon, lat] = f.geometry.coordinates;
      const classes = ["mk"];
      if (p.coord_origem === "pendente") classes.push("aprox");
      if (p.verificacao === "nao_confirmado") classes.push("nconf");
      const m = L.marker([lat, lon], {
        icon: L.divIcon({
          className: "mk-wrap", iconSize: [26, 26], iconAnchor: [13, 13], popupAnchor: [0, -12], tooltipAnchor: [0, -14],
          html: `<div class="${classes.join(" ")}" style="--cor: var(--${FAMILIA_DA_CAMADA[p.camada]})">${svg(CAMADAS[p.camada].icone)}</div>`,
        }),
        title: `${p.nome} (${CAMADAS[p.camada].rotulo})`,
        riseOnHover: true,
      });
      m.on("click", () => prepararPopup(m));
      m.bindPopup(ficha(p), { maxWidth: 300, autoPanPaddingTopLeft: L.point(16, 64) });
      if (comMouse.matches) m.bindTooltip(esc(p.nome), { direction: "top", className: "dica" });
      m.props = p;
      marcadores.push(m);
      equipamentos.push({ ...p, lat, lon, marcador: m });
    }
    atualizarMarcadores();
  }

  function atualizarMarcadores() {
    const nomeSel = estado.territorio ? porNumero[estado.territorio].nome : null;
    for (const m of marcadores) {
      const visivel = estado.camadas.has(m.props.camada) && (!nomeSel || m.props.territorio === nomeSel);
      if (visivel && !mapa.hasLayer(m)) m.addTo(mapa);
      if (!visivel && mapa.hasLayer(m)) m.remove();
    }
  }

  // Área útil do mapa: no celular, desconta a folha (no máximo a altura média); em cima, os botões flutuantes
  function margens() {
    const alt = alturas();
    let baixo = largo.matches ? 20 : Math.min(alt[posicaoFolha], alt.meio) + 16;
    baixo = Math.max(20, Math.min(baixo, mapa.getSize().y - 68 - 120)); // tela baixa (celular deitado): sobra ao menos 120 px
    return { paddingTopLeft: L.point(20, 68), paddingBottomRight: L.point(20, baixo) };
  }
  function ajustarVista(limites, opcoes = {}) {
    mapa.fitBounds(limites, { ...margens(), animate: !reduzMovimento, ...opcoes });
  }
  const enquadrarCotia = () => limitesCotia && ajustarVista(limitesCotia);

  // Não deixa arrastar Cotia para fora da tela nem afastar além de um passo do enquadramento.
  // Folga maior ao sul: no celular, a folha cobre a parte de baixo do mapa.
  function limitarMapa() {
    const sw = limitesCotia.getSouthWest(), ne = limitesCotia.getNorthEast();
    const dLat = ne.lat - sw.lat, dLng = ne.lng - sw.lng;
    mapa.setMaxBounds(L.latLngBounds([sw.lat - dLat * 2.5, sw.lng - dLng * 0.6], [ne.lat + dLat * 0.6, ne.lng + dLng * 0.6]));
    ajustarZoomMinimo();
  }
  function ajustarZoomMinimo() {
    const { x, y } = mapa.getSize();
    if (!x || !y) return;
    const m = margens();
    mapa.options.minZoom = 8;
    const zCotia = mapa.getBoundsZoom(limitesCotia, false, m.paddingTopLeft.add(m.paddingBottomRight));
    mapa.setMinZoom(Math.max(8, zCotia - 1));
  }

  // ---------- folha (celular) ----------

  const POSICOES = ["baixo", "meio", "alto"];
  let posicaoFolha = "meio";

  function alturas() {
    const h = window.innerHeight;
    const alto = Math.max(160, h - topo.offsetHeight - 10);
    return { baixo: Math.min(132, alto), meio: Math.min(alto, Math.max(280, Math.round(h * 0.44))), alto };
  }

  function definirFolha(pos) {
    posicaoFolha = pos;
    folha.dataset.posicao = pos;
    if (largo.matches) {
      folha.style.removeProperty("--folha-h");
      return;
    }
    folha.style.setProperty("--folha-h", `${alturas()[pos]}px`);
    if (pos === "alto") mapa.closePopup();
    alca.setAttribute("aria-expanded", String(pos !== "baixo"));
    alca.setAttribute("aria-label", { baixo: "Abrir o painel", meio: "Expandir o painel", alto: "Recolher o painel" }[pos]);
  }

  let arrasto = null;
  let fimDoArrasto = 0;
  alca.addEventListener("pointerdown", (e) => {
    if (largo.matches || e.button !== 0) return;
    arrasto = { id: e.pointerId, y0: e.clientY, h0: folha.getBoundingClientRect().height, yAnt: e.clientY, tAnt: e.timeStamp, v: 0, moveu: false };
    alca.setPointerCapture(e.pointerId);
  });
  alca.addEventListener("pointermove", (e) => {
    if (!arrasto || e.pointerId !== arrasto.id) return;
    const dy = e.clientY - arrasto.y0;
    if (!arrasto.moveu && Math.abs(dy) < 6) return;
    if (!arrasto.moveu) { arrasto.moveu = true; folha.classList.add("arrastando"); }
    const dt = e.timeStamp - arrasto.tAnt;
    if (dt > 0) arrasto.v = 0.7 * ((e.clientY - arrasto.yAnt) / dt) + 0.3 * arrasto.v;
    arrasto.yAnt = e.clientY;
    arrasto.tAnt = e.timeStamp;
    const alt = alturas();
    folha.style.setProperty("--folha-h", `${Math.min(alt.alto, Math.max(alt.baixo * 0.75, arrasto.h0 - dy))}px`);
  });
  function soltarFolha(e) {
    if (!arrasto || e.pointerId !== arrasto.id) return;
    const a = arrasto;
    arrasto = null;
    if (!a.moveu) return; // toque simples: o clique decide
    fimDoArrasto = performance.now();
    folha.classList.remove("arrastando");
    const h = folha.getBoundingClientRect().height;
    const alt = alturas();
    let alvo;
    if (Math.abs(a.v) > 0.45) {
      const acima = POSICOES.filter((p) => alt[p] > h + 1);
      const abaixo = POSICOES.filter((p) => alt[p] < h - 1);
      alvo = a.v < 0 ? acima[0] || "alto" : abaixo[abaixo.length - 1] || "baixo";
    } else {
      alvo = POSICOES.reduce((m, p) => (Math.abs(alt[p] - h) < Math.abs(alt[m] - h) ? p : m), "meio");
    }
    definirFolha(alvo);
  }
  alca.addEventListener("pointerup", soltarFolha);
  alca.addEventListener("pointercancel", soltarFolha);
  alca.addEventListener("click", () => {
    if (performance.now() - fimDoArrasto < 400) return;
    definirFolha(posicaoFolha === "alto" ? "baixo" : POSICOES[POSICOES.indexOf(posicaoFolha) + 1]);
  });
  alca.addEventListener("keydown", (e) => {
    const i = POSICOES.indexOf(posicaoFolha);
    if (e.key === "ArrowUp") { e.preventDefault(); definirFolha(POSICOES[Math.min(2, i + 1)]); }
    if (e.key === "ArrowDown") { e.preventDefault(); definirFolha(POSICOES[Math.max(0, i - 1)]); }
  });

  // ---------- abas e vistas da folha ----------

  const listaAbas = () => [...document.querySelectorAll('.abas [role="tab"]')];

  function atualizarComparando() {
    const agora = largo.matches && !vistaAbas.hidden && estado.aba === "comparar";
    if (app.classList.contains("comparando") !== agora) {
      app.classList.toggle("comparando", agora);
      mapa.invalidateSize({ animate: false });
      if (!estado.territorio && limitesCotia) ajustarVista(limitesCotia, { animate: false });
    }
  }

  function mostrarVista(qual) {
    vistaAbas.hidden = qual !== "abas";
    vistaTerritorio.hidden = qual !== "territorio";
    atualizarComparando();
  }

  function ativarAba(id, { focar = false, posicao = null, rolar = true } = {}) {
    estado.aba = id;
    for (const a of listaAbas()) {
      const sel = a.id === `aba-btn-${id}`;
      a.setAttribute("aria-selected", String(sel));
      a.tabIndex = sel ? 0 : -1;
      document.getElementById(a.getAttribute("aria-controls")).hidden = !sel;
      if (sel && focar) a.focus();
    }
    mostrarVista("abas");
    if (rolar) corpoAbas.scrollTop = 0;
    if (!largo.matches) definirFolha(posicao || (id === "bairro" || id === "comparar" ? "alto" : "meio"));
  }

  function montarAbas() {
    const abas = listaAbas();
    abas.forEach((a, i) => {
      const id = a.id.replace("aba-btn-", "");
      a.addEventListener("click", () => ativarAba(id));
      a.addEventListener("keydown", (e) => {
        const ir = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: abas.length - 1 }[e.key];
        if (ir === undefined) return;
        e.preventDefault();
        ativarAba(abas[(ir + abas.length) % abas.length].id.replace("aba-btn-", ""), { focar: true, posicao: posicaoFolha });
      });
    });
  }

  // ---------- painel do território ----------

  function regua(t, r) {
    const valores = territorios.map((x) => ({ t: x, v: razao(x, r) })).filter((x) => x.v !== null);
    const m = media(r);
    const max = Math.max(m, ...valores.map((x) => x.v)) * 1.08;
    const X = (v) => 12 + (v / max) * 276;
    const outros = valores.filter((x) => x.t.numero !== t.numero)
      .map((x) => `<circle class="outro" cx="${X(x.v).toFixed(1)}" cy="27" r="4"><title>${esc(x.t.nome)}: 1 para ${fmt(x.v)}</title></circle>`).join("");
    const este = valores.find((x) => x.t.numero === t.numero);
    const xm = X(m);
    return `<svg class="regua" viewBox="0 0 300 40" role="img" aria-label="Comparação com os outros territórios: ${esc(t.nome)} ${este ? `tem 1 para ${fmt(este.v)}` : "não tem este equipamento"}; média de Cotia 1 para ${fmt(m)}.">
      <line class="eixo" x1="12" x2="288" y1="27" y2="27"/>
      <line class="media" x1="${xm.toFixed(1)}" x2="${xm.toFixed(1)}" y1="16" y2="36"/>
      <text x="${xm.toFixed(1)}" y="11" text-anchor="middle">média de Cotia</text>
      ${outros}
      ${este ? `<circle class="este" cx="${X(este.v).toFixed(1)}" cy="27" r="6.5"><title>${esc(t.nome)}: 1 para ${fmt(este.v)}</title></circle>` : ""}
    </svg>`;
  }

  function htmlPainel(t) {
    const cras = equipamentos.find((e) => e.id === t.cras_referencia);
    const crasTexto = cras
      ? `${esc(cras.nome)} — ${esc(cras.endereco)}${cras.coord_origem === "pendente" ? " (ponto aproximado no mapa)" : ""}`
      : "não identificado";
    const razoes = RAZOES.map((r) => {
      const v = razao(t, r);
      const texto = v === null
        ? `${r.nenhum} Média de Cotia: 1 para ${fmt(media(r))} crianças.`
        : `${r.um} para cada <strong>${fmt(v)}</strong> crianças. Média de Cotia: 1 para ${fmt(media(r))}.`;
      return `<div class="razao"><p class="razao-titulo">${r.nome}</p><p class="razao-texto">${texto}</p>${regua(t, r)}</div>`;
    }).join("");
    const lista = TODAS_CAMADAS.map((c) => {
      const n = t[`n_${c}`] || 0;
      return `<li class="${n ? "" : "zero"}">${amostra(c)}<span>${esc(CAMADAS[c].rotulo)}</span><span class="n">${n}</span></li>`;
    }).join("");
    const aprox = t.n_aproximados
      ? ` ${t.n_aproximados} ${t.n_aproximados === 1 ? "equipamento deste território tem" : "equipamentos deste território têm"} localização aproximada.`
      : "";
    const nb = t.bairros.length;
    return `
      <div class="pt-cabeca">
        <p class="sobretitulo pt-numero" style="--c: ${corFundo(t.numero)}">Território ${t.numero} de 7</p>
        <h2 id="pt-nome" tabindex="-1">${esc(t.nome)}</h2>
        <p class="pt-cras">CRAS de referência: ${crasTexto}</p>
      </div>
      <section class="pt-secao">
        <h3>Quem mora aqui · Censo 2022</h3>
        <div class="pop-destaque"><strong>${fmt(t.criancas)}</strong><span>crianças de 0 a 14 anos</span></div>
        <dl class="pop-faixas">
          <div><dt>0 a 4 anos</dt><dd>${fmt(t.pop_0_4)}</dd></div>
          <div><dt>5 a 9 anos</dt><dd>${fmt(t.pop_5_9)}</dd></div>
          <div><dt>10 a 14 anos</dt><dd>${fmt(t.pop_10_14)}</dd></div>
        </dl>
        <p class="pop-extra">${fmt(t.pop_15_19)} adolescentes de 15 a 19 anos · ${fmt(t.pop_total)} moradores no total</p>
      </section>
      <section class="pt-secao">
        <h3>Crianças por equipamento</h3>
        ${razoes}
      </section>
      <section class="pt-secao">
        <h3>Equipamentos no território · ${t.n_equipamentos}</h3>
        <ul class="eq-lista">${lista}</ul>
      </section>
      ${nb ? `<section class="pt-secao">
        <h3>Bairros na lista do PMAS · ${nb}</h3>
        <details class="pt-bairros"><summary>Ver ${nb === 1 ? "o bairro" : `os ${nb} bairros`}</summary>
          <p>${t.bairros.map((b) => esc(b.nome)).join(" · ")}</p></details>
      </section>` : ""}
      <p class="pt-nota">Os limites são uma aproximação do mapa do PMAS 2026–2029, refeita com os setores do Censo 2022.${aprox}
        Contar equipamentos não mede qualidade, equipe nem fila. <a href="metodologia.html#territorios">Como os territórios foram desenhados</a></p>`;
  }

  let origemFoco = null;
  let rolagemAbas = 0;

  function marcarSelecionados() {
    document.querySelectorAll("#tabela tbody tr").forEach((tr) => tr.classList.toggle("selecionada", Number(tr.dataset.t) === estado.territorio));
    document.querySelectorAll("#ranking button").forEach((b) => b.classList.toggle("selecionada", Number(b.dataset.t) === estado.territorio));
  }

  function selecionarTerritorio(num, { enquadrar = true, focar = false } = {}) {
    const anterior = estado.territorio;
    estado.territorio = num || null;
    redesenharMapa();
    atualizarMarcadores();
    marcarSelecionados();
    if (num) {
      if (!anterior) rolagemAbas = corpoAbas.scrollTop;
      conteudoPainel.innerHTML = htmlPainel(porNumero[num]);
      botaoVoltar.textContent = ROTULO_VOLTAR[estado.aba] || ROTULO_VOLTAR.territorio;
      mostrarVista("territorio");
      corpoTerritorio.scrollTop = 0;
      if (!largo.matches && posicaoFolha !== "meio") definirFolha("meio");
      if (focar) document.getElementById("pt-nome").focus({ preventScroll: true });
      if (enquadrar) ajustarVista(camadaDoTerritorio(num).getBounds(), { maxZoom: 15 });
      history.replaceState(null, "", `#t${num}`);
    } else {
      mostrarVista("abas");
      if (location.hash) history.replaceState(null, "", location.pathname + location.search);
    }
  }

  function voltarDoTerritorio() {
    const num = estado.territorio;
    selecionarTerritorio(null);
    ativarAba(estado.aba, { rolar: false });
    corpoAbas.scrollTop = rolagemAbas;
    enquadrarCotia();
    const alvo = origemFoco && document.contains(origemFoco) ? origemFoco
      : (estado.aba === "territorio" && document.querySelector(`#lista-territorios [data-t="${num}"]`)) || document.getElementById(`aba-btn-${estado.aba}`);
    alvo?.focus({ preventScroll: true });
    origemFoco = null;
  }
  botaoVoltar.addEventListener("click", voltarDoTerritorio);

  // ---------- lista de territórios e de bairros ----------

  function montarListaTerritorios() {
    document.getElementById("lista-territorios").innerHTML = territorios.map((t) => `
      <li><button type="button" data-t="${t.numero}">
        <span class="sw" style="--c: ${corFundo(t.numero)}"></span>
        <span><span class="lt-nome">${esc(t.nome)}</span>
          <span class="lt-info">${fmt(t.criancas)} crianças · ${t.n_equipamentos} equipamentos</span></span>
        <span class="lt-seta" aria-hidden="true">›</span>
      </button></li>`).join("");
  }

  const entradaBairro = document.getElementById("in-bairro");
  const listaBairros = document.getElementById("lista-bairros");
  let statusBairros;

  function filtrarBairros() {
    const q = leve(entradaBairro.value);
    return territorios
      .map((t) => ({ t, lista: q ? t.bairros.filter((b) => b.busca.some((x) => x.includes(q))) : t.bairros }))
      .filter((g) => g.lista.length);
  }

  function desenharBairros() {
    const filtro = entradaBairro.value.trim();
    const grupos = filtrarBairros();
    const total = grupos.reduce((s, g) => s + g.lista.length, 0);
    statusBairros.textContent = filtro ? (total ? `${total} ${total === 1 ? "bairro encontrado" : "bairros encontrados"}` : "Nenhum bairro encontrado") : "";
    if (!grupos.length) {
      listaBairros.innerHTML = `<p class="vazio">“${esc(filtro)}” não está nas listas de bairros do PMAS 2026–2029. Tente outra grafia ou busque pelo endereço.</p>`;
      return;
    }
    listaBairros.innerHTML = grupos.map(({ t, lista }) => `
      <section class="grupo-bairros" aria-labelledby="gb-${t.numero}">
        <h3 class="titulo-grupo" id="gb-${t.numero}"><span class="sw" style="--c: ${corFundo(t.numero)}"></span>${esc(t.nome)}<span class="contagem">${lista.length} ${lista.length === 1 ? "bairro" : "bairros"}</span></h3>
        <ul class="bairros">${lista.map((b) => {
          const outros = b.territorios.filter((n) => n !== t.numero).map((n) => porNumero[n].nome);
          return `<li><button type="button" data-t="${t.numero}"><span class="b-nome">${esc(b.nome)}</span>${outros.length ? `<span class="tambem">também na lista de ${esc(outros.join(" e "))}</span>` : ""}</button></li>`;
        }).join("")}</ul>
      </section>`).join("");
  }

  function montarBairros() {
    for (const b of bairros) b.busca = [leve(b.nome), porExtenso(b.nome)];
    listaBairros.insertAdjacentHTML("beforebegin", '<p class="sr-only" id="bairros-status" aria-live="polite"></p>');
    statusBairros = document.getElementById("bairros-status");
    entradaBairro.addEventListener("input", desenharBairros);
    entradaBairro.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      e.preventDefault();
      const botoes = listaBairros.querySelectorAll("button[data-t]");
      if (botoes.length === 1) botoes[0].click();
    });
    desenharBairros();
  }

  // ---------- busca por endereço e localização ----------

  const mostrar = (html) => { resultado.innerHTML = html; };

  async function geocodificar(q) {
    const url = new URL("https://nominatim.openstreetmap.org/search");
    url.search = new URLSearchParams({
      q: `${q}, Cotia, SP`, format: "jsonv2", limit: "1", countrycodes: "br",
      viewbox: "-47.20,-23.48,-46.75,-23.88", bounded: "1", "accept-language": "pt-BR",
    });
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if (!r.ok) throw new Error(String(r.status));
    const [h] = await r.json();
    return h ? { lat: Number(h.lat), lon: Number(h.lon), nome: h.display_name.split(",").slice(0, 3).join(",") } : null;
  }

  const territorioDoPonto = (lat, lon) => territorios.find((t) => dentroDaGeometria(lon, lat, t.geometria)) || null;

  function mostrarPerto(lat, lon, rotulo) {
    if (estado.territorio) selecionarTerritorio(null, { enquadrar: false });
    if (marcadorBusca) marcadorBusca.remove();
    marcadorBusca = L.marker([lat, lon], {
      icon: L.divIcon({ className: "", html: '<div class="marcador-busca"></div>', iconSize: [20, 20], iconAnchor: [10, 10] }),
      title: rotulo, keyboard: false, zIndexOffset: 1000,
    }).addTo(mapa).bindTooltip(esc(rotulo), { direction: "top", offset: [0, -10], className: "dica", permanent: !comMouse.matches });

    const terr = territorioDoPonto(lat, lon);
    const perto = GRUPOS_PERTO.map((g) => {
      const candidatos = equipamentos.filter(g.teste).map((e) => ({ e, d: distanciaM([lat, lon], [e.lat, e.lon]) })).sort((a, b) => a.d - b.d);
      return candidatos.length ? { g, ...candidatos[0] } : null;
    }).filter(Boolean);
    const itens = perto.map(({ g, e, d }) => `
      <li><button type="button" data-eq="${esc(e.id)}">${amostra(e.camada)}
        <span><span class="perto-nome">${esc(e.nome)}</span><span class="perto-tipo">${esc(g.rotulo)} mais perto${e.coord_origem === "pendente" ? " · ponto aproximado" : ""}</span></span>
        <span class="perto-dist">${textoDistancia(d)}</span></button></li>`).join("");
    mostrar(`<p><strong>${esc(rotulo)}</strong>${terr ? ` fica no território <button type="button" class="escolha" data-t="${terr.numero}">${esc(terr.nome)}</button>` : " fica fora dos limites de Cotia."}</p>
      <p>Mais perto deste ponto, em linha reta:</p><ul class="perto">${itens}</ul>`);
    const grupo = L.featureGroup([marcadorBusca, ...perto.map((p) => L.marker([p.e.lat, p.e.lon]))]);
    ajustarVista(grupo.getBounds(), { maxZoom: 15 });
  }

  function abrirEquipamento(id) {
    const e = equipamentos.find((x) => x.id === id);
    if (!e) return;
    if (!estado.camadas.has(e.camada)) {
      estado.camadas.add(e.camada);
      const caixa = document.querySelector(`[data-camada="${e.camada}"]`);
      if (caixa) caixa.checked = true;
    }
    atualizarMarcadores();
    prepararPopup(e.marcador);
    mapa.setView([e.lat, e.lon], Math.max(mapa.getZoom(), 15), { animate: false });
    e.marcador.openPopup();
  }

  function montarEndereco() {
    const form = document.getElementById("form-endereco");
    if (!form) return;
    const entrada = document.getElementById("in-endereco");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = entrada.value.trim();
      if (!q) return;
      entrada.blur();
      mostrar("<p>Buscando o endereço…</p>");
      try {
        const achado = await geocodificar(q);
        if (!achado) {
          mostrar(`<p>Não encontrei “${esc(q)}” em Cotia. Confira a grafia ou escreva só a rua e o bairro.</p>`);
          return;
        }
        mostrarPerto(achado.lat, achado.lon, achado.nome);
      } catch {
        mostrar("<p>A busca de endereço não respondeu. Tente de novo em alguns segundos.</p>");
      }
    });
    document.getElementById("btn-local").addEventListener("click", () => {
      if (!navigator.geolocation) { mostrar("<p>Este navegador não informa a localização.</p>"); return; }
      mostrar("<p>Pedindo a localização ao navegador…</p>");
      navigator.geolocation.getCurrentPosition(
        (pos) => mostrarPerto(pos.coords.latitude, pos.coords.longitude, "Sua localização"),
        (erro) => mostrar(`<p>${erro.code === 1 ? "A permissão de localização foi negada no navegador." : "Não foi possível obter a localização agora."} Você pode buscar pelo endereço.</p>`),
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
      );
    });
  }

  // Botões com território (listas, ranking, resultado da busca) e com equipamento
  folha.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.eq) { abrirEquipamento(b.dataset.eq); return; }
    if (b.dataset.t) {
      origemFoco = b;
      selecionarTerritorio(Number(b.dataset.t), { focar: true });
    }
  });

  // ---------- camadas, cores e legendas ----------

  function alternarCamadas(abrir = painelCamadas.hidden, devolverFoco = false) {
    painelCamadas.hidden = !abrir;
    btnCamadas.setAttribute("aria-expanded", String(abrir));
    legendaModo.hidden = abrir || estado.modo === "pmas";
    if (abrir) {
      if (!menu.hidden) alternarMenu(false);
      document.getElementById("fechar-camadas").focus();
    } else if (devolverFoco) {
      btnCamadas.focus();
    }
  }
  btnCamadas.addEventListener("click", () => alternarCamadas());
  document.getElementById("fechar-camadas").addEventListener("click", () => alternarCamadas(false, true));
  document.getElementById("btn-cotia").addEventListener("click", enquadrarCotia);

  function montarCamadas() {
    const contagem = {};
    for (const e of equipamentos) contagem[e.camada] = (contagem[e.camada] || 0) + 1;
    const lista = document.getElementById("lista-camadas");
    lista.innerHTML = FAMILIAS.map((f) => `
      <div class="familia" style="--cor: var(--${f.id})">
        <p class="familia-nome">${esc(f.nome)}</p>
        ${f.camadas.map((c) => `
          <label class="camada${contagem[c] ? "" : " vazia"}">
            <input type="checkbox" data-camada="${c}" checked>
            ${amostra(c)}<span>${esc(CAMADAS[c].rotulo)}</span><span class="contagem">${contagem[c] || 0}</span>
          </label>`).join("")}
      </div>`).join("");
    lista.addEventListener("change", (e) => {
      const c = e.target.dataset.camada;
      if (!c) return;
      if (e.target.checked) estado.camadas.add(c); else estado.camadas.delete(c);
      atualizarMarcadores();
    });
  }

  function montarModos() {
    const modos = document.getElementById("modos");
    modos.innerHTML = MODOS.map((m) => `<button type="button" role="radio" data-modo="${m.id}" aria-checked="${m.id === estado.modo}" tabindex="${m.id === estado.modo ? 0 : -1}">${esc(m.rotulo)}</button>`).join("");
    const escolherModo = (id, focar) => {
      estado.modo = id;
      modos.querySelectorAll("button").forEach((b) => {
        const ativo = b.dataset.modo === id;
        b.setAttribute("aria-checked", String(ativo));
        b.tabIndex = ativo ? 0 : -1;
        if (ativo && focar) b.focus();
      });
      redesenharMapa();
      desenharLegenda();
    };
    modos.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) escolherModo(b.dataset.modo); });
    modos.addEventListener("keydown", (e) => {
      const ids = MODOS.map((m) => m.id);
      const i = ids.indexOf(estado.modo);
      if (["ArrowRight", "ArrowDown"].includes(e.key)) { e.preventDefault(); escolherModo(ids[(i + 1) % ids.length], true); }
      if (["ArrowLeft", "ArrowUp"].includes(e.key)) { e.preventDefault(); escolherModo(ids[(i - 1 + ids.length) % ids.length], true); }
    });
    desenharLegenda();
  }

  function desenharLegenda() {
    const alvo = document.getElementById("legenda-territorios");
    if (estado.modo === "pmas") {
      alvo.innerHTML = `<p>As cores do mapa oficial do Plano Municipal de Assistência Social 2026–2029, em tom mais claro. Toque num território para ver os números.</p>` +
        territorios.map((t) => `<div class="leg-item"><span class="leg-cor" style="--c: ${corFundo(t.numero)}"></span><span>${t.numero}. ${esc(t.nome)}</span></div>`).join("");
      legendaModo.hidden = true;
      legendaModo.innerHTML = "";
      return;
    }
    const r = RAZOES.find((x) => x.id === estado.modo);
    const temSem = territorios.some((t) => razao(t, r) === null);
    alvo.innerHTML = `<p>Crianças de 0 a 14 anos por ${nomeRazao(r)} em cada território, comparado com a média de Cotia (1 para ${fmt(media(r))}). Acima da média = mais crianças para cada equipamento.</p>` +
      CLASSES.map((c) => `<div class="leg-item"><span class="leg-cor" style="--c: var(--div-${c.id})"></span><span>${c.texto}</span></div>`).join("") +
      (temSem ? `<div class="leg-item"><span class="leg-cor" style="--c: var(--div-nenhum)"></span><span>nenhum equipamento deste tipo no território</span></div>` : "");
    legendaModo.innerHTML = `<strong>Crianças por ${esc(nomeRazao(r))} × média de Cotia</strong>
      <div class="escala">${CLASSES.map((c) => `<span style="--c: var(--div-${c.id})"></span>`).join("")}</div>
      <div class="escala-rotulos"><span>menos</span><span>média</span><span>mais</span></div>
      ${temSem ? `<span class="sem">${esc(r.nenhum.replace(" dentro do território.", ""))} no território</span>` : ""}`;
    legendaModo.hidden = !painelCamadas.hidden;
  }

  // ---------- menu do topo e atalhos ----------

  function alternarMenu(abrir = menu.hidden, devolverFoco = false) {
    menu.hidden = !abrir;
    btnMenu.setAttribute("aria-expanded", String(abrir));
    if (abrir) {
      if (!painelCamadas.hidden) alternarCamadas(false);
      menu.querySelector("a")?.focus();
    } else if (devolverFoco) {
      btnMenu.focus();
    }
  }
  btnMenu.addEventListener("click", () => alternarMenu());

  function irPara(alvo) {
    if (estado.territorio) selecionarTerritorio(null, { enquadrar: false });
    ativarAba("comparar", { posicao: "alto" });
    const titulo = document.getElementById(alvo === "dados" ? "t-dados" : "t-comparar");
    titulo.tabIndex = -1;
    // Rola só a folha (scrollIntoView rolaria também a página que contém o site, quando ele está num iframe)
    requestAnimationFrame(() => {
      corpoAbas.scrollTop += titulo.getBoundingClientRect().top - corpoAbas.getBoundingClientRect().top - 8;
      titulo.focus({ preventScroll: true });
    });
  }

  document.addEventListener("click", (e) => {
    const ir = e.target.closest("[data-ir]");
    if (ir) {
      e.preventDefault();
      alternarMenu(false);
      irPara(ir.dataset.ir);
      return;
    }
    if (!menu.hidden && !e.target.closest("#menu, #btn-menu")) alternarMenu(false);
    if (!painelCamadas.hidden && !e.target.closest("#painel-camadas, #btn-camadas")) alternarCamadas(false);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (!menu.hidden) { alternarMenu(false, true); return; }
    if (!painelCamadas.hidden) { alternarCamadas(false, true); return; }
    if (e.target.matches("input, select, textarea")) return;
    if (document.querySelector(".leaflet-popup")) { mapa.closePopup(); return; }
    if (estado.territorio) voltarDoTerritorio();
  });

  // ---------- comparar ----------

  const COLUNAS = [
    { id: "numero", rotulo: "Território", valor: (t) => t.numero },
    { id: "pop_total", rotulo: "Moradores", grupo: true },
    { id: "criancas", rotulo: "Crianças 0–14", grupo: true },
    { id: "pop_0_4", rotulo: "0–4 anos" },
    { id: "pop_5_9", rotulo: "5–9 anos" },
    { id: "pop_10_14", rotulo: "10–14 anos" },
    { id: "pop_15_19", rotulo: "Adolescentes 15–19" },
    { id: "n_saude_atencao_basica", rotulo: "UBS", grupo: true },
    { id: "n_saude_urgencia", rotulo: "Urgência" },
    { id: "n_saude_hospital", rotulo: "Hospital" },
    { id: "n_saude_mental", rotulo: "CAPS" },
    { id: "n_saude_especializada", rotulo: "Especializada" },
    { id: "n_reabilitacao", rotulo: "Reabilitação" },
    { id: "n_educacao_infantil", rotulo: "Creches e pré-escolas", grupo: true },
    { id: "n_cras", rotulo: "CRAS", grupo: true },
    { id: "n_creas", rotulo: "CREAS" },
    { id: "n_protecao", rotulo: "Conselhos Tutelares" },
    ...RAZOES.map((r, i) => ({ id: `r_${r.id}`, rotulo: `Crianças por ${nomeRazao(r)}`, valor: (t) => razao(t, r), razao: r, grupo: i === 0 })),
  ];
  const valorDe = (c, t) => (c.valor ? c.valor(t) : t[c.id]);

  function desenharRanking() {
    const col = COLUNAS.find((c) => c.id === estado.metrica) || COLUNAS.find((c) => c.id === "criancas");
    const itens = territorios.map((t) => ({ t, v: valorDe(col, t) ?? null }));
    const ordenados = [
      ...itens.filter((x) => x.v !== null).sort((a, b) => b.v - a.v || a.t.numero - b.t.numero),
      ...itens.filter((x) => x.v === null),
    ];
    const max = Math.max(...ordenados.map((x) => x.v || 0)) || 1;
    document.getElementById("ranking").innerHTML = ordenados.map(({ t, v }) => `
      <li><button type="button" data-t="${t.numero}" class="${estado.territorio === t.numero ? "selecionada" : ""}">
        <span class="sw" style="--c: ${corFundo(t.numero)}"></span>
        <span class="r-nome">${esc(t.nome)}</span>
        <span class="r-valor">${v === null ? "—" : fmt(v)}</span>
        <span class="r-trilho" aria-hidden="true"><span class="r-barra" style="width: ${v === null ? 0 : Math.max(1.5, (v / max) * 100).toFixed(1)}%"></span></span>
      </button></li>`).join("");
    let nota;
    if (col.razao) {
      const r = col.razao;
      nota = `Crianças de 0 a 14 anos para cada ${nomeRazao(r)} dentro do território. Média de Cotia: 1 para ${fmt(media(r))}.`;
      if (ordenados.some((x) => x.v === null)) nota += ` “—”: ${r.nenhum.charAt(0).toLowerCase()}${r.nenhum.slice(1)}`;
    } else if (col.id === "criancas" || col.id.startsWith("pop_")) {
      nota = "Censo 2022 (IBGE).";
    } else {
      nota = "Equipamentos dentro dos limites do território. Contar equipamentos não mede qualidade, equipe, horário nem fila.";
    }
    document.getElementById("nota-ranking").textContent = nota;
  }

  function desenharTabela() {
    const tabela = document.getElementById("tabela");
    tabela.querySelector("thead").innerHTML = `<tr>${COLUNAS.map((c) => {
      const sort = estado.ordem.col === c.id ? (estado.ordem.dir > 0 ? "ascending" : "descending") : "none";
      return `<th scope="col" aria-sort="${sort}" class="${c.grupo ? "grupo-ini" : ""}"><button type="button" data-col="${c.id}">${esc(c.rotulo)}</button></th>`;
    }).join("")}</tr>`;

    const col = COLUNAS.find((c) => c.id === estado.ordem.col);
    const linhas = [...territorios].sort((a, b) => {
      const va = valorDe(col, a), vb = valorDe(col, b);
      if (va === null) return 1;
      if (vb === null) return -1;
      return (va - vb) * estado.ordem.dir;
    });
    const maxRazao = Object.fromEntries(RAZOES.map((r) => [r.id, Math.max(...territorios.map((t) => razao(t, r) || 0))]));
    tabela.querySelector("tbody").innerHTML = linhas.map((t) => `
      <tr data-t="${t.numero}" class="${estado.territorio === t.numero ? "selecionada" : ""}">${COLUNAS.map((c, i) => {
        if (i === 0) return `<td><span class="terr" style="--c: ${corFundo(t.numero)}">${t.numero}. ${esc(t.nome)}</span></td>`;
        const v = valorDe(c, t);
        const cls = c.grupo ? ' class="grupo-ini"' : "";
        if (c.razao) {
          if (v === null) return `<td${cls}>—</td>`;
          const w = Math.max(2, Math.round((v / maxRazao[c.razao.id]) * 48));
          return `<td${cls}><span class="barra" style="width:${w}px" aria-hidden="true"></span>${fmt(v)}</td>`;
        }
        return `<td${cls}>${fmt(v)}</td>`;
      }).join("")}</tr>`).join("");

    const soma = (id) => territorios.reduce((s, t) => s + (t[id] || 0), 0);
    const sigilo = territorios[0]?.moradores_em_sigilo_municipio || 0;
    document.getElementById("nota-tabela").textContent =
      `A linha Cotia soma os 7 territórios. Ficam de fora os ${fmt(sigilo)} moradores dos setores em que o IBGE omite os números por sigilo (total oficial: ${fmt(soma("pop_total") + sigilo)}).`;
    tabela.querySelector("tfoot").innerHTML = `<tr>${COLUNAS.map((c, i) => {
      const cls = c.grupo ? ' class="grupo-ini"' : "";
      if (i === 0) return "<td>Cotia</td>";
      if (c.razao) return `<td${cls}>${fmt(media(c.razao))}</td>`;
      return `<td${cls}>${fmt(soma(c.id))}</td>`;
    }).join("")}</tr>`;
  }

  function montarComparar() {
    const sel = document.getElementById("sel-metrica");
    sel.innerHTML = COLUNAS.filter((c) => c.id !== "numero")
      .map((c) => `<option value="${c.id}"${c.id === estado.metrica ? " selected" : ""}>${esc(c.rotulo)}</option>`).join("");
    sel.addEventListener("change", () => { estado.metrica = sel.value; desenharRanking(); });
    desenharRanking();

    desenharTabela();
    const tabela = document.getElementById("tabela");
    tabela.addEventListener("click", (e) => {
      const b = e.target.closest("th button");
      if (b) {
        const col = b.dataset.col;
        estado.ordem = { col, dir: estado.ordem.col === col ? -estado.ordem.dir : col === "numero" ? 1 : -1 };
        desenharTabela();
        tabela.querySelector(`th button[data-col="${col}"]`).focus();
        return;
      }
      const tr = e.target.closest("tbody tr");
      if (tr) {
        origemFoco = null;
        selecionarTerritorio(Number(tr.dataset.t), { focar: true });
      }
    });
  }

  // ---------- prévia ----------

  function ajustarPrevia() {
    if (!PREVIA) return;
    document.getElementById("aba-btn-endereco").remove();
    document.getElementById("aba-endereco").remove();
    document.getElementById("aba-territorio").insertAdjacentHTML("afterbegin",
      '<p class="aviso-previa">Prévia: a busca por endereço e os downloads funcionam no site publicado.</p>');
    const downloads = document.querySelector(".downloads");
    if (downloads) {
      downloads.outerHTML = '<p class="nota">Na prévia, os arquivos não podem ser baixados. No site publicado ficam aqui os links para <strong>equipamentos.csv</strong> e <strong>territorios.geojson</strong>.</p>';
    }
  }

  // ---------- início ----------

  function aplicarHash() {
    const h = location.hash;
    const m = h.match(/^#t([1-7])$/);
    if (m) {
      if (estado.territorio !== Number(m[1])) selecionarTerritorio(Number(m[1]));
      return true;
    }
    if (h === "#comparar" || h === "#dados") irPara(h.slice(1));
    return false;
  }

  let aoTerTamanho = null;
  new ResizeObserver(() => {
    mapa.invalidateSize({ animate: false });
    const { x, y } = mapa.getSize();
    if (aoTerTamanho && x > 0 && y > 0) {
      const fn = aoTerTamanho;
      aoTerTamanho = null;
      fn();
    }
  }).observe(mapa.getContainer());

  let quadro = 0;
  window.addEventListener("resize", () => {
    cancelAnimationFrame(quadro);
    quadro = requestAnimationFrame(() => {
      if (!largo.matches) definirFolha(posicaoFolha);
      mapa.invalidateSize({ animate: false });
      if (limitesCotia) ajustarZoomMinimo();
    });
  });
  largo.addEventListener("change", () => {
    definirFolha(posicaoFolha);
    atualizarComparando();
    mapa.invalidateSize({ animate: false });
  });
  temaEscuro.addEventListener("change", () => { if (camadaTerritorios) redesenharMapa(); });

  async function iniciar() {
    const [contorno, terrGJ, eqGJ, dadosBairros] = await Promise.all([
      carregar("data/cotia.geojson"), carregar("data/territorios.geojson"),
      carregar("data/equipamentos.geojson"), carregar("data/bairros.json"),
    ]);
    bairros = dadosBairros;
    prepararTerritorios(terrGJ);
    camadaBase = L.geoJSON(contorno, { style: estiloBase, interactive: false }).addTo(mapa);
    desenharTerritorios(terrGJ);
    camadaContorno = L.geoJSON(contorno, { style: estiloContorno, interactive: false }).addTo(mapa);
    limitesCotia = camadaContorno.getBounds();
    desenharRotulos();
    desenharEquipamentos(eqGJ);

    ajustarPrevia();
    montarAbas();
    montarListaTerritorios();
    montarBairros();
    montarEndereco();
    montarCamadas();
    montarModos();
    montarComparar();
    document.getElementById("carimbo-sub").textContent = `${equipamentos.length} equipamentos · ${territorios.length} territórios`;
    definirFolha(posicaoFolha);
    document.fonts?.ready.then(() => definirFolha(posicaoFolha)); // a altura do topo muda quando as fontes chegam
    window.addEventListener("hashchange", aplicarHash);

    const aplicarInicio = () => {
      mapa.fitBounds(limitesCotia, { ...margens(), animate: false });
      limitarMapa();
      atualizarZoom();
      aplicarHash();
    };
    const { x, y } = mapa.getSize();
    if (x > 0 && y > 0) aplicarInicio(); else aoTerTamanho = aplicarInicio;
  }

  iniciar().catch((erro) => {
    console.error(erro);
    document.getElementById("mapa").insertAdjacentHTML("beforeend",
      `<p style="position:relative;z-index:1000;margin:16px;padding:12px;background:#fff;color:#14202a;border-radius:6px">Não foi possível carregar os dados do mapa: ${esc(erro.message)}. Recarregue a página.</p>`);
  });
})();
