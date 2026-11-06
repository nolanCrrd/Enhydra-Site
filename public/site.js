// Animations du site : apparitions au défilement, chat de démonstration, chiffres qui montent, copie des commandes.
// Rien n'est nécessaire pour lire le site : sans JavaScript, tout est visible tel quel.
document.documentElement.classList.add("js");

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

  // Chat de démonstration : le message s'écrit, Hermes réfléchit, répond, et la carte apparaît
  const chat = $("#chat");
  if (chat) {
    const SCENES = [
      { me: "Rappelle-moi demain à 9 h d'appeler le garage", bot: "C'est noté. Je te le rappelle demain à 9 h.", title: "Appeler le garage", meta: "Demain · 9 h 00" },
      { me: "Range cette note dans Recettes : gratin dauphinois, 1 h 15 à 180 °C", bot: "Rangée dans le dossier Recettes.", title: "Gratin dauphinois", meta: "Recettes · note" },
      { me: "Chaque matin à 7 h, résume-moi l'actualité tech", bot: "Fait. Ton résumé arrivera chaque matin à 7 h sur ton accueil.", title: "Résumé tech", meta: "Tous les jours · 7 h 00" },
    ];
    const chips = $$(".chip");
    let run = 0;
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const el = (cls, html = "") => Object.assign(document.createElement("div"), { className: cls, innerHTML: html });
    const show = (n) => {
      chips.forEach((c, k) => {
        c.classList.toggle("on", k === n);
        c.setAttribute("aria-selected", String(k === n));
      });
    };

    async function play(n, id) {
      const s = SCENES[n];
      show(n);
      chat.replaceChildren();
      const me = el("msg me");
      chat.append(me);
      for (let k = 1; k <= s.me.length; k++) {
        if (id !== run) return;
        const caret = Object.assign(document.createElement("span"), { className: "caret" });
        me.replaceChildren(document.createTextNode(s.me.slice(0, k)), caret);
        await sleep(28);
      }
      me.textContent = s.me;
      await sleep(350);
      const dots = el("typing", "<i></i><i></i><i></i>");
      chat.append(dots);
      await sleep(1100);
      if (id !== run) return;
      dots.remove();
      chat.append(el("msg bot", s.bot.replace(/&/g, "&amp;").replace(/</g, "&lt;")));
      await sleep(550);
      if (id !== run) return;
      const card = el("cardmsg");
      card.innerHTML = '<i class="ico"></i><span><b></b><small></small></span>';
      $("b", card).textContent = s.title;
      $("small", card).textContent = s.meta;
      chat.append(card);
      await sleep(3800);
      if (id === run) play((n + 1) % SCENES.length, run);
    }

    const start = (n) => play(n, ++run);
    chips.forEach((c) => c.addEventListener("click", () => start(Number(c.dataset.scene))));

    if (still || !("IntersectionObserver" in window)) {
      // sans animation : on montre simplement la première scène terminée (déjà dans la page)
    } else {
      const io = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          io.disconnect();
          start(0);
        }
      }, { threshold: 0.4 });
      io.observe(chat);
    }
  }
});
