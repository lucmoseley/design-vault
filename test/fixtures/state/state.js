// The state fixtures' shared behaviour. A part marked data-fault on the
// fault page behaves the faulty way that record names; unmarked, it behaves
// as the record asks. The check script never reads data-fault to judge.
(() => {
  // node --test loads every .js under test/, where there is no document.
  if (!globalThis.document) return;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const faulty = (el, id) => el?.closest("[data-fault]")?.getAttribute("data-fault") === id;

  // Tooltips: Escape dismisses the one showing until the pointer leaves.
  addEventListener("keydown", (e) => {
    if (e.key === "Escape") $$(".tip-host").forEach((h) => h.classList.add("dismissed"));
  });
  $$(".tip-host").forEach((h) => {
    h.addEventListener("mouseleave", () => h.classList.remove("dismissed"));
    h.addEventListener("blur", () => h.classList.remove("dismissed"));
  });
  // vault.hover-content: a tooltip that goes a second after it shows.
  $$(".timed-host").forEach((h) => {
    const tip = $(".timed-tip", h);
    h.addEventListener("mouseenter", () => {
      tip.hidden = false;
      setTimeout(() => (tip.hidden = true), 1000);
    });
    h.addEventListener("mouseleave", () => (tip.hidden = true));
  });

  // Disclosures and menu buttons: aria-expanded flips, aria-controls shows.
  const menus = [];
  const shut = (b) => {
    b.setAttribute("aria-expanded", "false");
    $("#" + b.getAttribute("aria-controls")).hidden = true;
    $$("[aria-expanded=true]", $("#" + b.getAttribute("aria-controls")))
      .filter((c) => !faulty(c, "vault.submenu-close"))
      .forEach(shut);
  };
  $$("button[aria-controls][aria-expanded]").forEach((b) => {
    menus.push(b);
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      if (b.getAttribute("aria-expanded") === "true") return shut(b);
      b.setAttribute("aria-expanded", "true");
      $("#" + b.getAttribute("aria-controls")).hidden = false;
    });
  });
  addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = menus.filter((b) => b.getAttribute("aria-expanded") === "true" && !b.closest("[role=menu]"));
    open.forEach((b) => {
      shut(b);
      b.focus();
    });
  });
  // vault.expanded-state: a button that shows a panel and says nothing.
  $$("button[data-panel]").forEach((b) =>
    b.addEventListener("click", () => {
      const p = $("#" + b.dataset.panel);
      p.hidden = !p.hidden;
    }),
  );

  // Menu items: one ending in "…" asks for more in a dialog; others act.
  $$("[role=menuitem][data-opens]").forEach((m) =>
    m.addEventListener("click", () => $("#" + m.dataset.opens).showModal()),
  );

  // Dialog openers and closers.
  $$("button[data-opens]").forEach((b) => b.addEventListener("click", () => $("#" + b.dataset.opens).showModal()));
  $$("dialog button[data-close]").forEach((b) => b.addEventListener("click", () => b.closest("dialog").close()));
  $$(".banner button").forEach((b) => b.addEventListener("click", () => b.closest(".banner").remove()));

  // Toggle buttons.
  $$("[aria-pressed]").forEach((b) =>
    b.addEventListener("click", () => {
      const on = b.getAttribute("aria-pressed") !== "true";
      b.setAttribute("aria-pressed", String(on));
      if (!faulty(b, "vault.toggle-state")) b.textContent = on ? "Bold on" : "Bold off";
    }),
  );

  // vault.act-on-release: a button that acts as it is pressed down, and one
  // that deletes as it is pressed down and offers an Undo that restores nothing.
  $$("[data-fault='vault.act-on-release']:not([data-removes])").forEach((b) =>
    b.addEventListener("pointerdown", () => (b.textContent = "Sent")),
  );
  $$("[data-fault='vault.act-on-release'][data-removes]").forEach((b) =>
    b.addEventListener("pointerdown", () => {
      const item = $("#" + b.dataset.removes).firstElementChild;
      if (!item) return;
      item.remove();
      const undo = document.createElement("button");
      undo.type = "button";
      undo.textContent = "Undo";
      b.after(undo);
    }),
  );
  // vault.key-shortcuts: "s" alone jumps to the search field.
  if ($("[data-fault='vault.key-shortcuts']")) {
    addEventListener("keydown", (e) => {
      if (e.key === "s" && document.activeElement === document.body) {
        e.preventDefault();
        $("[data-fault='vault.key-shortcuts']").focus();
      }
    });
  }
  // vault.on-focus: focusing a field sends focus on to the next.
  $$("[data-fault='vault.on-focus']").forEach((f) =>
    f.addEventListener("focus", () => $("#" + f.dataset.next).focus()),
  );

  // Players: the play control toggles its audio.
  $$(".player").forEach((p) => {
    const media = $("audio", p);
    $("[data-play]", p).addEventListener("click", () => (media.paused ? media.play() : media.pause()));
  });

  // Sliders: keys, a click on the track and a captured drag, in the
  // reading direction.
  $$(".thumb").forEach((t) => {
    const track = t.parentElement;
    const low = +t.getAttribute("aria-valuemin");
    const high = +t.getAttribute("aria-valuemax");
    const rtl = () => !faulty(t, "vault.slider-direction") && getComputedStyle(track).direction === "rtl";
    const set = (v) => {
      v = Math.max(low, Math.min(high, Math.round(v)));
      t.setAttribute("aria-valuenow", v);
      const f = (v - low) / (high - low);
      t.style.left = (rtl() ? 1 - f : f) * (track.clientWidth - t.offsetWidth) + "px";
    };
    set(+t.getAttribute("aria-valuenow"));
    const at = (x) => {
      const r = track.getBoundingClientRect();
      const f = Math.max(0, Math.min(1, (x - r.left) / r.width));
      set(low + (rtl() ? 1 - f : f) * (high - low));
    };
    const keys = !faulty(t, "vault.slider-keys");
    t.addEventListener("keydown", (e) => {
      const v = +t.getAttribute("aria-valuenow");
      const step = { ArrowRight: rtl() ? -1 : 1, ArrowLeft: rtl() ? 1 : -1, ArrowUp: 1, ArrowDown: -1 }[e.key];
      if (step && (keys || e.key.startsWith("ArrowR") || e.key.startsWith("ArrowL"))) set(v + step);
      else if (keys && e.key === "Home") set(low);
      else if (keys && e.key === "End") set(high);
      else return;
      e.preventDefault();
    });
    if (faulty(t, "vault.drag-tracking")) {
      let down = false;
      t.addEventListener("pointerdown", () => (down = true));
      t.addEventListener("pointermove", (e) => down && at(e.clientX));
      t.addEventListener("pointerup", () => (down = false));
      return;
    }
    if (keys) {
      track.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        t.setPointerCapture(e.pointerId);
        at(e.clientX);
        t.focus();
      });
    } else {
      t.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        t.setPointerCapture(e.pointerId);
      });
    }
    t.addEventListener("pointermove", (e) => t.hasPointerCapture(e.pointerId) && at(e.clientX));
  });

  // Carousels: previous and next scroll by a slide.
  $$(".carousel").forEach((c) => {
    const reel = $(".reel", c);
    $$("[data-step]", c).forEach((b) =>
      b.addEventListener("click", () => reel.scrollBy({ left: +b.dataset.step * 308, behavior: "instant" })),
    );
  });

  // Zoomable images: a two-finger spread scales about the point between
  // the fingers; the faulty one about its corner.
  $$(".zoomable").forEach((z) => {
    const img = $("img", z);
    let start = null;
    const mid = (ts) => [(ts[0].clientX + ts[1].clientX) / 2, (ts[0].clientY + ts[1].clientY) / 2];
    const gap = (ts) => Math.hypot(ts[0].clientX - ts[1].clientX, ts[0].clientY - ts[1].clientY);
    z.addEventListener("touchstart", (e) => {
      if (e.touches.length !== 2) return;
      const r = z.getBoundingClientRect();
      start = { gap: gap(e.touches), mid: mid(e.touches), x: r.left, y: r.top };
      e.preventDefault();
    }, { passive: false });
    z.addEventListener("touchmove", (e) => {
      if (!start || e.touches.length !== 2) return;
      const s = gap(e.touches) / start.gap;
      const anchored = !faulty(z, "vault.pinch-anchor");
      const tx = anchored ? (start.mid[0] - start.x) * (1 - s) : 0;
      const ty = anchored ? (start.mid[1] - start.y) * (1 - s) : 0;
      img.style.transform = `translate(${tx}px, ${ty}px) scale(${s})`;
      e.preventDefault();
    }, { passive: false });
    z.addEventListener("touchend", () => (start = null));
  });

  // Forms: checked on leaving a field, an error cleared on the key that
  // fixes it, and on a failed submit an error summary above the h1 that
  // takes focus and links to each field.
  const message = (f) => {
    if (f.validity.valueMissing) return "Enter your " + f.labels[0].textContent.toLowerCase();
    if (!f.validity.valid) return "Enter a valid " + f.labels[0].textContent.toLowerCase();
    return "";
  };
  const show = (f) => {
    const m = message(f);
    const box = $("#" + f.id + "-error");
    if (m) {
      f.setAttribute("aria-invalid", "true");
      box.textContent = m;
    } else {
      f.removeAttribute("aria-invalid");
      box.textContent = "";
    }
    return !m;
  };
  $$("form.v").forEach((form) => {
    const checked = $$("input[required], input[type=email]", form).filter((f) => $("#" + f.id + "-error"));
    checked.forEach((f) => {
      if (faulty(form, "vault.validation-timing")) f.addEventListener("input", () => show(f));
      else {
        f.addEventListener("blur", () => f.value && show(f));
        f.addEventListener("input", () => f.getAttribute("aria-invalid") && show(f));
      }
    });
    form.addEventListener("submit", (e) => {
      const wrong = checked.filter((f) => !show(f));
      if (!wrong.length) return;
      e.preventDefault();
      if (faulty(form, "vault.answers-kept")) form.reset();
      if (faulty(form, "vault.error-summary-focus")) return wrong[0].focus();
      const summary = $("#summary");
      $("ul", summary).replaceChildren(
        ...wrong.map((f) => {
          const li = document.createElement("li");
          li.innerHTML = `<a href="#${f.id}">${message(f)}</a>`;
          return li;
        }),
      );
      summary.hidden = false;
      summary.focus();
    });
  });
  $$("[data-fault='vault.field-paste'], [data-fault='vault.auth-paste']").forEach((f) =>
    f.addEventListener("paste", (e) => e.preventDefault()),
  );
  // Split code boxes: one paste fills them all.
  $$(".code").forEach((group) => {
    const boxes = $$("input", group);
    boxes.forEach((b) =>
      b.addEventListener("paste", (e) => {
        const text = e.clipboardData.getData("text").replace(/\D/g, "");
        if (text.length < 2) return;
        e.preventDefault();
        boxes.forEach((x, i) => (x.value = text[i] || ""));
      }),
    );
  });

  // The search field: an APG combobox, its count in a status region; the
  // faulty one draws a bare list.
  $$("[data-suggest]").forEach((input) => {
    const list = $("#" + input.dataset.suggest);
    const status = $("#" + input.dataset.status);
    const words = ["Amsterdam", "Athens", "Auckland", "Berlin"];
    const combo = input.getAttribute("role") === "combobox";
    input.addEventListener("input", () => {
      const got = input.value ? words.filter((w) => w.toLowerCase().startsWith(input.value.toLowerCase())) : [];
      list.replaceChildren(
        ...got.map((w, i) => {
          const li = document.createElement("li");
          li.textContent = w;
          if (combo) {
            li.id = input.id + "-o" + i;
            li.setAttribute("role", "option");
          }
          return li;
        }),
      );
      list.hidden = !got.length;
      if (combo) {
        input.setAttribute("aria-expanded", String(got.length > 0));
        input.removeAttribute("aria-activedescendant");
        status.textContent = got.length + " suggestions";
      }
    });
    if (!combo) return;
    input.addEventListener("keydown", (e) => {
      const options = $$("[role=option]", list);
      if (e.key !== "ArrowDown" || !options.length) return;
      e.preventDefault();
      const now = options.findIndex((o) => o.id === input.getAttribute("aria-activedescendant"));
      const next = options[(now + 1) % options.length];
      options.forEach((o) => o.setAttribute("aria-selected", String(o === next)));
      input.setAttribute("aria-activedescendant", next.id);
    });
  });

  // Select-all: mixed when some are checked.
  $$(".select-all").forEach((all) => {
    const members = all.getAttribute("aria-controls").split(" ").map((id) => $("#" + id));
    const sync = () => {
      const n = members.filter((m) => m.checked).length;
      all.checked = n === members.length;
      all.indeterminate = !faulty(all, "vault.mixed-check") && n > 0 && n < members.length;
    };
    members.forEach((m) => m.addEventListener("change", sync));
    all.addEventListener("change", () => {
      members.forEach((m) => (m.checked = all.checked));
      sync();
    });
  });

  // Toasts: a message written into a status region the first markup holds.
  $$("button[data-toast]").forEach((b) =>
    b.addEventListener("click", () => {
      const region = $("#" + b.dataset.toast);
      region.innerHTML = b.dataset.say;
      if (faulty(b, "vault.status-no-focus")) setTimeout(() => (region.innerHTML = ""), 2000);
    }),
  );
  // vault.live-region-ready: a status region added with its message.
  $$("[data-fault='vault.live-region-ready']").forEach((b) =>
    b.addEventListener("click", () => {
      const region = document.createElement("div");
      region.setAttribute("role", "status");
      region.className = "toast";
      region.textContent = "Copied";
      b.after(region);
    }),
  );
  // vault.exit-warning: a link off the site that asks first.
  $$("[data-fault='vault.exit-warning']").forEach((a) =>
    a.addEventListener("click", (e) => {
      if (!confirm("You are leaving this site.")) e.preventDefault();
    }),
  );

  // The session limit: half an hour, warned a minute before with a button
  // that restarts it, unless the page is the faulty one.
  const LIMIT = 30 * 60 * 1000;
  const warned = !$("[data-fault='vault.time-limit']");
  let timers = [];
  const start = () => {
    timers.forEach(clearTimeout);
    timers = [setTimeout(() => (location.href = "pages/a.html"), LIMIT)];
    if (warned) timers.push(setTimeout(() => $("#session").showModal(), LIMIT - 60 * 1000));
  };
  $$("#session [data-restart]").forEach((b) =>
    b.addEventListener("click", () => {
      $("#session").close();
      start();
    }),
  );
  start();
})();
