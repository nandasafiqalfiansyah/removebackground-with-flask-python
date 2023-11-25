function processImage() {
  // Show loading spinner with transparent background
  document.getElementById("loadingSpinner").style.display = "flex";

  // Hide particle effect
  document.getElementById("particles-js").style.display = "none";

  var form = document.getElementById("uploadForm");
  var formData = new FormData(form);

  fetch("http://localhost:5000/process_image", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide loading spinner
      document.getElementById("loadingSpinner").style.display = "none";

      // Show particle effect
      document.getElementById("particles-js").style.display = "block";

      if (data.result === "success") {
        document.getElementById(
          "rgbValues"
        ).innerText = `R: ${data.rgb_values.R.toFixed(
          2
        )}, G: ${data.rgb_values.G.toFixed(2)}, B: ${data.rgb_values.B.toFixed(
          2
        )}`;
        document.getElementById(
          "originalImage"
        ).src = `data:image/png;base64,${data.original_image}`;
        document.getElementById(
          "removedBgImage"
        ).src = `data:image/png;base64,${data.image_with_removed_bg}`;
        document.getElementById("result").style.display = "block";
      } else {
        alert(`Error: ${data.error_message}`);
      }
    })
    .catch((error) => console.error("Error:", error));
}
function downloadImage() {
  var removedBgImage = document.getElementById("removedBgImage");
  var dataUrl = removedBgImage.src;
  var a = document.createElement("a");
  a.href = dataUrl;
  a.download = "removed_background_image.png";
  a.click();
}

function clearImage() {
  // Reload the page to clear content
  location.reload();
}

// Particle Effect Configuration
particlesJS("particles-js", {
  particles: {
    number: { value: 80, density: { enable: true, value_area: 800 } },
    color: { value: "#000" },
    shape: {
      type: "circle",
      stroke: { width: 0, color: "#000000" },
      polygon: { nb_sides: 5 },
      image: { src: "img/github.svg", width: 100, height: 100 },
    },
    opacity: {
      value: 0.5,
      random: false,
      anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false },
    },
    size: {
      value: 3,
      random: true,
      anim: { enable: false, speed: 40, size_min: 0.1, sync: false },
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#000",
      opacity: 0.4,
      width: 1,
    },
    move: {
      enable: true,
      speed: 6,
      direction: "none",
      random: false,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: { enable: false, rotateX: 600, rotateY: 1200 },
    },
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: { enable: true, mode: "repulse" },
      onclick: { enable: true, mode: "push" },
      resize: true,
    },
    modes: {
      grab: { distance: 400, line_linked: { opacity: 1 } },
      bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
      repulse: { distance: 200, duration: 0.4 },
      push: { particles_nb: 4 },
      remove: { particles_nb: 2 },
    },
  },
  retina_detect: true,
});
