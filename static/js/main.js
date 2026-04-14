document.addEventListener("DOMContentLoaded", function () {

    document.addEventListener("click", function (e) {

        if (e.target.classList.contains("highlight")) {

            // 1. Try ID first (friend system)
            let id = e.target.dataset.id;

            let url = "";

            if (id) {
                // ID ভিত্তিক (recommended)
                url = `/get-explanation/${id}/`;
            } else {
                // fallback (your old system)
                let word = e.target.innerText.trim();
                url = `/get-explanation/?word=${encodeURIComponent(word)}`;
            }

            fetch(url)
                .then(res => res.json())
                .then(data => {

                    let html = "";

                    // Text
                    if (data.text || data.content) {
                        html += `<p class="mb-3">${data.text || data.content}</p>`;
                    }

                    // Image
                    if (data.image) {
                        html += `<img src="${data.image}" class="img-fluid rounded mb-3">`;
                    }

                    // Audio
                    if (data.audio) {
                        html += `
                        <audio controls class="w-100 mb-3">
                            <source src="${data.audio}" type="audio/mpeg">
                            Your browser does not support audio
                        </audio>`;
                    }

                    // Video
                    if (data.video) {
                        html += `
                        <video controls class="w-100 rounded mb-3">
                            <source src="${data.video}" type="video/mp4">
                        </video>`;
                    }

                // YouTube embed
                if (data.youtube) {
                    html += `
                    <div class="ratio ratio-16x9 mb-3">
                        <iframe 
                            src="${data.youtube}?rel=0&modestbranding=1"
                            title="YouTube video player"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>`;
                }

                    //  fallback
                    if (!html) {
                        html = `<p>No explanation found</p>`;
                    }

                    //  Insert into modal
                    document.getElementById("modal-content").innerHTML = html;

                    //  Bootstrap modal open
                    let modalEl = document.getElementById("exampleModal");

                    if (modalEl) {
                        let modal = new bootstrap.Modal(modalEl);
                        modal.show();
                    } else {
                        // fallback (your old modal)
                        document.getElementById("modal").style.display = "block";
                    }

                })
                .catch(err => {
                    console.error("Error:", err);
                });

        }

    });

});