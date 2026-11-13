const input = document.getElementById("inputPicture");
const preview = document.getElementById("preview");
const hint = document.getElementById("hint");
const submitBtn = document.getElementById("submitBtn");
const dropzone = document.querySelector(".dropzone");

function showPreview(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.hidden = false;
        hint.hidden = true;
        submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

input.addEventListener("change", () => showPreview(input.files[0]));

// Glisser-déposer
["dragenter", "dragover"].forEach(evt =>
    dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.add("drag"); }));
["dragleave", "drop"].forEach(evt =>
    dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.remove("drag"); }));
dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        showPreview(input.files[0]);
    }
});
