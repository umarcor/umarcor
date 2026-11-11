const RELEASE = "https://github.com/umarcor/umarcor/releases/download/gource-videos/";
const API = "https://api.github.com/repos/umarcor/umarcor/releases/tags/gource-videos";
const NAMES = [
  "CHIPSAlliance", "CoCoTb", "DBHI", "EDAA", "EDAA-Utilities", "EDAA-Workflows",
  "F4PGA", "FPGAwars", "HDL", "HDLC", "Hitchhiker", "LibreCores", "LiteX",
  "NEORV32", "SymbiFlow", "VTR", "VUnit", "YosysHQ", "f4pga-core", "ghdl",
  "iverilog", "openFPGALoader", "osvb", "osvb-noroot", "osvvm", "pyTooling",
  "renode", "spf13", "verilator"
];
const FALLBACK = NAMES.map((name) => ({
  name,
  image: RELEASE + name + ".jpg",
  video: RELEASE + name + ".mp4"
}));
const IMAGE = /^(.+)\.(jpe?g|png|gif|webp)$/i;
const VIDEO = /^(.+)\.(mp4|webm|ogg)$/i;
const gallery = document.getElementById("gallery");
const count = document.getElementById("count");
const fmt = new Intl.NumberFormat();

function byName(a, b) {
  return a.name.localeCompare(b.name, undefined, { sensitivity: "base" });
}

function parseRelease(data) {
  const map = new Map();
  for (const asset of data.assets || []) {
    const image = asset.name.match(IMAGE);
    const video = asset.name.match(VIDEO);
    const match = image || video;
    if (!match) continue;
    const item = map.get(match[1]) || { name: match[1] };
    if (image) item.image = asset.browser_download_url;
    else item.video = asset.browser_download_url;
    map.set(match[1], item);
  }
  return [...map.values()].filter((item) => item.image && item.video);
}

async function discover() {
  let timer;
  try {
    const controller = new AbortController();
    timer = setTimeout(() => controller.abort(), 5000);
    const response = await fetch(API, {
      signal: controller.signal,
      headers: { Accept: "application/vnd.github+json" }
    });
    if (!response.ok) throw new Error("HTTP " + response.status);
    const items = parseRelease(await response.json());
    return items.length ? items : null;
  } catch (error) {
    console.info("Using the built-in asset list:", error.message);
    return null;
  } finally {
    clearTimeout(timer);
  }
}

async function loadMeta(items) {
  try {
    const response = await fetch("metadata.json");
    if (!response.ok) return;
    const meta = await response.json();
    for (const item of items) if (meta[item.name]) item.meta = meta[item.name];
  } catch { /* no metadata: bare cards */ }
}

const observer = "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const video = entry.target;
        video.poster = video.dataset.poster;
        video.src = video.dataset.src;
        delete video.dataset.poster;
        delete video.dataset.src;
        observer.unobserve(video);
      }
    }, { rootMargin: "300px" })
  : null;

function observePosters() {
  for (const video of gallery.querySelectorAll("video[data-src]")) {
    if (observer) observer.observe(video);
    else {
      video.poster = video.dataset.poster;
      video.src = video.dataset.src;
      delete video.dataset.poster;
      delete video.dataset.src;
    }
  }
}

function card(item) {
  const label = item.meta?.title || item.name;
  const figure = document.createElement("figure");
  figure.className = "card";

  const video = document.createElement("video");
  video.controls = true;
  video.preload = "none";
  video.setAttribute("playsinline", "");
  video.dataset.src = item.video;
  video.dataset.poster = item.image;
  video.setAttribute("aria-label", label + " gource video");

  const error = document.createElement("p");
  error.className = "error";
  error.hidden = true;
  error.append("Inline playback unavailable. ");
  const direct = document.createElement("a");
  direct.href = item.video;
  direct.target = "_blank";
  direct.rel = "noopener";
  direct.textContent = "Open the video directly";
  error.append(direct);
  video.addEventListener("error", () => { error.hidden = false; });

  const caption = document.createElement("figcaption");
  const text = document.createElement("div");
  text.className = "caption";
  const name = document.createElement("span");
  name.className = "name";
  name.textContent = label;
  text.append(name);
  const stats = [];
  if (item.meta?.first) stats.push(item.meta.first === item.meta.last
    ? item.meta.first : item.meta.first + " – " + item.meta.last);
  if (Number.isFinite(item.meta?.changes)) stats.push(fmt.format(item.meta.changes) + " changes");
  if (Number.isFinite(item.meta?.contributors)) stats.push(fmt.format(item.meta.contributors) + " contributors");
  if (stats.length) {
    const detail = document.createElement("span");
    detail.className = "stats";
    detail.textContent = stats.join(" · ");
    text.append(detail);
  }
  const links = document.createElement("span");
  links.className = "links";

  const imageLink = document.createElement("a");
  imageLink.href = item.image;
  imageLink.target = "_blank";
  imageLink.rel = "noopener";
  imageLink.textContent = "🖼️";
  imageLink.title = "Open " + label + " image";
  imageLink.setAttribute("aria-label", "Open " + label + " image");

  const videoLink = document.createElement("a");
  videoLink.href = item.video;
  videoLink.target = "_blank";
  videoLink.rel = "noopener";
  videoLink.textContent = "🎬";
  videoLink.title = "Open or download " + label + " video";
  videoLink.setAttribute("aria-label", "Open or download " + label + " video");

  links.append(imageLink, videoLink);
  caption.append(text, links);
  figure.append(video, error, caption);
  return figure;
}

function render(items) {
  const sorted = [...items].sort(byName);
  const fragment = document.createDocumentFragment();
  for (const item of sorted) fragment.append(card(item));
  gallery.replaceChildren(fragment);
  count.textContent = sorted.length;
  observePosters();
}

render(FALLBACK);
discover().then(async (items) => {
  const list = items ?? FALLBACK;
  await loadMeta(list);
  render(list);
});
