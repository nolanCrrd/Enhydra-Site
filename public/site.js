// Animations du site : apparitions au défilement, chat de démonstration, chiffres qui montent, copie des commandes.
// Rien n'est nécessaire pour lire le site : sans JavaScript, tout est visible tel quel.
document.documentElement.classList.add("js");
// Le rideau d'ouverture ne passe qu'une fois par visite (et jamais si la personne veut moins de mouvement)
try {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || sessionStorage.getItem("intro")) document.documentElement.classList.add("no-intro");
  else sessionStorage.setItem("intro", "1");
} catch {
  document.documentElement.classList.add("no-intro");
}

addEventListener("DOMContentLoaded", () => {
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Barre de progression et en-tête qui se fixe
  const bar = $("#progress");
  const head = $("header.top");
  const onScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
    head?.classList.toggle("stuck", scrollY > 12);
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Apparition des blocs quand ils entrent à l'écran
  const targets = $$(".reveal, .pop, .slide, .pop-in");
  if (still || !("IntersectionObserver" in window)) targets.forEach((el) => el.classList.add("seen"));
  else {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.classList.add("seen");
          io.unobserve(e.target);
        }),
      { threshold: 0.18, rootMargin: "0px 0px -6% 0px" },
    );
    targets.forEach((el) => io.observe(el));
  }

  // Chiffres qui montent
  $$("[data-count]").forEach((el) => {
    const end = Number(el.dataset.count);
    const suffix = el.dataset.suffix ?? "";
    if (still || !("IntersectionObserver" in window)) return;
    el.textContent = `0${suffix}`;
    const io = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      io.disconnect();
      const t0 = performance.now();
      const step = (now) => {
        const k = Math.min(1, (now - t0) / 1400);
        el.textContent = `${Math.round(end * (1 - Math.pow(1 - k, 3)))}${suffix}`;
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
    io.observe(el);
  });

  // Phrase qui change dans l'en-tête
  const rotor = $("[data-rotor]");
  if (rotor && !still) {
    const words = rotor.dataset.rotor.split("|");
    let i = 0;
    setInterval(() => {
      rotor.classList.add("out");
      setTimeout(() => {
        i = (i + 1) % words.length;
        rotor.textContent = words[i];
        rotor.classList.remove("out");
        rotor.classList.add("in");
        requestAnimationFrame(() => requestAnimationFrame(() => rotor.classList.remove("in")));
      }, 350);
    }, 2600);
  }

  // Les téléphones suivent un peu la souris
  const tilt = $("[data-tilt]");
  if (tilt && !still && matchMedia("(pointer: fine)").matches) {
    addEventListener("pointermove", (e) => {
      const x = (e.clientX / innerWidth - 0.5) * 2;
      const y = (e.clientY / innerHeight - 0.5) * 2;
      $$("img", tilt).forEach((img, n) => {
        img.style.rotate = `${x * (n ? 4 : -4)}deg`;
        img.style.marginTop = `${y * (n ? 6 : -6)}px`;
      });
    });
  }

  // Boutons « Copier »
  $$(".copy").forEach((b) =>
    b.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(b.dataset.copy);
        b.textContent = "Copié !";
      } catch {
        b.textContent = "Sélectionne le texte";
      }
      b.classList.add("done");
      setTimeout(() => {
        b.textContent = "Copier";
        b.classList.remove("done");
      }, 1800);
    }),
  );

  // Chat de démonstration : deux bulles qui se répondent, chacune « pop » à sa place (toutes sont déjà dans la page,
  // invisibles : rien ne se décale quand l'une apparaît), puis la carte de confirmation.
  const chat = $("#chat");
  if (chat) {
    const SCENES = [
      { me: "Rappelle-moi demain à 9 h d'appeler le garage", bot: "C'est noté. Je te le rappelle demain à 9 h.", title: "Appeler le garage", meta: "Demain · 9 h 00" },
      { me: "Range cette note dans Recettes : gratin dauphinois, 1 h 15 à 180 °C", bot: "Rangée dans le dossier Recettes.", title: "Gratin dauphinois", meta: "Recettes · note" },
      { me: "Chaque matin à 7 h, résume-moi l'actualité tech", bot: "Fait. Ton résumé arrivera chaque matin à 7 h sur ton accueil.", title: "Résumé tech", meta: "Tous les jours · 7 h 00" },
    ];
    const chips = $$(".chip");
    const rows = $$(".row", chat);
    let run = 0;
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

    async function play(n, id) {
      const s = SCENES[n];
      chips.forEach((c, k) => {
        c.classList.toggle("on", k === n);
        c.setAttribute("aria-selected", String(k === n));
      });
      rows.forEach((r) => r.classList.remove("on"));
      await sleep(350);
      if (id !== run) return;
      $("#m-me").textContent = s.me;
      $("#m-bot").textContent = s.bot;
      $("#m-title").textContent = s.title;
      $("#m-meta").textContent = s.meta;
      for (const [k, row] of rows.entries()) {
        row.classList.add("on");
        await sleep(k === 0 ? 1100 : 1000);
        if (id !== run) return;
      }
      await sleep(3200);
      if (id === run) play((n + 1) % SCENES.length, id);
    }

    const start = (n) => play(n, ++run);
    chips.forEach((c) => c.addEventListener("click", () => start(Number(c.dataset.scene))));

    if (!still && "IntersectionObserver" in window) {
      rows.forEach((r) => r.classList.remove("on")); // elles apparaîtront quand la démo sera à l'écran
      const io = new IntersectionObserver((entries) => {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        start(0);
      }, { threshold: 0.4 });
      io.observe(chat);
    } else rows.forEach((r) => r.classList.add("on")); // sans animation : la première scène, terminée
  }
});
