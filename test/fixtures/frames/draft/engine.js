function build(stone, arch) {
  stone.animate([{ transform: "translateY(-200px)" }, { transform: "none" }],
    { duration: 1200, easing: "ease-in-out", fill: "both" });
  arch.animate([{ opacity: 0, transform: "scale(0.6)" }, { opacity: 1, transform: "none" }],
    { duration: 800, delay: 1000, easing: "ease-out", fill: "both" });
}
