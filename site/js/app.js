"use strict";

(() => {
  const NUM = new Intl.NumberFormat("pt-BR");
  const fmt = (n) => NUM.format(Math.round(n));
  const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const reduzMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const celular = window.matchMedia("(max-width: 759.98px)");
  // Prévia hospedada onde a página não pode carregar recursos de outros sites (tiles, Nominatim, downloads)
  const PREVIA = window.MODO_PREVIA === true || new URLSearchParams(location.search).has("previa");

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

  const RAZOES = [
    { id: "ubs", campo: "n_saude_atencao_basica", nome: "UBS", um: "1 UBS", nenhum: "Nenhuma UBS dentro do território." },
    { id: "cras", campo: "n_cras", nome: "CRAS", um: "1 CRAS", nenhum: "Nenhum CRAS dentro do território." },
    { id: "educ", campo: "n_educacao_infantil", nome: "Educação infantil", um: "1 creche ou pré-escola", nenhum: "Nenhuma creche ou pré-escola dentro do território." },
  ];
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

  const estado = {
    camadas: new Set(Object.keys(CAMADAS)),
    territorio: null,
    modo: "pmas",
    ordem: { col: "numero", dir: 1 },
  };

  // ---------- utilidades ----------

  const cssVar = (nome) => getComputedStyle(document.documentElement).getPropertyValue(nome).trim();
  const normalizar = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/\b(jd|jardim|pq|parque|vl|vila|chac|chacara|res|residencial)\b\.?/g, " ")
    .replace(/[^a-z0-9]+/g, " ").trim();
  const dataBR = (iso) => (iso || "").split("-").reverse().join("/");

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

  // ---------- mapa ----------

  const mapa = L.map("mapa", { zoomSnap: 0.5, minZoom: 10, maxZoom: 18 });
  if (!PREVIA) {
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    }).addTo(mapa);
  }
  L.control.scale({ imperial: false, position: "bottomleft" }).addTo(mapa);
  mapa.createPane("rotulos");
  mapa.getPane("rotulos").style.zIndex = 450;
  mapa.getPane("rotulos").style.pointerEvents = "none";

  const atualizarZoom = () => mapa.getContainer().classList.toggle("zoom-baixo", mapa.getZoom() < 13);
  mapa.on("zoomend", atualizarZoom);

  let camadaTerritorios, camadaContorno, limitesCotia;
  const marcadores = [];
  let marcadorBusca = null;

  function corDoTerritorio(t) {
    if (estado.modo === "pmas") return { cor: t.cor_png, opacidade: 0.32 };
    const r = RAZOES.find((x) => x.id === estado.modo);
    const c = classeDe(t, r);
    return { cor: cssVar(`--div-${c.id}`), opacidade: c.id === "nenhum" ? 0.45 : 0.62 };
  }

  function estiloTerritorio(f) {
    const t = porNumero[f.properties.numero];
    const sel = estado.territorio;
    const ativo = !sel || sel === t.numero;
    const { cor, opacidade } = corDoTerritorio(t);
    return {
      color: sel === t.numero ? cssVar("--tinta") : estado.modo === "pmas" ? t.cor_png : cssVar("--tinta-2"),
      weight: sel === t.numero ? 3 : estado.modo === "pmas" ? 1.6 : 1,
      opacity: ativo ? 0.95 : 0.35,
      fillColor: cor,
      fillOpacity: ativo ? opacidade : 0.06,
    };
  }

  function desenharTerritorios(gj) {
    camadaTerritorios = L.geoJSON(gj, {
      style: estiloTerritorio,
      onEachFeature: (f, camada) => {
        camada.on("click", (e) => {
          L.DomEvent.stopPropagation(e);
          selecionarTerritorio(f.properties.numero, { enquadrar: false });
        });
      },
    }).addTo(mapa);
    for (const t of territorios) {
      L.marker([t.rotulo_lat, t.rotulo_lon], {
        pane: "rotulos", interactive: false, keyboard: false,
        icon: L.divIcon({ className: "rotulo-territorio", html: `<span style="display:inline-block;transform:translate(-50%,-50%)">${esc(t.nome)}</span>`, iconSize: [0, 0] }),
      }).addTo(mapa);
    }
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
      m.bindPopup(ficha(p), { maxWidth: 320 });
      m.bindTooltip(esc(p.nome), { direction: "top", className: "dica" });
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

  function enquadrarCotia() {
    if (limitesCotia) mapa.fitBounds(limitesCotia, { padding: [16, 16] });
  }

  // O contêiner do mapa pode nascer sem tamanho (aba em segundo plano); enquadra quando houver tamanho.
  function quandoVisivel(fn) {
    let feito = false;
    const tentar = () => {
      mapa.invalidateSize();
      const { x, y } = mapa.getSize();
      if (!feito && x > 0 && y > 0) { feito = true; fn(); }
    };
    new ResizeObserver(tentar).observe(mapa.getContainer());
    tentar();
  }

  // ---------- painel do território ----------

  const area = document.getElementById("area-mapa");
  const painel = document.getElementById("painel-territorio");
  const conteudoPainel = document.getElementById("pt-conteudo");

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
    const lista = FAMILIAS.flatMap((f) => f.camadas).map((c) => {
      const n = t[`n_${c}`] || 0;
      return `<li class="${n ? "" : "zero"}">${amostra(c)}<span>${esc(CAMADAS[c].rotulo)}</span><span class="n">${n}</span></li>`;
    }).join("");
    const aprox = t.n_aproximados
      ? ` ${t.n_aproximados} ${t.n_aproximados === 1 ? "equipamento deste território tem" : "equipamentos deste território têm"} localização aproximada.`
      : "";
    return `
      <div class="pt-cabeca">
        <p class="sobretitulo pt-numero" style="--c: ${esc(t.cor_png)}">Território ${t.numero} de 7</p>
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
        <h3>Equipamentos no território</h3>
        <ul class="eq-lista">${lista}</ul>
      </section>
      <p class="pt-nota">Os limites são uma aproximação do mapa do PMAS 2026–2029, refeita com os setores do Censo 2022.${aprox}
        Contar equipamentos não mede qualidade, equipe nem fila. <a href="metodologia.html#territorios">Como os territórios foram desenhados</a></p>`;
  }

  function abrirPainel(t, focar) {
    conteudoPainel.innerHTML = htmlPainel(t);
    painel.hidden = false;
    area.classList.add("com-painel");
    document.getElementById("carimbo").open = false;
    if (focar) document.getElementById("pt-nome").focus({ preventScroll: true });
  }
  function fecharPainel() {
    painel.hidden = true;
    area.classList.remove("com-painel");
  }
  document.getElementById("pt-fechar").addEventListener("click", () => selecionarTerritorio(null));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && estado.territorio && !document.querySelector(".leaflet-popup")) selecionarTerritorio(null);
  });

  // ---------- seleção de território ----------

  const selTerritorio = document.getElementById("sel-territorio");

  function selecionarTerritorio(num, { enquadrar = true, focar = false } = {}) {
    estado.territorio = num || null;
    selTerritorio.value = num ? String(num) : "";
    camadaTerritorios.setStyle(estiloTerritorio);
    atualizarMarcadores();
    document.querySelectorAll("#tabela tbody tr").forEach((tr) => tr.classList.toggle("selecionada", Number(tr.dataset.t) === estado.territorio));
    if (num) {
      abrirPainel(porNumero[num], focar);
      mapa.invalidateSize({ animate: false });
      if (enquadrar) {
        const camada = camadaTerritorios.getLayers().find((l) => l.feature.properties.numero === num);
        let baixo = 24;
        if (celular.matches) {
          // no celular o painel é uma gaveta sobre o mapa: enquadra o território na faixa que fica visível
          mapa.getContainer().scrollIntoView({ block: "start", behavior: "auto" });
          const r = mapa.getContainer().getBoundingClientRect();
          baixo += Math.max(0, r.bottom - (window.innerHeight - painel.offsetHeight));
        }
        mapa.fitBounds(camada.getBounds(), { paddingTopLeft: [24, 24], paddingBottomRight: [24, baixo], animate: !reduzMovimento });
      }
      history.replaceState(null, "", `#t${num}`);
    } else {
      fecharPainel();
      mapa.invalidateSize({ animate: false });
      history.replaceState(null, "", location.pathname + location.search);
    }
  }

  // ---------- controles ----------

  function ajustarPrevia() {
    if (!PREVIA) return;
    document.getElementById("aba-btn-endereco").remove();
    document.getElementById("aba-endereco").remove();
    document.querySelector(".mapa-wrap").insertAdjacentHTML("afterbegin",
      '<p class="aviso-previa">Prévia: sem o mapa de ruas ao fundo e sem a busca por endereço, que funcionam no site publicado.</p>');
    const downloads = document.querySelector(".downloads");
    if (downloads) {
      downloads.outerHTML = '<p class="secao-texto">Na prévia, os arquivos não podem ser baixados. No site publicado ficam aqui os links para <strong>equipamentos.csv</strong> e <strong>territorios.geojson</strong>.</p>';
    }
  }

  function montarControles() {
    ajustarPrevia();
    for (const t of territorios) selTerritorio.insertAdjacentHTML("beforeend", `<option value="${t.numero}">${t.numero}. ${esc(t.nome)}</option>`);
    selTerritorio.addEventListener("change", () => selecionarTerritorio(Number(selTerritorio.value) || null, { focar: false }));

    const contagem = {};
    for (const e of equipamentos) contagem[e.camada] = (contagem[e.camada] || 0) + 1;
    document.getElementById("lista-camadas").innerHTML = FAMILIAS.map((f) => `
      <div class="familia" style="--cor: var(--${f.id})">
        <p class="familia-nome">${esc(f.nome)}</p>
        ${f.camadas.map((c) => `
          <label class="camada${contagem[c] ? "" : " vazia"}">
            <input type="checkbox" data-camada="${c}" checked>
            ${amostra(c)}<span>${esc(CAMADAS[c].rotulo)}</span><span class="contagem">${contagem[c] || 0}</span>
          </label>`).join("")}
      </div>`).join("");
    document.getElementById("lista-camadas").addEventListener("change", (e) => {
      const c = e.target.dataset.camada;
      if (!c) return;
      if (e.target.checked) estado.camadas.add(c); else estado.camadas.delete(c);
      atualizarMarcadores();
    });

    const modos = document.getElementById("modos");
    modos.innerHTML = MODOS.map((m) => `<button type="button" role="radio" data-modo="${m.id}" aria-checked="${m.id === estado.modo}" tabindex="${m.id === estado.modo ? 0 : -1}">${esc(m.rotulo)}</button>`).join("");
    const escolherModo = (id, focar) => {
      estado.modo = id;
      modos.querySelectorAll("button").forEach((b) => {
        const ativo = b.dataset.modo === id;
        b.setAttribute("aria-checked", ativo);
        b.tabIndex = ativo ? 0 : -1;
        if (ativo && focar) b.focus();
      });
      camadaTerritorios.setStyle(estiloTerritorio);
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

    montarAbas();
    montarBuscas();
  }

  function desenharLegenda() {
    const alvo = document.getElementById("legenda-territorios");
    if (estado.modo === "pmas") {
      alvo.innerHTML = `<p>As cores do mapa oficial do Plano Municipal de Assistência Social 2026–2029. Clique num território para ver os números.</p>` +
        territorios.map((t) => `<div class="leg-item"><span class="leg-cor" style="--c: ${esc(t.cor_png)}"></span><span>${t.numero}. ${esc(t.nome)}</span></div>`).join("");
      return;
    }
    const r = RAZOES.find((x) => x.id === estado.modo);
    alvo.innerHTML = `<p>Crianças de 0 a 14 anos por ${r.id === "educ" ? "creche ou pré-escola" : r.nome} em cada território, comparado com a média de Cotia (1 para ${fmt(media(r))}). Acima da média = mais crianças para cada equipamento.</p>` +
      CLASSES.map((c) => `<div class="leg-item"><span class="leg-cor" style="--c: var(--div-${c.id})"></span><span>${c.texto}</span></div>`).join("") +
      (territorios.some((t) => razao(t, r) === null) ? `<div class="leg-item"><span class="leg-cor" style="--c: var(--div-nenhum)"></span><span>nenhum equipamento deste tipo no território</span></div>` : "");
  }

  function montarAbas() {
    const abas = [...document.querySelectorAll('.abas [role="tab"]')];
    const ativar = (aba, focar) => {
      for (const a of abas) {
        const sel = a === aba;
        a.setAttribute("aria-selected", sel);
        a.tabIndex = sel ? 0 : -1;
        document.getElementById(a.getAttribute("aria-controls")).hidden = !sel;
      }
      if (focar) aba.focus();
    };
    abas.forEach((a, i) => {
      a.addEventListener("click", () => ativar(a));
      a.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") { e.preventDefault(); ativar(abas[(i + 1) % abas.length], true); }
        if (e.key === "ArrowLeft") { e.preventDefault(); ativar(abas[(i - 1 + abas.length) % abas.length], true); }
      });
    });
  }

  // ---------- buscas: bairro, endereço, localização ----------

  const resultado = document.getElementById("resultado-busca");
  const mostrar = (html) => { resultado.innerHTML = html; };

  function montarBuscas() {
    document.getElementById("lista-bairros").innerHTML = bairros.map((b) => `<option value="${esc(b.nome)}"></option>`).join("");

    document.getElementById("form-bairro").addEventListener("submit", (e) => {
      e.preventDefault();
      buscarBairro(document.getElementById("in-bairro").value.trim());
    });
    document.getElementById("form-endereco")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = document.getElementById("in-endereco").value.trim();
      if (!q) return;
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
    document.getElementById("btn-local")?.addEventListener("click", () => {
      if (!navigator.geolocation) { mostrar("<p>Este navegador não informa a localização.</p>"); return; }
      mostrar("<p>Pedindo a localização ao navegador…</p>");
      navigator.geolocation.getCurrentPosition(
        (pos) => mostrarPerto(pos.coords.latitude, pos.coords.longitude, "Sua localização"),
        (erro) => mostrar(`<p>${erro.code === 1 ? "A permissão de localização foi negada no navegador." : "Não foi possível obter a localização agora."} Você pode buscar pelo endereço.</p>`),
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
      );
    });
    resultado.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.t) selecionarTerritorio(Number(b.dataset.t), { focar: true });
      if (b.dataset.bairro) buscarBairro(b.dataset.bairro);
      if (b.dataset.eq) abrirEquipamento(b.dataset.eq);
    });
  }

  function buscarBairro(texto) {
    if (!texto) return;
    const alvo = normalizar(texto);
    let achados = bairros.filter((b) => normalizar(b.nome) === alvo || b.nome.toLowerCase() === texto.toLowerCase());
    if (!achados.length && alvo.length >= 3) achados = bairros.filter((b) => normalizar(b.nome).includes(alvo));
    if (!achados.length) {
      mostrar(`<p>“${esc(texto)}” não está nas listas de bairros do PMAS 2026–2029. Tente outra grafia ou busque pelo endereço.</p>`);
      return;
    }
    if (achados.length > 1 && !achados.every((b) => normalizar(b.nome) === alvo)) {
      mostrar(`<p>Encontrei ${achados.length} bairros parecidos:</p>` +
        achados.slice(0, 10).map((b) => `<button type="button" data-bairro="${esc(b.nome)}">${esc(b.nome)}</button>`).join(""));
      return;
    }
    const b = achados[0];
    const terrs = [...new Set(achados.flatMap((x) => x.territorios))];
    if (terrs.length === 1) {
      mostrar(`<p><strong>${esc(b.nome)}</strong> está na lista do território <strong>${esc(porNumero[terrs[0]].nome)}</strong> no PMAS 2026–2029.</p>`);
      selecionarTerritorio(terrs[0]);
    } else {
      mostrar(`<p><strong>${esc(b.nome)}</strong> aparece na lista de ${terrs.length} territórios no PMAS 2026–2029:</p>` +
        terrs.map((n) => `<button type="button" data-t="${n}">${esc(porNumero[n].nome)}</button>`).join(""));
    }
  }

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

  function territorioDoPonto(lat, lon) {
    return territorios.find((t) => dentroDaGeometria(lon, lat, t.geometria)) || null;
  }

  function mostrarPerto(lat, lon, rotulo) {
    if (estado.territorio) selecionarTerritorio(null, { enquadrar: false });
    if (marcadorBusca) marcadorBusca.remove();
    marcadorBusca = L.marker([lat, lon], {
      icon: L.divIcon({ className: "", html: '<div class="marcador-busca"></div>', iconSize: [18, 18], iconAnchor: [9, 9] }),
      title: rotulo, keyboard: false, zIndexOffset: 1000,
    }).addTo(mapa).bindTooltip(esc(rotulo), { direction: "top", offset: [0, -10], className: "dica" });

    const terr = territorioDoPonto(lat, lon);
    const perto = GRUPOS_PERTO.map((g) => {
      const candidatos = equipamentos.filter(g.teste).map((e) => ({ e, d: distanciaM([lat, lon], [e.lat, e.lon]) })).sort((a, b) => a.d - b.d);
      return candidatos.length ? { g, ...candidatos[0] } : null;
    }).filter(Boolean);
    const itens = perto.map(({ g, e, d }) => `
      <li><button type="button" data-eq="${esc(e.id)}">${amostra(e.camada)}
        <span><span class="perto-nome">${esc(e.nome)}</span><span class="perto-tipo">${esc(g.rotulo)} mais perto${e.coord_origem === "pendente" ? " · ponto aproximado" : ""}</span></span>
        <span class="perto-dist">${textoDistancia(d)}</span></button></li>`).join("");
    mostrar(`<p><strong>${esc(rotulo)}</strong>${terr ? ` fica no território <button type="button" data-t="${terr.numero}">${esc(terr.nome)}</button>` : " fica fora dos limites de Cotia."}</p>
      <p>Mais perto deste ponto, em linha reta:</p><ul class="perto">${itens}</ul>`);
    const grupo = L.featureGroup([marcadorBusca, ...perto.map((p) => L.marker([p.e.lat, p.e.lon]))]);
    mapa.fitBounds(grupo.getBounds(), { padding: [40, 40], maxZoom: 15, animate: !reduzMovimento });
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
    mapa.setView([e.lat, e.lon], Math.max(mapa.getZoom(), 15), { animate: !reduzMovimento });
    e.marcador.openPopup();
  }

  // ---------- tabela comparativa ----------

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
    ...RAZOES.map((r, i) => ({ id: `r_${r.id}`, rotulo: `Crianças por ${r.id === "educ" ? "creche ou pré-escola" : r.nome}`, valor: (t) => razao(t, r), razao: r, grupo: i === 0 })),
  ];
  const valorDe = (c, t) => (c.valor ? c.valor(t) : t[c.id]);

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
        if (i === 0) return `<td><span class="terr" style="--c: ${esc(t.cor_png)}">${t.numero}. ${esc(t.nome)}</span></td>`;
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

  function montarTabela() {
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
        selecionarTerritorio(Number(tr.dataset.t));
        area.scrollIntoView({ behavior: reduzMovimento ? "auto" : "smooth", block: "start" });
      }
    });
  }

  // ---------- início ----------

  function ajustarTopo() {
    document.documentElement.style.setProperty("--h-topo", `${document.querySelector(".topo").offsetHeight}px`);
  }
  window.addEventListener("resize", ajustarTopo);
  ajustarTopo();
  if (window.matchMedia("(max-width: 759.98px)").matches) document.getElementById("carimbo").open = false;

  async function iniciar() {
    const [contorno, terrGJ, eqGJ, listaBairros] = await Promise.all([
      carregar("data/cotia.geojson"), carregar("data/territorios.geojson"),
      carregar("data/equipamentos.geojson"), carregar("data/bairros.json"),
    ]);
    bairros = listaBairros;
    prepararTerritorios(terrGJ);
    desenharTerritorios(terrGJ);
    camadaContorno = L.geoJSON(contorno, { style: { color: cssVar("--tinta"), weight: 2.2, fill: false }, interactive: false }).addTo(mapa);
    limitesCotia = camadaContorno.getBounds();
    desenharEquipamentos(eqGJ);
    montarControles();
    montarTabela();
    document.getElementById("carimbo-sub").textContent = `${equipamentos.length} equipamentos · ${territorios.length} territórios · fontes e datas`;
    atualizarZoom();
    quandoVisivel(() => {
      const m = location.hash.match(/^#t([1-7])$/);
      if (m) selecionarTerritorio(Number(m[1]));
      else enquadrarCotia();
    });
  }

  iniciar().catch((erro) => {
    console.error(erro);
    document.getElementById("mapa").insertAdjacentHTML("beforeend",
      `<p style="position:relative;z-index:1000;margin:16px;padding:12px;background:#fff;border-radius:6px">Não foi possível carregar os dados do mapa: ${esc(erro.message)}. Recarregue a página.</p>`);
  });
})();
