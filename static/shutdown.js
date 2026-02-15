function openShutdownConfirm() {
  const popup = document.createElement("div");
  popup.id = "shutdown-popup";
  popup.style.position = "fixed";
  popup.style.top = "0";
  popup.style.left = "0";
  popup.style.width = "100%";
  popup.style.height = "100%";
  popup.style.background = "rgba(0,0,0,0.5)";
  popup.style.display = "flex";
  popup.style.alignItems = "center";
  popup.style.justifyContent = "center";
  popup.style.zIndex = "9999";

  popup.innerHTML = `
    <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
      <h3>Shut down Raspberry Pi?</h3>
      <p>Are you sure you want to shut down?</p>
      <button id="shutdown-yes" class="mode-button" style="margin-right: 10px;">Yes</button>
      <button id="shutdown-no" class="mode-button">No</button>
    </div>
  `;

  document.body.appendChild(popup);

  document.getElementById("shutdown-yes").onclick = shutdownPi;
  document.getElementById("shutdown-no").onclick = () => popup.remove();
}

async function shutdownPi() {
  try {
    await fetch("http://192.168.178.88:8080/shutdown", { method: "POST" });
    alert("The Raspberry Pi is shutting down now.");
  } catch (err) {
    alert("Error while shutting down: " + err);
  }

  document.getElementById("shutdown-popup").remove();
}