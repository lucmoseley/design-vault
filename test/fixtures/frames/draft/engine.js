// A shared engine for design-vault#67's hash tests: each draft that loads it is
// re-checked after an edit here. The tests copy this folder and edit the copy.
function build(stone, arch) {
  stone.animate([{ transform: "translateY(-200px)" }, { transform: "none" }],
    { duration: 1200, easing: "ease-in-out", fill: "both" });
  arch.animate([{ opacity: 0, transform: "scale(0.6)" }, { opacity: 1, transform: "none" }],
    { duration: 800, delay: 1000, easing: "ease-out", fill: "both" });
}
